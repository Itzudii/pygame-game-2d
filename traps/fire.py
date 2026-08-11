from traps.dependency.fire import FireObj

class Fire(FireObj):
    assets = {
            'idle':(r'assets\Traps\Fire\Off.png',1),
            'active':(r'assets\Traps\Fire\On (16x32).png',3),
            'hit':(r'assets\Traps\Fire\Hit (16x32).png',4),
        }
    