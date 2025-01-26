import displayio
import math

class ParallaxFrame:
    def __init__(self, file, speed):
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
    
    def getRepeatOffset(self, offset):
        return math.floor((offset * self.speed) / (self.sheet.width)) * self.sheet.width 
     
    def updatePosition(self, offset):
        repeatOffset = self.getRepeatOffset(offset)
        
        self.sprite.x = int(offset * self.speed - repeatOffset)
        self.spriteNext.x = int(offset * self.speed - self.sheet.width - repeatOffset)
        

class Parallax:
    def __init__(self, frames):
        self.frames = frames
    
    

    def updatePosition(self, offset):
        debugIndex = 1
        debugInfo = ""

        for frame in self.frames:
            frame.updatePosition(offset)
            debugInfo = debugInfo + str(debugIndex) + ": " + str(frame.sprite.x) + " | "
            debugIndex += 1

        print(debugInfo)