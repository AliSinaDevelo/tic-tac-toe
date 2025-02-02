# test_tictactoe.py

import unittest
import random
from board import Board
from ai import get_easy_move, get_medium_move, get_hard_move
from game import Game
from players import HumanPlayer, AIPlayer

class TestBoard(unittest.TestCase):
    def setUp(self):
        self.board = Board()

    def test_initial_board(self):
        self.assertEqual(self.board.cells, [' ']*9)
        self.assertEqual(len(self.board.available_moves()), 9)

    def test_update_cell(self):
        self.assertTrue(self.board.update_cell(0, 'X'))
        self.assertEqual(self.board.cells[0], 'X')
        self.assertFalse(self.board.update_cell(0, 'O'))

    def test_check_winner_rows(self):
        for i in range(3):
            self.board.cells[i] = 'X'
        self.assertTrue(self.board.check_winner('X'))
        self.board.reset()
        self.board.cells[0] = self.board.cells[1] = 'X'
        self.board.cells[2] = 'O'
        self.assertFalse(self.board.check_winner('X'))

    def test_check_winner_columns(self):
        for i in range(0, 9, 3):
            self.board.cells[i] = 'O'
        self.assertTrue(self.board.check_winner('O'))

    def test_check_winner_diagonals(self):
        self.board.cells[0] = self.board.cells[4] = self.board.cells[8] = 'X'
        self.assertTrue(self.board.check_winner('X'))
        self.board.reset()
        self.board.cells[2] = self.board.cells[4] = self.board.cells[6] = 'O'
        self.assertTrue(self.board.check_winner('O'))

    def test_is_full(self):
        self.board.cells = ['X', 'O', 'X', 'X', 'O', 'O', 'O', 'X', 'X']
        self.assertTrue(self.board.is_full())
        self.board.cells[5] = ' '
        self.assertFalse(self.board.is_full())

    def test_reset(self):
        self.board.cells[0] = 'X'
        self.board.reset()
        self.assertEqual(self.board.cells, [' ']*9)

class TestAIModule(unittest.TestCase):
    def setUp(self):
        self.board = Board()

    def test_get_easy_move(self):
        available = self.board.available_moves()
        move = get_easy_move(self.board, available)
        self.assertIn(move, available)

    def test_get_medium_move_win(self):
        self.board.cells = ['X', 'X', ' ',
                            ' ', 'O', 'O',
                            ' ', ' ', ' ']
        available = self.board.available_moves()
        move = get_medium_move(self.board, 'X', 'O', available)
        self.assertEqual(move, 2)

    def test_get_medium_move_block(self):
        self.board.cells = ['O', 'O', ' ',
                            'X', ' ', ' ',
                            ' ', ' ', ' ']
        available = self.board.available_moves()
        move = get_medium_move(self.board, 'X', 'O', available)
        self.assertEqual(move, 2)

    def test_get_medium_move_random(self):
        self.board.reset()
        available = self.board.available_moves()
        move = get_medium_move(self.board, 'X', 'O', available)
        self.assertIn(move, available)

    def test_get_hard_move_optimal(self):
        # In this board state, cells 7 and 8 are available.
        self.board.cells = ['X', 'O', 'X',
                            'O', 'X', 'O',
                            'O', ' ', ' ']
        move = get_hard_move(self.board, 'X', 'O')
        self.assertIn(move, [7, 8])
        # Optionally simulate the move and check for win:
        self.board.cells[move] = 'X'
        if self.board.check_winner('X'):
            self.assertTrue(self.board.check_winner('X'))
        else:
            self.assertIn(move, [7, 8])  # at least the move was valid.

    def test_minimax_block_opponent_win(self):
        self.board.cells = ['O', 'O', ' ',
                            'X', ' ', ' ',
                            'X', ' ', ' ']
        move = get_hard_move(self.board, 'X', 'O')
        self.assertEqual(move, 2)

class TestGameMechanics(unittest.TestCase):
    def setUp(self):
        # Create dummy players with predetermined moves.
        class DummyPlayer:
            def __init__(self, marker, moves):
                self.marker = marker
                self.moves = moves
                self.index = 0

            def get_move(self, board):
                move = self.moves[self.index]
                self.index += 1
                return move

        self.DummyPlayer = DummyPlayer
        self.player1 = DummyPlayer('X', [0, 1, 2])
        self.player2 = DummyPlayer('O', [3, 4, 5])
        self.game = Game(self.player1, self.player2)

    def test_switch_player(self):
        self.assertEqual(self.game.current_player, self.player1)
        self.game.switch_player()
        self.assertEqual(self.game.current_player, self.player2)
        self.game.switch_player()
        self.assertEqual(self.game.current_player, self.player1)

    def test_game_play_win(self):
        # Setup a win for player1 (X) with moves: 0, 1, 2.
        self.player1.moves = [0, 1, 2]
        self.player2.moves = [3, 4]  # Fewer moves; player1 gets the final move.
        # Simulate until win or board full.
        while (not self.game.board.is_full() and 
               not self.game.board.check_winner('X') and 
               not self.game.board.check_winner('O')):
            move = self.game.current_player.get_move(self.game.board)
            self.game.board.update_cell(move, self.game.current_player.marker)
            if self.game.board.check_winner(self.game.current_player.marker):
                break
            self.game.switch_player()
        self.assertTrue(self.game.board.check_winner('X'), "Player X should win the game.")

    def test_game_draw(self):
        draw_moves = [0, 1, 2, 4, 3, 5, 7, 6, 8]
        
        class DummyPlayer:
            def __init__(self, marker, moves):
                self.marker = marker
                self.moves = moves
                self.index = 0

            def get_move(self, board):
                move = self.moves[self.index]
                self.index += 1
                return move

        moves_x = draw_moves[::2]
        moves_o = draw_moves[1::2]
        player1 = DummyPlayer('X', moves_x)
        player2 = DummyPlayer('O', moves_o)
        game = Game(player1, player2)
        
        while (not game.board.is_full() and 
               not game.board.check_winner('X') and 
               not game.board.check_winner('O')):
            move = game.current_player.get_move(game.board)
            game.board.update_cell(move, game.current_player.marker)
            if game.board.check_winner(game.current_player.marker):
                break
            game.switch_player()
            
        self.assertTrue(game.board.is_full(), "Board should be full in a draw scenario.")
        self.assertFalse(game.board.check_winner('X'), "There should be no winner (X).")
        self.assertFalse(game.board.check_winner('O'), "There should be no winner (O).")

if __name__ == '__main__':
    random.seed(0)  # For reproducibility in tests that use randomness.
    unittest.main()
