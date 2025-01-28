import displayio
from blinka_displayio_pygamedisplay import PyGameDisplay

import pygame
import time

from adafruit_bitmap_font import bitmap_font
from adafruit_display_text import label

from instances.goose import Goose
from instances.stella import Stella
from instances.greygoose import GreyGoose
from instances.greygoosebossfight import GreyGooseBossfight

from map import Map, Interactable, updateMaps, Trigger
from instances.parallax import Parallax, ParallaxFrame
from instances.button_indicator import ButtonIndicator
from instances.fade import Fade

import timer
import random
from dialogue import Dialogue

pygame.init()

display = PyGameDisplay(width=128, height=128)
splash = displayio.Group()
display.show(splash)

fade = Fade()
dialogue = Dialogue()

global currentMap

currentMap = "outside_hotel"
currentState = "start"

def enterHotel():
    def afterFade():
        global currentMap
        
        fade.direction = -1
        currentMap = "inside_hotel"
        goose.x = 0
    
    fade.direction = 1
    timer.createAndStartTimer(6, afterFade)

def startFight():
    global currentMap

    fade.direction = -1
    greygooseBossfight.sprite.hidden = False
    goose.cameraFollow = False
    goose.x = 48
    goose.SPEED = 10
    goose.sprite.hidden = False
    goose.frozen = False
    goose.sprite.y = 64+24
    
    currentMap = "void"

    def attackLeft():
        greygooseBossfight.attackLeft(goose.x, splash)
        timer.createAndStartTimer(random.randint(10,20), attackLeft)

    def attackRight():
        greygooseBossfight.attackRight(goose.x, splash)
        timer.createAndStartTimer(random.randint(10,20), attackRight)

    timer.createAndStartTimer(random.randint(10,20), attackLeft)
    timer.createAndStartTimer(random.randint(10,20), attackRight)

def encounter():
    def frame1():
        global currentMap
        fade.direction = -1
        currentMap = "encounter_1"
        goose.x = 0
        goose.sprite.hidden = True

        def afterWait():
            def frame2():
                global currentMap
                fade.direction = -1
                currentMap = "encounter_2"
                
                def afterWait2():
                    fade.direction = 1
                    timer.createAndStartTimer(6, startFight)

                timer.createAndStartTimer(15, afterWait2)
                
            

            fade.direction = 1
            timer.createAndStartTimer(6, frame2)
        
        timer.createAndStartTimer(15, afterWait)

    fade.direction = 1
    timer.createAndStartTimer(6, frame1)

def exitHotel():
    def afterFade():
        global currentMap
        global currentState

        fade.direction = -1
        currentMap = "outside_hotel"
        goose.x = 120
        
        if currentState == "metStella":
            def afterSpeak():
                def stellaScare():
                    
                    goose.frozen = True
                    goose.sprite.flip_x = True
                    greygoose.x = stella.x + 100
                    greygoose.direction = -5

                    greygoose.map = "outside_hotel"
                    stella.customUpdate = None
                    stella.direction = -15
                    stella.sprite.flip_x = True
                    dialogue.speak("stella", stella.dialogues["meetOutside3"], None, True)

                dialogue.speak("stella", stella.dialogues["meetOutside2"], stellaScare, True)
                
                stella.direction = 5
                stella.walking = True
                stella.sprite.flip_x = False
                stella.customUpdate = stella.metStellaOutside
            
            dialogue.speak("stella", stella.dialogues["meetOutside"], afterSpeak, True)
    
    fade.direction = 1
    timer.createAndStartTimer(6, afterFade)

def upstairsHotel():
    global currentMap
    
    def afterFade():
        global currentMap
        global currentState

        fade.direction = -1
        currentMap = "inside_hotel_floor2"
        goose.x = 60 # 400
        goose.sprite.flip_x = False
    
    fade.direction = 1
    timer.createAndStartTimer(6, afterFade)

def downstairsHotel():
    global currentMap

    def afterFade():
        global currentMap
        global currentState

        fade.direction = -1
        currentMap = "inside_hotel"
        goose.x = 390
        goose.sprite.flip_x = False
        
        if currentState == "metStella" and stella.map == "inside_hotel":
            stella.direction = -5
            stella.customUpdate = stella.metStellaDownstairs

    
    fade.direction = 1
    timer.createAndStartTimer(6, afterFade)

