import pygame
from copy import copy

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
    'BLACKe': BLACK_EMPEROR,
    'BLACKb': BLACK_BISHOP,
    'BLACKw': BLACK_SWORDSMAN,
    'BLACKt': BLACK_TIGER,
    'GOLDe': GOLD_EMPEROR,
    'GOLDb': GOLD_BISHOP,
    'GOLDw': GOLD_SWORDSMAN,
    'GOLDt': GOLD_TIGER,
    '-': '-'
}

BLACK_PIECES = ('BLACKe', 'BLACKb', 'BLACKw', 'BLACKt')
GOLD_PIECES = ('GOLDe', 'GOLDb', 'GOLDw', 'GOLDt')

GOLD_EMPEROR_DIRECTION = [0, -1]
BLACK_EMPEROR_DIRECTION = [0, 1]

GOLD_TARGET_ROW = 0
BLACK_TARGET_ROW = BOARD_SIZE[1] - 1

is_empty_tile = lambda move: board[move[0]][move[1]] == '-'


def get_moves(piece, location, board):
    if piece[-1] == 'e':
        if piece[0] == 'B':
            theoretical_moves = [(location[0] + y, location[1] + x) for y in [0, BLACK_EMPEROR_DIRECTION[1]] for x in range(-1, 2)]
        else:
            theoretical_moves = [(location[0] + y, location[1] + x) for y in [0, GOLD_EMPEROR_DIRECTION[1]] for x in range(-1, 2)]
        theoretical_moves = filter(CHECK_IN_BOARD, theoretical_moves)
        theoretical_moves = list(filter(is_empty_tile, theoretical_moves))
        if location in theoretical_moves:
            theoretical_moves.remove(location)
        return theoretical_moves

    elif piece[-1] == 'b':
        theoretical_moves = []
        for change in range(1, BOARD_SIZE[0]):
            new_move = (location[0] + change, location[1] + change)
            if not CHECK_IN_BOARD(new_move):
                break
            if not is_empty_tile(new_move):
                break
            theoretical_moves.append(new_move)
        for change in range(1, BOARD_SIZE[0]):
            new_move = (location[0] - change, location[1] + change)
            if not CHECK_IN_BOARD(new_move):
                break
            if not is_empty_tile(new_move):
                break
            theoretical_moves.append(new_move)
        for change in range(1, BOARD_SIZE[0]):
            new_move = (location[0] + change, location[1] - change)
            if not CHECK_IN_BOARD(new_move):
                break
            if not is_empty_tile(new_move):
                break
            theoretical_moves.append(new_move)
        for change in range(1, BOARD_SIZE[0]):
            new_move = (location[0] - change, location[1] - change)
            if not CHECK_IN_BOARD(new_move):
                break
            if not is_empty_tile(new_move):
                break
            theoretical_moves.append(new_move)
        return theoretical_moves

    elif piece[-1] == 'w':
        theoretical_moves = [(location[0] + 1, location[1] + 1),
                             (location[0] - 1, location[1] + 1),
                             (location[0] + 1, location[1] - 1),
                             (location[0] - 1, location[1] - 1)]
        theoretical_moves = filter(CHECK_IN_BOARD, theoretical_moves)
        theoretical_moves = filter(lambda move: board[move[0]][move[1]] == '-', theoretical_moves)
        return theoretical_moves

    elif piece[-1] == 't':
        theoretical_moves = []
        for change in range(1, BOARD_SIZE[0]):
            new_move = (location[0], location[1] + change)
            if not CHECK_IN_BOARD(new_move):
                break
            if not is_empty_tile(new_move):
                break
            theoretical_moves.append(new_move)
        for change in range(1, BOARD_SIZE[0]):
            new_move = (location[0], location[1] - change)
            if not CHECK_IN_BOARD(new_move):
                break
            if not is_empty_tile(new_move):
                break
            theoretical_moves.append(new_move)
        for change in range(1, BOARD_SIZE[0]):
            new_move = (location[0] + change, location[1])
            if not CHECK_IN_BOARD(new_move):
                break
            if not is_empty_tile(new_move):
                break
            theoretical_moves.append(new_move)
        for change in range(1, BOARD_SIZE[0]):
            new_move = (location[0] - change, location[1])
            if not CHECK_IN_BOARD(new_move):
                break
            if not is_empty_tile(new_move):
                break
            theoretical_moves.append(new_move)
        return theoretical_moves


