# from sympy import Point, Polygon
from shapely import Polygon


class Box:
    def __init__(self, top_left, bottom_right):
        self.top_left = top_left
        self.bottom_right = bottom_right
        self.width = bottom_right[0] - top_left[0]
        self.height = top_left[1] - bottom_right[1]

    def getPolygon(self):
        return [
            (self.top_left[0], self.top_left[1]),
            (self.bottom_right[0], self.top_left[1]),
            (self.bottom_right[0], self.bottom_right[1]),
            (self.top_left[0], self.bottom_right[1]),
        ]

    def getBottomLeft(self):
        return (self.top_left[0], self.bottom_right[1])

    def hasIntersectionWithPolygonPoints(self, polygon_points):
        pol = Polygon(polygon_points)
        box_pol = Polygon(self.getPolygon())
        return pol.intersects(box_pol)

    def isBoxEnclosedByPolygon(self, polygon_points):
        pol = Polygon(polygon_points)
        box_pol = Polygon(self.getPolygon())
        return box_pol.within(pol)

    def isPolygonInsideBox(self, polygon_points):
        pol = Polygon(polygon_points)
        box_pol = Polygon(self.getPolygon())
        return pol.within(box_pol)


def combine_boxes(box1, box2):
    # Define the maximum allowed difference for corners to be considered overlapping
    max_delta = 1e-6  # You can adjust this value based on precision requirements

    # check if they are at the same y coordinate and have the same height
    found_combination = False
    if (abs(box1.top_left[1] - box2.top_left[1]) < max_delta) and (
        abs(box1.bottom_right[1] - box2.bottom_right[1]) < max_delta
    ):
        if (abs(box1.top_left[0] - box2.bottom_right[0]) < max_delta) or (
            abs(box1.bottom_right[0] - box2.top_left[0]) < max_delta
        ):
            found_combination = True

    # check if they are at the same x coordinate and have the same width
    if (abs(box1.top_left[0] - box2.top_left[0]) < max_delta) and (
        abs(box1.bottom_right[0] - box2.bottom_right[0]) < max_delta
    ):
        if (abs(box1.top_left[1] - box2.bottom_right[1]) < max_delta) or (
            abs(box1.bottom_right[1] - box2.top_left[1]) < max_delta
        ):
            found_combination = True

    # If at least 2 corners overlap, combine the boxes
    if found_combination:
        # Determine the combined box dimensions
        combined_top_left = (
            min(box1.top_left[0], box2.top_left[0]),
            max(box1.top_left[1], box2.top_left[1]),
        )
        combined_bottom_right = (
            max(box1.bottom_right[0], box2.bottom_right[0]),
            min(box1.bottom_right[1], box2.bottom_right[1]),
        )

        # Create the combined box
        combined_box = Box(combined_top_left, combined_bottom_right)
        return combined_box
    else:
        return None


def get_bounding_box_polygon(polygon):
    # Initialize the bounding box with the first point in the polygon
    x_min, x_max = polygon[0][0], polygon[0][0]
    y_min, y_max = polygon[0][1], polygon[0][1]

    # Loop through each point in the polygon
    for point in polygon:
        # Update the bounding box based on the current point
        x_min = min(x_min, point[0])
        x_max = max(x_max, point[0])
        y_min = min(y_min, point[1])
        y_max = max(y_max, point[1])

    box = Box((x_min, y_max), (x_max, y_min))
    return box
