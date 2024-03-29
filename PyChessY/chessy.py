from .utils.structure import *
from .utils.nodes import Nodes
from typing import List
from math import ceil


class ChessY:
    def __init__(self, isDebug=False) -> None:
        self.isDebug = isDebug

    def printBoardFromNodes(self, nodes):
        return 0

    def getPositionFromPieceFileRank(
        self,
        p,
        enPassant=0,
        castling=[[True, True], [True, True]],
        check=False,
        checkmate=False,
    ) -> Position:
        pos = Position(
            enpassant=node(f2f[str(enPassant)], r2r[str(enPassant)]),
            castling=castling,
            check=check,
            checkmate=checkmate,
            places=[],
        )
        for ps in p:
            pos.places.append([node(f2f[ps[2]], r2r[ps[3]]), p2p[ps[:2]]])
        return pos

    def pgn_clean(self, pgn: str):
        """_summary_

        Args:
            pgn (str): _description_
        """

        def _rm_analyze(pgn):
            def _check(move):
                if not (
                    (move == "{")
                    or (move == "}")
                    or (move[-3:-1] == "..")
                    or (move[0] == "[")
                    or (move[-1] == "]")
                ):
                    return True
                return False

            def _rm_annotations(move):
                return move.replace("?", "").replace("!", "")

            moves = pgn.split(" ")
            moves = [_rm_annotations(move) for move in moves if move if _check(move)]
            return moves

        return " ".join(_rm_analyze(pgn.strip()))

    def parsePGNMove(self, pgn) -> Move:
        m = self.pgn_clean(pgn)
        m1, p, f, r, c, da, ca, ep, pr, ch, cm, gr = (
            "",
            "",
            "",
            "",
            False,
            "",
            "",
            False,
            "",
            False,
            False,
            "",
        )
        df, dr = "", ""

        if m == "O-O":
            ca, m = "KS", ""
        if m == "O-O+":
            ca, m, ch = "KS", "", True
        if m == "O-O++":
            ca, m, cm = "KS", "", True
        if m == "O-O-O":
            ca, m = "QS", ""
        if m == "O-O-O+":
            ca, m, ch = "QS", "", True
        if m == "O-O-O++":
            ca, m, cm = "QS", "", True
        if m in ["1-0", "0-1", "1/2-1/2"]:
            gr = m
            m = ""

        if m == "":
            return Move(
                piece=p,
                file=f,
                rank=r,
                capture=c,
                disambiguation=da,
                castling=ca,
                enpassant=ep,
                promotion=pr,
                check=ch,
                checkmate=cm,
                result=gr,
            )
        if m != "" and m[0] in ["K", "Q", "R", "B", "N"]:
            p = m[0]
            m = m[1:]
        else:
            p = "P"

        if m != "" and m[0] in ["a", "b", "c", "d", "e", "f", "g", "h"]:
            df = m[0]
            m = m[1:]
        if m != "" and m[0] in ["1", "2", "3", "4", "5", "6", "7", "8"]:
            dr = m[0]
            m = m[1:]

        if m != "" and m[0] in ["x"]:
            c = True
            m = m[1:]

        if m != "" and m[0] in ["a", "b", "c", "d", "e", "f", "g", "h"]:
            da = dr if dr != "" else df
            f = m[0]
            m = m[1:]

        if m != "" and m[0] in ["1", "2", "3", "4", "5", "6", "7", "8"]:
            r = m[0]
            m = m[1:]

        if m != "" and m[0] == "=":
            m = m[1:]

        if m != "" and m[0] in ["Q", "R", "B", "N"]:
            pr = m[0]
            m = m[1:]

        if m == "e.p.":
            ep = True
        elif m == "+":
            ch = True
        elif m == "++":
            cm = True
        elif m == "#":
            cm = True

        return Move(
            piece=p,
            file=df if f == "" else f,
            rank=dr if r == "" else r,
            capture=c,
            disambiguation=da,
            castling=ca,
            enpassant=ep,
            promotion=pr,
            check=ch,
            checkmate=cm,
            result=gr,
        )

    def getMovesFromGameGPN(self, pgn):
        moves, mwb = [], []
        for i, move in enumerate(pgn.split()[1:]):
            if i % 3 == 0:
                mwb.append(move)
            elif i % 3 == 1:
                mwb.append(move)
            elif i % 3 == 2:
                moves.append(mwb)
                mwb = []
            if i == len(pgn.split()) - 2:
                if i % 3 == 2:
                    moves.append([move, ""])
                else:
                    moves.append(mwb)
        return moves

    def getFlatMovesFromGameGPN(self, pgn):
        """get one-dimension list for stockfish further process"""
        moves, mw, mb = [], "", ""
        for i, move in enumerate(pgn.split()[1:]):
            if i % 3 == 0:
                mw = move
            elif i % 3 == 1:
                mb = move
            elif i % 3 == 2:
                moves.append("".join((mw, mb)))
                mw, mb = "", ""
            if i == len(pgn.split()) - 2:
                moves.append("".join((mw, mb)))
        return moves

    def getFENfromPosition(self, position: Position):
        pass

    def getFENfromPositions(self, positions: List[Position]):
        fen_lst = []
        halfmove = 0
        for i, position in enumerate(positions):
            places = sorted(position.places, key=lambda x: x[0])
            rank_lst = [[], [], [], [], [], [], [], []]
            for r in range(8):
                sub_fen, space = "", 0
                for p in range(1, 9):
                    if len(places) > 0:
                        if places[0][0] == r * 8 + p:
                            if space > 0:
                                sub_fen += str(space)
                            sub_fen += p2fen[places[0][1]]
                            places.pop(0)
                            space = 0
                        else:
                            space += 1
                    else:
                        space += 1
                    if p == 8 and space > 0:
                        sub_fen += str(space)
                rank_lst[r] = sub_fen
            fen = [
                "/".join(rank_lst[::-1]),
                "b" if i % 2 > 0 else "w",
            ]

            is_castling = ""
            if position.castling.wKside or position.castling.wQside:
                is_castling += "KQ"
            if position.castling.bKside or position.castling.bQside:
                is_castling += "kq"
            if len(is_castling):
                fen.append(is_castling)
            else:
                fen.append("-")

            if position.enpassant != 0:
                fen.append(
                    f2f[file(position.enpassant)] + r2r[rank(position.enpassant)]
                )
            else:
                fen.append("-")

            if position.halfmove:
                halfmove += 1
            else:
                halfmove = 0

            fen.append(str(halfmove))
            fen.append(str(ceil((i + 1) / 2)))

            fen_lst.append(" ".join(fen))
        return fen_lst

    def getPositionsFromMoves(self, moves):
        (
            positions,
            places,
            m,
            w_move,
            b_move,
            dep_node,
            arr_node,
            passant_move,
            castling_move,
            i,
        ) = ([], "", "", [], [], "", "", "", "", "")

        """
        function which returns the disambiguated node of departure, given the node
        of arrival (ana), a list of potential departure nodes (andl), the piece
        (ap), a move's PGN disambiguation (ada), whether a move is a capture/rank/
        en passant move (ac/ar/aep; only used for Pawn disambiguation) and the
        current position (apos)   '
        """

        def getDepartureNode(ana, andl, ap, ada, ac, ar, aep, apos):
            if self.isDebug:
                print(ana, ";", andl, ";", ap, ";", ada, ";", ac, ";", ar, ";", aep)
            if ap not in [PieceType.wP, PieceType.bP]:
                if len(andl) == 1:
                    return andl[0]
                if len(andl) > 1 and ada in ["a", "b", "c", "d", "e", "f", "g", "h"]:
                    for a in andl:
                        if self.isDebug:
                            print(f2f[ada], a, file(a))
                        if f2f[ada] == file(a):
                            return a
                if len(andl) > 1 and ada in ["1", "2", "3", "4", "5", "6", "7", "8"]:
                    for a in andl:
                        if self.isDebug:
                            print(r2r[ada], a, rank(a))
                        if r2r[ada] == rank(a):
                            return a
                if len(andl) > 1 and ada == "":
                    edges = self.getEdgesFromPosition(apos, sameColorTargets=False)
                    for edge in edges:
                        if edge[0] in andl and edge[1] == ana:
                            return edge[0]

            else:
                # handle pawns
                if not ac and not aep:
                    if ap == PieceType.wP:
                        return ana - 16 if ar else ana - 8
                    else:
                        return ana + 16 if ar else ana + 8
                if ac:
                    if ap == PieceType.wP:
                        return node(f2f[ada], rank(ana) - 1)
                    else:
                        return node(f2f[ada], rank(ana) + 1)
            return 0

        positions = [position_start]
        places = position_start.places

        castling_move = Castling()
        passant_move = 0

        # process moves
        for move in moves:
            if self.isDebug:
                print("-----move-----")
                print(move)
            # get details for white/black move
            w_move = self.parsePGNMove(move[0])
            if w_move.result != "":
                break
            # if (self.isDebug):
            #     print('mw', w_move.__slots__)
            #     print('mb', b_move.__slots__ if len(move) > 1 else [])

            # * process move of white piece
            arr_node, dep_node, passant_move = 0, 0, 0
            places = places.copy()
            # handle castling
            if w_move.castling == "QS":
                places.remove([5, PieceType.wK])
                places.remove([1, PieceType.wR])
                places.extend([[3, PieceType.wK], [4, PieceType.wR]])
                castling_move.wKside, castling_move.wQside = False, False

            elif w_move.castling == "KS":
                places.remove([5, PieceType.wK])
                places.remove([8, PieceType.wR])
                places.extend([[7, PieceType.wK], [6, PieceType.wR]])
                castling_move.wKside, castling_move.wQside = False, False

            if self.isDebug:
                print("---white---")

            # get node of arrival
            if w_move.file != "" and w_move.rank != "":
                arr_node = node(f2f[w_move.file], r2r[w_move.rank])
                if self.isDebug:
                    print("na", arr_node)

            # handle capture moves by removing first the captured piece;
            # NOTE: capturing by pawn needs to be handled separately, as as en
            # passant captures are not always indicated by "e.p." in PGN records
            if w_move.capture and not w_move.enpassant:
                target_piece = None
                for pos in places:
                    if pos[0] == arr_node and pos[1] != w_move.piece:
                        target_piece = pos[1]
                        break
                if target_piece is not None:
                    places = [pos for pos in places if pos != [arr_node, target_piece]]

            if (
                w_move.capture
                and w_move.piece == "P"
                and rank(arr_node) == 6
                and any(place[0] == arr_node for place in places)
            ):
                if self.isDebug:
                    print(
                        "white pawn enpassant:",
                        w_move.piece,
                        ";",
                        rank(arr_node),
                        ";",
                        any(place[0] == arr_node for place in places),
                    )
                w_move.enpassant = True
            else:
                w_move.enpassant = False

            if w_move.enpassant:
                target_piece = None
                for pos in places:
                    if pos[0] == arr_node - 8 and pos[1] != w_move.piece:
                        target_piece = pos[1]
                        break
                if target_piece is not None:
                    places = [
                        pos for pos in places if pos != [arr_node - 8, target_piece]
                    ]
            # handle moves
            if w_move.piece == "K":
                for pos in places:
                    if pos[1] == PieceType.wK:
                        dep_node = pos[0]
                        break
                places = list(filter(lambda x: x != [dep_node, PieceType.wK], places))
                places.append([arr_node, PieceType.wK])
                castling_move.wKside, castling_move.wQside = False, False

            elif w_move.piece == "Q":
                andl = [pos[0] for pos in places if pos[1] == PieceType.wQ]
                dep_node = getDepartureNode(
                    arr_node,
                    andl,
                    PieceType.wQ,
                    w_move.disambiguation,
                    w_move.capture,
                    False,
                    False,
                    positions[-1],
                )
                places = list(filter(lambda x: x != [dep_node, PieceType.wQ], places))
                places.append([arr_node, PieceType.wQ])

            elif w_move.piece == "R":
                andl = [pos[0] for pos in places if pos[1] == PieceType.wR]

                dep_node = getDepartureNode(
                    arr_node,
                    andl,
                    PieceType.wR,
                    w_move.disambiguation,
                    w_move.capture,
                    False,
                    False,
                    positions[-1],
                )

                places = list(filter(lambda x: x != [dep_node, PieceType.wR], places))

                places.append([arr_node, PieceType.wR])

                if castling_move.wKside or castling_move.wQside:
                    if dep_node == 1:
                        castling_move.wKside = False
                    if dep_node == 8:
                        castling_move.wQside = False

            elif w_move.piece == "B":
                andl = [pos[0] for pos in places if pos[1] == PieceType.wB]
                dep_node = getDepartureNode(
                    arr_node,
                    andl,
                    PieceType.wB,
                    w_move.disambiguation,
                    w_move.capture,
                    False,
                    False,
                    positions[-1],
                )
                places = list(filter(lambda x: x != [dep_node, PieceType.wB], places))
                places.append([arr_node, PieceType.wB])
            elif w_move.piece == "N":
                andl = [pos[0] for pos in places if pos[1] == PieceType.wN]
                dep_node = getDepartureNode(
                    arr_node,
                    andl,
                    PieceType.wN,
                    w_move.disambiguation,
                    w_move.capture,
                    False,
                    False,
                    positions[-1],
                )
                places = list(filter(lambda x: x != [dep_node, PieceType.wN], places))
                places.append([arr_node, PieceType.wN])

            elif w_move.piece == "P":
                andl = [pos[0] for pos in places if pos[1] == PieceType.wP]
                dep_node = getDepartureNode(
                    arr_node,
                    andl,
                    PieceType.wP,
                    w_move.disambiguation,
                    w_move.capture,
                    True
                    if (
                        (rank(arr_node) == 4)
                        and (
                            not any(
                                piece[0] == arr_node - 8
                                for piece in positions[-1].places
                            )
                        )
                    )
                    else False,
                    w_move.enpassant,
                    positions[-1],
                )
                # len([True for an in andl if rank(na) == 4 and an == (na - 8)]) == 0
                if self.isDebug:
                    print(
                        "ar:\t",
                        True
                        if (
                            (rank(arr_node) == 4)
                            and (
                                not any(
                                    piece[0] == arr_node - 8
                                    for piece in positions[-1].places
                                )
                            )
                        )
                        else False,
                    )
                places = list(filter(lambda x: x != [dep_node, PieceType.wP], places))
                places.append([arr_node, PieceType.wP])
                if rank(dep_node) == 2 and rank(arr_node) == 4:
                    # TODO minus one or not
                    passant_move = enPassantXw[arr_node - 1]

            if self.isDebug:
                print("dis:\t", w_move.disambiguation)
                print("nd:\t", dep_node)

            # handle promotion
            if w_move.promotion != "":
                places.remove([arr_node, PieceType.wP])
                places.append([arr_node, p2wp[w_move.promotion]])

            # append position to positions list
            positions.append(
                Position(
                    enpassant=passant_move,
                    castling=Castling(
                        castling_move.wKside,
                        castling_move.wQside,
                        castling_move.bKside,
                        castling_move.bQside,
                    ),
                    check=w_move.check,
                    checkmate=w_move.checkmate,
                    places=places,
                    halfmove=False if w_move.capture or w_move.piece == "P" else True,
                )
            )

            # * process move of black piece
            if len(move) <= 1:
                break

            b_move = self.parsePGNMove(move[1])
            if w_move.result != "":
                break

            if self.isDebug:
                print("---black---")

            arr_node, dep_node, passant_move = 0, 0, 0

            # handle castling
            if b_move.castling == "QS":
                places.remove([61, PieceType.bK])
                places.remove([57, PieceType.bR])
                places.extend([[59, PieceType.bK], [60, PieceType.bR]])
                castling_move.bKside, castling_move.bQside = False, False
            elif b_move.castling == "KS":
                places.remove([61, PieceType.bK])
                places.remove([64, PieceType.bR])
                places.extend([[63, PieceType.bK], [62, PieceType.bR]])
                castling_move.bKside, castling_move.bQside = False, False

            # get node of arrival
            if b_move.file != "" and b_move.rank != "":
                arr_node = node(f2f[b_move.file], r2r[b_move.rank])
                if self.isDebug:
                    print("na", arr_node)

            # handle capture moves by removing first the captured piece;
            # NOTE: capturing by pawn needs to be handled separately, as as en
            # passant captures are not always indicated by "e.p." in PGN records
            if b_move.capture and not b_move.enpassant:
                target_piece = None
                for pos in places:
                    if pos[0] == arr_node and pos[1] != b_move.piece:
                        target_piece = pos[1]
                        break
                if target_piece is not None:
                    places = [pos for pos in places if pos != [arr_node, target_piece]]

            if (
                b_move.capture
                and b_move.piece == "P"
                and rank(arr_node) == 3
                and any(place[0] == arr_node for place in places)
            ):
                if self.isDebug:
                    print(
                        "black pawn enpassant:",
                        b_move.piece,
                        ";",
                        rank(arr_node),
                        ";",
                        any(place[0] == arr_node for place in places),
                    )
                b_move.enpassant = True
            else:
                b_move.enpassant = False

            if b_move.enpassant:
                target_piece = None
                for pos in places:
                    if pos[0] == arr_node + 8 and pos[1] != b_move.piece:
                        target_piece = pos[1]
                        break
                if target_piece is not None:
                    places = [
                        pos for pos in places if pos != [arr_node + 8, target_piece]
                    ]

            # handle moves
            if b_move.piece == "K":
                for pos in places:
                    if pos[1] == PieceType.bK:
                        dep_node = pos[0]
                        break
                places = list(filter(lambda x: x != [dep_node, PieceType.bK], places))
                places.append([arr_node, PieceType.bK])
                castling_move.bKside, castling_move.bQside = False, False
            elif b_move.piece == "Q":
                andl = [pos[0] for pos in places if pos[1] == PieceType.bQ]
                dep_node = getDepartureNode(
                    arr_node,
                    andl,
                    PieceType.bQ,
                    b_move.disambiguation,
                    b_move.capture,
                    False,
                    False,
                    positions[-1],
                )

                places = list(filter(lambda x: x != [dep_node, PieceType.bQ], places))
                places.append([arr_node, PieceType.bQ])
            elif b_move.piece == "R":
                andl = [pos[0] for pos in places if pos[1] == PieceType.bR]
                dep_node = getDepartureNode(
                    arr_node,
                    andl,
                    PieceType.bR,
                    b_move.disambiguation,
                    b_move.capture,
                    False,
                    False,
                    positions[-1],
                )

                places = list(filter(lambda x: x != [dep_node, PieceType.bR], places))
                places.append([arr_node, PieceType.bR])
                if castling_move.bKside or castling_move.bQside:
                    if dep_node == 57:
                        castling_move.bKside = False
                    if dep_node == 64:
                        castling_move.bQside = False
            elif b_move.piece == "B":
                andl = [pos[0] for pos in places if pos[1] == PieceType.bB]
                dep_node = getDepartureNode(
                    arr_node,
                    andl,
                    PieceType.bB,
                    b_move.disambiguation,
                    b_move.capture,
                    False,
                    False,
                    positions[-1],
                )

                places = list(filter(lambda x: x != [dep_node, PieceType.bB], places))
                places.append([arr_node, PieceType.bB])
            elif b_move.piece == "N":
                andl = [pos[0] for pos in places if pos[1] == PieceType.bN]
                dep_node = getDepartureNode(
                    arr_node,
                    andl,
                    PieceType.bN,
                    b_move.disambiguation,
                    b_move.capture,
                    False,
                    False,
                    positions[-1],
                )
                places = list(filter(lambda x: x != [dep_node, PieceType.bN], places))
                places.append([arr_node, PieceType.bN])

            elif b_move.piece == "P":
                andl = [pos[0] for pos in places if pos[1] == PieceType.bP]
                dep_node = getDepartureNode(
                    arr_node,
                    andl,
                    PieceType.bP,
                    b_move.disambiguation,
                    b_move.capture,
                    True
                    if (
                        (rank(arr_node) == 5)
                        and (
                            not any(
                                piece[0] == arr_node + 8
                                for piece in positions[-1].places
                            )
                        )
                    )
                    else False,
                    b_move.enpassant,
                    positions[-1],
                )
                places = list(filter(lambda x: x != [dep_node, PieceType.bP], places))
                places.append([arr_node, PieceType.bP])
                if rank(dep_node) == 7 and rank(arr_node) == 5:
                    # TODO minus one or not
                    passant_move = enPassantXw[arr_node - 1]

            if self.isDebug:
                print("dis:\t", b_move.disambiguation)
                print("nd:\t", dep_node)

            # handle promotion
            if b_move.promotion != "":
                places.remove([arr_node, PieceType.bP])
                places.append([arr_node, p2bp[b_move.promotion]])

            # append position to positions list
            positions.append(
                Position(
                    enpassant=passant_move,
                    castling=Castling(
                        castling_move.wKside,
                        castling_move.wQside,
                        castling_move.bKside,
                        castling_move.bQside,
                    ),
                    check=b_move.check,
                    checkmate=b_move.checkmate,
                    places=places,
                    halfmove=False if b_move.capture or b_move.piece == "P" else True,
                )
            )

        return positions

    def getEdgesFromPosition(self, position, state="Color", sameColorTargets=False):
        """Function returning a 2d list of all weighted edges in a given chess position.

        ARGUMENTS:
        ------
        pos - chess position

        OPTIONS:
        ------
        State            - edge state/weight:
                        (D) State->"Color" : state indicating color of chess pieces
                            State->"Simple" : state indicating whether node is
                                            occupied or not
                            State->"Piece":
        SameColorTargets - True/False indicating whether edges are included for
                            which both source and target nodes have same color;
                        (D) sameColorTargets->False
                            NOTE: this argument must be set to False (default) for
                                generating valid chess graphs

        RETURN:
        ------
        list {{<SOURCE>,<TARGET>,<WEIGHT>},{<SOURCE>,<TARGET>,<WEIGHT>},...}
        holding the set of all edges indicated by source node, target node and edge
        weight (state) information
        """
        edges = []  # master list of edges to be returned
        w_edges = []  # list of all edges originating from white pieces
        b_edges = []  # list of all edges originating from black pieces
        w_nodes = []  # list of white-occupied nodes
        b_nodes = []  # list of black-occupied nodes
        a_nodes = []  # list of all occupied nodes
        w_Knode, b_Knode = "", ""  # node of white/black King
        wt_nodes = []  # list of all nodes targeted by white pieces
        bt_nodes = []  # list of all nodes targeted by black pieces
        t_pos = ""  # temporary position being evaluated
        t_Knode = ""  # node for King in temporary position being evaluated

        i, te = "", ""
        atni = sameColorTargets

        if self.isDebug:
            print("-----edges-running-----")

        # get white/black/all occupied nodes
        # get node with white/black King
        for p in position.places:
            if p[1] in w_pieces:
                w_nodes.append(p[0])
                if p[1] == PieceType.wK:
                    w_Knode = p[0]
            else:
                b_nodes.append(p[0])
                if p[1] == PieceType.bK:
                    b_Knode = p[0]
        a_nodes.extend(w_nodes)
        a_nodes.extend(b_nodes)

        # get all potential edges for white/black pieces

        if state == "Color" or state == "Simple":
            w_edges = self.getTargetEdgesFromPosition(
                position, p2p=p2wp, side="w", sameColorTargets=atni
            )
            b_edges = self.getTargetEdgesFromPosition(
                position, p2p=p2bp, side="b", sameColorTargets=atni
            )
        elif state == "Piece":
            w_edges = self.getTargetEdgesFromPosition(
                position, p2p=p2wp, side="w", sameColorTargets=atni, state="Piece"
            )
            b_edges = self.getTargetEdgesFromPosition(
                position, p2p=p2bp, side="b", sameColorTargets=atni, state="Piece"
            )

        if self.isDebug:
            print("wedges:\t", w_edges)
            print("bedges:\t", b_edges)

        # get all nodes targeted by white/black pieces
        wt_nodes = [edge[1] for edge in w_edges] if w_edges else []
        bt_nodes = [edge[1] for edge in b_edges] if b_edges else []

        # assess if white/black King is in check
        w_check = True if w_Knode in bt_nodes else False
        b_check = True if b_Knode in wt_nodes else False

        # perform each possible move of white pieces and remove those which yield check for the white King
        for i in range(len(w_edges)):
            # generate new temporary position from move
            t_pos = [
                piece
                for piece in position.places
                if (piece[0] == w_edges[i][1] and piece[1] != PieceType.bK)
                or piece != [0, 0]
            ]

            t_pos = [
                [w_edges[i][1] if item[0] == w_edges[i][0] else item[0], item[1]]
                for item in t_pos
            ]

            t_Knode = None
            for piece in t_pos:
                if piece[1] == PieceType.wK:
                    t_Knode = piece[0]
                    break
            # test/discard edge if white King is in check
            te = self.getTargetEdgesFromPosition(
                position=Position(
                    enpassant=position.enpassant,
                    castling=position.castling,
                    check=position.check,
                    checkmate=position.checkmate,
                    places=t_pos,
                ),
                p2p=p2bp,
                side="b",
                sameColorTargets=atni,
            )

            if te != []:
                if t_Knode in [edge[1] for edge in zip(*te)]:
                    w_edges[i] = []
            # if tKn in [x[1] for x in self.getTargetEdgesFromPosition(t_pos=Position(enpassant=supp.enpassant, castling=supp.castling, check=supp.check, checkmate=supp.checkmate, position=tpos), p2p=p2bp, side='b', sameColorTargets=atni)]:
            #     wedges[i] = []
        # remove empty elements from wedges
        w_edges = [edge for edge in w_edges if edge != []]

        # perform each possible move of black pieces and remove those which yield check for the black King
        for i in range(len(b_edges)):
            # generate new temporary position from move
            t_pos = [
                piece
                for piece in position.places
                if (piece[0] == b_edges[i][1] and piece[1] != PieceType.wK)
                or piece != [0, 0]
            ]

            t_pos = [
                [b_edges[i][1] if item[0] == b_edges[i][0] else item[0], item[1]]
                for item in t_pos
            ]

            t_Knode = None
            for piece in t_pos:
                if piece[1] == PieceType.wK:
                    t_Knode = piece[0]
                    break

            te = self.getTargetEdgesFromPosition(
                position=Position(
                    enpassant=position.enpassant,
                    castling=position.castling,
                    check=position.check,
                    checkmate=position.checkmate,
                    places=t_pos,
                ),
                p2p=p2bp,
                side="w",
                sameColorTargets=atni,
                state="Piece",
            )

            if te != []:
                if t_Knode in [edge[1] for edge in zip(*te)]:
                    b_edges[i] = []
        # remove empty elements from wedges
        b_edges = [edge for edge in b_edges if edge != []]

        # add edges for queen/kingside castling moves of white King/Rook
        if (
            (not w_check)
            and ([5, PieceType.wK] in position.places)
            and ([1, PieceType.wR] in position.places)
            and (position.castling.wKside)
            and (len(set([2, 3, 4]).intersection(a_nodes)) == 0)
            and (len(set([3, 4]).intersection(bt_nodes)) == 0)
        ):
            if state == "Color" or state == "Simple":
                w_edges += [[5, 3], [1, 4]]
            elif state == "Piece":
                w_edges += [[5, 3, PieceType.wK], [1, 4, PieceType.wR]]
        if (
            (not w_check)
            and ([5, PieceType.wK] in position.places)
            and ([8, PieceType.wR] in position.places)
            and (position.castling.wQside)
            and (len(set([6, 7]).intersection(a_nodes)) == 0)
            and (len(set([6, 7]).intersection(bt_nodes)) == 0)
        ):
            if state == "Color" or state == "Simple":
                w_edges += [[5, 7], [8, 6]]
            elif state == "Piece":
                w_edges += [[5, 7, PieceType.wK], [8, 6, PieceType.wR]]

        # add edges for queen/kingside castling moves of black King/Rook
        if (
            (not b_check)
            and ([61, PieceType.bK] in position.places)
            and ([57, PieceType.bR] in position.places)
            and (position.castling.bKside)
            and (len(set([58, 59, 60]).intersection(a_nodes)) == 0)
            and (len(set([59, 60]).intersection(wt_nodes)) == 0)
        ):
            if state == "Color" or state == "Simple":
                b_edges += [[61, 59], [57, 60]]
            elif state == "Piece":
                b_edges += [[61, 59, PieceType.bK], [57, 60, PieceType.bR]]
        if (
            (not b_check)
            and ([61, PieceType.bK] in position.places)
            and ([64, PieceType.bR] in position.places)
            and (position.castling.bQside)
            and (len(set([62, 63]).intersection(a_nodes)) == 0)
            and (len(set([62, 63]).intersection(wt_nodes)) == 0)
        ):
            if state == "Color" or state == "Simple":
                b_edges += [[61, 63], [64, 62]]
            elif state == "Piece":
                b_edges += [[61, 63, PieceType.bK], [64, 62, PieceType.bR]]

        # set global checkmate variable
        if len(w_edges) == 0:
            wCheckmate = True
        if len(b_edges) == 0:
            bCheckmate = True

        # format and return master list of weighted edges

        if state == "Color" or state == "Simple":
            lst = [[edge[0], edge[1], PieceType._pw] for edge in w_edges] + [
                [edge[0], edge[1], PieceType._pb] for edge in b_edges
            ]

        elif state == "Piece":
            lst = w_edges + b_edges

        edges = []
        for e in lst:
            if e not in edges:
                edges.append(e)
            # print(edges)

        if state == "Simple":
            return [[abs(edge[1]) for edge in edges]]
        else:
            return edges

    def getTargetEdgesFromPosition(
        self, position: Position, p2p, side="w", sameColorTargets=False, state="Color"
    ):
        """
        parameters
            position: Position,
            p2p: dict,
            side: string,
            sameColorTaragets: bool
            state: string, in Color or Piece
        """

        assert state in ["Color", "Piece"]

        assert side in ["w", "b"]
        edges = []  # master list of edges to be returned
        main_nodes = []  # list of white-occupied nodes
        oppo_nodes = []  # list of black-occupied nodes
        a_nodes = []  # list of all occupied nodes
        n = ""  # node being processed
        p = ""  # piece on node being processed
        f, r = "", ""  # file/rank of node being processed
        tn = ""  # temporary list of target nodes of white/black pieces
        tni = ""  # target node included? (True/False)
        tnt = ""  # target node
        ep = ""  # target node of possible en passant move
        pos, i = "", ""
        atni = sameColorTargets
        nodes = Nodes(side)

        # NOTE
        # wn -> ma_n, main nodes
        # bn -> op_n, opposite nodes

        if len(position.places) <= 0:
            return Position

        # get white/black/all occupied nodes
        for pos in position.places:
            if pos[1] in w_pieces:
                if side == "w":
                    main_nodes.append(pos[0])
                elif side == "b":
                    oppo_nodes.append(pos[0])
            elif pos[1] in b_pieces:
                if side == "b":
                    main_nodes.append(pos[0])
                elif side == "w":
                    oppo_nodes.append(pos[0])

        a_nodes.extend(main_nodes)
        a_nodes.extend(oppo_nodes)

        for pos in position.places:
            n = pos[0]
            p = pos[1]
            f = file(n)
            r = rank(n)
            tn = []

            if p == p2p["K"]:
                # add target nodes for standard moves of the black King, modulo target nodes occupied with black pieces
                tn.extend(
                    [node for node in nodes.mKing[n] if node not in main_nodes]
                    if not atni
                    else nodes.mKing[n]
                )
            elif p in [p2p["Q"], p2p["R"], p2p["B"]]:
                for direction in (
                    nodes.mQueen
                    if p == p2p["Q"]
                    else (nodes.mRook if p == p2p["R"] else nodes.mBishop)
                ):
                    tnt, tni = 0, True
                    for tnt in direction[n]:
                        if tnt in main_nodes:
                            tni = False
                            break
                        elif tnt in oppo_nodes:
                            tni = True
                            break

                    if tni or atni:
                        tn.extend(
                            [
                                node
                                for node in direction[n]
                                if node not in direction[tnt]
                            ]
                        )
                    else:
                        tn.extend(
                            [
                                node
                                for node in direction[n]
                                if node not in direction[tnt] + [tnt]
                            ]
                        )
                    tn
                    # tn.extend([node for node in direction[n] if node not in (
                    #     direction[tnt] if (tni or atni) else direction[tnt] + tnt)])

            elif p == p2p["N"]:
                tn.extend(
                    [node for node in nodes.mKnight[n] if node not in main_nodes]
                    if not atni
                    else nodes.mKnight[n]
                )
            elif p == p2p["P"]:
                tn.extend([node for node in nodes.mPawn_main[n] if node not in a_nodes])
                if r == 2 and len(tn) != 0:
                    tn.extend(
                        [node for node in nodes.mPawnR_main[n] if node not in a_nodes]
                    )
                if not atni:
                    tn.extend(
                        [value for value in nodes.mPawnX_main[n] if value in oppo_nodes]
                    )
                else:
                    tn.extend(
                        [value for value in nodes.mPawnX_main[n] if value in a_nodes]
                    )
                if r == 5 and ep != 0:
                    tn.extend(
                        [value for value in nodes.mPawnEP_main[n] if value in [ep]]
                    )

            # generate edges and add to master list

            if state == "Color":
                for e in tn:
                    edges.append([n, e])
            elif state == "Piece":
                for e in tn:
                    edges.append([n, e, p])

        return edges

    def getNodesFromPosition(self, position: Position, state="Color"):
        assert state in ["Color", "Piece", "Simple"]
        nodes = [0] * 64
        for p in position.places:
            if state == "Color":
                nodes[p[0] - 1] = PieceType._pw if p[1] in w_pieces else PieceType._pb

            elif state == "Piece":
                nodes[p[0] - 1] = p[1]

            elif state == "Simple":
                nodes[p[0] - 1] = abs(p[1])

        return nodes

    def getDomainance(self, nodes, edges, state="Color"):
        if state == "Color":
            wn = [idx + 1 for idx, node in enumerate(nodes) if node == PieceType._pw]
            bn = [idx + 1 for idx, node in enumerate(nodes) if node == PieceType._pb]
            d = [
                len(set(wn + [edge[1] for edge in edges if edge[0] in wn])) / 64.0,
                len(set(bn + [edge[1] for edge in edges if edge[0] in bn])) / 64.0,
            ]
        elif state == "Simple":
            an = [idx for idx, node in enumerate(nodes) if node != 0 and idx in edges]
            d = [len(set(an + [edge[1] for edge in edges if edge[0] in an])) / 64.0]

        return d

    def getOffensiveness(self, nodes, edges, state="Color"):
        if state == "Color":
            wn = [idx + 1 for idx, node in enumerate(nodes) if node == PieceType._pw]
            bn = [idx + 1 for idx, node in enumerate(nodes) if node == PieceType._pb]
            o = [
                len(set(edge[1] for edge in edges if edge[1] in wn and edge[2] in bn)),
                len(set(edge[1] for edge in edges if edge[1] in bn and edge[2] in wn)),
            ]
        elif state == "Simple":
            an = [idx for idx, node in enumerate(nodes) if node != 0]
            o = [len(set(edge[1] for edge in edges if edge[1] in an and edge[2] in an))]

        return o

    def getDefensiveness(self, nodes, pos, state="Color"):
        edges = self.getEdgesFromPosition(pos, sameColorTargets=True)
        wn = [idx for idx, node in enumerate(nodes) if node in w_pieces]
        bn = [idx for idx, node in enumerate(nodes) if node in b_pieces]
        d = 0

        if state == "Color":
            wn = [idx for idx in wn if idx in edges]
            bn = [idx for idx in bn if idx in edges]
            d = len(
                set([edge[1] for edge in edges if (edge[0] in wn) and (edge[1] in wn)])
            ) + len(
                set([edge[1] for edge in edges if (edge[0] in bn) and (edge[1] in bn)])
            )
        elif state == "Simple":
            d = len(
                set([edge[1] for edge in edges if (edge[0] in wn) and (edge[1] in wn)])
            ) + len(
                set([edge[1] for edge in edges if (edge[0] in bn) and (edge[1] in bn)])
            )

        return d


# %%
