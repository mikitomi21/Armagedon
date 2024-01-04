import chess
import time
from stockfish import Stockfish, StockfishException
import matplotlib.pyplot as plt

STOCKFISH_PATH = "C:\\Users\\kubas\\Desktop\\stockfish\\stockfish-windows-x86-64-avx2.exe"
GAME_IS_ON = "*"
COLORS = [WHITE, BLACK] = [True, False]
NUMBER_OF_GAMES = 10

parameters_white = {
            "Debug Log File": "debug_white.txt",
            "Contempt": 20,
            "Min Split Depth": 0,
            "Threads": 6,
            "Ponder": "false",
            "Hash": 2048,
            "MultiPV": 1,
            "Skill Level": 20,
            "Move Overhead": 10,
            "Minimum Thinking Time": 1,
            "Slow Mover": 100,
            "UCI_Chess960": "false",
            "UCI_LimitStrength": "false",
            "UCI_Elo": 2035
}

parameters_black = {
            "Debug Log File": "debug_black.txt",
            "Contempt": -20,
            "Min Split Depth": 0,
            "Threads": 6,
            "Ponder": "false",
            "Hash": 2048,
            "MultiPV": 1,
            "Skill Level": 20,
            "Move Overhead": 10,
            "Minimum Thinking Time": 1,
            "Slow Mover": 100,
            "UCI_Chess960": "false",
            "UCI_LimitStrength": "false",
            "UCI_Elo": 2035
}

class ResultOfGame:
    DRAW = "1/2-1/2"
    WHITE_WIN = "1-0"
    BLACK_WIN = "0-1"

def set_engine(parameters: dict) -> Stockfish:
    engine = Stockfish(path=STOCKFISH_PATH)
    engine.update_engine_parameters(parameters)
    return engine


def make_move(engine: Stockfish, board: chess.Board) -> None:
    try:
        engine.set_fen_position(board.fen())
        move = engine.get_best_move()
        # print(f"move: {move}")
        board.push_san(move)
        # print(board)
    except StockfishException as e:
        print(e)


def set_result(result_of_game: str, results: list[int, int, int]) -> None:
    if result_of_game == ResultOfGame.DRAW:
        results[0] += 1
    elif result_of_game == ResultOfGame.WHITE_WIN:
        results[1] += 1
    elif result_of_game == ResultOfGame.BLACK_WIN:
        results[2] += 1


def draw_results(results: list[int, int, int]) -> None:
    print(results)
    fig, ax = plt.subplots()
    results_of_game = [ResultOfGame.DRAW, ResultOfGame.WHITE_WIN, ResultOfGame.BLACK_WIN]
    bar_labels = ['draw', 'white win', 'black win']
    bar_colors = ['grey', 'green', 'red']

    ax.bar(results_of_game, results, label=bar_labels, color=bar_colors)

    ax.set_ylabel('Number of games')
    ax.set_xlabel('Results of games')

    ax.set_yticks(range(0, max(results) + 1))
    ax.set_xticks(results_of_game)
    ax.set_xticklabels(bar_labels)

    ax.legend(bar_labels)

    plt.show()


if __name__ == "__main__":
    stockfish_white = set_engine(parameters_white)
    stockfish_black = set_engine(parameters_black)

    version = stockfish_white.get_stockfish_major_version()
    print(f"Version of stockfish engine: {version}")

    results = [0, 0, 0]   # draw - white - black

    for i in range(NUMBER_OF_GAMES):
        board = chess.Board()

        while board.result() == GAME_IS_ON:
            if board.turn == WHITE:
                make_move(stockfish_white, board)
            elif board.turn == BLACK:
                make_move(stockfish_black, board)

        # print("Koniec gry")
        # print("Wynik:", board.result())
        set_result(board.result(), results)
        print(results)

    draw_results(results)