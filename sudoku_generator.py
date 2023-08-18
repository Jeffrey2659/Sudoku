import math
import random
import copy


class SudokuGenerator:
    def __init__(self, row_length, removed_cells):   # constructor for Sudoku Generator class
        self.row_length = row_length
        self.removed_cells = removed_cells
        self.box_length = int(math.sqrt(row_length))   # setting box_length to square root of row_length without decimal
        self.board = [["0" for i in range(self.row_length)] for j in range(self.row_length)]  # 2D list

    def get_board(self):   # returns the 2D list
        return self.board

    def print_board(self):    # prints out the sudoku board
        for row in self.board:
            for col in row:
                print(col, end=" ")
            print()

    def valid_in_row(self, row, num):    # checks if num is in the indexed sublist within the 2D list
        if num in self.board[row]:
            return False   # if in, return False
        return True

    def valid_in_col(self, col, num):    # checks if num is in the vertical column of the same index in the list
        for row in self.board:
            if row[col] == num:
                return False    # if in, return False
        return True

    def valid_in_box(self, row_start, col_start, num):    # checks the number of repeats in a 3x3 box
        for i in range(row_start, row_start + 3):
            for j in range(col_start, col_start + 3):
                if num == self.board[i][j]:
                    return False
        return True

    def is_valid(self, row, col, num):    # checks if a number is valid within the rules of sudoku overall
        if row <= 2:
            row_start_index = 0
        elif row <= 5:
            row_start_index = 3
        else:
            row_start_index = 6

        if col <= 2:
            col_start_index = 0
        elif col <= 5:
            col_start_index = 3
        else:
            col_start_index = 6

        if self.valid_in_col(col, num) and self.valid_in_row(row, num) and \
                self.valid_in_box(row_start_index, col_start_index, num) is True:    # if all conditions meet
            return True    # input value is valid
        return False

    def fill_box(self, row_start, col_start):   # fill a 3x3 box without repeated number
        num_list = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        for i in range(row_start, row_start + 3):
            for j in range(col_start, col_start + 3):
                if self.board[i][j] == "0":
                    self.board[i][j] = int(random.choice(num_list))    # random module, choose number in num_list
                    if self.board[i][j] in num_list:
                        num_list.remove(int(self.board[i][j]))    # if number chosen before, remove number from num_list

    def fill_diagonal(self):    # fills the board diagonally from left to right
        self.fill_box(0, 0)
        self.fill_box(3, 3)
        self.fill_box(6, 6)

    def fill_remaining(self, row, col):    # provided to fill the rest of the board
        if col >= self.row_length and row < self.row_length - 1:
            row += 1
            col = 0
        if row >= self.row_length and col >= self.row_length:
            return True
        if row < self.box_length:
            if col < self.box_length:
                col = self.box_length
        elif row < self.row_length - self.box_length:
            if col == int(row // self.box_length * self.box_length):
                col += self.box_length
        else:
            if col == self.row_length - self.box_length:
                row += 1
                col = 0
                if row >= self.row_length:
                    return True

        for num in range(1, self.row_length + 1):    # provides a range of num from 1-9
            if self.is_valid(row, col, num):    # if number 1-9 is valid within rules of Sudoku, change value to number
                self.board[row][col] = num
                if self.fill_remaining(row, col + 1):
                    return True
                self.board[row][col] = 0
        return False

    def fill_values(self):    # fill the whole board
        self.fill_diagonal()
        self.fill_remaining(0, self.box_length)

    def remove_cells(self):
        num = 0
        while num < self.removed_cells:    # while num is less than the removed cells value, keep looping
            index_1, index_2 = random.randint(0, 8), random.randint(0, 8)    # random value selected for indexing
            if self.board[index_1][index_2] != 0:  # if element in sublist not = 0, change the element value to 0
                self.board[index_1][index_2] = 0
                num += 1    # increment by 1

def generate_sudoku(size, removed):    # generates the board for sudoku game
    sudoku = SudokuGenerator(size, removed)
    sudoku.fill_values()
    correct = copy.deepcopy(sudoku.get_board())
    sudoku.remove_cells()
    board = sudoku.get_board()
    return (board, correct)
