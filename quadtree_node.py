from quadtree_check import *


class Node:
    def __init__(self, box):
        self.box = box
        self.children = None
        self.node_type = None
        self.depth = 0

    def split(self, box_checker):
        if self.children is not None:
            return
        if self.node_type is None:
            self.node_type = box_checker.check_for_box(self.box)
        if self.node_type is None:
            raise ValueError("Node type is not set")
        if self.node_type != BoxOverlap.Mixed:
            return

        self.children = []
        child_width = self.box.width / 2
        child_height = self.box.height / 2
        for i in range(2):
            for j in range(2):
                x = self.box.top_left[0] + i * child_width
                y = self.box.top_left[1] - j * child_height
                child_box = Box((x, y), (x + child_width, y - child_height))
                child = Node(child_box)
                child.node_type = box_checker.check_for_box(child.box)
                child.depth = self.depth + 1
                self.children.append(child)

    def combine(self, other):
        if self.children is not None:
            return None
        if self.node_type != other.node_type:
            return None
        combined_box = combine_boxes(self.box, other.box)
        if combined_box is None:
            return None
        combined_node = Node(combined_box)
        combined_node.node_type = self.node_type
        combined_node.depth = self.depth
        return combined_node


def split_node(node, box_checker, min_width=1, min_height=1):
    node.split(box_checker)
    if node.children is not None:
        for child in node.children:
            if child.box.width > min_width and child.box.height > min_height:
                split_node(
                    child, box_checker, min_width=min_width, min_height=min_height
                )


def visit_nodes(node, callback_at_leaf=None):
    if node.children is None:
        callback_at_leaf(node)
    else:
        if len(node.children) != 4:
            raise ValueError("Node does not have 4 children")
        for child in node.children:
            visit_nodes(child, callback_at_leaf=callback_at_leaf)
