from __future__ import annotations

from utils.exceptions import WrongMoveException
from utils.types import NodeType


class Node:
    __x: int
    __y: int
    __type: list[NodeType]

    __g: int  # Distance to start node
    __h: int  # Distance to goal node
    __f: int  # Total cost

    def __init__(self, x: int, y: int, type_: NodeType = None):
        self.__x = x
        self.__y = y
        self.__type = []

        if type_ is not None:
            self.__type.append(type_)

        self.__g = 0
        self.__h = 0
        self.__f = 0

    def add_info(self, type_: NodeType) -> None:
        self.__type.append(type_)

    @staticmethod
    def heuristics(node1: Node, node2: Node) -> int:
        return abs(node1.x - node2.x) + abs(node1.y - node2.y)

    @property
    def x(self) -> int:
        return self.__x

    @property
    def y(self) -> int:
        return self.__y

    @property
    def f(self) -> int:
        return self.__f

    @property
    def g(self) -> int:
        return self.__g

    @property
    def h(self) -> int:
        return self.__h

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
        self.__x = 0
        self.__y = 0
        self.__has_shield = False

        self.__perception_type = perception_type

    def get_perception_type(self) -> int:
        return self.__perception_type

    @property
    def x(self) -> int:
        return self.__x

    @property
    def y(self) -> int:
        return self.__y

    @property
    def has_shield(self):
        return self.__has_shield

    def give_shield(self):
        self.__has_shield = True

    def move(self, delta_x: int, delta_y: int) -> tuple[int, int]:
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
        self.thanos = Thanos(perception_type)
        self.__map = [[Node(x, y) for y in range(0, 9)] for x in range(0, 9)]
        self.__map[stone[0]][stone[1]].add_info(NodeType.STONE)
        self.__steps = 0
        self.__stone_coords = stone

    def __repr__(self):
        max_width = max([max(len(str(element)) for element in row) for row in self.__map])

        return "\n".join(" | ".join(str(element).ljust(max_width) for element in row) for row in self.__map)

    def get_node(self, x: int, y: int):
        if (not 0 <= x <= 9) or (not 0 <= y <= 9):
            raise IndexError(f"Map is 8x8, Point ({x}, {y}) is out of bounds")

        return self.__map[x][y]

    @property
    def steps(self):
        return self.__steps

    def move_thanos(self, delta_x: int, delta_y: int) -> Node:
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
