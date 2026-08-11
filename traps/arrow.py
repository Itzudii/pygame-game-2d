from traps.dependency.jumping import Jumper
class Arrow(Jumper):
    assets = {
            'hit':(r'assets\Traps\Arrow\Hit (18x18).png',4),
            'idle':(r'assets\Traps\Arrow\Idle (18x18).png',10),
        }

    def update(self):
        super().update()
        if self.animation.isfinished and self.ishit:
            self.kill()