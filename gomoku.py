def is_empty(board):
    for y in range(len(board)):
        for x in range(len(board)):
            if board[y][x] != " ":
                return False

    return True


def is_bounded(board, y_end, x_end, length, d_y, d_x):
    #Square next to end of sequence
    y1 = y_end + d_y
    x1 = x_end + d_x

    #Square next to start of sequence
    y2 = y_end - length*d_y
    x2 = x_end - length*d_x

    #Check if square next to end of sequence is outside the board
    if (x1 not in range(len(board))) or (y1 not in range(len(board))):
        if (x2 not in range(len(board))) or (y2 not in range(len(board))):
            return "CLOSED"

        elif board[y2][x2] == " ":
            return "SEMIOPEN"

        elif board[y2][x2] != board[y_end][x_end]:
            return "CLOSED"

    #Check if square next to start of sequence is outside the board
    elif (x2 not in range(len(board))) or (y2 not in range(len(board))):
        if board[y1][x1] == " ":
            return "SEMIOPEN"

        elif board[y1][x1] != board[y_end][x_end]:
            return "CLOSED"

    #Check remaining scenarios
    elif board[y1][x1] == " " and board[y2][x2] == " ":
        return "OPEN"

    elif board[y1][x1] == " " or board[y2][x2] == " ":
        return "SEMIOPEN"

    else:
        return "CLOSED"


def detect_row(board, col, y_start, x_start, length, d_y, d_x):
    open_seq_count = 0
    semi_open_seq_count = 0
    counter = 0
    while (y_start in range(len(board))) and (x_start in range(len(board))):
        if board[y_start][x_start] == col:
            counter += 1
            if (y_start not in range(len(board))) or (x_start not in range(len(board))):
                if counter == length:
                    if is_bounded(board, y_start, x_start, length, d_y, d_x) == "OPEN":
                        open_seq_count += 1

                    elif is_bounded(board, y_start, x_start, length, d_y, d_x) == "SEMIOPEN":
                            semi_open_seq_count += 1

                counter = 0



        elif board[y_start][x_start] != col:
            if counter == length:
                if is_bounded(board, y_start - d_y, x_start - d_x, length, d_y, d_x) == "OPEN":
                    open_seq_count += 1

                elif is_bounded(board, y_start - d_y, x_start - d_x, length, d_y, d_x) == "SEMIOPEN":
                        semi_open_seq_count += 1

            counter = 0


        y_start += d_y
        x_start += d_x

    if y_start == len(board) or x_start == len(board):
        if counter == length:
            if is_bounded(board, y_start - d_y, x_start - d_x, length, d_y, d_x) == "OPEN":
                open_seq_count += 1

            elif is_bounded(board, y_start - d_y, x_start - d_x, length, d_y, d_x) == "SEMIOPEN":
                semi_open_seq_count += 1


    return open_seq_count, semi_open_seq_count





def detect_rows(board, col, length):
    open_seq_count, semi_open_seq_count = 0, 0
    #Count all rows
    for rows in range(len(board)):
        open_seq_count += detect_row(board, col, rows, 0, length, 0, 1)[0]
        semi_open_seq_count += detect_row(board, col, rows, 0, length, 0, 1)[1]

    #Count all columns
    for columns in range(len(board)):
        open_seq_count += detect_row(board, col, 0, columns, length, 1, 0)[0]
        semi_open_seq_count += detect_row(board, col, 0, columns, length, 1, 0)[1]

    #Count all diagonals with direction vectors(1, 1)
    for i in range(len(board) - length + 1):
        open_seq_count += detect_row(board, col, 0, i, length, 1, 1)[0]
        semi_open_seq_count += detect_row(board, col, 0, i, length, 1, 1)[1]

    for j in range(1, len(board) - length + 1):
        open_seq_count += detect_row(board, col, j, 0, length, 1, 1)[0]
        semi_open_seq_count += detect_row(board, col, j, 0, length, 1, 1)[1]

    #Count all diagonals with direction vectors(1, -1)
    for k in range(len(board) - 1, length - 2, -1):
        open_seq_count += detect_row(board, col, 0, k, length, 1, -1)[0]
        semi_open_seq_count += detect_row(board, col, 0, k, length, 1, -1)[1]

    for l in range(1, len(board) - length + 1):
        open_seq_count += detect_row(board, col, l, 7, length, 1, -1)[0]
        semi_open_seq_count += detect_row(board, col, l, 7, length, 1, -1)[1]

    return open_seq_count, semi_open_seq_count


def search_max(board):
    move_y = 0
    move_x = 0
    max_score = None
    for y in range(len(board)):
        for x in range(len(board)):
            if board[y][x] == " ":
                board[y][x] = "b"
                if max_score == None:
                    max_score = score(board)
                    move_y = y
                    move_x = x

                elif score(board) >= max_score:
                    max_score = score(board)
                    move_y = y
                    move_x = x


                board[y][x] = " "



    return move_y, move_x

