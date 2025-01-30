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
        self.walking = False
        self.walkFrame = 0
        self.sleeping = False
        self.map = "inside_hotel"
        self.direction = 0
        self.customUpdate = None

        self.dialogues = {
            "testing" : ["i aint reading\nallat"],
            "meet" : [
                "HUH!", 
                "Oh...Hi?",
                "Umm...",
                "I haven't seen\nanyone alive\nin..", 
                "A while...", 
                "...",
                "Never thought\nthis would \nhappen...",
                "Where'd you\ncome from?",
                "How have I\nnever seen\nyou?",
                "The incident\nwas... a long\ntime ago...",
                "And what\nhappened to\nyou?",
                "..I asssume\nthe radiation\nmade you...\nthat color...",
                "...sorry if\nI'm asking too\nmany\nquestions...",
                "I never have\nanyone to\ntalk to...",
                "...",
                "It's really\ndangerous out\nthere y'know.",
                "I should\nprobably show \nyou around...",
                "But those grey\ngeese are\nEVERYWHERE.",
                "And they are\nvery vicious.",
                "Reminds me of\nmy old sister\nRory.",
                "She bit my\nparents a lot.",
                "...",
                "I miss my\nfamily...",
                "...",
                "...well I\nwas gonna\nsearch for\nsome food...",
                "Guess it might\nbe a bit\nsafer with\nyou around.",
                "Come with me."
            ],
            "meetOutside": [
                "I remember \nseeing some\nmushrooms\nthis way...",
                "...I think.",
            ],
            "meetOutside2": [
                "Not sure how\nthey're safe\nto eat...",
                "Especially\nwith all the\nradiation...",
                "But I've had\nthem before.",
                "And they keep\nme alive.",
                "And they grow\neverywhere...",
                "I've seen some\ngrow inside\nthe hotel!...\nSomehow.",
                "It's nice\nwhen that\nhappens.",
                "Then I don't\nhave to come\nout here.",
                "With all the...",
                "...",
            ],
            "meetOutside3": [
                "OH NO"
            ],
            "afterFight": [
                "Oh... you...",
                "Fought it...",
                "Uhmm...",
                "Wow.",
                "Uhh..",
                "I'm too\nparanoid to\ngather the\nmushrooms now...",
                "Would you\nbe willing to\nget them for\nme?",
                "If you\nencounter any\nmore of those...",
                "...Geese...",
                "I'm sure you\ncould handle\nit."
            ]
        }

    def metStellaUpstairs(self, gooseX, currentMap):
        if abs(self.x - 40 - gooseX) >= 50:
            self.direction = 0
            self.walking = False
        else:
            self.direction = 5
            self.walking = True

        if self.x >= 440:
            self.map = "inside_hotel"
            self.x = 400

            if currentMap == "inside_hotel":
                self.direction = -5
                self.customUpdate = self.metStellaDownstairs
            else:
                self.direction = 0
            
            self.sprite.flip_x = True
    
    def metStellaDownstairs(self, gooseX, currentMap):
        if abs(self.x - 50 - gooseX) >= 50:
            self.direction = 0
            self.walking = False
        else:
            self.direction = -5
            self.walking = True

        if self.x <= 50:
            self.map = "outside_hotel"
            self.direction = 0
            self.x = 230
            self.sprite.flip_x = True
            self.walking = False
            self.sleeping = False
            self.customUpdate = None

    def metStellaOutside(self, gooseX, currentMap):
        if self.x - 90 >= gooseX:
            self.direction = 0
            self.walking = False
        else:
            self.direction = 5
            self.walking = True
    
    def update(self, gooseX, currentMap):
        if self.sleeping:
            self.sprite[0] = 0
        elif self.walking:
            self.walkFrame += 1
            
            if self.walkFrame == 6:
                self.walkFrame = 0
            
            self.sprite[0] = 2 + self.walkFrame
        else:
            self.sprite[0] = 1

        self.sprite.hidden = self.map != currentMap
        self.x += self.direction
        self.sprite.x = self.x - gooseX

