import random

def get_easy_move(board, available_moves):
    return random.choice(available_moves)

def get_medium_move(board, ai_marker, opponent_marker, available_moves):

    for move in available_moves:
        backup = board.cells[move]
        board.cells[move] = ai_marker
        if board.check_winner(ai_marker):
            board.cells[move] = backup
            return move
        board.cells[move] = backup
    for move in available_moves:
        backup = board.cells[move]
        board.cells[move] = opponent_marker
        if board.check_winner(opponent_marker):
            board.cells[move] = backup
            return move
        board.cells[move] = backup
    return random.choice(available_moves)

def get_hard_move(board, ai_marker, opponent_marker):
    best_score = -float("inf")
    best_move = None

    for move in board.available_moves():

        board.cells[move] = ai_marker
        score = minimax(board, 0, False, ai_marker, opponent_marker)
        board.cells[move] = ' '  
        if score > best_score:
            best_score = score
            best_move = move

    return best_move

def minimax(board, depth, is_maximizing, ai_marker, opponent_marker):
    if board.check_winner(ai_marker):
        return 10 - depth
    elif board.check_winner(opponent_marker):
        return depth - 10
    elif board.is_full():
        return 0

    if is_maximizing:
        best_score = -float("inf")
        for move in board.available_moves():
            board.cells[move] = ai_marker
            score = minimax(board, depth + 1, False, ai_marker, opponent_marker)
            board.cells[move] = ' '  # Undo move
            best_score = max(score, best_score)
        return best_score
    else:
        best_score = float("inf")
        for move in board.available_moves():
            board.cells[move] = opponent_marker
            score = minimax(board, depth + 1, True, ai_marker, opponent_marker)
            board.cells[move] = ' '  # Undo move
            best_score = min(score, best_score)
        return best_score
