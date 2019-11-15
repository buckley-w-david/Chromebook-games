import asyncio
import queue
import struct
import os
import threading

_KEYS_A_LIST = [
    ("1", 2),
    ("2", 3),
    ("3", 4),
    ("4", 5),
    ("5", 6),
    ("6", 7),
    ("7", 8),
    ("8", 9),
    ("9", 10),
    ("0", 11),
    ("q", 16),
    ("w", 17),
    ("e", 18),
    ("r", 19),
    ("t", 20),
    ("y", 21),
    ("u", 22),
    ("i", 23),
    ("o", 24),
    ("p", 25),
    ("a", 30),
    ("s", 31),
    ("d", 32),
    ("f", 33),
    ("g", 34),
    ("h", 35),
    ("j", 36),
    ("k", 37),
    ("l", 38),
    ("z", 44),
    ("x", 45),
    ("c", 46),
    ("v", 47),
    ("b", 48),
    ("n", 49),
    ("m", 50),
    ("UP", 103),
    ("RIGHT", 106),
    ("DOWN", 108),
    ("LEFT", 105),
    ("SPACE", 57),
]
KEYS = {}
EVENTS = {}
for key, event in _KEYS_A_LIST:
    KEYS[key] = event
    EVENTS[event] = key

def key_to_event(key: str) -> int:
    return KEYS[key]

def event_to_key(event: int) -> str:
    return EVENTS[event]

KEY_DOWN = 0b1
KEY_HOLD = 0b10
KEY_UP   = 0b100

class KeyboardListener:
    def __init__(self, event_file='/dev/input/event0'):
        self.events = queue.Queue()
        self.registered = set()
        self.event_file = event_file

    def register_key(self, key, event_type=0b111):
        key_num = KEYS[key]
        if event_type & KEY_DOWN:
            self.registered.add((key_num, 1))
        if event_type & KEY_HOLD:
            self.registered.add((key_num, 2))
        if event_type & KEY_UP:
            self.registered.add((key_num, 0))

    def _listen_for_keys(self):
        self.event_loop.run_forever()

    def start(self):
        self.fd = open(self.event_file, 'rb', buffering=0)
        self.event_loop = asyncio.get_event_loop()
        def add_to_queue():
            data = os.read(self.fd.fileno(), 16)
            _, key_num, event = struct.unpack('HHI', data[8:])
            if (key_num, event) in self.registered:
                self.events.put((EVENTS[key_num], event))

        self.event_loop.add_reader(self.fd, add_to_queue)
        self.thread = threading.Thread(target=self._listen_for_keys)
        self.thread.start()

    def close(self):
        self.event_loop.stop()
        self.thread.join()
        self.fd.close()

    def __enter__(self):
        self.start()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

if __name__ == '__main__':
    listener = KeyboardListener()
    listener.register_key('q')
    import time
    n = 0
    with listener as l:
        while n < 5:
            print(n)
            event = None
            while not l.events.empty():
                print(l.events.get())
            else:
                print('No keys!')
            time.sleep(1)
            n += 1


