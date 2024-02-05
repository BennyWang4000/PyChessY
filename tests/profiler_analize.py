import pandas as pd
from tqdm import tqdm
from PyChessY import ChessY
from time import time


def flatten_concatenation(matrix):
    flat_list = []
    for row in matrix:
        flat_list += row
    return flat_list


if __name__ == "__main__":
    t = time()
    pgn_path = "/home/wirl/bennywang/InterpretableChess/data/lichess_db_standard_rated_2014-06.pgn.csv"
    pgn_df = pd.read_csv(pgn_path).head(50)
    for i, row in tqdm(pgn_df.iterrows(), total=len(pgn_df.index)):
        chessy = ChessY(isDebug=False)
        moves = chessy.getMovesFromGameGPN(row["pgn"])
        for fen, move in zip(
            chessy.getFENfromPositions(chessy.getPositionsFromMoves(moves)),
            flatten_concatenation(moves),
        ):
            pass
    print("time:\t", time() - t)
