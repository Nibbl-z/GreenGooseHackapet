import displayio
import random
import timer

FEATHER_START_Y = 30
FEATHER_END_Y = 128

class Feather:
    def __init__(self, x, target):
        self.sheet = displayio.OnDiskBitmap("assets/feather.bmp")
        self.sprite = displayio.TileGrid(self.sheet, pixel_shader=self.sheet.pixel_shader)
        
        self.start = x
        self.target = target
        self.sprite.x = x
        
        self.progress = 0
        self.duration = 10
    
    def update(self):
        time = (self.progress / self.duration)
        
        self.sprite.x = int((1 - time) * self.start + time * self.target)
        self.sprite.y = int((1 - time) * FEATHER_START_Y + time * FEATHER_END_Y)

        self.progress += 1


class GreyGooseBossfight:
    def __init__(self):
        self.sheet = displayio.OnDiskBitmap("assets/greygoose_fight.bmp")
        self.sprite = displayio.TileGrid(
            self.sheet,
            pixel_shader=self.sheet.pixel_shader,
            width=1, height=1,
            tile_width=128, tile_height=128,
            default_tile=0,
        )

        self.sprite.hidden = True
        
        self.featherSheet = displayio.OnDiskBitmap("assets/feather.bmp")
        self.leftWing = False
        self.rightWing = False
        self.feathers = []
    
    def update(self):
        if self.leftWing and self.rightWing:
            self.sprite[0] = 3
        elif self.rightWing and not self.leftWing:
            self.sprite[0] = 2
        elif self.leftWing and not self.rightWing:
            self.sprite[0] = 1
        else:
            self.sprite[0] = 0
        
        for feather in self.feathers:
            feather.update()

            if feather.progress > feather.duration:
                self.feathers.remove(feather)
    
    def attackLeft(self, gooseX, splash):
        self.leftWing = True

        def lowerWing():
            self.leftWing = False

        timer.createAndStartTimer(5, lowerWing)

        feather = Feather(x=random.randint(0,40), target=gooseX + random.randint(-4,4))
        splash.append(feather.sprite)
        self.feathers.append(feather)
    
    def attackRight(self, gooseX, splash):
        self.rightWing = True

        def lowerWing():
            self.rightWing = False

        timer.createAndStartTimer(5, lowerWing)

        feather = Feather(x=random.randint(80,120), target=gooseX + random.randint(-4,4))
        splash.append(feather.sprite)
        self.feathers.append(feather)
