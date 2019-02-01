from abc import ABC

BOARD_SIZE = (4, 4)

CHECK_IN_BOARD = lambda x, y: 0 <= x <= BOARD_SIZE[0] and 0 <= y <= BOARD_SIZE[1]

GRID_SIZE = 50
MARGIN = 5

class Piece(ABC):
    def __init__(self, x, y, allegiance):
        self.position = [x, y]
        self.allegiance = allegiance

    @property
    def x(self):
        return self.position[0]

    @property
    def y(self):
        return self.position[1]

    def get_moves(self):
        return ()

    def get_takes(self):
        return ()


class Emperor(Piece):
    def get_moves(self):
        theoretical_moves = [(self.position[0] + x, self.position[1] + y) for y in range(0, 2) for x in range(-1, 2)]
        return filter(CHECK_IN_BOARD, theoretical_moves)

    def get_takes(self):
        return self.get_moves()


class Bishop(Piece):
    def get_moves(self):
        theoretical_moves = []
        for change in range(1, BOARD_SIZE[0]):
            theoretical_moves.append((self.position[0] + change, self.position[1] + change))
            theoretical_moves.append((self.position[0] - change, self.position[1] + change))
            theoretical_moves.append((self.position[0] + change, self.position[1] - change))
            theoretical_moves.append((self.position[0] - change, self.position[1] - change))

        return filter(CHECK_IN_BOARD, theoretical_moves)

    def get_takes(self):
        return self.get_moves()


class Swordsman(Piece):
    def get_moves(self):
        theoretical_moves = [(self.position[0] + 1, self.position[1] + 1),
                             (self.position[0] - 1, self.position[1] + 1),
                             (self.position[0] + 1, self.position[1] - 1),
                             (self.position[0] - 1, self.position[1] - 1)]
        return filter(CHECK_IN_BOARD, theoretical_moves)

    def get_takes(self):
        theoretical_takes = [(self.position[0] + 1, self.position[1]),
                             (self.position[0] - 1, self.position[1]),
                             (self.position[0], self.position[1] + 1),
                             (self.position[0], self.position[1] - 1)
                            ]
        return filter(CHECK_IN_BOARD, theoretical_takes)


class Tiger(Piece):
    pass


KEY = {'e': Emperor,
       'b': Bishop,
       'w': Swordsman,
       't': Tiger
       }


def create_pieces(path, key):
    pieces = []
    with open(path) as board_file:
        for y, line in enumerate(board_file.readlines()):
            for x, item in enumerate(line.split(',')):
                try:
                    pieces.append(key[item.strip()](x, y))
                except KeyError:
                    pass

    return pieces


def display_board(screen, pieces)




print(create_pieces('default_board.csv', KEY))
