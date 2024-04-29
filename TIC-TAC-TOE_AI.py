import math

def print_board(board):
    for row in board:
        print(" | ".join(row))
        print("--" * 3)

def check_winner(board, player):
    win_conditions = (
        any(all(cell == player for cell in line) for line in board) or  # rows
        any(all(board[row][col] == player for row in range(3)) for col in range(3)) or  # cols
        all(board[i][i] == player for i in range(3)) or  # main diagonal
        all(board[i][2-i] == player for i in range(3))  # anti diagonal
    )
    return win_conditions

def get_empty_cells(board):
    return [(i, j) for i in range(3) for j in range(3) if board[i][j] == " "]

def minimax(board, depth, is_maximizing, alpha, beta):
    scores = {"X": 1, "O": -1, "Tie": 0}
    winner = next((player for player in ['X', 'O'] if check_winner(board, player)), None)
    if winner or not get_empty_cells(board):
        return scores.get(winner, 0)
    if is_maximizing:
        max_eval = -math.inf
        for i, j in get_empty_cells(board):
            board[i][j] = "X"
            max_eval = max(max_eval, minimax(board, depth + 1, False, alpha, beta))
            board[i][j] = " "
            alpha = max(alpha, max_eval)
            if beta <= alpha:
                break
        return max_eval
    else:
        min_eval = math.inf
        for i, j in get_empty_cells(board):
            board[i][j] = "O"
            min_eval = min(min_eval, minimax(board, depth + 1, True, alpha, beta))
            board[i][j] = " "
            beta = min(beta, min_eval)
            if beta <= alpha:
                break
        return min_eval

def get_best_move(board):
    best_eval, best_move = -math.inf, None
    for i, j in get_empty_cells(board):
        board[i][j] = "X"
        eval = minimax(board, 0, False, -math.inf, math.inf)
        board[i][j] = " "
        if eval > best_eval:
            best_eval, best_move = eval, (i, j)
    return best_move

def play_game():
    board = [[" "]*3 for _ in range(3)]
    print("Welcome to Tic-Tac-Toe!")
    print_board(board)

    while True:
        player_move = tuple(map(int, input("Enter your move (row col): ").split()))
        if board[player_move[0]][player_move[1]] != " ":
            print("Invalid move. Try again.")
            continue
        board[player_move[0]][player_move[1]] = "O"
        print_board(board)
        if check_winner(board, "O"):
            print("You win!")
            break
        if not get_empty_cells(board):
            print("It's a tie!")
            break
        ai_move = get_best_move(board)
        board[ai_move[0]][ai_move[1]] = "X"
        print("AI's move:")
        print_board(board)
        if check_winner(board, "X"):
            print("AI wins!")
            break
        if not get_empty_cells(board):
            print("It's a tie!")
            break

play_game()
