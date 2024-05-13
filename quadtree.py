import numpy as np
from quadtree_check import *


class Node:
    def __init__(self, x, y, width, height, depth):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.depth = depth
        self.children = None
        self.value = None

    def split(self):
        if self.children is not None:
            return
        self.children = []
        width = self.width // 2
        height = self.height // 2
        for i in range(2):
            for j in range(2):
                x = self.x + i * width
                y = self.y + j * height
                self.children.append(Node(x, y, width, height, self.depth + 1))

    def get(self, x, y):
        if self.children is None:
            return self.value
        index = 2 * (x > self.x) + (y > self.y)
        return self.children[index].get(x, y)

    def set(self, x, y, value):
        if self.children is not None:
            index = 2 * (x > self.x) + (y > self.y)
            self.children[index].set(x, y, value)
            return
        self.value = value