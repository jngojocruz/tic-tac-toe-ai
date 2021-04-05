'''
* Gojo Cruz, Jamlech Iram N.
* CMSC170 Exercise 11: Min-Max Algorithm

* The goal of the exercise is to implement the Min-Max algorithm
* that would make a smart AI agent.

* December 16, 2020
'''

# Modules
import numpy as np
import random
from tkinter import *
from tkinter import messagebox

# Tkinter window
root = Tk()
root.title("Gojo Cruz - Tic-Tac-Toe")
f1 = Frame(root) # Menu 
f2 = Frame(root) # Game board
f3 = Frame(root) # Info frame

# Photos used are in the 'photos' folder
background = PhotoImage(file = "photos\\background.png")
background2 = PhotoImage(file = "photos\\background2.png")
play_img = PhotoImage(file = "photos\\play_img.png")
play_again = PhotoImage(file = "photos\\play_again.png")
info = PhotoImage(file = "photos\\info.png")
exit = PhotoImage(file = "photos\\exit.png")
go_back = PhotoImage(file = "photos\\go_back.png")
sun = PhotoImage(file = "photos\\sun.png")
moon = PhotoImage(file = "photos\\moon.png") 
star = PhotoImage(file = "photos\\star.png")
yes = PhotoImage(file = "photos\\yes.png")
no = PhotoImage(file = "photos\\no.png")

# Values for blanks, X, and O
B = " "
B_Photo = star
HUMAN = "O"
HUMAN_Photo = moon
AI = "X"
AI_Photo = sun

# Determines the current player (if maximizing)
MAX = 1
MIN = -1
GamePlayX = 0

# Other global variables' initializations
turn = True
board = None
winner = False
buttons = list()

'''
-----------------------------------------------------------------------------------------
Creates and returns the initial board with blank squares
-----------------------------------------------------------------------------------------
'''
def create_board():
	board = [[B,B,B],[B,B,B],[B,B,B]]
	return board


'''
-----------------------------------------------------------------------------------------
Used for printing the board to the terminal
@param:
	state - current configuration of the board
-----------------------------------------------------------------------------------------
'''
def print_board(state):
	for i in state:
		print(i)


'''
-----------------------------------------------------------------------------------------
Check whether the current state/board is a terminal state - if there is already a
winner or the board is full (draw)
@param:
	state - current configuration of the board
-----------------------------------------------------------------------------------------
'''
def terminal(state):
	# Check rows and columns
	new_board = [state, np.transpose(state)]
	for i in new_board:
		for row in i:
			if B not in set(row) and len(set(row)) == 1:
				return row[0]
	
	# Check diagonal
	new_board = list()
	for i in range(len(state)):
		new_board.append(state[i][i])
	if B not in set(new_board) and len(set(new_board)) == 1:
		return new_board[0]
	
	# Check reversed diagonal
	new_board = list()
	for i in range(len(state)):
		new_board.append(state[i][len(state)-i-1])
	if B not in set(new_board) and len(set(new_board)) == 1:
		return new_board[0]

	# Check if no possible moves
	cnt = 0
	for row in state:
		if B not in set(row):
			cnt += 1
	if cnt == len(state): 
		return "DRAW"

	# Not terminal
	return 0


'''
-----------------------------------------------------------------------------------------
Checks if the board is the initial board
@param:
	state - current configuration of the board
-----------------------------------------------------------------------------------------
'''
def is_board_empty(state):
	for i in range(3): # copy the list
		for j in range(3):
			if(state[i][j] != B):
				return False
	return True


'''
-----------------------------------------------------------------------------------------
Returns the utility value from the terminal state - +1 for the maximizing player,
-1 for the opponent, and 0 if draw; returns the current value of the state s to a player p.
@param:
	state - current configuration of the board
	t - symbol of the player who won
-----------------------------------------------------------------------------------------
'''
def utility(state, t):
	if t == AI:
		return 1
	elif t == HUMAN:
		return -1
	else:
		return 0


'''
-----------------------------------------------------------------------------------------
Minmax function; recursively computes for every node until utility is returned
@param:
	state - current configuration of the board
	next_agent - the player who's taking turn
	depth - depth of the tree (starting from 0, root node); total number of turns for P1
		    and P 2 to reach a terminal state
	alpha - The best solution (lower bound) for the maximizer on the path to the root.
	beta - The best solution (upper bound) for the minimizer on the path to the root.
-----------------------------------------------------------------------------------------
'''
def value(state, next_agent, depth, alpha, beta):
	global GamePlayX, GamePlayO
	GamePlayX += 1
	t = terminal(state)
	if t:
		return utility(state, t)
	if next_agent == MAX:
		return max_value(state, depth, alpha, beta)
	if next_agent == MIN:
		return min_value(state, depth, alpha, beta)


