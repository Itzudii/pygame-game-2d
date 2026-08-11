from pytmx_mapper.utils import get_transform_images
from baseclass.intractive import IntractiveObject

class Fruit(IntractiveObject):

    def __init__(self,data):
        super().__init__(data)
        self.animation.add('collect',{1:get_transform_images(r'assets\Items\Fruits\Collected.png',6,data.size,data.transform)})
        self.ishit = False

    def update(self):
        if self.animation.isfinished and self.ishit:
            self.kill()
        self.animation.update()

    def hit(self):
        self.animation.set_state('collect')
        self.ishit = True

    def __type__(self):
        return Fruit

class Apple(Fruit):
    assets = {'idle':(r'assets\Items\Fruits\Apple.png',17)} 

class Bananas(Fruit):
    assets = {'idle':(r'assets\Items\Fruits\Bananas.png',17)} 

class Cherries(Fruit):
    assets = {'idle':(r'assets\Items\Fruits\Cherries.png',17)} 

class Kiwi(Fruit):
    assets = {'idle':(r'assets\Items\Fruits\Kiwi.png',17)} 

class Melon(Fruit):
    assets = {'idle':(r'assets\Items\Fruits\Melon.png',17)} 

class Orange(Fruit):
    assets = {'idle':(r'assets\Items\Fruits\Orange.png',17)} 

class Pineapple(Fruit):
    assets = {'idle':(r'assets\Items\Fruits\Pineapple.png',17)} 

class Strawberry(Fruit):
    assets = {'idle':(r'assets\Items\Fruits\Strawberry.png',17)} 


        