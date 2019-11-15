import os, sys, time
import tty, termios

def clear():
    os.write(sys.stdout.fileno(), b'\x1b[3J\x1b[H\x1b[2J')

class Game:
    def __init__(self, size_x, size_y, refresh):
        self.size_x, self.size_y = size_x, size_y
        self.refresh = 1/refresh

    def __str__(self):
        size_x, size_y = self.size_x, self.size_y
        board = [[' ' for _ in range(size_x+2)] for _ in range(size_y+2)]
        board[0] = ['#'] * (size_x+2)
        board[-1] = ['#'] * (size_x+2)
        for i in range(size_y+2):
            board[i][0] = '#'
            board[i][-1] = '#'
        return '\n'.join(''.join(row) for row in board)

    def run(self, step):
        clear()
        fd = sys.stdin.fileno()
        old = termios.tcgetattr(fd)
        try:
            tty.setcbreak(sys.stdin)
            print(self)
            time.sleep(self.refresh)
            while True:
                clear()
                if not step():
                    return
                print(self)
                time.sleep(self.refresh)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old)
            print('Game Over!\nPress any key to continue...')