'''
-----------------------------------------------------------------------------------------
For the maximizing player; finds the maximum attainable value/optimal move for the player
@param:
	state - current configuration of the board
	depth - depth of the tree (starting from 0, root node); total number of turns for P1
		    and P 2 to reach a terminal state
	alpha - The best solution (lower bound) for the maximizer on the path to the root.
	beta - The best solution (upper bound) for the minimizer on the path to the root.
-----------------------------------------------------------------------------------------
'''
def max_value(state, depth, alpha, beta):
	# Max is initially negative infinity
	v = -np.inf
	# For all successors
	for i in range(len(state)):
		for j in range(len(state)):
			# If the square is available for a move
			if state[i][j] == B:
				# Temporarily update the board with that move
				state[i][j] = AI
				# Call minmax function
				val = value(state, MIN, depth+1, alpha, beta)
				# Undo board update
				state[i][j] = B
				# If the value obtained from the successor is greater than the current max value
				if val > v:
					# Update the current maximum value
					v = val
					# Get the coordinates to keep track the action
					a = (i,j)
				# Alpha-beta pruning
				if val >= beta:
					return v
				alpha = max(alpha, v)
	# If it is already the root node; terminating condition
	if depth == 0:
		# Return the optimal move/action
		return a
	# Else, return the current max value
	return v


'''
-----------------------------------------------------------------------------------------
For the minimizing player; finds the minimum attainable value for the opponent
@param:
	state - current configuration of the board
	depth - depth of the tree (starting from 0, root node); total number of turns for P1
		    and P 2 to reach a terminal state
	alpha - The best solution (lower bound) for the maximizer on the path to the root.
	beta - The best solution (upper bound) for the minimizer on the path to the root.
-----------------------------------------------------------------------------------------
'''
def min_value(state, depth, alpha, beta):
	v = np.inf
	for i in range(len(state)):
		for j in range(len(state)):
			if state[i][j] == B:
				state[i][j] = HUMAN
				# Minmax function
				val = value(state, MAX, depth+1, alpha, beta)
				state[i][j] = B
				
				v = min(val, v)
				
				# Alpha-beta pruning
				if v <= alpha:
					return v
				beta = min(beta, v)
	return v


'''
-----------------------------------------------------------------------------------------
Updates the previous board
@param:
	row - 
	col - 
	state - current configuration of the board
	player - char symbol to put
-----------------------------------------------------------------------------------------
'''
def update_board(row, col, state, player):
	state[row][col] = player


'''
-----------------------------------------------------------------------------------------
Returns False if there is already a winner and True if not; sets the global variable
winner for flag purposes; pops-up a message box to notify if computer won or a draw
@param:
	state - current configuration of the board
-----------------------------------------------------------------------------------------
'''
def check_winner(state):
	global winner
	t = terminal(state)
	if t != 0:
		if t == "DRAW":
			#print("It's a Tie!")
			messagebox.showinfo("Game Over", "It's a Draw!")
			winner = False
		else:
			#print(t+" (Computer) Wins! ")
			messagebox.showinfo("Game Over", "Computer Won!")
			winner = True
		return False
	return True


'''
-----------------------------------------------------------------------------------------
Sets the global variable turn if the player wants to be first or not
@param:
	choice - either 'y' or 'n' which will be returned by button click
-----------------------------------------------------------------------------------------
'''
def ask_turn(choice):
	global turn
	if choice.lower() == 'y':
		turn = False
	else:
		turn = True


'''
-----------------------------------------------------------------------------------------
Sets the global variables for HUMAN and AI char symbol, and their corresponding photos
for the buttons
@param:
	choice - either 'X' or 'O' which will be returned by button click
-----------------------------------------------------------------------------------------
'''
def ask_symbol(choice):
	global HUMAN, AI, HUMAN_Photo, AI_Photo
	# choice = input("What do you want? [X/O]: ")
	if choice.upper() == 'X':
		HUMAN = "X"
		HUMAN_Photo = moon
		AI = "O"
		AI_Photo = sun
	else:
		HUMAN = "O"
		HUMAN_Photo = sun
		AI = "X"
		AI_Photo = moon 


'''
-----------------------------------------------------------------------------------------
Changes the frame viewed from the window
@param:
	frame - the frame to be raised
-----------------------------------------------------------------------------------------
'''
def raise_frame(frame):
    frame.tkraise()


'''
-----------------------------------------------------------------------------------------
Changes the frame viewed from the window and restarts the board
@param:
	frame - the frame to be raised
-----------------------------------------------------------------------------------------
'''
def raise_game_frame(frame):
	restart_board()
	frame.tkraise()


'''
-----------------------------------------------------------------------------------------
Sets all the buttons' state to disabled; called if game has a winner or is a draw
-----------------------------------------------------------------------------------------
'''
def disable_buttons():
	for b in buttons:
		b.config(command=0)
		b.config(relief=SUNKEN)


