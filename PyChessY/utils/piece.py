from .structure import node2file, node2rank, filerank2node


class Piece:
    __slots__ = ("file", "rank", "piece")

    def __init__(self, file: int = 0, rank: int = 0, node: int = 0) -> None:
        assert (file and rank) or node, "assert (file and rank) or node"

        if file and rank:
            node = filerank2node(file=file, rank=rank)
        else:
            file = node2file(node)
            rank = node2rank(node)

        self.file = file
        self.rank = rank
        self.node = node


# ---------------------------------------------------------------------------- #
#                                     Piece                                    #
# ---------------------------------------------------------------------------- #


class WhitePiece(Piece):
    def __init__(self, file: int = 0, rank: int = 0, node: int = 0) -> None:
        super().__init__(file, rank, node)


class BlackPiece(Piece):
    def __init__(self, file: int = 0, rank: int = 0, node: int = 0) -> None:
        super().__init__(file, rank, node)


# ---------------------------------------------------------------------------- #
#                                     Pawn                                     #
# ---------------------------------------------------------------------------- #


class WhitePawn(WhitePiece):
    def __init__(self, file: int = 0, rank: int = 0, node: int = 0) -> None:
        super().__init__(file, rank, node)


class BlackPawn(BlackPiece):
    def __init__(self, file: int = 0, rank: int = 0, node: int = 0) -> None:
        super().__init__(file, rank, node)


# ---------------------------------------------------------------------------- #
#                                     King                                     #
# ---------------------------------------------------------------------------- #


class WhiteKing(WhitePiece):
    def __init__(self, file: int = 0, rank: int = 0, node: int = 0) -> None:
        super().__init__(file, rank, node)


class BlackKing(BlackPiece):
    def __init__(self, file: int = 0, rank: int = 0, node: int = 0) -> None:
        super().__init__(file, rank, node)


# ---------------------------------------------------------------------------- #
#                                     Queen                                    #
# ---------------------------------------------------------------------------- #


class WhiteQueen(WhitePiece):
    def __init__(self, file: int = 0, rank: int = 0, node: int = 0) -> None:
        super().__init__(file, rank, node)


class BlackQueen(BlackPiece):
    def __init__(self, file: int = 0, rank: int = 0, node: int = 0) -> None:
        super().__init__(file, rank, node)


# ---------------------------------------------------------------------------- #
#                                    Knight                                    #
# ---------------------------------------------------------------------------- #
class WhiteKnight(WhitePiece):
    def __init__(self, file: int = 0, rank: int = 0, node: int = 0) -> None:
        super().__init__(file, rank, node)


class BlackKnight(BlackPiece):
    def __init__(self, file: int = 0, rank: int = 0, node: int = 0) -> None:
        super().__init__(file, rank, node)


# ---------------------------------------------------------------------------- #
#                                    Bishop                                    #
# ---------------------------------------------------------------------------- #


class WhiteBishop(WhitePiece):
    def __init__(self, file: int = 0, rank: int = 0, node: int = 0) -> None:
        super().__init__(file, rank, node)


class BlackBishop(BlackPiece):
    def __init__(self, file: int = 0, rank: int = 0, node: int = 0) -> None:
        super().__init__(file, rank, node)


# ---------------------------------------------------------------------------- #
#                                     Root                                     #
# ---------------------------------------------------------------------------- #


class WhiteRoot(WhitePiece):
    def __init__(self, file: int = 0, rank: int = 0, node: int = 0) -> None:
        super().__init__(file, rank, node)


class BlackRoot(BlackPiece):
    def __init__(self, file: int = 0, rank: int = 0, node: int = 0) -> None:
        super().__init__(file, rank, node)
