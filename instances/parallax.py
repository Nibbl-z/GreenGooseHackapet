import displayio
import math

class ParallaxFrame:
    def __init__(self, file, speed, doRepeat):
        self.speed = speed
        self.sheet = displayio.OnDiskBitmap(file)
        
        self.sprite = displayio.TileGrid(
            self.sheet,
            pixel_shader=self.sheet.pixel_shader
        )

        self.spriteNext = displayio.TileGrid(
            self.sheet,
            pixel_shader=self.sheet.pixel_shader,
            x=self.sheet.width
        )
        
        self.doRepeat = doRepeat
    
    def getRepeatOffset(self, offset):
        return math.floor((offset * self.speed) / (self.sheet.width)) * self.sheet.width 
     
    def updatePosition(self, offset):
        repeatOffset = self.getRepeatOffset(offset) if self.doRepeat else 0
        
        self.sprite.x = int(offset * self.speed - repeatOffset)

        if self.doRepeat:
            self.spriteNext.x = int(offset * self.speed - self.sheet.width - repeatOffset)
        

class Parallax:
    def __init__(self, frames):
        self.frames = frames

    def updatePosition(self, offset):
        for frame in self.frames:
            frame.updatePosition(offset)
