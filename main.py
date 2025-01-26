import displayio
from blinka_displayio_pygamedisplay import PyGameDisplay
import pygame
import time
from adafruit_display_text import label

from goose import Goose

from parallax import Parallax, ParallaxFrame

pygame.init()

display = PyGameDisplay(width=128, height=128)
splash = displayio.Group()
display.show(splash)

mainParallax = Parallax(
    [
        ParallaxFrame("assets/bg_sky.bmp", 0.1),
        ParallaxFrame("assets/bg_hill.bmp", 0.3),
        ParallaxFrame("assets/ground.bmp", 1),
    ]
)

for frame in mainParallax.frames:
    splash.append(frame.sprite)
    splash.append(frame.spriteNext)

goose = Goose()
splash.append(goose.sprite)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
    
    keys = pygame.key.get_pressed()

    if keys[pygame.K_LEFT]:
        goose.walking = True
        goose.x -= goose.SPEED
        goose.sprite.flip_x = False
        
        goose.updateGooseWalk()
    
    elif keys[pygame.K_RIGHT]:
        goose.walking = True
        goose.x += goose.SPEED
        goose.sprite.flip_x = True

        goose.updateGooseWalk()
    else:
        goose.walking = False

    
    goose.sprite[0] = goose.frame()
    
    mainParallax.updatePosition(-goose.x)

    time.sleep(0.1)