'''
-----------------------------------------------------------------------------------------
Sets all the buttons' state to normal; called if the game restarts
-----------------------------------------------------------------------------------------
'''
def enable_buttons():
	for b in buttons:
		b.config(state=NORMAL)


'''
-----------------------------------------------------------------------------------------
Function that updates AI's move on the board 
@param:
	state - current configuration of the board
-----------------------------------------------------------------------------------------
'''
def ai_turn(state):
	global turn, count
	# If computer is is first to play, randomize the first move
	# Comment this if randomization is to be disabled
	if is_board_empty(state):
		x = [random.randint(0,2), random.randint(0,2)]
	# Else, call minmax function
	else:
		x = value(state, MAX, 0, -np.inf, np.inf)
	# Update the board
	update_board(x[0], x[1], state, AI)
	buttons[x[0]*3+x[1]].config(image=AI_Photo)
	buttons[x[0]*3+x[1]].config(command=0)
	buttons[x[0]*3+x[1]].config(relief=SUNKEN)
	turn = False

'''
-----------------------------------------------------------------------------------------
If button is clicked, update the board for whatever move the player made;
It will always be followed by the move of AI; always checks if there is already
a terminal state (winner or draw)
@param:
	i - index of the button from the buttons list
-----------------------------------------------------------------------------------------
'''
def b_click(i):
	global turn, count
	# Check if player's move is allowed (blank) and it is player's turn
	if board[int(i/3)][int(i%3)] == B and turn == False:
		# Update board which corresponds to the player's move
		buttons[i].config(image=HUMAN_Photo)
		board[int(i/3)][int(i%3)] = HUMAN
		buttons[i].config(command=0)
		buttons[i].config(relief=SUNKEN)
		turn = True
		if not check_winner(board):
			disable_buttons()
			return

		# AI will play
		ai_turn(board)
		if not check_winner(board):
			disable_buttons()


'''
-----------------------------------------------------------------------------------------
Restarts the board and reset the values if button 'play again' is clicked
-----------------------------------------------------------------------------------------
'''
def restart_board():
	global board, buttons, turn, B_Photo
	# Make sure previously disabled buttons are enabled again
	enable_buttons()
	# Recreate the board by making all squares blank
	board = create_board()
	# Update photos for buttons
	for i in range(9):
		buttons[i].config(image=B_Photo)
		buttons[i].config(command=lambda i=i: b_click(i))
		buttons[i].config(relief=RAISED)
	# Check if the first one to play is the AI
	if turn == True:
		ai_turn(board)


'''
-----------------------------------------------------------------------------------------
Position frames
-----------------------------------------------------------------------------------------
'''
for frame in (f1, f2, f3):
    frame.grid(row=0, column=0, sticky='news')


'''
-----------------------------------------------------------------------------------------
Labels and buttons for frame 1 - Menu
-----------------------------------------------------------------------------------------
'''
Label(f1, image=background).place(x=0, y=0, relwidth=1, relheight=1)
Button(f1, image=yes, command=lambda:ask_turn("y")).place(x = 90, y=180)
Button(f1, image=no, command=lambda:ask_turn("n")).place(x = 270, y=180)
Button(f1, image=moon, command=lambda:ask_symbol("X")).place(x = 90, y=320)
Button(f1, image=sun, command=lambda:ask_symbol("O")).place(x = 270, y=320)
Button(f1, image=play_img, command=lambda:raise_game_frame(f2)).place(x = 180, y=530)


'''
-----------------------------------------------------------------------------------------
Labels and buttons for frame 2 - Game board
-----------------------------------------------------------------------------------------
'''
Label(f2, image=background).place(x=0, y=0, relwidth=1, relheight=1)
Button(f2, image=play_again, command=lambda:raise_frame(f1)).grid(row=3, column=0)
Button(f2, image=info, command=lambda:raise_frame(f3)).grid(row=3, column=1)
Button(f2, image=exit, command=lambda:root.destroy()).grid(row=3, column=2)

# Creates 9 buttons (for 3x3 grid)
for i in range(9):
	buttons.append(Button(f2, image=B_Photo, command=lambda i=i: b_click(i)))

for i in range(3):
	for j in range(3):
		buttons[i*3+j].grid(row=i, column=j)


'''
-----------------------------------------------------------------------------------------
Labels and buttons for frame 3 - Info
-----------------------------------------------------------------------------------------
'''
Label(f3, image=background2).place(x=0, y=0, relwidth=1, relheight=1)
Button(f3, image=go_back, command=lambda:raise_frame(f2)).place(x = 180, y=480)


# Main Driver
raise_frame(f1) # Raise the first frame (Menu)
root.mainloop()