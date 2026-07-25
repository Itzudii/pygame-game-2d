class Animation:
    def __init__(self, frames, dt=1, loop=True):
        self.frames = frames
        self.loop = loop
        self.idx = 0
        self.dt = dt
        self.timer = 0

    def update(self):
        self.timer += self.dt
        self.idx = round(self.timer)

        if self.idx >= len(self.frames):
            if self.loop:
                self.idx = 0
                self.timer = 0
            else:
                self.idx = len(self.frames) - 1

    def end(self):
        self.loop = False

    @property
    def index(self):
        return self.idx
    
    @property
    def image(self):
        return self.frames[self.idx]

    @property
    def finished(self):
        return not self.loop and self.idx == len(self.frames) - 1