import os, sys
import enum
import time

from key_events import keys
import game.game as game

class Action(enum.Enum):
    LEFT = enum.auto()
    RIGHT = enum.auto()
    SHOOT = enum.auto()
    QUIT = enum.auto()

class Invaders(game.Game):
    def __init__(self, size_x, size_y):
        super().__init__(size_x, size_y, refresh=6)

        self.aliens = self._gen_aliens()
        self.alien_shots = set()

        self.tank = size_x // 2, size_y-1
        self.tank_shots = set()

        self.barriers = self._gen_barriers()

    def _gen_aliens(self):
        return {(self.size_x // 2, 0)}

    def _gen_barriers(self):
        return {(self.size_x // 2, self.size_y-2)}

    def _update_shots(self):
        new_shots = set()
        while self.alien_shots:
            shot_x, shot_y = self.alien_shots.pop()
            shot_y += 1
            new_shot = shot_x, shot_y
            if new_shot == self.tank:
                return False
            if 0 <= shot_x < self.size_x and 0 <= shot_y < self.size_y:
                new_shots.add(new_shot)
        self.alien_shots = new_shots

        new_shots = set()
        while self.tank_shots:
            shot_x, shot_y = self.tank_shots.pop()
            shot_y -= 1
            new_shot = shot_x, shot_y
            if new_shot in self.aliens:
                self.aliens.discard(new_shot)
            elif new_shot in self.barriers:
                self.barriers.discard(new_shot)
            elif 0 <= shot_x < self.size_x and 0 <= shot_y < self.size_y:
                new_shots.add(new_shot)
        self.tank_shots = new_shots
        return True

    def _update_aliens(self):
        return True

    def _shoot(self):
        self.tank_shots.add(self.tank)

    def step(self, actions):
        dx = 0
        if Action.LEFT in actions:
            dx = -1
        if Action.RIGHT in actions:
            dx = 1
        if Action.SHOOT in actions:
            self._shoot()

        x, y = self.tank
        self.tank = x+dx, y

        r = self._update_shots()
        r2 = self._update_aliens()
        return r2 and r and Action.QUIT not in actions

    def __str__(self):
        board = [[' ' for _ in range(self.size_x+2)] for _ in range(self.size_y+2)]
        board[0] = ['#' for _ in range(self.size_x+2)]
        board[-1] = ['#' for _ in range(self.size_x+2)]

        for j in range(1, self.size_y+2):
                board[j][0] = '#'
                board[j][-1] = '#'

        for x, y in self.aliens:
            board[y+1][x+1] = 'v'
        for x, y in self.barriers:
            board[y+1][x+1] = '-'
        for x, y in self.tank_shots.union(self.alien_shots):
            board[y+1][x+1] = '|'

        x, y = self.tank
        board[y+1][x+1] = '^'
        return '\n'.join([''.join(row) for row in board])


if __name__ == '__main__':
    listener = keys.KeyboardListener()
    listener.register_key('LEFT', keys.KEY_DOWN)
    listener.register_key('RIGHT', keys.KEY_DOWN)
    listener.register_key('SPACE', keys.KEY_DOWN)
    listener.register_key('q', keys.KEY_DOWN)

    invaders = Invaders(20, 10)
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
            if event == 'SPACE':
                actions.append(Action.SHOOT)
            if event == 'q':
                actions.append(Action.QUIT)
        return invaders.step(actions)

    with listener:
        invaders.run(_step)
