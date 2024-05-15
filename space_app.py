import argparse
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

import json
from polygon_utils import *
from quadtree_node import *


def find_nested_objects(json_data, key):
    for k, v in json_data.items():
        if k == key:
            return v
        if isinstance(v, dict):
            item = find_nested_objects(v, key)
            if item is not None:
                return item
        elif isinstance(v, list):
            for item in v:
                if isinstance(item, dict):
                    nested_item = find_nested_objects(item, key)
                    if nested_item is not None:
                        return nested_item
    return None


if __name__ == "__main__":
    # Parse command line arguments
    parser = argparse.ArgumentParser(description="Space partitioning with quadtrees")
    parser.add_argument(
        "filename",
        type=str,
        help="Name of the file containing the polygon data",
        default="test_data/test_space.json",
    )
    args = parser.parse_args()

    # Load the polygon data from the file
    with open(args.filename, "r") as file:
        polygon_data = json.load(file)

    workspace = find_nested_objects(polygon_data, "workspace")["points"]
    workspace = [(point["x"], point["y"]) for point in workspace]

    obstacle_definitions = find_nested_objects(polygon_data, "obstacles")
    obstacles = []
    for obstacle in obstacle_definitions:
        obstacles.append(
            [(point["x"], point["y"]) for point in obstacle["boundary"]["points"]]
        )

    BoxChecker = BoxChecker(workspace, obstacles)
    # get the bounding box of the workspace
    workspace_bbox = get_bounding_box_polygon(workspace)
    root = Node(workspace_bbox)

    for obstacle in obstacles:
        obstacle_bbox = get_bounding_box_polygon(obstacle)
        print(f"obstacle : {obstacle_bbox.width}x {obstacle_bbox.height}")

    # recursive split the root node
    split_node(root, BoxChecker, min_width=0.2, min_height=0.2)

    # visit the nodes

    # collect all the obstacle leaf nodes
    leaf_nodes = []
    visit_nodes(root, callback_at_leaf=lambda node: leaf_nodes.append(node))

    # try to combine the leaf nodes until no more combinations are found
    found_combination=True
    while found_combination:
        found_combination = False
        for i in range(len(leaf_nodes)):
            for j in range(i + 1, len(leaf_nodes)):
                combined_node = leaf_nodes[i].combine(leaf_nodes[j])
                if combined_node is not None:
                    leaf_nodes[i] = combined_node
                    leaf_nodes.remove(leaf_nodes[j])
                    # remove the individual nodes
                    print(f"combined node: {combined_node.box.width}x {combined_node.box.height}")
                    found_combination = True
                    break
            if found_combination:
                break

    fig, ax = plt.subplots()
    ax.set_aspect("equal")
    ax.plot()
    for node in leaf_nodes:
        if node.node_type != BoxOverlap.FreeSpace:
            ax.add_patch(
                Rectangle(
                    node.box.getBottomLeft(),
                    node.box.width,
                    node.box.height,
                    facecolor="red",
                    edgecolor="black",
                )
            )
        else:
            ax.add_patch(
                Rectangle(
                    node.box.getBottomLeft(),
                    node.box.width,
                    node.box.height,
                    facecolor="lightsteelblue",
                    edgecolor="black",
                )
            )
    plt.show()
