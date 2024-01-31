from math import floor
import enum

# ----------------------------
#           pieces
# ----------------------------


class PieceType(enum.Enum):
    _pw = -1
    _pb = 1
    wK, wQ, wR, wB, wN, wP = _pw * 2, _pw * 3, _pw * 4, _pw * 5, _pw * 6, _pw * 7
    bK, bQ, bR, bB, bN, bP = _pb * 2, _pb * 3, _pb * 4, _pb * 5, _pb * 6, _pb * 7


class Place:
    __slots__ = (
        "file",
        "rank",
        "piece",
    )

    def __init__(self, file: int, rank: int, piece: PieceType) -> None:
        self.file = file
        self.rank = rank
        self.piece = piece


class Node:
    def __init__(self) -> None:
        pass


class Edge:
    __slots__ = ("t_from", "t_to", "piece")

    def __init__(self, t_from: int, t_to: int, piece) -> None:
        pass


# ----------------------------
#           position
# ----------------------------


class Castling:
    __slots__ = (
        "bKside",
        "bQside",
        "wKside",
        "wQside",
    )

    def __init__(
        self,
        wKside=True,
        wQside=True,
        bKside=True,
        bQside=True,
    ) -> None:
        self.wKside = wKside
        self.wQside = wQside
        self.bKside = bKside
        self.bQside = bQside


class Position:
    __slots__ = (
        "enpassant",
        "castling",
        "check",
        "checkmate",
        "places",
        "halfmove",
    )

    def __init__(
        self,
        enpassant=0,
        castling=Castling(),
        check=False,
        checkmate=False,
        places=[],
        halfmove=False,
    ) -> None:
        """default is empty

        params
        ------
        enpassant, enpassant targets.
        castling
        check
        checkmate
        places
        """
        self.enpassant = enpassant
        self.castling = castling
        self.check = check
        self.checkmate = checkmate
        self.places = places
        self.halfmove = halfmove


class Move:
    __slots__ = (
        "piece",
        "file",
        "rank",
        "capture",
        "disambiguation",
        "castling",
        "enpassant",
        "promotion",
        "check",
        "checkmate",
        "result",
    )

    def __init__(
        self,
        piece,
        file,
        rank,
        capture,
        disambiguation,
        castling,
        enpassant,
        promotion: str,
        check: bool,
        checkmate: bool,
        result,
    ) -> None:
        self.piece = piece
        self.file = file
        self.rank = rank
        self.capture = capture
        self.disambiguation = disambiguation
        self.castling = castling
        self.enpassant = enpassant
        self.promotion = promotion
        self.check = check
        self.checkmate = checkmate
        self.result = result


# ----------------------------
#           node
# ----------------------------

f2f = {
    "a": 1,
    "b": 2,
    "c": 3,
    "d": 4,
    "e": 5,
    "f": 6,
    "g": 7,
    "h": 8,
    1: "a",
    2: "b",
    3: "c",
    4: "d",
    5: "e",
    6: "f",
    7: "g",
    8: "h",
    "0": 0,
    0: "0",
}


r2r = {
    "1": 1,
    "2": 2,
    "3": 3,
    "4": 4,
    "5": 5,
    "6": 6,
    "7": 7,
    "8": 8,
    1: "1",
    2: "2",
    3: "3",
    4: "4",
    5: "5",
    6: "6",
    7: "7",
    8: "8",
    "0": 0,
    0: "0",
}

# f2f = {'0': 0, 'a': 1, 'b': 2, 'c': 3,
#        'd': 4, 'e': 5, 'f': 6, 'g': 7, 'h': 8}


# r2r = {'0': 0, '1': 1, '2': 2, '3': 3,
#        '4': 4, '5': 5, '6': 6, '7': 7, '8': 8}


def file(node):
    """node -> file"""
    if node < 1 or node > 64:
        return 0
    else:
        return node - (8 * floor((node - 1) / 8))


def rank(node):
    """node -> rank"""
    if node < 1 or node > 64:
        return 0
    else:
        return floor((node - 1) / 8 + 1)


def node(file, rank):
    """(file, rank) -> node"""
    if file < 1 or file > 8 or rank < 1 or rank > 8:
        return 0
    else:
        return 8 * (rank - 1) + (file - 1) + 1


