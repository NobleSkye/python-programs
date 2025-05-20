import os

def clear():
    os.system('clear' if os.name == 'posix' else 'cls')

def tictactoe():
    board = [' ' for _ in range(9)]
    
    def print_board():
        clear()
        print('Current board:')
        print(f' {board[0]} | {board[1]} | {board[2]} ')
        print('-----------')
        print(f' {board[3]} | {board[4]} | {board[5]} ')
        print('-----------')
        print(f' {board[6]} | {board[7]} | {board[8]} ')

    def is_winner(brd, player):
        # Check rows, columns and diagonals
        win_combinations = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8],  # Rows
            [0, 3, 6], [1, 4, 7], [2, 5, 8],  # Columns
            [0, 4, 8], [2, 4, 6]  # Diagonals
        ]
        return any(all(brd[i] == player for i in combo) for combo in win_combinations)

    def is_board_full():
        return ' ' not in board

    def get_player_move():
        while True:
            try:
                move = int(input('Enter your move (1-9): ')) - 1
                if 0 <= move <= 8 and board[move] == ' ':
                    return move
                print('Invalid move. Try again.')
            except ValueError:
                print('Please enter a number between 1 and 9.')

    def get_computer_move():
        # First check if computer can win
        for i in range(9):
            if board[i] == ' ':
                board[i] = 'O'
                if is_winner(board, 'O'):
                    return i
                board[i] = ' '

        # Then check if player can win and block
        for i in range(9):
            if board[i] == ' ':
                board[i] = 'X'
                if is_winner(board, 'X'):
                    board[i] = ' '
                    return i
                board[i] = ' '

        # Choose center if available
        if board[4] == ' ':
            return 4

        # Choose corners
        corners = [0, 2, 6, 8]
        available_corners = [i for i in corners if board[i] == ' ']
        if available_corners:
            return available_corners[0]

        # Choose any available edge
        edges = [1, 3, 5, 7]
        available_edges = [i for i in edges if board[i] == ' ']
        if available_edges:
            return available_edges[0]

    print("Welcome to Tic-tac-toe!")
    print("You are X, computer is O")
    print("Positions are numbered from 1-9 starting from top left:")
    print(" 1 | 2 | 3 ")
    print("-----------")
    print(" 4 | 5 | 6 ")
    print("-----------")
    print(" 7 | 8 | 9 ")
    input("Press Enter to start...")

    while True:
        # Player's turn
        print_board()
        move = get_player_move()
        board[move] = 'X'

        if is_winner(board, 'X'):
            print_board()
            print('Congratulations! You win!')
            break

        if is_board_full():
            print_board()
            print("It's a tie!")
            break

        # Computer's turn
        move = get_computer_move()
        board[move] = 'O'

        if is_winner(board, 'O'):
            print_board()
            print('Computer wins!')
            break

        if is_board_full():
            print_board()
            print("It's a tie!")
            break

if __name__ == "__main__":
    tictactoe()
