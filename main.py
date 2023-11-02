#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: Sviatoslav Sviatkin
"""
from __future__ import annotations

from utils.exceptions import WrongMoveException
from utils.types import NodeType

MAP_LENGTH = 8


class Node:
    __x: int
    __y: int
    __type: list[NodeType]

    __g: int  # Distance to start node
    __h: int  # Distance to goal node
    __f: int  # Total cost

    __neighbors: list[Node]  # Neighbors of this Node
    __map: Map

    def __init__(self, x: int, y: int, field: Map, type_: NodeType = None):
        """
               Represents a node on the map.
               Args:
                   x (int): X-coordinate.
                   y (int): Y-coordinate.
                   field (Map): field with all nodes.
                   type_ (NodeType): Type of the node.
               """
        self.__x = x
        self.__y = y
        self.__type = []

        if type_ is not None:
            self.__type.append(type_)

        self.__g = 0
        self.__h = 0
        self.__f = 0

        # add neighbours
        self.__neighbors = []

        neighbor_x = self.x
        neighbor_y = self.y
        if neighbor_x + 1 <= MAP_LENGTH:
            self.__neighbors.append(field.get_node(neighbor_x + 1, neighbor_y))
        if neighbor_x - 1 >= 0:
            self.__neighbors.append(field.get_node(neighbor_x - 1, neighbor_y))
        if neighbor_y + 1 <= MAP_LENGTH:
            self.__neighbors.append(field.get_node(neighbor_x, neighbor_y + 1))
        if neighbor_y - 1 >= 0:
            self.__neighbors.append(field.get_node(neighbor_x, neighbor_y - 1))

    def add_info(self, type_: NodeType) -> None:
        """Add information about the node type."""
        self.__type.append(type_)

    @staticmethod
    def heuristics(node1: Node, node2: Node) -> int:
        """Calculate heuristic distance between two nodes."""
        return abs(node1.x - node2.x) + abs(node1.y - node2.y)

    @property
    def x(self) -> int:
        """Get the X-coordinate of the node."""
        return self.__x

    @property
    def y(self) -> int:
        """Get the Y-coordinate of the node."""
        return self.__y

    @property
    def f(self) -> int:
        """Get the total cost (f) of the node."""
        return self.__g + self.__h

    @property
    def g(self) -> int:
        """Get the distance to the start node (g) of the node."""
        return self.__g

    @property
    def h(self) -> int:
        """Get the heuristic distance to the goal node (h) of the node."""
        return self.__h

    @property
    def neighbors(self) -> list[Node]:
        return self.__neighbors

    def __repr__(self):
        return f'Node{{X={self.__x};Y={self.__y};Info:[{",".join(map(lambda x: str(x).split(".")[-1], self.__type))}];}}'

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __lt__(self, other):
        return self.f < other.f


class Thanos:
    __perception_type: int
    __x: int
    __y: int
    __has_shield: bool

    def __init__(self, perception_type: int):
        """
            Represents Thanos character on the map.

            Args:
                perception_type (int): The perception type of Thanos.
            """
        self.__x = 0
        self.__y = 0
        self.__has_shield = False

        self.__perception_type = perception_type

    @property
    def perception_type(self) -> int:
        """Get the perception type of Thanos."""
        return self.__perception_type

    @property
    def x(self) -> int:
        """Get the X-coordinate of Thanos."""
        return self.__x

    @property
    def y(self) -> int:
        """Get the Y-coordinate of Thanos."""
        return self.__y

    @property
    def has_shield(self):
        """Check if Thanos has a shield."""
        return self.__has_shield

    def give_shield(self):
        """Give a shield to Thanos."""
        self.__has_shield = True

    def move(self, delta_x: int, delta_y: int) -> tuple[int, int]:
        """
        Move Thanos to a neighboring position on the map.

        Args:
            delta_x (int): Change in X-coordinate.
            delta_y (int): Change in Y-coordinate.

        Returns:
            tuple[int, int]: New X and Y coordinates of Thanos after the move.
        """
        if not (-1 <= delta_x + delta_y <= 1):
            raise WrongMoveException("Thanos can go only at neighbour coordinated")

        self.__x += delta_x
        self.__y += delta_y

        return self.__x, self.__y


class Map:
    __map: list[list[Node]]
    __thanos: Thanos
    __steps: int
    __stone_coords: tuple[int, int]

    def __init__(self, perception_type: int, stone: tuple[int, int]):
        """
        Represents the game map.

        Args:
            perception_type (int): The perception type of Thanos.
            stone (tuple[int, int]): Initial coordinates of the stone.
        """
        self.thanos = Thanos(perception_type)
        self.__map = [[Node(x, y) for y in range(0, MAP_LENGTH + 1)] for x in range(0, MAP_LENGTH + 1)]
        self.__map[stone[0]][stone[1]].add_info(NodeType.STONE)
        self.__steps = 0
        self.__stone_coords = stone

    def __repr__(self):
        max_width = max([max(len(str(element)) for element in row) for row in self.__map])

        return "\n".join(" | ".join(str(element).ljust(max_width) for element in row) for row in self.__map)

    @property
    def steps(self):
        """Get the number of steps taken in the game."""
        return self.__steps

    def get_node(self, x: int, y: int):
        """
        Get a node from the map by its coordinates.

        Args:
            x (int): X-coordinate of the node.
            y (int): Y-coordinate of the node.

        Returns:
            Node: The node at the specified coordinates.
        """
        if (not 0 <= x <= MAP_LENGTH + 1) or (not 0 <= y <= MAP_LENGTH + 1):
            raise IndexError(f"Map is {MAP_LENGTH}x{MAP_LENGTH}, Point ({x}, {y}) is out of bounds")

        return self.__map[x][y]

    def move_thanos(self, delta_x: int, delta_y: int) -> Node:
        """
        Move Thanos on the map and return the node he moved to.

        Args:
            delta_x (int): Change in X-coordinate.
            delta_y (int): Change in Y-coordinate.

        Returns:
            Node: The node that Thanos moved to.
        """
        move_coords = self.thanos.move(delta_x, delta_y)
        self.__steps += 1
        return self.__map[move_coords[0]][move_coords[1]]

    def astar_search(self):
        pass


def main() -> None:
    perception_type = int(input())
    x, y = [int(x) for x in input().split()]

    field = Map(perception_type, (x, y))


main()
