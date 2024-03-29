import unittest
import sys

sys.path.append("/home/wirl/bennywang/PyChessY/PyChessY")
from PyChessY import ChessY
from PyChessY.utils.structure import PieceType

"""


"""


class TestBoard(unittest.TestCase):
    def __init__(self, methodName: str = "runTest") -> None:
        super().__init__(methodName)
        self.pgn1 = "1. d4 Nf6 2. c4 e6 3. Nf3 d5 4. Nc3"
        self.pgn2 = "1. d4 Nf6 2. c4 e6 3. Nf3 d5 4. Nc3 e5 5. Be3 exd4 6. Qxd4 Nc6 7. O-O-O Nb4 8. cxd5"
        self.pgn3 = "1. d4 Nf6 2. c4 e6 3. Nf3 b6 4. g3 Ba6 5. Qc2 Bb7 6. Bg2 c5 7. d5 exd5 8. cxd5 Nxd5 9. O-O Be7 10. Rd1 Nc6 11. Qf5 Nf6 12. e4 d6 13. e5 Qd7 14. Qxd7+ Nxd7 15. exd6 Bf6 16. Re1+ Kf8 17. Nc3 Nb4 18. Ne5 Nxe5 19. Bxb7 Rd8 20. Rd1 Nc4 21. d7 Nc2 22. Rb1 Nd4 23. b4 Rxd7 24. Bd5 Nd6 25. bxc5 bxc5 26. Ba3 Ke7 27. Bxc5 Ne6 28. Bb4 a5 29. Bxa5 Rc8 30. Na4 Nc4 31. Rbc1 Be5 32. Bb4+ Kf6 33. Nc5 Nxc5 34. Rxc4 Rdc7 35. Ba5 1-0"
        self.pgn4 = "1. e4 e5 2. Nf3 Nc6 3. Bc4 Bc5 4. O-O Nf6 5. d3 d6 6. c3 a6 7. Re1 Ba7 8. a4 O-O 9. h3 Be6 10. Bxe6 fxe6 11. Be3 Bxe3 12. fxe3 a5 13. Nbd2 Qd7 14. Qb3 b6 15. Rad1 Kh8 16. Qb5 Nd8 17. Qxd7 Nxd7 18. d4 Nf7 19. Kf2 Ng5 20. Ke2 Nxf3 21. Nxf3 Nf6 22. Nd2 Kg8 23. Rf1 Rfe8 24. Rf3 Rad8 25. g4 d5 26. Rff1 exd4 27. cxd4 dxe4 28. g5 Nd5 29. Nxe4 e5 30. Rf5 Nb4 31. dxe5 Rxd1 32. Kxd1 Nd3 33. Kc2 Nxe5 34. Nd2 Re6 35. Rf4 Rc6+ 36. Kb1 Nd3 37. Rd4 Rc1+ 38. Ka2 Nb4+ 39. Kb3 Kf7 40. Nc4 Kg6 41. h4 Kh5 42. Ne5 Re1 43. Re4 Rh1 44. Nd7 Rxh4 45. Re7 Kxg5 46. Rxg7+ Kh6 47. Re7 Kg5 48. Nf8 h5 49. Rg7+ Kf5 50. Rf7+ Ke4 51. Rxc7 Kxe3 52. Ng6 Rd4 53. Rh7 Rd3+ 54. Kc4 Rd5 55. Re7+ Kf2 56. Rb7 Rd6 57. Nf4 h4 58. Rg7 Kf3 59. Nh3 Nc6 60. Ng5+ Kf4 61. Nh3+ Kf3 62. Ng5+ Ke3 63. Nh3 Nd4 64. Rg4 Rc6+ 65. Kd5 Rc5+ 66. Kd6 Nf5+ 67. Kd7 Kf3 68. Rg6 Rd5+ 69. Ke6 Ne3 70. Ng1+ Ke4 71. Nh3 Rd4 72. b3 Rb4 73. Rf6 Kd3 0-1"
        self.pgn5 = "1. g3 b6 2. f3 c6 3. e3 d6 4. f4 d5 5. d4 e5 6. dxe5"
        self.pgn6 = "1. e4 { [%eval 0.25] } 1... c5 { [%eval 0.31] } 2. Nf3 { [%eval 0.23] } 2... d6 { [%eval 0.34] } 3. d4 { [%eval 0.26] } 3... Nf6 { [%eval 0.23] } 4. dxc5 { [%eval 0.13] } 4... Nxe4 { [%eval 0.17] } 5. cxd6 { [%eval 0.19] } 5... Nxd6 { [%eval 0.34] } 6. Bf4 { [%eval 0.37] } 6... Bg4 { [%eval 0.68] } 7. Bxd6 { [%eval 0.29] } 7... exd6 { [%eval 0.16] } 8. Qe2+ { [%eval 0.01] } 8... Be7 { [%eval -0.1] } 9. Nc3 { [%eval -0.14] } 9... O-O { [%eval -0.2] } 10. Nd5?! { [%eval -0.83] } 10... Re8 { [%eval -0.66] } 11. O-O-O { [%eval -0.61] } 11... Bg5+ { [%eval -0.68] } 12. Ne3 { [%eval -0.68] } 12... Nc6 { [%eval -0.64] } 13. h3 { [%eval -0.7] } 13... Bh5 { [%eval -0.47] } 14. g4 { [%eval -0.8] } 14... Bg6?! { [%eval 0.0] } 15. Nxg5 { [%eval 0.06] } 15... h6? { [%eval 2.75] } 16. Nf3 { [%eval 3.0] } 16... Be4 { [%eval 2.32] } 17. Bg2 { [%eval 2.51] } 17... Qa5 { [%eval 2.75] } 18. a3 { [%eval 2.71] } 18... Ne5? { [%eval 4.49] } 19. Rxd6 { [%eval 4.04] } 19... Qc5 { [%eval 4.05] } 20. Rd2?! { [%eval 3.54] } 20... Nxf3? { [%eval 5.12] } 21. Bxf3 { [%eval 5.17] } 21... Bg6 { [%eval 5.43] } 22. Qc4 { [%eval 5.09] } 22... Qxc4 { [%eval 5.29] } 23. Nxc4 { [%eval 5.34] } 23... Rac8? { [%eval 7.79] } 24. Nd6 { [%eval 7.93] } 1-0"
        self.pgn7 = "1. d4 d5 2. Nc3 e6 3. f3 Nf6 4. e4 Bb4 5. e5 Bxc3+ 6. bxc3 Nfd7 7. Bd3 f5 8. Ne2 O-O 9. Bf4 c5 10. Qd2 c4 11. O-O cxd3 12. cxd3 Nc6 13. h3 Nb6 14. Rab1 Bd7 15. Rb2 Rab8 16. Rfb1 Qc7 17. Nc1 Nc8 18. Nb3 b6 19. a4 Nc8e7 20. Ra2 Na5 21. Nxa5 bxa5 22. Rab2 Rxb2 23. Qxb2 h6 24. Qb7 Qxb7 25. Rxb7 Rd8 26. Rxa7 Kf7 27. Rxa5 Nc6 28. Rc5 Ra8 29. a5 Rxa5 30. Rxa5 Nxa5 31. Kf2 Bb5 32. Ke3 g5 33. Bh2 f4+ 34. Kd2 1-0"

        self.fen1 = "rnbqkb1r/ppp2ppp/4pn2/3p4/2PP4/2N2N2/PP2PPPP/R1BQKB1R b KQkq - 1 4"
        self.fen2 = "r1bqkb1r/ppp2ppp/5n2/3P4/1n1Q4/2N1BN2/PP2PPPP/2KR1B1R b kq - 0 8"
        self.fen3 = "2r5/2r2ppp/5k2/B1nBb3/2R5/6P1/P4P1P/3R2K1 b - - 2 35"
        self.fen4 = "8/8/1p2KR2/p7/Pr5p/1P1kn2N/8/8 w - - 3 74"
        self.fen5 = "rnbqkbnr/p4ppp/1pp5/3pP3/5P2/4P1P1/PPP4P/RNBQKBNR b KQkq - 0 6"
        self.fen6 = "2r1r1k1/pp3pp1/3N2bp/8/6P1/P4B1P/1PPR1P2/2K4R b - - 2 24"

    def test_parse_moves(self):
        chessy = ChessY()
        moves = chessy.getMovesFromGameGPN(self.pgn1)
        ans = [["d4", "Nf6"], ["c4", "e6"], ["Nf3", "d5"], ["Nc3"]]
        self.assertEquals(ans, moves)

    def test_parse_positions2(self):
        chessy = ChessY(isDebug=False)
        moves = chessy.getMovesFromGameGPN(self.pgn7)
        positions = chessy.getPositionsFromMoves(moves)
        self.assertEqual(
            "rnbq1rk1/pp1n2pp/4p3/3pPp2/2pP1B2/2PB1P2/P1PQN1PP/R4RK1 b - - 1 11",
            chessy.getFENfromPositions(positions)[21],
        )
        self.assertEqual(
            "1r3rk1/ppqb2pp/1nn1p3/3pPp2/3P1B2/2PP1P1P/PR1QN1P1/1R4K1 w - - 7 17",
            chessy.getFENfromPositions(positions)[32],
        )
        self.assertEqual(
            "1rn2rk1/p1qb2pp/1pn1p3/3pPp2/3P1B2/1NPP1P1P/PR1Q2P1/1R4K1 w - - 0 19",
            chessy.getFENfromPositions(positions)[36],
        )
        self.assertEqual(
            "1r3rk1/p1qbn1pp/1pn1p3/3pPp2/P2P1B2/1NPP1P1P/1R1Q2P1/1R4K1 w - - 1 20",
            chessy.getFENfromPositions(positions)[38],
        )
        self.assertEqual(
            "1r3rk1/p1qbn1pp/4p3/p2pPp2/P2P1B2/2PP1P1P/R2Q2P1/1R4K1 w - - 0 22",
            chessy.getFENfromPositions(positions)[42],
        )
        self.assertEqual(
            "8/5k2/4p2p/nb1pP1p1/3P1p2/2PP1P1P/3K2PB/8 b - - 1 34",
            chessy.getFENfromPositions(positions)[-2],
        )

    def test_parse_positions(self):
        chessy = ChessY()
        moves = chessy.getMovesFromGameGPN(self.pgn4)
        positions = chessy.getPositionsFromMoves(moves)
        self.assertEqual(
            "8/8/1p2KR2/p7/Pr5p/1P1kn2N/8/8 w - - 3 74",
            chessy.getFENfromPositions(positions)[-1],
        )


if __name__ == "__main__":
    unittest.main()
