import pygame
from sudoku_generator import *

width, height = 675, 750  # interface design variables, used for color, length, width, etc.
black_color = (0, 0, 0)
gray_color = (128, 128, 128)
white_pearl = (250, 251, 245)
red_color = (255, 0, 0)
white_color = (255, 255, 255)
yellow_color = (255, 255, 0)
emerald = (0, 134, 139)
turquoise = (64, 224, 208)
menu_green = (148, 171, 67)
darker_green = (123, 144, 56)
game_over_green = (88, 104, 38)
aqua_marine = (127, 255, 212)
brown_color = (139, 35, 35)
crimson_color = (220, 20, 60)
maroon = (128, 0, 0)
orange = (255, 97, 3)
dark = (3, 3, 3)
cell_size = 75
line_width1 = 6
line_width2 = 2
rows = 9
cols = 9


class Cell:
    def __init__(self, value, row, col, width, height, sketch_val=None):  # constructor for the cell class
        self.value = value
        self.row = row
        self.col = col
        self.width = width
        self.height = height
        self.sketch_val = sketch_val

    def set_value(self, val):
        self.value = val

    def set_sketch_value(self, val):
        self.sketch_val = val

    def draw(self, screen):  # draws the specified cell with value
        if self.value != 0:    # if sudoku board's box value is not 0 in 2D list, draw value of box
            font = pygame.font.Font(None, 80)
            num_surf = font.render(str(self.value), True, black_color)
            num_rect = num_surf.get_rect(center=(cell_size * self.col + cell_size // 2,
                                                 cell_size * self.row + cell_size // 2))
            screen.blit(num_surf, num_rect)

        if self.sketch_val is not None:    # if sketch value is available, draw the sketch value
            sketch_font = pygame.font.Font(None, 30)
            sketch_surf = sketch_font.render(str(self.sketch_val), True, maroon)
            sketch_rect = sketch_surf.get_rect(center=(cell_size * self.col + cell_size // 5, cell_size * self.row +
                                                       cell_size // 5))
            screen.blit(sketch_surf, sketch_rect)


class Board:
    def __init__(self, rows, cols, width, height, screen, difficulty):
        self.rows = rows
        self.cols = cols
        self.width = width
        self.height = height
        self.screen = screen
        self.difficulty = difficulty
        if self.difficulty == "Easy":    # if game mode selected is easy, self.val is set to 30, take away 30 boxes
            self.val = 1
        elif self.difficulty == 'Medium':       # if game mode selected id hard, self.val set to 40, take away 40 boxes
            self.val = 40
        else:
            self.val = 50    # for hard mode, take away 50 boxes
        self.tupl_board = generate_sudoku(9, self.val)  # creates a tuple, contains the ready board & correct solution
        self.board = copy.deepcopy(self.tupl_board[0])    # sudoku board after randomly taking away values
        self.correct = self.tupl_board[1]    # the sudoku board's initial state before randomly taking away values
        # draws individual boxes contains values for the sudoku board
        self.cell = [[Cell(self.board[i][j], i, j, cell_size, cell_size) for j in range(cols)] for i in range(rows)]

    def draw(self):
        for r in range(2):  # draws the border of the sudoku board
            pygame.draw.line(
                screen,
                black_color,
                (0, r * 9 * cell_size),
                (width, r * 9 * cell_size),
                line_width2
            )

        for b in range(2):
            pygame.draw.line(
                screen,
                black_color,
                (b * 9 * cell_size, 0),
                (b * 9 * cell_size, 9 * cell_size),
                line_width2
            )

        for i in range(1, 4):  # draws the bolded lines (line width 1) to distinguish 3x3 boxes
            pygame.draw.line(
                screen,
                black_color,
                (0, 3 * i * cell_size),
                (width, 3 * i * cell_size),
                line_width1
            )

        for c in range(1, 3):
            pygame.draw.line(
                screen,
                black_color,
                (3 * c * cell_size, 0),
                (3 * c * cell_size, height - cell_size),
                line_width1
            )

        for h in range(1, 9):  # draws thinner lines (line_width2) to create 3x3 boxes
            pygame.draw.line(
                screen,
                black_color,
                (0, h * cell_size),
                (width, h * cell_size),
                line_width2
            )

        for v in range(1, 9):
            pygame.draw.line(
                screen,
                black_color,
                (v * cell_size, 0),
                (v * cell_size, height - cell_size),
                line_width2
            )

        for i in range(self.rows):  # draws the cells containing values
            for j in range(self.cols):
                self.cell[i][j].draw(screen)

    def select(self, row, col):  # draws red border for cell user selects
        pos = pygame.mouse.get_pos()
        if pos[1] <= 9 * cell_size:  # makes sure selections can't be made below the sudoku board
            for i in range(2):
                pygame.draw.line(
                    screen,
                    red_color,
                    ((col + i) * cell_size, row * cell_size),
                    ((col + i) * cell_size, (row + 1) * cell_size),
                    line_width2
                )

            for j in range(2):
                pygame.draw.line(
                    screen,
                    red_color,
                    (col * cell_size, (row + j) * cell_size),
                    ((col + 1) * cell_size, (row + j) * cell_size),
                    line_width2
                )

    def click(self):  # returns the position of the user's click
        click_pos = pygame.mouse.get_pos()
        x, y = click_pos[0] // cell_size, click_pos[1] // cell_size
        if x <= width:
            return y, x
        return None

    def clear(self):  # Clear a specific cell
        cur_board.board[y][x] = 0
        self.cell[y][x] = Cell(self.board[y][x], y, x, cell_size, cell_size)

    def sketch(self, pos):  # sketches the user's input but draws it in maroon color to distinguish
        cor_x, cor_y = pos[1] // cell_size, pos[0] // cell_size
        sketch_value = read_number()
        if sketch_value != 0:
            self.cell[cor_x][cor_y] = Cell(self.board[cor_x][cor_y], cor_x, cor_y, cell_size, cell_size, sketch_value)

    def place_number(self):  # user establishes their choice, this function is called when user enters number
        choice = read_number()
        cur_board.board[y][x] = int(choice)
        self.cell[y][x] = Cell(self.board[y][x], y, x, cell_size, cell_size)

    def reset_to_original(self):   # redraws the sudoku board to its beginning state
        self.board = copy.deepcopy(self.tupl_board[0])
        self.cell = [[Cell(self.board[i][j], i, j, cell_size, cell_size) for j in range(cols)] for i in range(rows)]

    def is_full(self):   # counts if the available boxes become full
        count = 0
        for row in self.board:
            for col in row:
                if col != 0:
                    count += 1
        if count == 81:
            return True
        else:
            return False

    def check_board(self): # checks if current board matches the original board before values are removed
        for n in range(rows):
            for m in range(cols):
                if self.board[n][m] != self.correct[n][m]:
                    return False
        else:
            return True


def menu_options():    # creates an interface for game mode selection
    font_2 = pygame.font.Font(None, 50)
    menu_bg = pygame.image.load("sudokustartscreen.jpg").convert()    # sets background picture for interface
    screen.blit(menu_bg, (-65, 0))
    prompt_text = "Select Game Mode"
    prompt_surf = font_2.render(prompt_text, True, menu_green)
    prompt_rect = prompt_surf.get_rect(center=(width // 3.35, 523))
    screen.blit(prompt_surf, prompt_rect)


class Button():  # inspired by https://www.youtube.com/watch?v=4_9twnEduFA&ab_channel=TechWithTim
    def __init__(self, color, x, y, width, height, text):
        self.color = color
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text

    def draw(self, screen, outline, font_size=45):    # draws the button
        pygame.draw.rect(screen, outline, (self.x - 2, self.y - 2, self.width + 4, self.height + 4), 0)
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height), 0)
        font = pygame.font.Font(None, font_size)
        text = font.render(self.text, True, white_color)
        screen.blit(text, (self.x + (self.width / 2 - text.get_width() / 2), self.y +
                           (self.height / 2 - text.get_height() / 2)))

    def click(self, pos):    # checks if user click is within the box's borders
        if ((pos[0] > self.x) and (pos[0] < self.x + self.width)) and \
                ((pos[1] > self.y) and (pos[1] < self.y + self.height)):
            return True
        return False


def interactive_button(bool):    # buttons can change color depending on mouse motion for game mode selection menu
    if bool is True:
        easy_button.draw(screen, darker_green)
        medium_button.draw(screen, darker_green)
        hard_button.draw(screen, darker_green)


def option_interactive(bol):   # buttons can change color depending on mouse motion for in-game menu
    if bol is True:
        reset_button.draw(screen, darker_green, 40)
        restart_button.draw(screen, darker_green, 40)
        quit_button.draw(screen, darker_green, 40)


def read_number():  # Read the last key that was pressed, if it is a number return it
    choice = 0

    if event.key == pygame.K_1:
        choice = 1
    elif event.key == pygame.K_2:
        choice = 2
    elif event.key == pygame.K_3:
        choice = 3
    elif event.key == pygame.K_4:
        choice = 4
    elif event.key == pygame.K_5:
        choice = 5
    elif event.key == pygame.K_6:
        choice = 6
    elif event.key == pygame.K_7:
        choice = 7
    elif event.key == pygame.K_8:
        choice = 8
    elif event.key == pygame.K_9:
        choice = 9

    return choice


def game_over_screen():  # creates an interface after the sudoku board is completely filled
    font = pygame.font.Font(None, 120)
    new_bg = pygame.image.load("sudokubackgroundblurred.png").convert()
    screen.blit(new_bg, (0, 0))
    if cur_board.check_board():    # if check_board returns true, user won
        over_text = "You Win! :)"
    else:
        over_text = "Game Over :("
    over_surf = font.render(over_text, True, game_over_green)
    over_rect = over_surf.get_rect(center=(width // 2, height // 2))
    screen.blit(over_surf, over_rect)

    res_button = Button(game_over_green, 290, height // 2 + 80, 100, 50, "Restart")
    exit_button = Button(game_over_green, 290, height // 2 + 150, 100, 50, "Exit")
    rst_button = Button(game_over_green, 150, 2000, 80, 50, "Reset")  # Move reset button off the screen
    return res_button, exit_button, rst_button


if __name__ == "__main__":
    pygame.init()    # initializing pygame

    while True:  # Game loop
        pygame.mixer.init()     # background music for game

        pygame.mixer.music.load('elevate.wav')
        pygame.mixer.music.set_volume(0.15)
        pygame.mixer.music.play(-1)

        double_break = False

        screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Sudoku")
        menu_options()
        # initialize the board and buttons for game
        board_easy = Board(rows, cols, width, height, screen, "Easy")
        board_medium = Board(rows, cols, width, height, screen, "Medium")
        board_hard = Board(rows, cols, width, height, screen, "Hard")
        easy_button = Button(menu_green, 50, 570, 75, 65, "Easy")
        medium_button = Button(menu_green, 180, 570, 120, 65, "Medium")
        hard_button = Button(menu_green, 350, 570, 75, 65, "Hard")
        reset_button = Button(menu_green, 150, 690, 80, 50, "Reset")
        restart_button = Button(menu_green, 290, 690, 100, 50, "Restart")
        quit_button = Button(menu_green, 450, 690, 80, 50, "Quit:(")

        game_over = False
        booly, bol = True, False
        game_on = False
        cur_board = None
        selected = False
        mode_sketch = False

        while True:
            if double_break:  # Breaks again if double break intended
                break

            for event in pygame.event.get():
                position = pygame.mouse.get_pos()
                interactive_button(booly)
                option_interactive(bol)
                pygame.display.update()

                if event.type == pygame.QUIT:
                    pygame.quit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_s:  # Toggle between sketch and non-sketch mode by pressing s
                        if mode_sketch is False:
                            mode_sketch = True
                        else:
                            mode_sketch = False

                    if selected:
                        # if user presses backspace or delete on keyboard, the cell value is cleared
                        if event.key == pygame.K_BACKSPACE or event.key == pygame.K_DELETE:
                            cur_board.clear()
                            screen.blit(new_bg, (0, 0))
                            cur_board.draw()

                        elif event.key != pygame.K_s:
                            if mode_sketch:
                                try:
                                    cur_board.sketch(pos)    # places a sketch value on box
                                except:
                                    pass
                            else:
                                cur_board.place_number()    # places number in box

                            screen.blit(new_bg, (0, 0))
                            cur_board.draw()
                            selected = False
                try:
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if game_on:
                            pos = pygame.mouse.get_pos()
                            y, x = cur_board.click()
                            selected = False
                            if (y <= 8) and cur_board.tupl_board[0][y][x] == 0:
                                screen.blit(new_bg, (0, 0))
                                cur_board.draw()
                                cur_board.select(y, x)      # selects the box if user clicks on the box
                                selected = True

                        if easy_button.click(position):  # if user clicks on the easy mode button, initialize easy board
                            bol, booly = True, False
                            easy_button = Button(menu_green, 1, 0, 0, 0, "Easy")
                            medium_button = Button(menu_green, 0, 0, 0, 0, "Medium")
                            hard_button = Button(menu_green, 0, 0, 0, 0, "Hard")
                            new_bg = pygame.image.load("backgroundblurinsert.png").convert()
                            screen.blit(new_bg, (0, 0))
                            board_easy.draw()
                            cur_board = board_easy
                            game_on = True

                        elif medium_button.click(position):   # if user clicks on medium mode button, init medium board
                            booly = False
                            bol = True
                            easy_button = Button(menu_green, 0, 1, 0, 0, "Easy")
                            medium_button = Button(menu_green, 0, 0, 0, 0, "Medium")
                            hard_button = Button(menu_green, 0, 0, 0, 0, "Hard")
                            new_bg = pygame.image.load("backgroundblurinsert.png").convert()
                            screen.blit(new_bg, (0, 0))
                            board_medium.draw()
                            cur_board = board_medium
                            game_on = True

                        elif hard_button.click(position):   # if user clicks on hard mode button, init hard board
                            booly, bol = False, True
                            easy_button = Button(menu_green, 0, 0, 0, 0, "Easy")
                            medium_button = Button(menu_green, 0, 0, 0, 0, "Medium")
                            hard_button = Button(menu_green, 0, 0, 0, 0, "Hard")
                            new_bg = pygame.image.load("backgroundblurinsert.png").convert()
                            screen.blit(new_bg, (0, 0))
                            board_hard.draw()
                            cur_board = board_hard
                            game_on = True

                        if game_on:
                            if restart_button.click(position):  # if restart button is clicked, return user to main menu
                                double_break = True
                                break

                            elif reset_button.click(position):   # if reset button is clicked, reset the board
                                cur_board.reset_to_original()
                                screen.blit(new_bg, (0, 0))
                                cur_board.draw()

                            elif quit_button.click(position):    # if quit button is clicked, exit pygame
                                pygame.quit()
                except:
                    pass

                if event.type == pygame.MOUSEMOTION:    # detects mouse motion to change button color when hovering
                    if easy_button.click(position):
                        easy_button.color = darker_green
                    elif medium_button.click(position):
                        medium_button.color = darker_green
                    elif hard_button.click(position):
                        hard_button.color = darker_green
                    else:
                        easy_button.color, medium_button.color, hard_button.color = menu_green, menu_green, menu_green

                    if reset_button.click(position):
                        reset_button.color = darker_green
                    elif restart_button.click(position):
                        restart_button.color = darker_green
                    elif quit_button.click(position):
                        quit_button.color = darker_green
                    else:
                        reset_button.color, restart_button.color, quit_button.color = menu_green, menu_green, menu_green

                if game_on and cur_board.is_full():   # checks if player has filled the board completely and won
                    pygame.display.update()
                    restart_button, quit_button, reset_button = game_over_screen()
                    if event.type == pygame.MOUSEMOTION: # detects mouse motion for hovering over buttons (color change)
                        if restart_button.click(position):
                            restart_button.color = darker_green
                        elif quit_button.click(position):
                            quit_button.color = darker_green
                        else:
                            restart_button.color, quit_button.color = menu_green, menu_green
