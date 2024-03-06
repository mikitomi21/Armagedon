import os
import datetime

from result_of_game import ResultOfGame


class FileManager:
    GAMES_DIRECTORY = 'games'
    RANGE_OF_GAMES = 4  # 0000.txt

    @staticmethod
    def create_new_file_game() -> str:
        games_path = os.path.join(os.getcwd(), FileManager.GAMES_DIRECTORY)

        if not os.path.exists(games_path):
            os.mkdir(games_path)

        games = sorted(os.listdir(games_path), reverse=True)
        last_game = games[0][:-FileManager.RANGE_OF_GAMES]

        game_name = f"{str(int(last_game)+1).zfill(FileManager.RANGE_OF_GAMES)}.txt"

        with open(f"{FileManager.GAMES_DIRECTORY}/{game_name}", 'w', encoding='utf-8') as file:
            data = datetime.datetime.now()
            file.write(data.strftime("%d/%m/%Y %H:%M:%S") + '\n')

        return game_name

    @staticmethod
    def save_result_into_file(game_name: str, result: ResultOfGame) -> None:
        with open(f"{FileManager.GAMES_DIRECTORY}/{game_name}", 'a', encoding='utf-8') as file:
            file.write(f"{result}\n")