def score(board):
    MAX_SCORE = 100000

    open_b = {}
    semi_open_b = {}
    open_w = {}
    semi_open_w = {}

    for i in range(2, 6):
        open_b[i], semi_open_b[i] = detect_rows(board, "b", i)
        open_w[i], semi_open_w[i] = detect_rows(board, "w", i)


    if open_b[5] >= 1 or semi_open_b[5] >= 1:
    #if is_win(board) == "Black won":
        return MAX_SCORE

    elif open_w[5] >= 1 or semi_open_w[5] >= 1:
    #if is_win(board) == "White won":
        return -MAX_SCORE

    return (-10000 * (open_w[4] + semi_open_w[4])+
            500  * open_b[4]                     +
            50   * semi_open_b[4]                +
            -100  * open_w[3]                    +
            -30   * semi_open_w[3]               +
            50   * open_b[3]                     +
            10   * semi_open_b[3]                +
            open_b[2] + semi_open_b[2] - open_w[2] - semi_open_w[2])


def is_win_rows(board, row):
    counter = 1
    for i in range(1, len(board[row])):
        if board[row][i] == board[row][i - 1] and board[row][i] != " ":
            counter += 1

        else:
            counter = 1

        if counter == 5:
            return board[row][i]

    return -1

def is_win_columns(board, column):
    counter = 1
    for i in range(1, len(board)):
        if board[i][column] == board[i - 1][column] and board[i][column] != " ":
            counter += 1

        else:
            counter = 1

        if counter == 5:
            return board[i][column]

    return -1

def is_win_diagonals(board, start_y, start_x, d_y, d_x):
    y = start_y
    x = start_x
    start_y += d_y
    start_x += d_x
    counter = 1

    while start_y in range(len(board)) and start_x in range(len(board)):
        if board[start_y][start_x] == board[y][x] and board[start_y][start_x] != " ":
            counter += 1

        else:
            counter = 1

        if counter == 5:
            return board[start_y][start_x]

        y = start_y
        x = start_x
        start_y += d_y
        start_x += d_x

    return -1


def is_win(board):
    #check rows for winning sequence
    for rows in range(len(board)):
        if is_win_rows(board, rows) != -1:
            if is_win_rows(board, rows) == "w":
                return "White won"

            else:
                return "Black won"

    #check column for winning sequence
    for columns in range(len(board)):
        if is_win_columns(board, columns) != -1:
            if is_win_columns(board, columns) == "w":
                return "White won"

            else:
                return "Black won"


    #Check (1, 1) diagonals for winning sequence
    for diagonals1 in range(len(board) - 4):
        if is_win_diagonals(board, diagonals1, 0, 1, 1) != -1:
            if is_win_diagonals(board, diagonals1, 0, 1, 1) == "w":
                return "White won"

            else:
                return "Black won"

    for diagonals2 in range(len(board) - 4):
        if is_win_diagonals(board, 0, diagonals2, 1, 1) != -1:
            if is_win_diagonals(board, 0, diagonals2, 1, 1) == "w":
                return "White won"

            else:
                return "Black won"

    #Check (1, -1) diagonals for winning sequence
    for diagonals3 in range(len(board) - 4):
        if is_win_diagonals(board, diagonals3, 0, 1, -1) != -1:
            if is_win_diagonals(board, diagonals3, 0, 1, -1) == "w":
                return "White won"

            else:
                return "Black won"


    for diagonals4 in range(4, len(board)):
        if is_win_diagonals(board, 0, diagonals4, 1, -1) != -1:
            if is_win_diagonals(board, 0, diagonals4, 1, -1) == "w":
                return "White won"

            else:
                return "Black won"

    #Check for draw
    for i in range(len(board)):
        for j in range(len(board)):
            if board[i][j] == " ":
                return "Continue playing"

    return "Draw"

def print_board(board):

    s = "*"
    for i in range(len(board[0])-1):
        s += str(i%10) + "|"
    s += str((len(board[0])-1)%10)
    s += "*\n"

    for i in range(len(board)):
        s += str(i%10)
        for j in range(len(board[0])-1):
            s += str(board[i][j]) + "|"
        s += str(board[i][len(board[0])-1])

        s += "*\n"
    s += (len(board[0])*2 + 1)*"*"

    print(s)


def make_empty_board(sz):
    board = []
    for i in range(sz):
        board.append([" "]*sz)
    return board



def analysis(board):
    for c, full_name in [["b", "Black"], ["w", "White"]]:
        print("%s stones" % (full_name))
        for i in range(2, 6):
            open, semi_open = detect_rows(board, c, i);
            print("Open rows of length %d: %d" % (i, open))
            print("Semi-open rows of length %d: %d" % (i, semi_open))






def play_gomoku(board_size):
    board = make_empty_board(board_size)
    board_height = len(board)
    board_width = len(board[0])

    while True:
        print_board(board)
        if is_empty(board):
            move_y = board_height // 2
            move_x = board_width // 2
        else:
            move_y, move_x = search_max(board)

        print("Computer move: (%d, %d)" % (move_y, move_x))
        board[move_y][move_x] = "b"
        print_board(board)
       # analysis(board)

        game_res = is_win(board)
        if game_res in ["White won", "Black won", "Draw"]:
            return game_res






        print("Your move:")
        move_y = int(input("y coord: "))
        move_x = int(input("x coord: "))
        board[move_y][move_x] = "w"
        print_board(board)
        #analysis(board)

        game_res = is_win(board)
        if game_res in ["White won", "Black won", "Draw"]:
            return game_res



def put_seq_on_board(board, y, x, d_y, d_x, length, col):
    for i in range(length):
        board[y][x] = col
        y += d_y
        x += d_x

if __name__ == '__main__':
	size = int(input("Size of the game board: "))
print(play_gomoku(size))