def get_takes(piece, location, board):

    def check_other_piece(take):
        if piece in BLACK_PIECES:
            return board[take[0]][take[1]] in GOLD_PIECES
        if piece in GOLD_PIECES:
            return board[take[0]][take[1]] in BLACK_PIECES

    if piece[-1] == 'e':
        if piece[0] == 'B':
            theoretical_takes = [(location[0] + y, location[1] + x) for y in [0, BLACK_EMPEROR_DIRECTION[1]] for x in range(-1, 2)]
        else:
            theoretical_takes = [(location[0] + y, location[1] + x) for y in [0, GOLD_EMPEROR_DIRECTION[1]] for x in range(-1, 2)]
        theoretical_takes = filter(CHECK_IN_BOARD, theoretical_takes)
        theoretical_takes = list(filter(check_other_piece, theoretical_takes))
        if location in theoretical_takes:
            theoretical_takes.remove(location)
        return theoretical_takes

    elif piece[-1] == 'b':
        theoretical_takes = []
        for change in range(1, BOARD_SIZE[0]):
            new_take = (location[0] + change, location[1] + change)
            if not CHECK_IN_BOARD(new_take):
                break
            theoretical_takes.append(new_take)
        for change in range(1, BOARD_SIZE[0]):
            new_take = (location[0] - change, location[1] + change)
            if not CHECK_IN_BOARD(new_take):
                break
            theoretical_takes.append(new_take)
        for change in range(1, BOARD_SIZE[0]):
            new_take = (location[0] + change, location[1] - change)
            if not CHECK_IN_BOARD(new_take):
                break
            theoretical_takes.append(new_take)
        for change in range(1, BOARD_SIZE[0]):
            new_take = (location[0] - change, location[1] - change)
            if not CHECK_IN_BOARD(new_take):
                break
            theoretical_takes.append(new_take)
        theoretical_takes = filter(check_other_piece, theoretical_takes)
        return list(theoretical_takes)

    elif piece[-1] == 'w':
        theoretical_takes = [(location[0] + 1, location[1]),
                             (location[0] - 1, location[1]),
                             (location[0], location[1] + 1),
                             (location[0], location[1] - 1)
                            ]
        theoretical_takes = filter(CHECK_IN_BOARD, theoretical_takes)
        theoretical_takes = filter(check_other_piece, theoretical_takes)
        return theoretical_takes

    elif piece[-1] == 't':
        theoretical_takes = []
        return []

        for change in range(1, BOARD_SIZE[0]):
            new_move = (location[0], location[1] + change)
            if not CHECK_IN_BOARD(new_move):
                break
            if not is_empty_tile(new_move):
                break
            theoretical_moves.append(new_move)
        for change in range(1, BOARD_SIZE[0]):
            new_move = (location[0], location[1] - change)
            if not CHECK_IN_BOARD(new_move):
                break
            if not is_empty_tile(new_move):
                break
            theoretical_moves.append(new_move)
        for change in range(1, BOARD_SIZE[0]):
            new_move = (location[0] + change, location[1])
            if not CHECK_IN_BOARD(new_move):
                break
            if not is_empty_tile(new_move):
                break
            theoretical_moves.append(new_move)
        for change in range(1, BOARD_SIZE[0]):
            new_move = (location[0] - change, location[1])
            if not CHECK_IN_BOARD(new_move):
                break
            if not is_empty_tile(new_move):
                break
            theoretical_moves.append(new_move)
        return theoretical_moves


def create_board(path):
    board = []
    with open(path) as board_file:
        for y, line in enumerate(board_file.readlines()):
            row = []
            for x, item in enumerate(line.split(',')):
                try:
                    row.append(('BLACK' if y == 0 else 'GOLD' if y == BOARD_SIZE[1] - 1 else '') + item.strip())
                except KeyError:
                    pass
            board.append(row)
    return board


