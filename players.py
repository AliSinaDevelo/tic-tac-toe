import random
from ai import get_easy_move, get_medium_move, get_hard_move

class HumanPlayer:
    def __init__(self, marker):
        self.marker = marker

    def get_move(self, board):
        available = board.available_moves()
        while True:
            try:
                move = int(input(f"Player {self.marker}, choose your move (0-8): "))
                if move in available:
                    return move
                else:
                    print("Invalid move! That cell is either taken or out of range.")
            except ValueError:
                print("Invalid input! Please enter a number.")


class AIPlayer:
    def __init__(self, marker, difficulty):
        self.marker = marker
        self.difficulty = difficulty.lower()

        self.opponent_marker = 'O' if marker == 'X' else 'X'

    def get_move(self, board):
        available = board.available_moves()
        if self.difficulty == 'easy':
            move = get_easy_move(board, available)
        elif self.difficulty == 'medium':
            move = get_medium_move(board, self.marker, self.opponent_marker, available)
        elif self.difficulty == 'hard':
            move = get_hard_move(board, self.marker, self.opponent_marker)
        else:
            move = random.choice(available)

        print(f"AI ({self.difficulty.capitalize()}) chooses move: {move}")
        return move
