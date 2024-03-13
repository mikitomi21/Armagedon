import matplotlib.pyplot as plt
import os
# import numpy as np

from file_manager import FileManager
from result_of_game import ResultOfGame


class ChartManager:
    DRAW_COLOR = 'blue'
    WHITE_WIN_COLOR = 'green'
    BLACK_WIN_COLOR = 'red'
    CHARTS_DIRECTORY = 'charts'

    @staticmethod
    def create_chart_dir() -> None:
        charts_path = os.path.join(os.getcwd(), ChartManager.CHARTS_DIRECTORY)
        if not os.path.exists(charts_path):
            os.mkdir(charts_path)

    @staticmethod
    def linear_chart(game_name: str) -> None:
        ChartManager.create_chart_dir()
        results = FileManager.get_results_for_every_game_from_file(game_name)
        draws = []
        white_wins = []
        black_wins = []
        for i, result in enumerate(results):
            draws.append(result.get_results()[ResultOfGame.DRAW] * 100 / (i+1))
            white_wins.append(result.get_results()[ResultOfGame.WHITE_WIN] * 100 / (i+1))
            black_wins.append(result.get_results()[ResultOfGame.BLACK_WIN] * 100 / (i+1))

        fig, ax = plt.subplots(figsize=(10,6))
        number_of_games = len(draws)
        for i in range(number_of_games):
            ax.bar(i, black_wins[i], color=ChartManager.BLACK_WIN_COLOR)
            ax.bar(i, draws[i], bottom=black_wins[i], color=ChartManager.DRAW_COLOR)
            ax.bar(i, white_wins[i], bottom=draws[i]+black_wins[i], color=ChartManager.WHITE_WIN_COLOR)

        labels = ["Black wins", "Draws", "White wins"]
        ax.legend(labels)
        chart_name = f"{ChartManager.CHARTS_DIRECTORY}/{game_name[:-4]}_linear.png"
        plt.savefig(chart_name)
        plt.show()

    @staticmethod
    def bar_chart(game_name: str, results: ResultOfGame = None) -> None:
        ChartManager.create_chart_dir()
        if not results:
            results = FileManager.get_results_from_file(game_name)

        fig, ax = plt.subplots()
        results_of_game = [ResultOfGame.DRAW, ResultOfGame.WHITE_WIN, ResultOfGame.BLACK_WIN]
        bar_labels = ['draw', 'white win', 'black win']
        bar_colors = ['grey', 'green', 'red']

        ax.bar(results_of_game, results.get_results().values(), label=bar_labels, color=bar_colors)

        ax.set_ylabel('Number of games')
        ax.set_xlabel('Results of games')

        ax.set_yticks(range(0, max(results.get_results().values()) + 1))
        ax.set_xticks(results_of_game)
        ax.set_xticklabels(bar_labels)

        ax.legend(bar_labels)
        chart_name = f"{ChartManager.CHARTS_DIRECTORY}/{game_name[:-4]}_bar.png"
        plt.savefig(chart_name)

        plt.show()
