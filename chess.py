
from utils import *
from pprint import pprint
# https://github.com/niklasf/python-chess
# use inconjunction with typst


def parse_fen(fen):
    # Mapping from FEN notation to piece piece and color
    piece_mapping = {
        'p': {'piece': 'pawn', 'color': 'black'},
        'r': {'piece': 'rook', 'color': 'black'},
        'n': {'piece': 'knight', 'color': 'black'},
        'b': {'piece': 'bishop', 'color': 'black'},
        'q': {'piece': 'queen', 'color': 'black'},
        'k': {'piece': 'king', 'color': 'black'},
        'P': {'piece': 'pawn', 'color': 'white'},
        'R': {'piece': 'rook', 'color': 'white'},
        'N': {'piece': 'knight', 'color': 'white'},
        'B': {'piece': 'bishop', 'color': 'white'},
        'Q': {'piece': 'queen', 'color': 'white'},
        'K': {'piece': 'king', 'color': 'white'}
    }

    # Split the FEN string into parts
    parts = fen.split(' ')
    if len(parts) != 6:
        raise ValueError("Invalid FEN: should contain 6 space-separated fields")

    # Parse the board layout
    board_layout = parts[0]
    rows = board_layout.split('/')
    if len(rows) != 8:
        raise ValueError("Invalid board layout: should contain 8 rows")

    board = []
    for row in rows:
        board_row = []
        for char in row:
            if char.isdigit():
                # Empty squares
                board_row.extend([None] * int(char))
            else:
                # Pieces
                piece = piece_mapping.get(char)
                if piece:
                    board_row.append(piece)
                else:
                    raise ValueError(f"Invalid piece character: {char}")
        board.append(board_row)

    # Active color
    active_color = parts[1]

    # Castling availability
    castling = parts[2]

    # En passant target square
    en_passant = parts[3]

    # Halfmove clock
    halfmove_clock = parts[4]

    # Fullmove number
    fullmove_number = parts[5]

    # Constructing the JSON object
    fen_json = {
        'board': board,
        'active_color': active_color,
        'last_move': None,
    }

    return fen_json

fen_str = "r4rk1/pb3pp1/2p1pn1p/2P1B3/1P6/q3R1P1/P1Q2P1P/R4BK1 b - - 4 21"
fen_json = parse_fen(fen_str)
clip(fen_json)

