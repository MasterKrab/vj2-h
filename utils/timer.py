from time import time


class Timer:
    def __init__(self):
        self.start = None
        self.is_paused = False

    def start_timer(self):
        self.start = time()

    def pause(self):
        if self.is_paused:
            return

        self.is_paused = True
        self.start_pause = time()

    def resume(self):
        if not self.is_paused:
            return

        self.is_paused = False
        self.start += time() - self.start_pause

    @property
    def current(self):
        if self.is_paused:
            return self.start_pause - self.start

        return time() - self.start


timer = Timer()
