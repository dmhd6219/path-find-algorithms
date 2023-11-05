#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: Sviatoslav Sviatkin
"""
from __future__ import annotations

import heapq
import enum
import logging
import sys

logging.basicConfig(level=logging.DEBUG, filename="py_log.log", filemode="w")

MAP_LENGTH = 8


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
    """
        Represents a node on the map.

        Attributes:
            __x (int): X-coordinate.
            __y (int): Y-coordinate.
            __type (list[NodeType]): List of node types.
            __g (int): Distance to start node.
            __h (int): Distance to goal node.
            __f (int): Total cost.
            __parent (Node | None): Parent node.
            __map (Map): The map containing this node.
            __visited (bool): Whether the node has been visited.
            __neighbors (list[Node]): List of neighboring nodes.
        """

    __x: int
    __y: int
    __type: list[NodeType]

    __g: int  # Distance to start node
    __h: int  # Distance to goal node
    __f: int  # Total cost

    __parent: Node | None
    __map: Map

    __visited: bool
    __neighbors: list[Node]

    def __init__(self, x: int, y: int):
        """
        Initializes a Node on the map.

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
        """
        Check if the node represents a character.

        Returns:
            bool: True if the node represents a character, False otherwise.
        """
        return bool({NodeType.HULK, NodeType.THOR, NodeType.CAPTAIN} & set(self.type))

    def is_perception(self) -> bool:
        """
        Check if the node represents a perception.

        Returns:
            bool: True if the node represents a perception, False otherwise.
        """
        return NodeType.PERCEPTION in self.type

    def can_break_shield(self):
        """
        Check if this node represents a character that can break a shield.

        Returns:
            bool: True if the character can break a shield, False otherwise.
        """
        return NodeType.CAPTAIN in self.type

    def is_stone(self) -> bool:
        """
        Check if the node represents a stone.

        Returns:
            bool: True if the node represents a stone, False otherwise.
        """
        return NodeType.STONE in self.type

    def is_shield(self) -> bool:
        """
        Check if the node represents a shield.

        Returns:
            bool: True if the node represents a shield, False otherwise.
        """
        return NodeType.SHIELD in self.type

    def is_empty(self) -> bool:
        """
        Check if the node is empty.

        Returns:
            bool: True if the node is empty, False otherwise.
        """
        return len(self.type) == 0

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
        """
        Get a list of neighboring nodes.

        Returns:
            list[Node]: List of neighboring nodes.
        """
        return self.__neighbors

    def add_neighbor(self, neighbor: Node) -> list[Node]:
        """
        Add a neighboring node to the list of neighbors.

        Args:
            neighbor (Node): The neighboring node to add.

        Returns:
            list[Node]: Updated list of neighboring nodes.
        """
        if neighbor.__class__ != Node:
            raise ValueError("Neighbor should be only Node class instance")

        self.__neighbors.append(neighbor)
        return self.__neighbors

    @property
    def visited(self) -> bool:
        """
        Check if the node has been visited.

        Returns:
            bool: True if the node has been visited, False otherwise.
        """
        return self.__visited

    def visit(self) -> None:
        """
        Mark the node as visited.
        """
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
        """
        Get the parent node.

        Returns:
            Node | None: The parent node or None if no parent is assigned.
        """
        return self.__parent

    @parent.setter
    def parent(self, value: Node):
        self.__parent = value

    @property
    def type(self) -> list[NodeType]:
        """
        Get the list of node types.

        Returns:
            list[NodeType]: List of node types.
        """
        return self.__type

    def __repr__(self) -> str:
        """
        Return a string representation of the node.

        Returns:
            str: String representation of the node.
        """
        return f'Node{{X={self.__x};Y={self.__y};Info:[{",".join(map(lambda x: str(x).split(".")[-1], self.__type))}];}}'

    def __hash__(self) -> int:
        """
        Get the hash value of the node.

        Returns:
            int: The hash value of the node.
        """
        return self.__x * 100 + self.__y

    def __eq__(self, other: Node) -> bool:
        """
        Check if two nodes are equal.

        Args:
            other: Another node to compare to.

        Returns:
            bool: True if the nodes are equal, False otherwise.
        """
        return self.x == other.x and self.y == other.y

    def __lt__(self, other):
        """
        Compare two nodes based on their total cost (f).

        Args:
            other: Another node to compare to.

        Returns:
            bool: True if this node has a lower total cost (f) than the other node, False otherwise.
        """
        return self.f < other.f


