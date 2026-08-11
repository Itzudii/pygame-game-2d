from traps.dependency.moving import MovingObject

class GrayP(MovingObject):
    assets = {
            'idle':(r'assets\Traps\Platforms\Grey Off.png',1),
            'active':(r'assets\Traps\Platforms\Grey On (32x8).png',8),
        }
    chain_src = r'assets/Traps/Platforms/Chain.png'
