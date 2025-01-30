import displayio
import math
import random

class Mushroom():
    def __init__(self, x, y):
        self.sheet = displayio.OnDiskBitmap("assets/mushroom.bmp")
        self.sprite = displayio.TileGrid(
            self.sheet, 
            pixel_shader=self.sheet.pixel_shader, 
            width=1, height=1,
            tile_width=36, tile_height=41,
            default_tile=0)
        
        self.sprite.x = x
        self.sprite.y = y

class MushroomScavenging:
    def __init__(self):
        self.sheet = displayio.OnDiskBitmap("assets/tree_stump.bmp")
        self.sprite = displayio.TileGrid(self.sheet, pixel_shader=self.sheet.pixel_shader)
        
        self.bladeSheet = displayio.OnDiskBitmap("assets/blade_wing.bmp")
        self.bladeSprite = displayio.TileGrid(self.bladeSheet, pixel_shader=self.bladeSheet.pixel_shader, x=60)
        
        self.bladeY = 0
        self.ySin = 0
        self.xSin = 0

        self.score = 0
        self.slashing = False
        self.sprite.hidden = True
        self.bladeSprite.hidden = True

        self.mushroom = None
    
    def slash(self):
        if self.slashing: return
        self.xSin = 0.0
        self.slashing = True

    def update(self):
        if not self.slashing:
            self.ySin += 0.2
            self.bladeY = int(math.sin(self.ySin) * 50 + 58)
            self.bladeSprite.y = self.bladeY
        else:
            self.xSin += 0.2
            self.bladeSprite.x = int(math.sin(self.xSin) * -40 + 60)
            
            if self.bladeY >= self.mushroom.sprite.y and self.bladeY <= self.mushroom.sprite.y + 20:
                self.mushroom.sprite[0] = 1
            
            if self.xSin > 3.0:
                self.bladeSprite.x = 60
                self.slashing = False

                if self.mushroom.sprite[0] == 1:
                    self.mushroom.sprite.y = random.randint(0,85)
                    self.mushroom.sprite[0] = 0

    def spawnMushroom(self, splash):
        self.mushroom = Mushroom(25, random.randint(0,85))
        splash.insert(splash.index(self.bladeSprite), self.mushroom.sprite)