class Thanos:
    """
    Represents the Thanos character on the map.

    Attributes:
        __perception_type (int): The perception type of Thanos.
        __x (int): X-coordinate of Thanos.
        __y (int): Y-coordinate of Thanos.
        __has_shield (bool): Whether Thanos has a shield.
    """

    __perception_type: int
    __x: int
    __y: int
    __has_shield: bool

    def __init__(self, perception_type: int):
        """
        Initializes Thanos character on the map.

        Args:
            perception_type (int): The perception type of Thanos.
        """
        self.__x = 0
        self.__y = 0
        self.__has_shield = False

        self.__perception_type = perception_type

    @property
    def perception_type(self) -> int:
        """
        Get the perception type of Thanos.

        Returns:
            int: The perception type of Thanos.
        """
        return self.__perception_type

    @property
    def x(self) -> int:
        """
        Get the X-coordinate of Thanos.

        Returns:
            int: The X-coordinate of Thanos.
        """
        return self.__x

    @property
    def y(self) -> int:
        """
        Get the Y-coordinate of Thanos.

        Returns:
            int: The Y-coordinate of Thanos.
        """
        return self.__y

    @property
    def has_shield(self) -> bool:
        """
        Check if Thanos has a shield.

        Returns:
            bool: True if Thanos has a shield, False otherwise.
        """
        return self.__has_shield

    def give_shield(self) -> None:
        """
        Give a shield to Thanos.
        """
        self.__has_shield = True

    def move(self, move_x: int, move_y: int) -> tuple[int, int]:
        """
        Move Thanos to a neighboring position on the map.

        Args:
            move_x (int): Change in X-coordinate.
            move_y (int): Change in Y-coordinate.

        Returns:
            tuple[int, int]: New X and Y coordinates of Thanos after the move.
        """

        if (abs(abs(move_x) - abs(self.x))) + (abs(abs(move_y) - abs(self.y))) > 1:
            logging.debug(f'Tried to go from {self.x}:{self.y} to {move_x}:{move_y}')
            raise WrongMoveException("Thanos can go only at neighbour coordinated")

        self.__x = move_x
        self.__y = move_y

        return self.__x, self.__y


