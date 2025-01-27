import displayio
from blinka_displayio_pygamedisplay import PyGameDisplay

import pygame
import time

from adafruit_bitmap_font import bitmap_font
from adafruit_display_text import label

from instances.goose import Goose

from map import Map, Interactable, updateMaps
from instances.parallax import Parallax, ParallaxFrame
from instances.button_indicator import ButtonIndicator
from instances.fade import Fade

import timer
from dialogue import Dialogue

pygame.init()

display = PyGameDisplay(width=128, height=128)
splash = displayio.Group()
display.show(splash)

fade = Fade()
dialogue = Dialogue()

global currentMap
currentMap = "outside_hotel"

def enterHotel():
    global currentMap
    def afterFade():
        global currentMap
        
        fade.direction = -1
        currentMap = "inside_hotel"
        goose.x = 0
    
    fade.direction = 1
    timer.createAndStartTimer(6, afterFade)

def exitHotel():
    global currentMap
    
    def afterFade():
        global currentMap
        
        fade.direction = -1
        currentMap = "outside_hotel"
        goose.x = 120
    
    fade.direction = 1
    timer.createAndStartTimer(6, afterFade)

def stellaTalk():
    dialogue.speak("stella", ["are you,, the\ngreen goose??", "wowwww", "thats pretty\nawesome sauce", "uhmmm", "ya"])

maps = {
    "outside_hotel" : Map(
        Parallax([
            ParallaxFrame("assets/bg_sky.bmp", 0.1, True),
            ParallaxFrame("assets/bg_hill.bmp", 0.3, True),
            ParallaxFrame("assets/building.bmp", 0.9, False),
            ParallaxFrame("assets/ground.bmp", 1, True),
        ]),
        [
            Interactable(110, 40, enterHotel)
        ],
        -100000, 
        100000
    ),
    
    "inside_hotel": Map(
        Parallax([
            ParallaxFrame("assets/hotel_floor.bmp", 1, False)
        ]),
        [
            Interactable(-15, 30, exitHotel),
            Interactable(-40, 10, stellaTalk)
        ],
        -50, 
        400
    )
}



for name, i in maps.items():
    for frame in i.parallax.frames:
        splash.append(frame.sprite)
        splash.append(frame.spriteNext)

goose = Goose()
splash.append(goose.sprite)

buttonIndicator = ButtonIndicator()
splash.append(buttonIndicator.sprite)

splash.append(fade.sprite)

font = bitmap_font.load_font("assets/RobotoMono.bdf")

debugLabel = label.Label(font, text="AwesomeSauce", color=0xFFFFFF)
debugLabel.x = 5
debugLabel.y = 5

splash.append(debugLabel)



splash.append(dialogue.bgSprite)
splash.append(dialogue.label)

dialogue.loadSpeaker("assets/faces/stella.bmp", "stella")

for name, speaker in dialogue.speakers.items():
    splash.append(speaker)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if event.type == pygame.KEYDOWN and event.key == pygame.K_UP:
            if dialogue.speaking:
                dialogue.nextText()
            else:
                for interactable in maps[currentMap].interactables:
                    interactable.use(goose.x)
    
    keys = pygame.key.get_pressed()
    
    if keys[pygame.K_LEFT]:
        if goose.x > maps[currentMap].leftBound:
            goose.walking = True
            goose.x -= goose.SPEED
            goose.sprite.flip_x = False
            
            goose.updateGooseWalk()
    
    elif keys[pygame.K_RIGHT]:
        if goose.x < maps[currentMap].rightBound:
            goose.walking = True
            goose.x += goose.SPEED
            goose.sprite.flip_x = True

            goose.updateGooseWalk()           
    else:
        goose.walking = False

    
    goose.sprite[0] = goose.frame()
    buttonIndicator.update()
    maps[currentMap].parallax.updatePosition(-goose.x)
    print(currentMap)
    debugLabel.text = str(goose.x)
    
    buttonIndicator.sprite.hidden = True
    
    for interactable in maps[currentMap].interactables:
        if interactable.canUse(goose.x):
            buttonIndicator.sprite.hidden = False
    
    updateMaps(maps, currentMap)
    
    fade.fade()
    timer.update()
    dialogue.update()
    time.sleep(0.1)