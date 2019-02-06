from abc import ABC
import pygame

__author__ = 'Jacob Wilson'


BOARD_SIZE = (4, 4)

CHECK_IN_BOARD = lambda pos: 0 <= pos[0] < BOARD_SIZE[0] and 0 <= pos[1] < BOARD_SIZE[1]

GRID_SIZE = 100
MARGIN = 5
HEIGHT = 1000
WIDTH = 1000


DARK_GREY = (100, 100, 100)
LIGHT_GREY = (150, 150, 150)

pygame.init()
pygame.display.set_mode((HEIGHT, WIDTH))

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

PIECE_TO_IMAGE = {
    'be': BLACK_EMPEROR,
    'bb': BLACK_BISHOP,
    'bw': BLACK_SWORDSMAN,
    'bt': BLACK_TIGER,
    'ge': GOLD_EMPEROR,
    'gb': GOLD_BISHOP,
    'gw': GOLD_SWORDSMAN,
    'gt': GOLD_TIGER,
    '-': '-'
}

BLACK_PIECES = (BLACK_EMPEROR, BLACK_BISHOP, BLACK_SWORDSMAN, BLACK_TIGER)
GOLD_PIECES = (GOLD_EMPEROR, GOLD_BISHOP, GOLD_SWORDSMAN, GOLD_TIGER)


def get_moves(piece, board):
    if board[piece[0]][piece[1]] == 'e':
        theoretical_moves = [(piece[0] + x, piece[1] + y) for y in range(0, 2) for x in range(-1, 2)]
        return filter(CHECK_IN_BOARD, theoretical_moves)

    elif board[piece[0]][piece[1]] == 'b':
        theoretical_moves = []
        for change in range(1, BOARD_SIZE[0]):
            theoretical_moves.append((piece[0] + change, piece[1] + change))
            theoretical_moves.append((piece[0] - change, piece[1] + change))
            theoretical_moves.append((piece[0] + change, piece[1] - change))
            theoretical_moves.append((piece[0] - change, piece[1] - change))

        return filter(CHECK_IN_BOARD, theoretical_moves)

    elif board[piece[0]][piece[1]] == 's':
        theoretical_moves = [(piece[0] + 1, piece[1] + 1),
                             (piece[0] - 1, piece[1] + 1),
                             (piece[0] + 1, piece[1] - 1),
                             (piece[0] - 1, piece[1] - 1)]
        return filter(CHECK_IN_BOARD, theoretical_moves)


def get_takes(piece, board):
    if board[piece[0]][piece[1]] == 'e':
        theoretical_moves = [(piece[0] + x, piece[1] + y) for y in range(0, 2) for x in range(-1, 2)]
        return filter(CHECK_IN_BOARD, theoretical_moves)

    elif board[piece[0]][piece[1]] == 'b':
        theoretical_moves = []
        for change in range(1, BOARD_SIZE[0]):
            theoretical_moves.append((piece[0] + change, piece[1] + change))
            theoretical_moves.append((piece[0] - change, piece[1] + change))
            theoretical_moves.append((piece[0] + change, piece[1] - change))
            theoretical_moves.append((piece[0] - change, piece[1] - change))

        return filter(CHECK_IN_BOARD, theoretical_moves)

    elif board[piece[0]][piece[1]] == 's':
        theoretical_takes = [(piece[0] + 1, piece[1]),
                             (piece[0] - 1, piece[1]),
                             (piece[0], piece[1] + 1),
                             (piece[0], piece[1] - 1)
                            ]
        return filter(CHECK_IN_BOARD, theoretical_takes)


def create_board(path):
    board = []
    with open(path) as board_file:
        for y, line in enumerate(board_file.readlines()):
            row = []
            for x, item in enumerate(line.split(',')):
                try:
                    row.append(PIECE_TO_IMAGE[('b' if y == 0 else 'g' if y == BOARD_SIZE[1] - 1 else '') + item.strip()])
                except KeyError:
                    pass
            board.append(row)
    return board


def display_board(screen, board, dead):
    screen.fill((0, 0, 0))
    for y, row in enumerate(board):
        for x, item in enumerate(row):
            if item == '-':
                pygame.draw.rect(screen, DARK_GREY if (x + y) % 2 else LIGHT_GREY, (GRID_SIZE * x, GRID_SIZE * y, GRID_SIZE, GRID_SIZE))
            else:
                screen.blit(item, (GRID_SIZE * x, GRID_SIZE * y))

    for index, piece in enumerate(dead['BLACK']):
        screen.blit(piece.get_image(), (GRID_SIZE * (BOARD_SIZE + 2), GRID_SIZE * index))
    for index, piece in enumerate(dead['BLACK']):
        screen.blit(piece.get_image(), (GRID_SIZE * (BOARD_SIZE + 3) + MARGIN, GRID_SIZE * index))


if __name__ == '__main__':
    WINDOW = pygame.display.set_mode((1000, 1000))
    pygame.display.set_caption('Gladiator')

    board = create_board('default_board.csv')
    dead = {'BLACK': [], 'GOLD': []}

    selected = None
    selected_position = (0, 0)

    display_board(WINDOW, board, dead)
    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                display_board(WINDOW, board, dead)
                if event.button == 1:
                    selected = (event.pos[0] // GRID_SIZE, event.pos[1] // GRID_SIZE)
                    board[selected[0]][selected[1]] = '-'
                    WINDOW.blit(selected.get_image(), (event.pos[0] - selected_position[0], event.pos[1] - selected_position[1]))
                    for move in get_moves(selected, board):
                        if board[move[0]][move[1]] == None:
                            WINDOW.blit(HIGHLIGHT_MOVE, (GRID_SIZE * move[0], GRID_SIZE * move[1]))
                    for take in get_takes(selected, board):
                        if selected in GOLD_PIECES and board[take[0]][take[1]] in BLACK_PIECES or \
                           selected in BLACK_PIECES and board[take[0]][take[1]] in GOLD_PIECES:
                            WINDOW.blit(HIGHLIGHT_TAKE, (GRID_SIZE * take[0], GRID_SIZE * take[1]))
            elif event.type == pygame.MOUSEMOTION:
                if selected is not None:
                    display_board(WINDOW, board, dead)
                    WINDOW.blit(selected.get_image(), (event.pos[0] - selected_position[0], event.pos[1] - selected_position[1]))
            elif event.type == pygame.MOUSEBUTTONUP:
                if selected is not None and event.button == 1:
                    current_tile = (event.pos[0] // GRID_SIZE, event.pos[1] // GRID_SIZE)
                    if current_tile in selected.get_takes():
                        pass

                    elif current_tile in selected.get_moves():
                        selected.position = current_tile
                    display_board(WINDOW, pieces)
                    selected = None
        pygame.display.flip()
