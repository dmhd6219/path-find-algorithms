from utils.exceptions import WrongMoveException
from utils.types import NodeType


class Node:
    __x: int
    __y: int
    __type: list[NodeType] = []

    def __init__(self, x: int, y: int, type_: NodeType = None):
        self.__x = x
        self.__y = y

        if type_ is not None:
            self.__type.append(type_)

    def add_info(self, type_: NodeType) -> None:
        self.__type.append(type_)

    @property
    def x(self) -> int:
        return self.__x

    @property
    def y(self) -> int:
        return self.__y


class Thanos:
    __perception_type: int
    __x: int = 0
    __y: int = 0

    def __init__(self, perception_type: int):
        self.__perception_type = perception_type

    def get_perception_type(self) -> int:
        return self.__perception_type

    @property
    def x(self) -> int:
        return self.__x

    @property
    def y(self) -> int:
        return self.__y

    def move(self, delta_x: int, delta_y: int) -> tuple[int, int]:
        if not (-1 <= delta_x + delta_y <= 1):
            raise WrongMoveException("Thanos can go only at neighbour coordinated")

        self.__x += delta_x
        self.__y += delta_y

        return self.__x, self.__y


class Map:
    __map: list[list[Node]]
    __thanos: Thanos
    __steps: int = 0

    def __init__(self, perception_type: int, stone: Node):
        self.thanos = Thanos(perception_type)
        self.__map = [[Node(x, y) for y in range(0, 9)] for x in range(0, 9)]
        self.__map[stone.x][stone.y] = stone

    def get_node(self, x: int, y: int):
        if (not 0 <= x <= 9) or (not 0 <= y <= 9):
            raise IndexError("Map is 8x8")

        return self.__map[x][y]

    @property
    def steps(self):
        return self.__steps

    def move_thanos(self, delta_x: int, delta_y: int) -> Node:
        move_coords = self.thanos.move(delta_x, delta_y)
        self.__steps += 1
        return self.__map[move_coords[0]][move_coords[1]]


def main() -> None:
    perception_type = int(input())
    stone_coords = [int(x) for x in input().split()]

    field = Map(perception_type, Node(*stone_coords, type_=NodeType.STONE))


if __name__ == "__main_":
    main()