w_pieces = [
    PieceType.wK,
    PieceType.wQ,
    PieceType.wR,
    PieceType.wB,
    PieceType.wN,
    PieceType.wP,
]

b_pieces = [
    PieceType.bK,
    PieceType.bQ,
    PieceType.bR,
    PieceType.bB,
    PieceType.bN,
    PieceType.bP,
]


p2wp = {
    "K": PieceType.wK,
    "Q": PieceType.wQ,
    "R": PieceType.wR,
    "B": PieceType.wB,
    "N": PieceType.wN,
    "P": PieceType.wP,
}
p2bp = {
    "K": PieceType.bK,
    "Q": PieceType.bQ,
    "R": PieceType.bR,
    "B": PieceType.bB,
    "N": PieceType.bN,
    "P": PieceType.bP,
}
p2p = {
    "wK": PieceType.wK,
    "wQ": PieceType.wQ,
    "wR": PieceType.wR,
    "wB": PieceType.wB,
    "wN": PieceType.wN,
    "wP": PieceType.wP,
    "bK": PieceType.bK,
    "bQ": PieceType.bQ,
    "bR": PieceType.bR,
    "bB": PieceType.bB,
    "bN": PieceType.bN,
    "bP": PieceType.bP,
}

p2fen = {
    PieceType.wK: "K",
    PieceType.wQ: "Q",
    PieceType.wR: "R",
    PieceType.wB: "B",
    PieceType.wN: "N",
    PieceType.wP: "P",
    PieceType.bK: "k",
    PieceType.bQ: "q",
    PieceType.bR: "r",
    PieceType.bB: "b",
    PieceType.bN: "n",
    PieceType.bP: "p",
}


enPassantXw = [
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    17,
    18,
    19,
    20,
    21,
    22,
    23,
    24,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
]

enPassantXb = [
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    41,
    42,
    43,
    44,
    45,
    46,
    47,
    48,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
]


# ----------------------------
#           positions
# ----------------------------

position_empty = Position()

position_start = Position(
    places=[
        [1, PieceType.wR],
        [2, PieceType.wN],
        [3, PieceType.wB],
        [4, PieceType.wQ],
        [5, PieceType.wK],
        [6, PieceType.wB],
        [7, PieceType.wN],
        [8, PieceType.wR],
        [9, PieceType.wP],
        [10, PieceType.wP],
        [11, PieceType.wP],
        [12, PieceType.wP],
        [13, PieceType.wP],
        [14, PieceType.wP],
        [15, PieceType.wP],
        [16, PieceType.wP],
        [49, PieceType.bP],
        [50, PieceType.bP],
        [51, PieceType.bP],
        [52, PieceType.bP],
        [53, PieceType.bP],
        [54, PieceType.bP],
        [55, PieceType.bP],
        [56, PieceType.bP],
        [57, PieceType.bR],
        [58, PieceType.bN],
        [59, PieceType.bB],
        [60, PieceType.bQ],
        [61, PieceType.bK],
        [62, PieceType.bB],
        [63, PieceType.bN],
        [64, PieceType.bR],
    ]
)

position_23_spassky_fischer_1972 = Position(
    enpassant=0,
    castling=[[False, False], [False, False]],
    check=False,
    checkmate=False,
    places=[
        [1, PieceType.wR],
        [3, PieceType.wB],
        [6, PieceType.wR],
        [7, PieceType.wK],
        [9, PieceType.wP],
        [10, PieceType.wP],
        [11, PieceType.wQ],
        [12, PieceType.wN],
        [13, PieceType.wB],
        [14, PieceType.wP],
        [15, PieceType.wP],
        [16, PieceType.wP],
        [19, PieceType.wN],
        [29, PieceType.wP],
        [35, PieceType.bP],
        [36, PieceType.wP],
        [40, PieceType.bN],
        [44, PieceType.bP],
        [47, PieceType.bP],
        [49, PieceType.bP],
        [50, PieceType.bP],
        [52, PieceType.bN],
        [54, PieceType.bP],
        [55, PieceType.bB],
        [56, PieceType.bP],
        [57, PieceType.bR],
        [59, PieceType.bB],
        [60, PieceType.bQ],
        [61, PieceType.bR],
        [63, PieceType.bK],
    ],
)
