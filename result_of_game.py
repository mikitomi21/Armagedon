class ResultOfGame:
    DRAW = "1/2-1/2"
    WHITE_WIN = "1-0"
    BLACK_WIN = "0-1"

    def __init__(self):
        self.draws = 0
        self.white_wins = 0
        self.black_wins = 0

    def draw(self) -> None:
        self.draws += 1

    def white_win(self) -> None:
        self.white_wins += 1

    def black_win(self) -> None:
        self.black_wins += 1

    def set_result(self, result: str) -> None:
        if result == ResultOfGame.DRAW:
            self.draw()
        elif result == ResultOfGame.WHITE_WIN:
            self.white_win()
        elif result == ResultOfGame.BLACK_WIN:
            self.black_win()

    def get_results(self) -> dict[str, int]:
        return {
            self.DRAW: self.draws,
            self.WHITE_WIN: self.white_wins,
            self.BLACK_WIN: self.black_wins,
        }

    def __str__(self):
        return f"{self.DRAW}: {self.draws}, {self.WHITE_WIN}: {self.white_wins}, {self.BLACK_WIN}: {self.black_wins}"
