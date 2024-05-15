from polygon_utils import *
from enum import Enum


class BoxOverlap(Enum):
    Mixed = 0
    Obstacle = 1
    FreeSpace = 2


class BoxChecker:
    def __init__(self, workspace, obstacles):
        self.workspace = workspace
        self.obstacles = obstacles

    def check_for_box(self, box):
        if (box.isBoxEnclosedByPolygon(self.workspace)):
            for obstacle in self.obstacles:
                if(box.isBoxEnclosedByPolygon(obstacle)):
                    return BoxOverlap.Obstacle
                if(box.isPolygonInsideBox(obstacle)):                
                    return BoxOverlap.Mixed
                if(box.hasIntersectionWithPolygonPoints(obstacle)):
                    return BoxOverlap.Mixed
            return BoxOverlap.FreeSpace

        elif (box.hasIntersectionWithPolygonPoints(self.workspace)):
            return BoxOverlap.Mixed
        
        return BoxOverlap.Obstacle
        


