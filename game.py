from board import Board

class Game:
    def __init__(self, player1, player2):
        self.board = Board()
        self.player1 = player1
        self.player2 = player2
        self.current_player = self.player1

    def switch_player(self):
        self.current_player = (
                self.player2 if self.current_player == self.player1
                else self.player1
        )

    def play(self):
        self.board.display()
        while True:
            move = self.current_player.get_move(self.board)
            if self.board.update_cell(move, self.current_player.marker):
                self.board.display()
                if self.board.check_winner(self.current_player.marker):
                    print(f"Player {self.current_player.marker} wins!")
                    break
                elif self.board.is_full():
                    print("It's a draw!")
                    break
                self.switch_player()
            else:
                print("Invalid move. Try again.")
