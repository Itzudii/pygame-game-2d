import tmj
import pygame
def get_img_src(name):
        assets = {
            'Terrain (16x16).png':'assets/tileset/',
            # 'apple.png':'tiled/',
            # 'box.png':'tiled/',
            # 'checkpoint.png':'tiled/',
            # 'end.png':'tiled/',
            # 'player.png':'tiled/',
            # 'start.png':'tiled/',
        }
        return assets[name]+name
TILESIZE = 30
class TileDraw():
    def __init__(self,tmj_file):
        self.src = tmj_file
        self.data = tmj.fetch_data(tmj_file)
        self.layers = self.data['layers']
        self.imgs = self.data['tilesets']
        self.tilesize = self.data['tilewidth']

        self.surfaces = dict()

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


    def draw_normal_tile_layer(self,layer,screen):
        w = layer['width']
        tilesize = TILESIZE
        x=0
        y=0
        for gid in layer['data']:
            
            img = self.get_surface(gid)
            if img:
                screen.blit(img,(x,y))
            x+=tilesize
            if x>=w*tilesize:
                x=0
                y+=tilesize

    def draw_layers(self,screen):
        for layer in self.layers:
            if layer['name'] == 'normal':
                self.draw_normal_tile_layer(layer,screen)
        

