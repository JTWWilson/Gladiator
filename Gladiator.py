from abc import ABC
import pygame

__author__ = 'Jacob Wilson'


BOARD_SIZE = (4, 4)

CHECK_IN_BOARD = lambda x, y: 0 <= x <= BOARD_SIZE[0] and 0 <= y <= BOARD_SIZE[1]

GRID_SIZE = 100
MARGIN = 5

DARK_GREY = (100, 100, 100)
LIGHT_GREY = (150, 150, 150)

pygame.init()
pygame.display.set_mode((1000, 1000))

# Piece Images
BLACK_BISHOP = pygame.image.load('Images/BlackBishop.png').convert()
BLACK_EMPEROR = pygame.image.load('Images/BlackEmperor.png').convert()
BLACK_SWORDSMAN = pygame.image.load('Images/BlackSwordsman.png').convert()
BLACK_TIGER = pygame.image.load('Images/BlackTiger.png').convert()

GOLD_BISHOP = pygame.image.load('Images/GoldBishop.png').convert()
GOLD_EMPEROR = pygame.image.load('Images/GoldEmperor.png').convert()
GOLD_SWORDSMAN = pygame.image.load('Images/GoldSwordsman.png').convert()
GOLD_TIGER = pygame.image.load('Images/GoldTiger.png').convert()




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

    def get_image(self):
        return


class Emperor(Piece):
    def get_moves(self):
        theoretical_moves = [(self.position[0] + x, self.position[1] + y) for y in range(0, 2) for x in range(-1, 2)]
        return filter(CHECK_IN_BOARD, theoretical_moves)

    def get_takes(self):
        return self.get_moves()

    def get_image(self):
        return BLACK_EMPEROR if self.allegiance == 'BLACK' else GOLD_EMPEROR


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

    def get_image(self):
        return BLACK_BISHOP if self.allegiance == 'BLACK' else GOLD_BISHOP


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

    def get_image(self):
        return BLACK_SWORDSMAN if self.allegiance == 'BLACK' else GOLD_SWORDSMAN


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
                    pieces.append(key[item.strip()](x, y, 'Black' if y == 0 else 'Gold'))
                except KeyError:
                    pass

    return pieces


def display_board(screen, pieces):
    for y in range(BOARD_SIZE[1]):
        for x in range(BOARD_SIZE[0]):
            pygame.draw.rect(screen, DARK_GREY if (x + y) % 2 else LIGHT_GREY, (GRID_SIZE * x, GRID_SIZE * y, GRID_SIZE, GRID_SIZE))

    for piece in pieces:
        screen.blit(piece.get_image(), (GRID_SIZE * piece.x, GRID_SIZE * piece.y))

    pygame.display.flip()


if __name__ == '__main__':
    WINDOW = pygame.display.set_mode((1000, 1000))
    pygame.display.set_caption('Gladiator')

    pieces = create_pieces('default_board.csv', KEY)

    while True:
        display_board(WINDOW, pieces)