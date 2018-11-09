# coding=utf-8
import random

print("Let's play a game.\n")

BOARD = []


def game_loop():
    # The game should run until we return
    game_turn = 0
    no_player = 0 # player_setting()
    diff_ai = 2 # ai_setting()

    create_board()

    while True:
        print_board(BOARD)

        # who's turn is it
        current_player = get_current_player(game_turn)
        print("It is " + current_player + "'s turn\n")

        # Get a move
        if no_player == 1 and current_player == "O":
            print("Computers turn")
            coordinates = random_coordinates(BOARD)
        elif no_player == 0:
            if diff_ai == 1:
                coordinates = random_coordinates(BOARD)
            else:
                coordinates = minimax_coordinates(game_turn, BOARD)
        else:
            coordinates = player_coordinates()

        # Make the move
        place_token(current_player, BOARD, coordinates[0], coordinates[1])

        # Does the game end:
        if did_win(current_player, BOARD):
            print('{} has won the game 🏅'.format(current_player))
            print_board(BOARD)
            return

        elif is_board_full(game_turn):
            print("The game is over. No winners!")
            print_board(BOARD)
            return

        else:
            print("Nobody has won yet, keep looping")
            game_turn += 1


def player_setting():
    player = raw_input("How many players? (0-2)")
    print(player)

    while not is_valid_input(player, 0, 2):
        player = raw_input("Please choose between 1 and 2 players?")

    player = int(player)
    return player


def ai_setting():
    ai = raw_input("How difficult? easy = 1, hard = 2")

    while not is_valid_input(ai, 1, 2):
        ai = raw_input("Please choose between 1 or 2.")

    ai = int(ai)

    return ai

def create_board():
    # create the board
    size = raw_input("What size should the game be? (3-5): ")
    while not is_valid_input(size, 3, 6):
        size = raw_input("What size should the game be? (3-5): ")

    size = int(size)

    for i in range(size):
        BOARD.append([])
        for j in range(size):
            BOARD[i].append('_')


def print_board(board):
    for row in board:
        print(row)


def get_current_player(num):
    if num % 2 == 0:
        return "X"
    else:
        return "O"


def player_coordinates():
    while True:
        x_coord = raw_input('Choose a row?\n')
        while not is_valid_input(x_coord, 1, len(BOARD)+1):
            x_coord = raw_input('please select a valid row?\n')

        y_coord = raw_input("Choose a column?")
        while not is_valid_input(y_coord, 1, len(BOARD)+1):
            y_coord = raw_input('please select a valid column?\n')

        x_coord = int(x_coord)-1
        y_coord = int(y_coord)-1

        if not is_legal_move(x_coord, y_coord):
            print"That spot is taken, try again.\n"
            continue
        break

    return [x_coord, y_coord]


def is_valid_input(input, min, max):
    if not input.isdigit():
        return False
    # Note the int(coordinate).
    # We need to cast to Int before
    if not int(input) in range(min, max+1):
        return False

    # All is well
    return True


def place_token(token, board, x_coord, y_coord):
    board[x_coord][y_coord] = token


def did_win(player, board):
    player_has_won = False

    '#test rows'
    for row in board:
        if same_token_in_row(player, row):
            player_has_won = True

    '#test column'
    for i in range(len(board)):
            column = []
            for x in board:
                column.append(x[i])
            if same_token_in_row(player, column):
                player_has_won = True

    '#test diagonal'
    x_test2 = []
    y_test2 = []
    for i in range(len(board)):
        x_test = board[i]
        x_test2.append(x_test[i])

        y_test = board[i]
        y_test2.append(y_test[-(i+1)])

    if same_token_in_row(player, x_test2) or same_token_in_row(player, y_test2):
        player_has_won = True

    return player_has_won


def same_token_in_row(player, row):
    tokens_in_row = 0

    for y in row:
        if y == player:
            tokens_in_row += 1

    return tokens_in_row == len(row)


def is_board_full(game_turn):
    return game_turn == len(BOARD)**2


def is_legal_move(x_coord, y_coord):
    tic = BOARD[x_coord][y_coord]

    if tic == 'X' or tic == 'O':
        return False

    return True


def random_coordinates(input_board):
    x_coord = random.randint(0, len(input_board)-1)
    y_coord = random.randint(0, len(input_board)-1)

    while not is_legal_move(x_coord, y_coord):
        x_coord = random.randint(0, len(input_board)-1)
        y_coord = random.randint(0, len(input_board)-1)

    return [x_coord, y_coord]


def available_moves(board):
    legal_moves = []
    # find all legal moves
    for x in range(len(board)):
        for y in range(len(board[x])):
            if board[x][y] == '_':
                legal_moves.append([x, y])

    return legal_moves


def minimax_recursion(board, game_turn, path, moves, best_solution):
    solutions = []

    # test each possible move
    for move in moves:

        # make move
        place_token(get_current_player(game_turn), board, int(move[0]), int(move[1]))

        # remember move
        path.append(move)

        remaining_moves = available_moves(board)

        print(path)
        print_board(board)

        #check to see if move wins the game
        if did_win('X', board):
            solutions.append({"score": -10, "turns": game_turn, "path": path})
            board[path[-1][0]][path[-1][1]] = '_'
            path.pop()
            if best_solution[0] >= game_turn:
                best_solution[0] = game_turn

            return solutions

        if did_win('O', board):
            solutions.append({"score": 10, "turns": game_turn, "path": path})
            board[path[-1][0]][path[-1][1]] = '_'
            path.pop()
            if best_solution[0] >= game_turn:
                best_solution[0] = game_turn

            return solutions

        if len(remaining_moves) == 0:
            solutions.append({"score": 0, "turns": game_turn, "path": path})
            board[path[-1][0]][path[-1][1]] = '_'
            path.pop()

            return solutions

        else:
            print(remaining_moves)
            # checks to see if it's a better solution
            if best_solution[0] >= game_turn:
                solutions.extend(minimax_recursion(board, game_turn+1, path, remaining_moves, best_solution))
            board[path[-1][0]][path[-1][1]] = '_'
            path.pop()


    return solutions



# Test this first:
def minimax_coordinates(game_turn, board):

    avail_moves = available_moves(board)
    best_solution = [len(board)**2]
    # find solutions
    solutions = minimax_recursion(board, game_turn, [], avail_moves, best_solution)



    return

# Run the program
game_loop()
