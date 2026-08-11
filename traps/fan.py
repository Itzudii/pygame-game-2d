from traps.dependency.fan import FanObj

class Fan(FanObj):
    assets = {
        'idle':   (r'assets\Traps\Fan\Off.png', 1),
        'active': (r'assets\Traps\Fan\On (24x8).png', 4),
    }