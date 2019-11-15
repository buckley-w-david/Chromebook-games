from collections import deque
from itertools import product
from random import choice
import enum

from game import game
from key_events import keys

class Action(enum.Enum):
    LEFT = enum.auto()
    RIGHT = enum.auto()
    UP = enum.auto()
    DOWN = enum.auto()
    QUIT = enum.auto()

class Snake(game.Game):
    def __init__(self, size_x, size_y):
        super().__init__(size_x, size_y, 8)

        self.body = deque()
        self.body.appendleft((size_x // 2, size_y // 2))
        self.apple = self._gen_apple()
        self.points = 0
        self.delta = (-1, 0)

    def _gen_apple(self):
        size_x, size_y = self.size_x, self.size_y
        board = set(product(range(size_x), range(size_y)))
        for segment in self.body:
            board.remove(segment)

        return choice(list(board))

    def step(self, actions):
        x, y = self.body[0]
        old_tail = self.body.pop() # Remove tail
        # TODO bounds check
        dx, dy = 0, 0
        if Action.QUIT in actions:
            return False
        elif Action.LEFT in actions:
            dx = -1
        elif Action.RIGHT in actions:
            dx = 1
        elif Action.UP in actions:
            dy = -1
        elif Action.DOWN in actions:
            dy = 1
        else:
            dx, dy = self.delta
        self.delta = (dx, dy)

        new_head = (x+dx, y+dy)
        # Could condense this, but it feels more readable as is
        if new_head in self.body:
            return False
        elif new_head[0] < 0 or new_head[0] >= self.size_x:
            return False
        elif new_head[1] < 0 or new_head[1] >= self.size_y:
            return False

        self.body.appendleft(new_head)
        if new_head == self.apple:
            self.points += 1
            self.body.append(old_tail)
            self.apple = self._gen_apple()
        return True

    def __str__(self):
        board = [[' ' for _ in range(self.size_x+2)] for _ in range(self.size_y+2)]
        board[0] = ['#' for _ in range(self.size_x+2)]
        board[-1] = ['#' for _ in range(self.size_x+2)]

        for j in range(1, self.size_y+2):
                board[j][0] = '#'
                board[j][-1] = '#'

        for x, y in self.body:
            board[y+1][x+1] = '*'
        x, y = self.apple
        board[y+1][x+1] = '@'
        return '\n'.join([''.join(row) for row in board])

if __name__ == '__main__':
    listener = keys.KeyboardListener()
    listener.register_key('LEFT', keys.KEY_DOWN)
    listener.register_key('RIGHT', keys.KEY_DOWN)
    listener.register_key('UP', keys.KEY_DOWN)
    listener.register_key('DOWN', keys.KEY_DOWN)
    listener.register_key('q', keys.KEY_DOWN)

    snek = Snake(20, 10)
    def _step():
        events = []
        while not listener.events.empty():
            events.append(listener.events.get()[0])

        actions = []
        for event in events:
            if event == 'LEFT':
                actions.append(Action.LEFT)
            if event == 'RIGHT':
                actions.append(Action.RIGHT)
            if event == 'UP':
                actions.append(Action.UP)
            if event == 'DOWN':
                actions.append(Action.DOWN)
            if event == 'q':
                actions.append(Action.QUIT)
        return snek.step(actions)

    with listener:
        snek.run(_step)