def display_board(screen, board, dead):
    screen.fill((0, 0, 0))
    for x, row in enumerate(board):
        for y, item in enumerate(row):
            if item == '-':
                pygame.draw.rect(screen, DARK_GREY if (x + y) % 2 else LIGHT_GREY, (GRID_SIZE * y, GRID_SIZE * x, GRID_SIZE, GRID_SIZE))
            else:
                screen.blit(PIECE_TO_IMAGE[item], (GRID_SIZE * y, GRID_SIZE * x))

    for index, piece in enumerate(dead['BLACK']):
        screen.blit(PIECE_TO_IMAGE[piece], (GRID_SIZE * (BOARD_SIZE[0] + 2), GRID_SIZE * index))
    for index, piece in enumerate(dead['GOLD']):
        screen.blit(PIECE_TO_IMAGE[piece], (GRID_SIZE * (BOARD_SIZE[0] + 3) + MARGIN, GRID_SIZE * index))


def check_win(board):
    if not any(['GOLDe' in row for row in board]):
        print('BLACK WIN')
        quit()
    if not any(['BLACKe' in row for row in board]):
        print('GOLD WIN')
        quit()


def rotate_board(board, piece, dead):



if __name__ == '__main__':
    WINDOW = pygame.display.set_mode((1000, 1000))
    pygame.display.set_caption('Gladiator')

    board = create_board('default_board.csv')
    dead = {'BLACK': [], 'GOLD': []}

    selected = None
    piece = None
    selected_position = (0, 0)
    turn = GOLD_PIECES

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
                    selected = (event.pos[1] // GRID_SIZE, event.pos[0] // GRID_SIZE)
                    selected_position = (event.pos[1] % GRID_SIZE, event.pos[0] % GRID_SIZE)
                    piece = board[selected[0]][selected[1]]
                    if piece not in turn:
                        selected = None
                        piece = None
                        continue
                    board[selected[0]][selected[1]] = '-'
                    WINDOW.blit(PIECE_TO_IMAGE[piece], (event.pos[0] - selected_position[0], event.pos[1] - selected_position[1]))
                    for move in get_moves(piece, selected, board):
                        if board[move[0]][move[1]] == '-':
                            WINDOW.blit(HIGHLIGHT_MOVE, (GRID_SIZE * move[1], GRID_SIZE * move[0]))
                    for take in get_takes(piece, selected, board):
                        WINDOW.blit(HIGHLIGHT_TAKE, (GRID_SIZE * take[1], GRID_SIZE * take[0]))
                    pygame.display.flip()
            elif event.type == pygame.MOUSEMOTION:
                if selected is not None:
                    display_board(WINDOW, board, dead)
                    for move in get_moves(piece, selected, board):
                        if board[move[0]][move[1]] == '-':
                            WINDOW.blit(HIGHLIGHT_MOVE, (GRID_SIZE * move[1], GRID_SIZE * move[0]))
                    for take in get_takes(piece, selected, board):
                        WINDOW.blit(HIGHLIGHT_TAKE, (GRID_SIZE * take[1], GRID_SIZE * take[0]))
                    WINDOW.blit(PIECE_TO_IMAGE[piece], (event.pos[0] - selected_position[0], event.pos[1] - selected_position[1]))
            elif event.type == pygame.MOUSEBUTTONUP:
                if selected is not None and event.button == 1:
                    current_tile = (event.pos[1] // GRID_SIZE, event.pos[0] // GRID_SIZE)
                    if current_tile in get_takes(piece, selected, board):
                        if board[current_tile[0]][current_tile[1]] in BLACK_PIECES:
                            dead['BLACK'].append((board[current_tile[0]][current_tile[1]]))
                        elif board[current_tile[0]][current_tile[1]] in GOLD_PIECES:
                            dead['GOLD'].append((board[current_tile[0]][current_tile[1]]))
                        board[current_tile[0]][current_tile[1]] = piece
                    elif current_tile in get_moves(piece, selected, board):
                        board[current_tile[0]][current_tile[1]] = piece
                    else:
                        board[selected[0]][selected[1]] = piece
                    display_board(WINDOW, board, dead)

                    if piece == 'GOLDe':
                        rotate_board(board, piece, dead)
                    if piece == 'BLACKe':
                        rotate_board(board, piece, dead)

                    selected = None
                    piece = None
                    turn = BLACK_PIECES if turn == GOLD_PIECES else GOLD_PIECES
                    check_win(board)
        pygame.display.flip()
