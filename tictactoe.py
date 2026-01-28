import math

AI = "O"
HUMAN = "X"
EMPTY = None

# shared board for external UIs (e.g., robot.py) to manipulate
# initialize as empty board
board = [EMPTY] * 9

WIN_LINES = [
	(0, 1, 2), (3, 4, 5), (6, 7, 8),  # rows
	(0, 3, 6), (1, 4, 7), (2, 5, 8),  # cols
	(0, 4, 8), (2, 4, 6)              # diagonals
]

def winner(board):
	for a, b, c in WIN_LINES:
		if board[a] and board[a] == board[b] == board[c]:
			return board[a]
	return None

def is_full(board):
	return all(cell is not None for cell in board)

def available_moves(board):
	return [i for i, cell in enumerate(board) if cell is None]

def minimax(board, current_player, depth=0):
	w = winner(board)
	if w == AI:
		return (10 - depth, None)     # prefer quicker wins
	if w == HUMAN:
		return (depth - 10, None)     # prefer slower losses
	if is_full(board):
		return (0, None)              # tie

	if current_player == AI:
		best_score = -math.inf
		best_move = None
		for move in available_moves(board):
			board[move] = AI
			score, _ = minimax(board, HUMAN, depth + 1)
			board[move] = EMPTY
			if score > best_score:
				best_score, best_move = score, move
		return best_score, best_move
	else:
		best_score = math.inf
		best_move = None
		for move in available_moves(board):
			board[move] = HUMAN
			score, _ = minimax(board, AI, depth + 1)
			board[move] = EMPTY
			if score < best_score:
				best_score, best_move = score, move
		return best_score, best_move

def best_ai_move(board):
	_, move = minimax(board, AI)
	return move

if __name__ == "__main__":
	board = [None] * 9
	# Example position (X to play already moved):
	# board[2] = "X"
	print(best_ai_move(board))

	# Just show AI's best first move on empty board:
	print("AI best move on empty board:", best_ai_move(board))