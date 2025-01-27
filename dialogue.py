import displayio
from adafruit_bitmap_font import bitmap_font
from adafruit_display_text import label

class Dialogue:
    def __init__(self):
        self.bgSheet = displayio.OnDiskBitmap("assets/dialogue.bmp")
        self.bgSprite = displayio.TileGrid(
            self.bgSheet,
            pixel_shader=self.bgSheet.pixel_shader
        )

        self.bgSprite.hidden = True
        self.speakers = {}
        
        self.font = bitmap_font.load_font("assets/RobotoMono.bdf")

        self.label = label.Label(self.font, text="", color=0xFFFFFF)
        self.label.x = 9
        self.label.y = 9
        
        self.texts = []
        self.currentText = 0
        self.textCutoff = 0
        self.speaking = False
    
    def loadSpeaker(self, file, name):
        sheet = displayio.OnDiskBitmap(file)
        self.speakers[name] = displayio.TileGrid(sheet, pixel_shader=sheet.pixel_shader, x=87, y=9)
        self.speakers[name].hidden = True
    
    def speak(self, speaker, dialogue):
        self.bgSprite.hidden = False
        self.speakers[speaker].hidden = False
        self.speaking = True
        self.texts = dialogue
        self.currentText = 0
        self.textCutoff = 0

    def hide(self):
        self.label.text = ""
        self.bgSprite.hidden = True
        self.speaking = False

        for name, speaker in self.speakers.items():
            speaker.hidden = True
        
        
    def update(self):
        if self.speaking:
            if self.textCutoff < len(self.texts[self.currentText]):
                self.textCutoff += 1
            
            self.label.text = self.texts[self.currentText][:self.textCutoff]
    
    def nextText(self):
        if self.textCutoff < len(self.texts[self.currentText]):
            self.textCutoff = len(self.texts[self.currentText])
            return

        self.textCutoff = 0
        self.currentText += 1
        
        if self.currentText >= len(self.texts):
            self.hide()

    


