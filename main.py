import chess
import time
from stockfish import Stockfish

STOCKFISH_PATH = "C:\\Users\\kubas\\Desktop\\stockfish\\stockfish-windows-x86-64-avx2.exe"
stockfish = Stockfish(path=STOCKFISH_PATH)
GAME_IS_ON = "*"

parameters = {
            "Debug Log File": "debug.txt",
            "Contempt": 1,
            "Min Split Depth": 0,
            "Threads": 6,
            "Ponder": "false",
            "Hash": 2048,
            "MultiPV": 1,
            "Skill Level": 20,
            "Move Overhead": 10,
            "Minimum Thinking Time": 20,
            "Slow Mover": 100,
            "UCI_Chess960": "false",
            "UCI_LimitStrength": "false",
            "UCI_Elo": 2035
}
stockfish.update_engine_parameters(parameters)

if __name__ == "__main__":
    board = chess.Board()

    version = stockfish.get_stockfish_major_version()
    print(f"Version of stockfish engine: {version}")
    print(stockfish.get_parameters())

    print(stockfish.set_position())

    while board.result() == GAME_IS_ON:
        pass
        # stockfish.set_fen_position(board.fen())
        # move = stockfish.get_best_move()
        # print(f"move: {move}")
        # board.push_san(move)
        # print(board)

    print("Koniec gry")
    print("Wynik:", board.result())
