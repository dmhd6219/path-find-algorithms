#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: Sviatoslav Sviatkin
"""
from __future__ import annotations

import heapq
import enum
import logging

MAP_LENGTH = 8
logging.basicConfig(level=logging.DEBUG, filename="py_log.log", filemode="w")


class WrongMoveException(Exception):
    pass


class NodeType(enum.Enum):
    EMPTY = "."
    PERCEPTION = "P"
    HULK = "H"
    THOR = "T"
    CAPTAIN = "M"
    SHIELD = "S"
    STONE = "I"


class Node:
    __x: int
    __y: int
    __type: list[NodeType]

    __g: int  # Distance to start node
    __h: int  # Distance to goal node
    __f: int  # Total cost

    __parent: Node | None
    __map: Map

    __visited: bool
    _neighbors: list[Node]

    def __init__(self, x: int, y: int):
        """
        Represents a node on the map.
        Args:
            x (int): X-coordinate.
            y (int): Y-coordinate.
        """
        self.__x = x
        self.__y = y
        self.__type = []

        self.__g = 0
        self.__h = 0
        self.__f = 0

        self.__parent = None
        self.__visited = False

        self.__neighbors = []

    def add_info(self, type_: NodeType) -> None:
        """
        Add information about the node type.

        Args:
            type_ (NodeType): The type of the node.
        """
        self.__type.append(type_)

    def is_character(self) -> bool:
        return bool({NodeType.HULK, NodeType.THOR, NodeType.CAPTAIN} & set(self.__type))

    def is_perception(self) -> bool:
        return NodeType.PERCEPTION in self.__type

    def is_stone(self) -> bool:
        return NodeType.STONE in self.__type

    def is_shield(self) -> bool:
        return NodeType.SHIELD in self.__type

    def is_empty(self) -> bool:
        return len(self.__type) == 0

    @staticmethod
    def heuristics(node1: Node, node2: Node) -> int:
        """
        Calculate heuristic distance between two nodes.

        Args:
            node1 (Node): The first node.
            node2 (Node): The second node.

        Returns:
            int: Heuristic distance between the two nodes.
        """
        return abs(node1.x - node2.x) + abs(node1.y - node2.y)

    @property
    def neighbors(self) -> list[Node]:
        return self.__neighbors

    def add_neighbor(self, neighbor: Node) -> list[Node]:
        if neighbor.__class__ != Node:
            raise ValueError("Neighbor should be only Node class instance")

        self.__neighbors.append(neighbor)
        return self.__neighbors

    @property
    def visited(self) -> bool:
        return self.__visited

    def visit(self) -> None:
        self.__visited = True

    @property
    def x(self) -> int:
        """
        Get the X-coordinate of the node.

        Returns:
            int: The X-coordinate.
        """
        return self.__x

    @property
    def y(self) -> int:
        """
        Get the Y-coordinate of the node.

        Returns:
            int: The Y-coordinate.
        """
        return self.__y

    @property
    def f(self) -> int:
        """
       Get the total cost (f) of the node.

       Returns:
           int: The total cost (f).
       """
        return self.__f

    @f.setter
    def f(self, value: int):
        self.__f = value

    @property
    def g(self) -> int:
        """
        Get the distance to the start node (g) of the node.

        Returns:
            int: The distance to the start node (g).
        """
        return self.__g

    @g.setter
    def g(self, value: int):
        self.__g = value

    @property
    def h(self) -> int:
        """
        Get the heuristic distance to the goal node (h) of the node.

        Returns:
            int: The heuristic distance to the goal node (h).
        """
        return self.__h

    @h.setter
    def h(self, value: int):
        self.__h = value

    @property
    def parent(self) -> Node | None:
        return self.__parent

    @parent.setter
    def parent(self, value: Node):
        self.__parent = value

    @property
    def type(self) -> list[NodeType]:
        return self.__type

    def __repr__(self) -> str:
        return f'Node{{X={self.__x};Y={self.__y};Info:[{",".join(map(lambda x: str(x).split(".")[-1], self.__type))}];}}'

    def __hash__(self) -> int:
        return self.__x * 100 + self.__y

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

    def get_perception_moves(self) -> list[tuple[int, int]]:
        # if self.__perception_type == 1:
        #     return [(-1, 0), (-1, 1), (0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1)]
        #
        # if self.__perception_type == 2:
        #     return [(-1, 0), (-1, 1), (0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1), (-2, 2), (2, 2), (2, -2),
        #             (-2, -2)]

        return []

    def get_perception_coords(self) -> list[tuple[int, int]]:
        return [(x[0] + self.x, x[1] + self.y) for x in self.get_perception_moves() if
                0 <= x[0] + self.x <= MAP_LENGTH and 0 <= x[1] + self.y <= MAP_LENGTH]

    @property
    def perception_type(self) -> int:
        """Get the perception type of Thanos."""
        return self.__perception_type

    @property
    def x(self) -> int:
        """
        Get the X-coordinate of Thanos.

        Returns:
            int: The X-coordinate.
        """
        return self.__x

    @property
    def y(self) -> int:
        """
        Get the Y-coordinate of Thanos.

        Returns:
            int: The Y-coordinate.
        """
        return self.__y

    @property
    def has_shield(self):
        """
        Check if Thanos has a shield.

        Returns:
            bool: True if Thanos has a shield, False otherwise.
        """
        return self.__has_shield

    def give_shield(self):
        """
        Give a shield to Thanos.
        """
        self.__has_shield = True

    def move(self, delta_x: int, delta_y: int, delta: bool = True) -> tuple[int, int]:
        """
        Move Thanos to a neighboring position on the map.

        Args:
            delta_x (int): Change in X-coordinate.
            delta_y (int): Change in Y-coordinate.

        Returns:
            tuple[int, int]: New X and Y coordinates of Thanos after the move.
        """
        if delta:
            if abs(delta_x) + abs(delta_y) > 1:
                logging.error(f"Tried to move on [{delta_x};{delta_y}]")
                raise WrongMoveException("Thanos can go only at neighbour coordinated")

            self.__x += delta_x
            self.__y += delta_y

        else:
            if (abs(abs(delta_x) - abs(self.x))) + (abs(abs(delta_y) - abs(self.y))) > 1:
                logging.error(f"Tried to move from [{self.x};{self.y}] to [{delta_x};{delta_y}]")
                raise WrongMoveException("Thanos can go only at neighbour coordinated")

            self.__x = delta_x
            self.__y = delta_y

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
        self.__thanos = Thanos(perception_type)
        self.__map = [[Node(x, y) for y in range(0, MAP_LENGTH + 1)] for x in range(0, MAP_LENGTH + 1)]

        # add neighbors to every node
        for i in self.__map:
            for j in i:
                neighbor_x = j.x
                neighbor_y = j.y
                if neighbor_x + 1 <= MAP_LENGTH:
                    j.add_neighbor(self.get_node(neighbor_x + 1, neighbor_y))
                if neighbor_x - 1 >= 0:
                    j.add_neighbor(self.get_node(neighbor_x - 1, neighbor_y))
                if neighbor_y + 1 <= MAP_LENGTH:
                    j.add_neighbor(self.get_node(neighbor_x, neighbor_y + 1))
                if neighbor_y - 1 >= 0:
                    j.add_neighbor(self.get_node(neighbor_x, neighbor_y - 1))

        self.__map[stone[0]][stone[1]].add_info(NodeType.STONE)
        self.__steps = 0
        self.__stone_coords = stone

    def __repr__(self):
        max_width = max([max(len(str(element)) for element in row) for row in self.__map])

        return "\n".join(" | ".join(str(element).ljust(max_width) for element in row) for row in self.__map)

    @property
    def steps(self):
        """
        Get the number of steps taken in the game.

        Returns:
            int: The number of steps.
        """
        return self.__steps

    def get_node(self, x: int, y: int) -> Node:
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
        move_coords = self.__thanos.move(delta_x, delta_y)
        self.__steps += 1
        return self.__map[move_coords[0]][move_coords[1]]

    def is_safe_move(self, delta_x: int, delta_y: int) -> bool:
        """
        Check if a move for Thanos is safe.

        Args:
            delta_x (int): Change in X-coordinate.
            delta_y (int): Change in Y-coordinate.

        Returns:
            bool: True if the move is safe, otherwise False.
                """
        if delta_x == 0 and delta_y == 0:
            return False

        if abs(delta_x) + abs(delta_y) > 1:
            return False

        new_x = self.__thanos.x + delta_x
        new_y = self.__thanos.y + delta_y

        if not (0 <= new_x <= MAP_LENGTH) or not (0 <= new_y <= MAP_LENGTH):
            return False

        new_node = self.get_node(new_x, new_y)
        # if new_node.visited:
        #     return False

        # for thanos_perception_move in self.__thanos.get_perception_coords():
        #     thanos_perception_x = thanos_perception_move[0]
        #     thanos_perception_y = thanos_perception_move[1]
        #     thanos_perception_node = self.get_node(thanos_perception_x, thanos_perception_y)
        #
        #     if thanos_perception_node.is_perception() or thanos_perception_node.is_character():
        #         return False

        if new_node.is_perception() or new_node.is_character():
            return False
        return True

    def get_possible_moves(self) -> list[tuple[int, int]]:
        moves = []
        for delta_x in range(-1, 2):
            for delta_y in range(-1, 2):
                if self.is_safe_move(delta_x, delta_y):
                    moves.append((delta_x, delta_y))

        return moves

    def return_to_start(self, end_node: Node):
        logging.debug("------")
        logging.debug(f"moving back, from [{end_node.x};{end_node.y}]")

        end_node.visit()
        prev_node = end_node
        end_node = end_node.parent

        while end_node != Node(0, 0):
            logging.debug(f"moving back, [{prev_node.x};{prev_node.y}]->[{end_node.x};{end_node.y}]")
            self.make_turn(end_node.x, end_node.y, False)
            prev_node = end_node
            end_node = end_node.parent

        logging.debug(f"moving back, [{prev_node.x};{prev_node.y}]->[{end_node.x};{end_node.y}]")
        self.make_turn(end_node.x, end_node.y, False)

        logging.debug("---------")

    def astar_search(self, end_node: Node):
        """
                Perform an A* search algorithm to find the path to the stone.
        """
        start_node = self.get_node(self.__thanos.x, self.__thanos.y)
        current_node = start_node

        # priority queue
        open_list = []
        heapq.heappush(open_list, start_node)

        # visited nodes
        closed_set = set()

        while open_list:
            start_node = current_node
            # get node with smallest f
            current_node = heapq.heappop(open_list)
            if (current_node not in start_node.neighbors) and (current_node != start_node):
                self.return_to_start(start_node)
                self.astar_search(current_node)
            else:
                self.make_turn(current_node.x, current_node.y, False)

            if current_node == end_node:
                path = []
                while current_node is not None:
                    path.append((current_node.x, current_node.y))
                    current_node = current_node.parent

                return path[::-1]

            closed_set.add(current_node)

            neighbors = []
            for move in self.get_possible_moves():
                move_x = self.__thanos.x + move[0]
                move_y = self.__thanos.y + move[1]

                neighbor = self.get_node(move_x, move_y)
                neighbors.append(neighbor)

            for neighbor in neighbors:
                if neighbor in closed_set or neighbor.visited:
                    continue

                new_g = current_node.g + 1

                if neighbor in open_list:

                    if new_g < neighbor.g:
                        neighbor.g = new_g
                        neighbor.h = Node.heuristics(end_node, neighbor)
                        neighbor.f = neighbor.g + neighbor.h
                        neighbor.parent = current_node

                        heapq.heapify(open_list)
                else:

                    neighbor.g = new_g
                    neighbor.h = Node.heuristics(end_node, neighbor)
                    neighbor.f = neighbor.g + neighbor.h
                    neighbor.parent = current_node

                    heapq.heappush(open_list, neighbor)

        return None

    def backtracking_search(self):
        pass

    def end_game(self, turns: int = -1) -> None:
        print(f"e {turns}")
        exit(0)

    def make_turn(self, delta_x: int, delta_y: int, delta: bool = True):
        if delta:
            turn_node = self.get_node(self.__thanos.x + delta_x, self.__thanos.y + delta_y)
            self.__thanos.move(delta_x, delta_y)
        else:
            turn_node = self.get_node(delta_x, delta_y)
            self.__thanos.move(delta_x, delta_y, delta=False)

        turn_node.visit()

        logging.debug(
            f"TURN MADE : to [{turn_node.x};{turn_node.y}]; Thanos now at [{self.__thanos.x};{self.__thanos.y}]")
        print(f"m {turn_node.x} {turn_node.y}")

        logging_string = ""
        response = int(input())
        logging_string += f"{response};"

        for _ in range(response):
            response = input()
            logging_string += f"{response};"
            info_x, info_y, info_status = response.split()
            self.get_node(int(info_x), int(info_y)).add_info(NodeType(info_status))
        logging.debug(f"RESPONSE GOT for [{turn_node.x};{turn_node.y}] : {logging_string}")


def main() -> None:
    perception_type = int(input())
    x, y = [int(x) for x in input().split()]

    field = Map(perception_type, (x, y))

    path = field.astar_search(field.get_node(x, y))
    field.end_game(len(path) if path else -1)


main()
