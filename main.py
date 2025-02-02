import sys
from game import Game
from players import HumanPlayer, AIPlayer

def print_menu():
    print("=================================")
    print("      Welcome to Tic-Tac-Toe     ")
    print("=================================")
    print("1. Two Players")
    print("2. Play against AI")
    print("3. Exit")
    print("=================================")

def choose_ai_difficulty():
    print("Choose AI Difficulty Level:")
    print("1. Easy")
    print("2. Medium")
    print("3. Hard")
    while True:
        choice = input("Enter your choice (1-3): ")
        if choice == '1':
            return 'easy'
        elif choice == '2':
            return 'medium'
        elif choice == '3':
            return 'hard'
        else:
            print("Invalid selection. Please choose 1, 2, or 3.")

def main():
    while True:
        print_menu()
        choice = input("Enter your choice (1-3): ")

        if choice == '1':
            print("Two player mode selected.")
            player1 = HumanPlayer('X')
            player2 = HumanPlayer('O')
            game = Game(player1, player2)
            game.play()
        elif choice == '2':
            difficulty = choose_ai_difficulty()
            print(f"You chose AI difficulty: {difficulty.capitalize()}")
            mode_choice = input("Do you want to be 'X' (first move) or 'O' (second move)? Enter X or O: ").upper()

            if mode_choice not in ['X', 'O']:
                print("Invalid selection. Defaulting to X.")
                mode_choice = 'X'
            if mode_choice == 'X':
                player1 = HumanPlayer('X')
                player2 = AIPlayer('O', difficulty)
            else:
                player1 = AIPlayer('X', difficulty)
                player2 = HumanPlayer('O')
            game = Game(player1, player2)
            game.play()
        elif choice == '3':
            print("Exiting game.")
            sys.exit()
        else:
            print("Invalid selection. Please choose 1, 2, or 3.")

        replay = input("Do you want to play again? (Y/N): ").upper()
        if replay != 'Y':
            print("Goodbye!")
            sys.exit()

if __name__ == '__main__':
    main()
