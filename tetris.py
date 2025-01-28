import curses
import random

# Tetris shapes
SHAPES = [
    [['#', '#', '#', '#']],  # I
    [['#', '#'], ['#', '#']],  # O
    [['#', '#', '#'], ['#', ' ']],  # J
    [['#', '#', '#'], [' ', '#']],  # L
    [['#', '#', '#'], [' ', ' ', '#']],  # S
    [['#', '#', ' '], [' ', '#', '#']],  # Z
    [[' ', '#', '#'], ['#', '#', ' ']],  # T
]

class Tetris:
    def __init__(self, window):
        self.window = window
        self.window.nodelay(1)
        self.window.timeout(500)  # Initial speed
        self.board_height = 20  #height
        self.board_width = 14  # width
        self.play_area_height = self.board_height + 2  # border
        self.play_area_width = self.board_width + 2
        self.board = [[' ' for _ in range(self.board_width)] for _ in range(self.board_height)]
        self.current_shape = self.new_shape()
        self.current_pos = [0, 4]
        self.score = 0
        self.win_score = 10  # target score to win

    def new_shape(self):
        return random.choice(SHAPES)

    def draw_board(self):
        self.window.clear()
        
        # Draw border
        for x in range(self.play_area_width):
            self.window.addstr(0, x, '#')
            self.window.addstr(self.play_area_height - 1, x, '#')
        for y in range(1, self.play_area_height - 1):
            self.window.addstr(y, 0, '#')
            self.window.addstr(y, self.play_area_width - 1, '#')

        # Draw current shape
        for i, row in enumerate(self.board):
            self.window.addstr(i + 1, 1, ''.join(row))
        
        for i, row in enumerate(self.current_shape):
            for j, cell in enumerate(row):
                if cell == '#':
                    self.window.addstr(self.current_pos[0] + 1 + i, self.current_pos[1] + 1 + j, cell)

        self.window.addstr(self.play_area_height - 1, 0, f'Score: {self.score}   Target: {self.win_score}')
        self.window.refresh()

    def valid_move(self, shape, offset):
        for i, row in enumerate(shape):
            for j, cell in enumerate(row):
                if cell == '#':
                    x, y = self.current_pos[0] + i + offset[0], self.current_pos[1] + j + offset[1]
                    if x < 0 or x >= self.board_height or y < 0 or y >= self.board_width or (x >= 0 and self.board[x][y] == '#'):
                        return False
        return True

    def merge_shape(self):
        for i, row in enumerate(self.current_shape):
            for j, cell in enumerate(row):
                if cell == '#':
                    self.board[self.current_pos[0] + i][self.current_pos[1] + j] = '#'

    def clear_lines(self):
        cleared = 0
        for i in range(self.board_height):
            if all(cell == '#' for cell in self.board[i]):
                cleared += 1
                self.board.pop(i)
                self.board.insert(0, [' ' for _ in range(self.board_width)])
        self.score += cleared

        # speed based on score
        if self.score % 5 == 0:  # speed @ every 5 points
            new_timeout = max(50, 1000 - self.score * 2)  # speed formula
            self.window.timeout(new_timeout)

    def rotate_shape(self):
        new_shape = [list(row) for row in zip(*self.current_shape[::-1])]
        if self.valid_move(new_shape, (0, 0)):
            self.current_shape = new_shape

    def drop(self):
        if self.valid_move(self.current_shape, (1, 0)):
            self.current_pos[0] += 1
        else:
            self.merge_shape()
            self.clear_lines()
            self.current_shape = self.new_shape()
            self.current_pos = [0, 4]
            if not self.valid_move(self.current_shape, (0, 0)):
                self.window.addstr(10, 0, "Game Over!")
                self.window.refresh()
                self.window.getch()
                return False
        return True

    def play(self):
        while True:
            self.draw_board()
            key = self.window.getch()

            if key == curses.KEY_LEFT:
                if self.valid_move(self.current_shape, (0, -1)):
                    self.current_pos[1] -= 1
            elif key == curses.KEY_RIGHT:
                if self.valid_move(self.current_shape, (0, 1)):
                    self.current_pos[1] += 1
            elif key == curses.KEY_DOWN:
                if not self.drop():
                    break
            elif key == curses.KEY_UP:
                self.rotate_shape()

            if not self.drop():
                break
            
            # Check win condition
            if self.score >= self.win_score:
                self.window.addstr(10, 0, "You Win! Press any key to exit.")
                self.window.refresh()
                self.window.getch()
                break

def main(window):
    tetris = Tetris(window)
    tetris.play()

if __name__ == "__main__":
    curses.wrapper(main)

# to play:   pip install windows-curses