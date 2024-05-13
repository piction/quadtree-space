
from polygon_check import *
from enum import Enum

class BoxOverlap(Enum): 
  Mixed=0
  Obstacle=1
  FreeSpace=2

class Box:
  def __init__(self, top_left, bottom_right):
    self.top_left = top_left
    self.bottom_right = bottom_right

class BoxChecker:
  def __init__(self, workspace,obstacles):
    self.workspace = workspace
    self.obstacles = obstacles

  def check_for_box(self, box):
    # check box corners in workspace
    corners_in_workspace=[]
    corners_in_workspace.append(point_in_polygon(box.top_left, self.workspace))
    corners_in_workspace.append(point_in_polygon(box.bottom_right, self.workspace))
    corners_in_workspace.append(point_in_polygon((box.top_left[0], box.bottom_right[1]), self.workspace))
    corners_in_workspace.append(point_in_polygon((box.bottom_right[0], box.top_left[1]), self.workspace))

    # if all of corners result false return obstacle
    if not any(corners_in_workspace):
      return BoxOverlap.Obstacle

    elif not all(corners_in_workspace):
      return BoxOverlap.Mixed
    
    else:
      for obstacle in self.obstacles:
        corners_in_obstacle = []
        corners_in_obstacle.append(point_in_polygon(box.top_left,obstacle))
        corners_in_obstacle.append(point_in_polygon(box.bottom_right,obstacle))
        corners_in_obstacle.append(point_in_polygon((box.top_left[0], box.bottom_right[1]),obstacle))
        corners_in_obstacle.append(point_in_polygon((box.bottom_right[0], box.top_left[1]),obstacle))
        if any(corners_in_obstacle) and not all(corners_in_obstacle):
          return BoxOverlap.Mixed
        if all(corners_in_obstacle):
          return BoxOverlap.Obstacle
        # check if obstacle is inside the box? at least one obstacle point is then within box
        if point_in_polygon(obstacle[0], box):
          return BoxOverlap.Mixed
        
    return BoxOverlap.FreeSpace
    