class Map:
    """
    Represents the game map.

    Attributes:
        __map (list[list[Node]]): The map containing nodes.
        __thanos (Thanos): The Thanos character on the map.
        __steps (int): The number of steps taken in the game.
        __stone_coords (tuple[int, int]): Initial coordinates of the stone.
    """
    __map: list[list[Node]]
    __thanos: Thanos
    __steps: int
    __stone_coords: tuple[int, int]

    def __init__(self, perception_type: int, stone: tuple[int, int]):
        """
        Initializes the game map.

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

    def __repr__(self) -> str:
        """
        Return a string representation of the map.

        Returns:
            str: String representation of the map.
        """
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

    @property
    def thanos(self) -> Thanos:
        """
        Get the instance of Thanos for the game.

        Returns:
            Thanos: The instance of Thanos.
        """
        return self.__thanos

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

    def move_thanos(self, move_x: int, move_y: int) -> Node:
        """
        Move Thanos on the map and return the node he moved to.

        Args:
            move_x (int): Change in X-coordinate.
            move_y (int): Change in Y-coordinate.

        Returns:
            Node: The node that Thanos moved to.
        """
        move_coords = self.__thanos.move(move_x, move_y)
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

        if new_node.is_character() or new_node.is_perception():
            return False
        return True

    def get_possible_moves(self) -> list[tuple[int, int]]:
        """
        Get a list of possible moves for Thanos.

        Returns:
            list[tuple[int, int]]: List of possible move directions as (delta_x, delta_y).
        """
        moves = []
        for delta_x in range(-1, 2):
            for delta_y in range(-1, 2):
                if self.is_safe_move(delta_x, delta_y):
                    moves.append((delta_x, delta_y))

        return moves

    def get_path(self, start_node: Node, end_node: Node) -> list[Node]:
        """
        Get the path from start to end node.

        Args:
            start_node (Node): The starting node.
            end_node (Node): The ending node.

        Returns:
            list[Node]: List of nodes representing the path from start to end node.
            """
        to_start = []
        from_start = []

        current_node = start_node.parent
        while current_node:
            to_start.append(current_node)
            current_node = current_node.parent

        current_node = end_node.parent
        while current_node:
            from_start.append(current_node)
            current_node = current_node.parent

        from_start.reverse()

        path = to_start + from_start[1::]
        path.append(end_node)

        return path


class Assignment:
    """
        Represents the assignment and game-solving logic.

        Attributes:
            __field (Map): The game map.
            __start_node (Node): The starting node.
            __end_node (Node): The ending node.
        """
    __field: Map
    __start_node: Node
    __end_node: Node

    __min_distance: int

    def __init__(self):
        """
        Initializes new Assignment.
        """
        perception_type = int(input())
        x, y = [int(x) for x in input().split()]
        self.__field = Map(perception_type, (x, y))

        self.__start_node = self.field.get_node(0, 0)
        self.__end_node = self.field.get_node(x, y)

        self.__min_distance = sys.maxsize * 2 + 1

    @property
    def field(self):
        """
        Get the game map.

        Returns:
            Map: The game map.
        """
        return self.__field

    @property
    def start_node(self):
        """
        Get the starting node.

        Returns:
            Node: The starting node.
        """
        return self.__start_node

    @property
    def end_node(self):
        """
        Get the ending node.

        Returns:
            Node: The ending node.
        """
        return self.__end_node

    def move_on_path(self, path: list[Node]) -> None:
        """
        Move Thanos character along a specified path.

        Args:
            path (list[Node]): List of nodes representing the path.
        """
        for node in path:
            self.make_turn(node.x, node.y)

    def astar_search(self) -> int:
        """
        Perform an A* search algorithm to find the path to the stone.

        Returns:
            list[tuple[int, int]]: List of coordinates representing the path.
        """
        current_node = self.start_node

        # priority queue
        open_list = []
        heapq.heappush(open_list, self.start_node)

        # visited nodes
        closed_set = set()

        while open_list:
            start_node = current_node
            # get node with smallest f
            current_node = heapq.heappop(open_list)
            if current_node not in start_node.neighbors:
                path = self.field.get_path(self.field.get_node(self.field.thanos.x, self.field.thanos.y), current_node)
                if path:
                    self.move_on_path(path)
            else:
                self.make_turn(current_node.x, current_node.y)

            if current_node == self.end_node:
                path = []
                while current_node is not None:
                    path.append((current_node.x, current_node.y))
                    current_node = current_node.parent

                return len(path[::-1]) - 1

            closed_set.add(current_node)

            neighbors = []
            for move in self.field.get_possible_moves():
                move_x = self.field.thanos.x + move[0]
                move_y = self.field.thanos.y + move[1]

                neighbor = self.field.get_node(move_x, move_y)
                neighbors.append(neighbor)

            for neighbor in neighbors:
                if neighbor in closed_set:
                    continue

                new_g = current_node.g + 1

                if neighbor in open_list:

                    if new_g < neighbor.g:
                        neighbor.g = new_g
                        neighbor.h = Node.heuristics(self.end_node, neighbor)
                        neighbor.f = neighbor.g + neighbor.h
                        neighbor.parent = current_node

                        heapq.heapify(open_list)
                else:

                    neighbor.g = new_g
                    neighbor.h = Node.heuristics(self.end_node, neighbor)
                    neighbor.f = neighbor.g + neighbor.h
                    neighbor.parent = current_node

                    heapq.heappush(open_list, neighbor)

        return -1

    def backtracking_search(self):
        self.run_dfs()
        if self.__min_distance == sys.maxsize * 2 + 1:
            return -1
        return self.__min_distance

    def run_dfs(self,
                current_node: Node = None,
                current_distance: int = 0,
                visited: set = None
                ) -> None:

        if current_node is None:
            current_node = self.start_node
        if visited is None:
            visited = set()

        if current_node == self.end_node:
            self.__min_distance = min(self.__min_distance, current_distance)
            logging.debug(f"PATH : {visited}")
            return

        if current_distance >= self.__min_distance or current_node in visited:
            return
        visited.add(current_node)

        thanos_position = (self.field.thanos.x, self.field.thanos.y)
        self.make_turn(current_node.x, current_node.y)

        neighbors = []
        for move in self.field.get_possible_moves():
            move_x = self.field.thanos.x + move[0]
            move_y = self.field.thanos.y + move[1]

            neighbor = self.field.get_node(move_x, move_y)
            neighbors.append(neighbor)

        for neighbor in neighbors:
            if neighbor.g == 0 or neighbor.g > current_distance:
                neighbor.g = current_distance

                self.run_dfs(neighbor, current_distance + 1, visited)

        visited.remove(current_node)
        self.make_turn(*thanos_position)

    def end_solution(self, turns: int = -1) -> int:
        """
        End the game and print the number of turns taken.

        Args:
            turns (int): The number of turns taken (default is -1 if no turns taken).

        Returns:
            int: The number of turns taken.
        """
        print(f"e {turns}")
        return turns

    def make_turn(self, move_x: int, move_y: int):
        """
        Perform a turn by moving Thanos character and updating the game state.

        Args:
            move_x (int): Change in X-coordinate.
            move_y (int): Change in Y-coordinate.
        """
        turn_node = self.field.get_node(move_x, move_y)
        self.field.thanos.move(move_x, move_y)

        turn_node.visit()

        print(f"m {turn_node.x} {turn_node.y}")
        logging.debug(f"m {turn_node.x} {turn_node.y}")

        response = int(input())
        response_str = ""

        for _ in range(response):
            response = input()
            response_str += f"{response}; "
            info_x, info_y, info_status = response.split()

            node_type = NodeType(info_status)
            if node_type == NodeType.EMPTY:
                pass
            elif node_type == NodeType.SHIELD:
                self.field.thanos.give_shield()
            else:
                self.field.get_node(int(info_x), int(info_y)).add_info(NodeType(info_status))
        logging.debug(response_str)

    def solve(self):
        """
        Solve the game using A* or Backtracking search and make necessary turns to reach the solution.
        """
        # uncomment algorythm you want

        # path_length = self.astar_search()
        path_length = self.backtracking_search()
        self.end_solution(path_length)


def main() -> None:
    solver = Assignment()

    solver.solve()


if __name__ == "__main__":
    main()
