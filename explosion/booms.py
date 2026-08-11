# https://craftpix.net/freebies/11-free-pixel-art-explosion-sprites/
from explosion.explosion import Explosion, Wave

class BOOM1(Explosion):
    'Circle explosion'
    LST = [f'./assets/explosion/PNG/Circle_explosion/Circle_explosion{i}.png' for i in range(1,11)]
    def __init__(self,x,y):
        super().__init__(BOOM1.LST,x,y)

class BOOM2(Explosion):
    'land explosion'
    LST = [f'./assets/explosion/PNG/Explosion/Explosion{i}.png' for i in range(1,11)]
    def __init__(self,x,y):
        super().__init__(BOOM2.LST,x,y-30)

class BOOM3(Explosion):
    'Explosion_blue_circle'
    LST = [f'./assets/explosion/PNG/Explosion_blue_circle/Explosion_blue_circle{i}.png' for i in range(1,11)]
    def __init__(self,x,y):
        super().__init__(BOOM3.LST,x,y)

class BOOM4(Explosion):
    'Explosion_blue_oval'
    LST = [f'./assets/explosion/PNG/Explosion_blue_oval/Explosion_blue_oval{i}.png' for i in range(1,11)]
    def __init__(self,x,y):
        super().__init__(BOOM4.LST,x,y)

class BOOM5(Explosion):
    'Explosion_gas'
    LST = [f'./assets/explosion/PNG/Explosion_gas/Explosion_gas{i}.png' for i in range(1,11)]
    def __init__(self,x,y):
        super().__init__(BOOM5.LST,x,y-30)

class BOOM6(Explosion):
    'Explosion_gas_circle'
    LST = [f'./assets/explosion/PNG/Explosion_gas_circle/Explosion_gas_circle{i}.png' for i in range(1,11)]
    def __init__(self,x,y):
        super().__init__(BOOM6.LST,x,y)

class BOOM7(Explosion):
    'Explosion_two_colors'
    LST = [f'./assets/explosion/PNG/Explosion_two_colors/Explosion_two_colors{i}.png' for i in range(1,11)]
    def __init__(self,x,y):
        super().__init__(BOOM7.LST,x,y-30)

class BOOM8(Explosion):
    'Nuclear_explosion'
    LST = [f'./assets/explosion/PNG/Nuclear_explosion/Nuclear_explosion{i}.png' for i in range(1,11)]
    def __init__(self,x,y):
        super().__init__(BOOM8.LST,x,y-30)

class Fire(Wave):
    'Nuclear_explosion'
    LST = [f'./assets/explosion/PNG/Fire/Fire{i}.png' for i in range(1,7)]
    def __init__(self,x,y):
        super().__init__(Fire.LST,x,y-30)

class Smoke(Wave):
    'Nuclear_explosion'
    LST = [f'./assets/explosion/PNG/Smoke/Smoke{i}.png' for i in range(1,7)]
    def __init__(self,x,y):
        super().__init__(Smoke.LST,x,y-30)