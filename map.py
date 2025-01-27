from instances.parallax import Parallax, ParallaxFrame

class Interactable:
    def __init__(self, x, width, function):
        self.x = x
        self.width = width
        self.function = function
    
    def canUse(self, x):
        return x >= self.x and x <= self.x + self.width
    
    def use(self, x):
        if self.canUse(x):
            self.function()

class Map:
    def __init__(self, parallax, interactables):
        self.parallax = parallax
        self.interactables = interactables

def updateMaps(maps, currentMap):
    for name, map in maps.items():
        if currentMap != name:
            for frame in map.parallax.frames:
                frame.sprite.hidden = True
        else:
            for frame in map.parallax.frames:
                frame.sprite.hidden = False