def meetStella():
    goose.frozen = True
    
    def afterWait():
        stella.sleeping = False
        
        def stellaSpeak():
            def afterSpeak():
                global currentState
                stella.walking = True
                stella.direction = 5
                goose.frozen = False
                currentState = "metStella"
                
                stella.customUpdate = stella.metStellaUpstairs

            dialogue.speak("stella", stella.dialogues["testing"], afterSpeak, False)
        
        timer.createAndStartTimer(10, stellaSpeak)

    timer.createAndStartTimer(10, afterWait)

maps = {
    "void" : Map(
        Parallax([]),
        [],
        [],
        0, 90
    ),
    "outside_hotel" : Map(
        Parallax([
            ParallaxFrame("assets/bg_sky.bmp", 0.1, True),
            ParallaxFrame("assets/bg_hill.bmp", 0.2, True),
            ParallaxFrame("assets/trees2.bmp", 0.5, True),
            ParallaxFrame("assets/trees1.bmp", 0.6, True),
            ParallaxFrame("assets/building.bmp", 0.9, False),
            ParallaxFrame("assets/ground.bmp", 1, True),
        ]),
        [
            Interactable(110, 40, encounter)
        ],
        [],
        -100000, 
        100000
    ),
    
    "inside_hotel": Map(
        Parallax([
            ParallaxFrame("assets/hotel_floor.bmp", 1, False)
        ]),
        [
            Interactable(-15, 30, exitHotel),
            Interactable(370, 30, upstairsHotel)
        ],
        [],
        -50, 
        400
    ),

    "inside_hotel_floor2": Map(
        Parallax([
            ParallaxFrame("assets/hotel_floor2.bmp", 1, False)
        ]),
        [
            Interactable(400, 50, downstairsHotel),
        ],
        [
            Trigger(10, True, meetStella)
        ],
        -50,
        430
    ),

    "encounter_1": Map(
        Parallax([
            ParallaxFrame("assets/encounter1.bmp", 1, False)
        ]),
        [], [], -100, 100
    ),

    "encounter_2": Map(
        Parallax([
            ParallaxFrame("assets/encounter2.bmp", 1, False)
        ]),
        [], [], -100, 100
    ),
}

for name, i in maps.items():
    for frame in i.parallax.frames:
        splash.append(frame.sprite)
        splash.append(frame.spriteNext)

greygooseBossfight = GreyGooseBossfight()
splash.append(greygooseBossfight.sprite)

goose = Goose()
splash.append(goose.sprite)

stella = Stella()
splash.append(stella.sprite)
stella.sleeping = True
stella.map = "inside_hotel_floor2"
stella.x = 15

greygoose = GreyGoose()
splash.append(greygoose.sprite)
greygoose.map = "inside_hotel"
greygoose.x = 60
greygoose.walking = True

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
                if not dialogue.autoContinue: dialogue.nextText() 
            else:
                for interactable in maps[currentMap].interactables:
                    interactable.use(goose.x)
    
    keys = pygame.key.get_pressed()
    
    if keys[pygame.K_LEFT]:
        if goose.x > maps[currentMap].leftBound and not goose.frozen:
            goose.walking = True
            goose.x -= goose.SPEED
            goose.sprite.flip_x = False
            
            goose.updateGooseWalk()
    
    elif keys[pygame.K_RIGHT]:
        if goose.x < maps[currentMap].rightBound and not goose.frozen:
            goose.walking = True
            goose.x += goose.SPEED
            goose.sprite.flip_x = True

            goose.updateGooseWalk()           
    else:
        goose.walking = False

    
    goose.sprite[0] = goose.frame()
    buttonIndicator.update()
    maps[currentMap].parallax.updatePosition(-goose.x)
    debugLabel.text = str(goose.x) + "/" + str(stella.x)
    
    buttonIndicator.sprite.hidden = True
    
    for interactable in maps[currentMap].interactables:
        if interactable.canUse(goose.x):
            buttonIndicator.sprite.hidden = False

    for trigger in maps[currentMap].triggers:
        trigger.update(goose.x)
    
    updateMaps(maps, currentMap)
    
    fade.fade()
    timer.update()
    dialogue.update()
    stella.update(goose.x, currentMap)
    greygoose.update(goose.x, currentMap)
    greygooseBossfight.update()
    goose.update()

    if stella.customUpdate != None: stella.customUpdate(goose.x, currentMap)
    
    time.sleep(0.1)