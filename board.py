class Board:
    def __init__(self):
        self.cells = [' ' for _ in range(9)]

    def display(self):

        print("\n")
        print(" {} | {} | {} ".format(self.cells[0], self.cells[1], self.cells[2]))
        print("---+---+---")
        print(" {} | {} | {} ".format(self.cells[3], self.cells[4], self.cells[5]))
        print("---+---+---")
        print(" {} | {} | {} ".format(self.cells[6], self.cells[7], self.cells[8]))
        print("\n")

    def update_cell(self, index, marker):
        if self.cells[index] == ' ':
            self.cells[index] = marker
            return True
        return False

    def available_moves(self):
        return [i for i, cell in enumerate(self.cells) if cell == ' ']

    def is_full(self):
        return ' ' not in self.cells

    def check_winner(self, marker):
        win_conditions = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8],  # rows
            [0, 3, 6], [1, 4, 7], [2, 5, 8],  # columns
            [0, 4, 8], [2, 4, 6]              # diagonals
        ]
        for condition in win_conditions:
            if all(self.cells[i] == marker for i in condition):
                return True
        return False

    def reset(self):
        self.cells = [' ' for _ in range(9)]

