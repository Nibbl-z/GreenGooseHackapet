import displayio
from blinka_displayio_pygamedisplay import PyGameDisplay
import pygame
import time
from adafruit_display_text import label

from goose import Goose

pygame.init()

display = PyGameDisplay(width=128, height=128)
splash = displayio.Group()
display.show(splash)

forestBackground = displayio.OnDiskBitmap("assets/bg_hill.bmp")
bgSprite = displayio.TileGrid(forestBackground, pixel_shader=forestBackground.pixel_shader)
splash.append(bgSprite)

goose = Goose()

splash.append(goose.sprite)

SPEED = 3

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
    
    keys = pygame.key.get_pressed()

    if keys[pygame.K_LEFT]:
        goose.walking = True
        goose.sprite.x -= SPEED
        goose.sprite.flip_x = False
        
        goose.updateGooseWalk()
    
    elif keys[pygame.K_RIGHT]:
        goose.walking = True
        goose.sprite.x += SPEED
        goose.sprite.flip_x = True

        goose.updateGooseWalk()
    else:
        goose.walking = False

    
    goose.sprite[0] = goose.frame()

    time.sleep(0.1)