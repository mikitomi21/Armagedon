import sys
import chess
import chess.polyglot
import time
from stockfish import Stockfish, StockfishException
import matplotlib.pyplot as plt
import logging

from file_manager import FileManager
from result_of_game import ResultOfGame
from chart_manager import ChartManager

LOGGER = logging.getLogger()
IS_LOGGER_DISABLED = False
LOGGING_LEVEL = logging.INFO  # DEBUG - position, moves, etc, INFO - simulation info?
STOCKFISH_PATH = str(sys.argv[1]) if len(sys.argv) > 1 else None
GAME_IS_ON = "*"
COLORS = [WHITE, BLACK] = [True, False]
NUMBER_OF_GAMES = 100
BLACK_TIME_LIMIT = 1
WHITE_TIME_LIMIT = 1
INCREMENT = 0
UCI_ELO = 2035
HASH = 6048
THREADS = 8
MIN_THINKING_TIME = 1

parameters_white = {
    "Debug Log File": "debug_white.txt",
    "Contempt": 0,
    "Min Split Depth": 0,
    "Threads": THREADS,
    "Ponder": "false",
    "Hash": HASH,
    "MultiPV": 1,
    "Skill Level": 20,
    "Move Overhead": 10,
    "Minimum Thinking Time": MIN_THINKING_TIME,
    "Slow Mover": 100,
    "UCI_Chess960": "false",
    "UCI_LimitStrength": "false",
    "UCI_Elo": UCI_ELO
}

parameters_black = {
    "Debug Log File": "debug_black.txt",
    "Contempt": 0,
    "Min Split Depth": 0,
    "Threads": THREADS,
    "Ponder": "false",
    "Hash": HASH,
    "MultiPV": 1,
    "Skill Level": 20,
    "Move Overhead": 10,
    "Minimum Thinking Time": MIN_THINKING_TIME,
    "Slow Mover": 100,
    "UCI_Chess960": "false",
    "UCI_LimitStrength": "false",
    "UCI_Elo": UCI_ELO
}


def set_engine(parameters: dict) -> Stockfish:
    engine = Stockfish(path=STOCKFISH_PATH)
    engine.update_engine_parameters(parameters)
    return engine


def make_move(engine: Stockfish, board: chess.Board, player: COLORS, player_time: float, enemy_time: float) -> None:
    try:
        move = None
        if player == WHITE:
            move = engine.get_best_move(wtime=int(player_time * 1000), btime=int(enemy_time * 1000))
        else:
            move = engine.get_best_move(btime=int(player_time * 1000), wtime=int(enemy_time * 1000))

        board.push_san(move)
    except StockfishException as e:
        LOGGER.error(e)


def time_is_over(player_time: float) -> bool:
    if player_time <= 0:
        LOGGER.debug(f"Lost on time: {player_time}")
        return True
    return False


def draw_results(results: list[int, int, int]) -> None:
    LOGGER.debug(results)
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
                LOGGER.debug(entry)
                chess_board.push(entry.move)
            except IndexError:
                # No more moves in opening book
                break

    return chess_board


if __name__ == "__main__":
    logging.basicConfig(level=LOGGING_LEVEL)
    LOGGER.disabled = IS_LOGGER_DISABLED

    stockfish_white = set_engine(parameters_white)
    stockfish_black = set_engine(parameters_black)

    version = stockfish_white.get_stockfish_major_version()
    LOGGER.info(f"Version of stockfish engine: {version}")

    game_name = FileManager.create_new_file_game()
    results = ResultOfGame()

    for i in range(NUMBER_OF_GAMES):
        if i % 10 == 0:
            LOGGER.info(f"Game number: {i}")
            LOGGER.info(f"Overall results: {results}")
        board = chess.Board()
        board = set_random_opening(board)
        stockfish_white.set_fen_position(board.fen())
        stockfish_black.set_fen_position(board.fen())
        white_time, black_time = WHITE_TIME_LIMIT, BLACK_TIME_LIMIT
        result = None

        while board.result() == GAME_IS_ON:
            if board.turn == WHITE:
                stockfish_white.set_fen_position(board.fen(), send_ucinewgame_token=False)
                current_time = time.time()
                make_move(stockfish_white, board, WHITE, white_time, black_time)
                white_time -= time.time() - current_time - INCREMENT

                if time_is_over(white_time):
                    result = ResultOfGame.BLACK_WIN
                    break

                LOGGER.debug(f"White time: {white_time}")

            elif board.turn == BLACK:
                stockfish_black.set_fen_position(board.fen(), send_ucinewgame_token=False)
                current_time = time.time()
                make_move(stockfish_black, board, BLACK, black_time, white_time)
                black_time -= time.time() - current_time - INCREMENT

                if time_is_over(black_time):
                    result = ResultOfGame.WHITE_WIN
                    break

                LOGGER.debug(f"Black time: {black_time}")
            LOGGER.debug(f"\n{board}")

        result = board.result() if not result else result
        FileManager.save_result_into_file(game_name, result)
        print("Wynik:", result)
        results.set_result(result)

        LOGGER.info(f"Result: {result}")

    ChartManager.bar_chart(game_name, results)
    ChartManager.linear_chart(game_name)
