from traps.dependency.moving import MovingObject

class Saw(MovingObject):
    assets = {
            'idle':(r'assets\Traps\Saw\Off.png',1),
            'active':(r'assets\Traps\Saw\On (38x38).png',8),
        }
    chain_src = r'assets\Traps\Saw\Chain.png'