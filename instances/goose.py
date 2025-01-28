import displayio

class Goose:
    def __init__(self):
        self.sheet = displayio.OnDiskBitmap("assets/goose.bmp")
        self.sprite = displayio.TileGrid(
            self.sheet,
            pixel_shader=self.sheet.pixel_shader,
            width=1, height=1,
            tile_width=32, tile_height=32,
            default_tile=0,
            x=int(64 - 16), y=64
        )
        
        self.x = 0
        
        self.walking = False
        self.walkFrame = 0
        
        self.frozen = False

        self.SPEED = 10
    
    def updateGooseWalk(self):
        self.walkFrame += 1

        if self.walkFrame == 6:
            self.walkFrame = 0

    def frame(self):
        if self.walking:
            return self.walkFrame + 1
        
        return 0