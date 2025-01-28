import displayio

class Stella:
    def __init__(self):
        self.sheet = displayio.OnDiskBitmap("assets/stella.bmp")
        self.sprite = displayio.TileGrid(
            self.sheet,
            pixel_shader=self.sheet.pixel_shader,
            width=1, height=1,
            tile_width=32, tile_height=32,
            default_tile=1,
            x=int(64 - 16), y=64
        )
        
        self.x = 100
        self.frame = 0
        self.walking = True
        self.walkFrame = 0
        self.sleeping = False
    
    def update(self, gooseX):
        if self.sleeping:
            self.sprite[0] = 0
        elif self.walking:
            self.walkFrame += 1
            
            if self.walkFrame == 6:
                self.walkFrame = 0

            self.sprite[0] = 2 + self.walkFrame
        else:
            self.sprite[0] = 1
        self.x += 2
        self.sprite.x = self.x - gooseX

