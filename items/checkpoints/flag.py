from items.checkpoints.baseclass import Checkpoint

class Flag(Checkpoint):
    assets = {
        'idle':(r'assets\Items\Checkpoints\Checkpoint\Checkpoint (No Flag).png',1),
        'move':(r'assets\Items\Checkpoints\Checkpoint\Checkpoint (Flag Out) (64x64).png',26),
        'active':(r'assets\Items\Checkpoints\Checkpoint\Checkpoint (Flag Idle)(64x64).png',10)
    } 

    def update(self):
        if self.animation.isfinished and self.ishit:
            self.animation.set_state('active')
        self.animation.update()
        