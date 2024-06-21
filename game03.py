def print_board(board):
    for row in board:
        print(" | ".join(row))
        print("-" * 9)


def check_winner(board, player):
    # Check rows
    for row in board:
        if all(cell == player for cell in row):
            return True

    # Check columns
    for col in range(3):
        if all(board[row][col] == player for row in range(3)):
            return True

    # Check diagonals
    if all(board[i][i] == player for i in range(3)) or all(board[i][2 - i] == player for i in range(3)):
        return True

    return False


def tic_tac_toe():
    board = [[" " for _ in range(3)] for _ in range(3)]
    players = ["X", "O"]
    current_player = 0

    print("Welcome to Tic Tac Toe!")
    print_board(board)

    for _ in range(9):
        row = int(input("Player {} - Enter row (1-3): ".format(players[current_player])))
        col = int(input("Player {} - Enter column (1-3): ".format(players[current_player])))

        if board[row - 1][col - 1] == " ":
            board[row - 1][col - 1] = players[current_player]
            print_board(board)

            if check_winner(board, players[current_player]):
                print("Player {} wins!".format(players[current_player]))
                return

            current_player = 1 - current_player
        else:
            print("That cell is already taken. Try again.")

    print("It's a tie!")


if __name__ == "__main__":
    tic_tac_toe()
