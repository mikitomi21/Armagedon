import sys
import chess
import chess.polyglot
import time
from stockfish import Stockfish, StockfishException
import matplotlib.pyplot as plt

STOCKFISH_PATH = str(sys.argv[1]) if len(sys.argv) > 1 else None
GAME_IS_ON = "*"
COLORS = [WHITE, BLACK] = [True, False]
NUMBER_OF_GAMES = 1
BLACK_TIME_LIMIT = 10
WHITE_TIME_LIMIT = 20
INCREMENT = 1

parameters_white = {
    "Debug Log File": "debug_white.txt",
    "Contempt": +20,
    "Min Split Depth": 0,
    "Threads": 6,
    "Ponder": "false",
    "Hash": 8192,
    "MultiPV": 1,
    "Skill Level": 20,
    "Move Overhead": 10,
    "Minimum Thinking Time": 0,
    "Slow Mover": 100,
    "UCI_Chess960": "false",
    "UCI_LimitStrength": "false",
    "UCI_Elo": 3190
}

parameters_black = {
    "Debug Log File": "debug_black.txt",
    "Contempt": -20,
    "Min Split Depth": 0,
    "Threads": 6,
    "Ponder": "false",
    "Hash": 8192,
    "MultiPV": 1,
    "Skill Level": 20,
    "Move Overhead": 10,
    "Minimum Thinking Time": 0,
    "Slow Mover": 100,
    "UCI_Chess960": "false",
    "UCI_LimitStrength": "false",
    "UCI_Elo": 3190
}


class ResultOfGame:
    DRAW = "1/2-1/2"
    WHITE_WIN = "1-0"
    BLACK_WIN = "0-1"


def set_engine(parameters: dict) -> Stockfish:
    engine = Stockfish(path=STOCKFISH_PATH)
    engine.update_engine_parameters(parameters)
    return engine


def make_move(engine: Stockfish, board: chess.Board) -> float:
    try:
        move_time = time.time()
        move = engine.get_best_move()
        print(f"move: {move}")
        board.push_san(move)

        return time.time() - move_time
    except StockfishException as e:
        print(e)


def time_is_over(player_time: float, player: COLORS) -> bool:
    if player == WHITE and player_time >= WHITE_TIME_LIMIT:
        print("White lost on time")
        print(player_time)
        return True
    elif player == BLACK and player_time >= BLACK_TIME_LIMIT:
        print("Black lost on time")
        print(player_time)
        return True

    return False


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


def set_random_opening(chess_board: chess.Board) -> chess.Board:
    with chess.polyglot.open_reader("static/opening_book/Perfect2023.bin") as reader:
        while True:
            try:
                entry = reader.weighted_choice(chess_board)
                print(entry)
                chess_board.push(entry.move)
            except IndexError:
                # No more moves in opening book
                break

    return chess_board


if __name__ == "__main__":
    stockfish_white = set_engine(parameters_white)
    stockfish_black = set_engine(parameters_black)

    version = stockfish_white.get_stockfish_major_version()
    print(f"Version of stockfish engine: {version}")

    results = [0, 0, 0]  # draw - white - black
    for i in range(NUMBER_OF_GAMES):
        board = chess.Board()
        board = set_random_opening(board)
        white_time, black_time = 0, 0
        result = None

        while board.result() == GAME_IS_ON:
            if board.turn == WHITE:
                stockfish_white.set_fen_position(board.fen())

                time_spent = make_move(stockfish_white, board)
                white_time += time_spent

                if time_is_over(white_time, WHITE):
                    result = ResultOfGame.BLACK_WIN
                    break

                print(f"White time: {white_time}")

            elif board.turn == BLACK:
                stockfish_black.set_fen_position(board.fen())

                time_spent = make_move(stockfish_black, board)
                black_time += time_spent

                if time_is_over(black_time, BLACK):
                    result = ResultOfGame.WHITE_WIN
                    break

                print(f"Black time: {black_time}")

            print(board)

        result = board.result() if not result else result
        print("Wynik:", result)

        set_result(result, results)
        print(results)

    draw_results(results)
