from traps.dependency.moving import MovingObject

class BrownP(MovingObject):
    assets = {
            'idle':(r'assets\Traps\Platforms\Brown Off.png',1),
            'active':(r'assets\Traps\Platforms\Brown On (32x8).png',8),
        }
    chain_src = r'assets/Traps/Platforms/Chain.png'
