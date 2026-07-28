import tmj.utils as utils
import pygame
from constant import TILESIZE
def get_img_src(name):
        assets = {
            'Terrain (16x16).png':'assets\Terrain\Terrain (16x16).png',
            # 'apple.png':'tiled/',
            # 'box.png':'tiled/',
            # 'checkpoint.png':'tiled/',
            # 'end.png':'tiled/',
            # 'player.png':'tiled/',
            # 'start.png':'tiled/',
        }
        return assets[name]
# TILESIZE = 30

# class Rect(pygame.Rect):
#     def __int__(self,*args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.surface = None

class TileDraw():
    def __init__(self,tmj_file):
        self.src = tmj_file
        self.data = utils.fetch_data(tmj_file)
        self.layers = self.data['layers']
        self.imgs = self.data['tilesets']
        self.tilesize = self.data['tilewidth']

        self.surfaces = dict()
        self.normal_tiles = []
        self.collision_tiles = []

        self.load_tiles()

    @property
    def window_width(self):
        return self.data['width']*TILESIZE
    
    @property
    def window_height(self):
        return self.data['height']*TILESIZE

    def load_surface(self,name):
        surface = self.surfaces.get(name)    
        if surface:
            return surface
        else:
            src = get_img_src(name)
            surface = pygame.image.load(src)

            self.surfaces[name] = surface
            return surface

    def get_surface(self,gid):
        for img in self.imgs:
            if 'firstgid' in img:
                fg = img.get('firstgid')
                lg = img.get('lastgid')
                if fg<=gid<lg:
                    surface = self.load_surface(img['source'])
                    tw =self.tilesize
                    w = surface.get_width()//tw
                    s = surface.subsurface(pygame.Rect(((gid-fg)%w)*tw,((gid-fg)//w)*tw,tw,tw))
                    return pygame.transform.scale(s,(TILESIZE,TILESIZE))
            else:
                _gid = img.get('gid')
                if gid == _gid:
                    return self.load_surface(img['source'])
        return None


    def load_normal_tiles(self,layer):
        w = layer['width']
        tilesize = TILESIZE
        for idx,gid in enumerate(layer['data']):
            img = self.get_surface(gid)
            if img:
                self.normal_tiles.append((img,((idx%w)*tilesize,(idx//w)*tilesize)))

    def load_collision_tiles(self,layer):
        w = layer['width']
        tilesize = TILESIZE
        for idx,gid in enumerate(layer['data']):
            img = self.get_surface(gid)
            if img:
                self.collision_tiles.append((img,((idx%w)*tilesize,(idx//w)*tilesize)))
        
    def load_tiles(self):
        for layer in self.layers:
            name = layer['name']
            if name == 'normal':
                self.load_normal_tiles(layer)
            elif name == 'collision':
                self.load_collision_tiles(layer)

    def draw_layers(self,screen):
        for img,pos in self.normal_tiles:
            screen.blit(img,pos)

        for img,pos in self.collision_tiles:
            screen.blit(img,pos)

