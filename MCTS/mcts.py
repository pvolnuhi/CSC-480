# Lab by Morgan Swanson
# Contributted some elements and functions by Polina Volnuhina
# CSC 480-01, Kurfess
# 10/14/2020
import numpy as np
from Metrics import * 
from tqdm.notebook import tqdm
#from tqdm.notebook import tqdm
example_board = np.array([[' ', ' ', ' '],
                          [' ', ' ', ' '],
                          [' ', ' ', ' ']])

# Calculates all successor states to a given state
def get_possible_moves(board, player):
    moves = []
    for (x, y), element in np.ndenumerate(board):
        if element == ' ':
            new_board = np.array(board, copy=True)
            new_board[x][y] = 'X' if player is 'max' else 'O'
            moves.append(new_board)
    return moves


def get_score(board, depth=0):
    if (np.any(np.all(board == 'X', axis=0)) or 
        np.any(np.all(board == 'X', axis=1)) or 
        np.all(board.diagonal() == 'X') or 
        np.all(np.fliplr(board).diagonal() == 'X')):
        # Max Victory
        return 1 * (1 / (1 + depth))
    elif (np.any(np.all(board == 'O', axis=0)) or 
          np.any(np.all(board == 'O', axis=1)) or
          np.all(board.diagonal() == 'O') or 
          np.all(np.fliplr(board).diagonal() == 'O')):
        # Min Victory
        return -1 * (1 / (1 + depth))
    elif not (board == ' ').any():
        # Draw
        return 0
    else:
        # Unfinished Game
        return None



# Your first task is to implement board selection. Within a simulation, 
# we must be able to, given a board, select a successor board. 
# We will do this by calculating the UCB for all possible successors and choosing 
# randomly between the boards that have the highest UCB.
# Formally, when given the current board, the table of metrics for all known boards, 
# and the current player, select_board will return a sucessor board. 
# Right now, select board returns a random successor. The model implementation is 13 lines long.



# Select the next board to simulate using upper confidence bound
#Implementation below: -Polina Volnuhina
def select_board(board, history, player):
	high_ucb = 0
    boards = get_possible_moves(board, player)
    for i in get_possible_moves(board, player):
    	return get_ucb(i)
    	if i >= high_ucb:
    		high_ucb = i;
    return random(high_ucb)
    boards_successor = get_ucb(board, player, c, default)
    policy_vector = np.ones(len(find_best_move)) / len(find_best_move)
    if get_possible_moves.tobytes() not in history:
    return boards[np.random.choice(np.arange(len(boards), dtype=int), 1, p=policy_vector)[0]]


#select_board(example_board, example_history, 'max')


#Your second task is to implement the simulations. 
#You must start with the given board and select successor boards using 'select_board' 
#until a terminal state is reached and then update the metrics along that game path with the result.
#Implementation below: -Polina Volnuhina
def simulation(board, history, player):
	track_score = get_score(board);
	if track_score != None:
		return track_score
	else:
		boarding = select_board(board, history, player)
		if boarding.tobytes() not in history:
			history[boarding.tobytes()] = Metrics()

		if player == "max":
			end_result = simulate(boarding, history, "min")
			history[boarding.tobytes()].update(end_result)
			return end_result

		elif player == "min":
			end_result = simulate(boarding, history, "max")
			history[boarding.tobytes()].update(end_result)
			return end_result


# Run a batch of monte carlo simulations, defaults to 100 simulations
def run_simulations(board, history, player, count=200):
    for i in tqdm(range(count)):
        # Adding some random data to the succesor board states 
        # This code should be replaced by your simulation code
        if board.tostring() not in history:
            history[board.tostring()] = Metrics
        for b in get_possible_moves(board, 'max'):
            if b.tostring() not in history:
                history[b.tostring()] = Metrics()
            rand_result = 1 if np.random.rand() > 0.5 else -1
            history[b.tostring()].update(rand_result)
            history[board.tostring()].update(rand_result)


# Finds the best move (state with highest/lowest value)
def find_best_move(board, history, player):
    if board.tostring() not in history:
        history[board.tostring()] = Metrics()
    print("Deciding best move...")
    run_simulations(board, history, player)
    boards = get_possible_moves(board, player)
    print(history[b.tostring()].count for b in boards)
    values = [history[b.tostring()].get_expected_value(player) for b in boards]
    return boards[np.argmax(values)]


# Testing find best move
#find_best_move(example_board, example_history, 'max')



# Starts a game against the AI Program
def run_demo():
    board = np.array([[' ', ' ', ' '],
                      [' ', ' ', ' '],
                      [' ', ' ', ' ']])
    history = {}
    score = get_score(board)
    player = "max"
    while score is None:
        if player == "max":
            board = find_best_move(board, history, player)
        else:
            move_entered = False
            while not move_entered:
                try:
                    move = int(input('Choose a move...')) - 1
                    if not 0 <= move <= 8:
                        print("Enter an integer between 1 and 9.\n")
                        continue
                    elif not board[move//3][move%3] == ' ':
                        print("That spot is already taken.\n")
                        continue
                    else:
                        board[move//3][move%3]= 'O'
                        move_entered = True
                except ValueError:
                    print("Enter an integer.\n")
        score = get_score(board)
        player = "min" if player == "max" else "max"
        print(board)
    if (score == 0):
        print("Draw")
    elif (score > 0):
        print("You Lose")
    else:
        print("You Win")
      
      
run_demo()