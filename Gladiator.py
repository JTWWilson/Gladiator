from abc import ABC
import pygame

__author__ = 'Jacob Wilson'


BOARD_SIZE = (4, 4)

CHECK_IN_BOARD = lambda pos: 0 <= pos[0] <= BOARD_SIZE[0] and 0 <= pos[1] <= BOARD_SIZE[1]

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

HIGHLIGHT_MOVE = pygame.image.load('Images/HighlightMove.png').convert_alpha()
HIGHLIGHT_TAKE = pygame.image.load('Images/HighlightTake.png').convert_alpha()


class Piece(ABC):
    def __init__(self, x, y, allegiance):
        self.position = [x, y]
        self.allegiance = allegiance
        self.selected = False

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

    for piece in filter(lambda x: not x.selected, pieces):
        screen.blit(piece.get_image(), (GRID_SIZE * piece.x, GRID_SIZE * piece.y))





if __name__ == '__main__':
    WINDOW = pygame.display.set_mode((1000, 1000))
    pygame.display.set_caption('Gladiator')

    pieces = create_pieces('default_board.csv', KEY)

    selected = None
    selected_position = (0, 0)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                display_board(WINDOW, pieces)
                if event.button == 1:
                    selected = None
                    for piece in pieces:
                        if pygame.Rect(piece.x * GRID_SIZE, piece.y * GRID_SIZE, GRID_SIZE, GRID_SIZE).collidepoint(event.pos[0], event.pos[1]):
                            #piece.selected = True
                            selected = piece
                            selected_position = (event.pos[0] % GRID_SIZE, event.pos[1] % GRID_SIZE)
                    if selected is not None:
                        for move in selected.get_moves():
                            WINDOW.blit(HIGHLIGHT_MOVE, (move[0] * GRID_SIZE, move[1] * GRID_SIZE))
                        for take in selected.get_takes():
                            if any(p.position == take for p in pieces):
                                WINDOW.blit(HIGHLIGHT_TAKE, (take[0] * GRID_SIZE, take[1] * GRID_SIZE))
            elif event.type == pygame.MOUSEMOTION:
                if selected is not None:
                    display_board(WINDOW, filter(lambda x: x is not selected, pieces))
                    WINDOW.blit(selected.get_image(), (event.pos[0] - selected_position[0], event.pos[1] - selected_position[1]))
            elif event.type == pygame.MOUSEBUTTONUP:
                if selected is not None and event.button == 1:
                    current_tile = (event.pos[0] // GRID_SIZE, event.pos[1] // GRID_SIZE)
                    if current_tile in selected.get_takes() or current_tile in selected.get_moves():
                        selected.position = current_tile
                    display_board(WINDOW, pieces)
                    selected = None
        pygame.display.flip()
