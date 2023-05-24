import arcade as ac
from pathlib import Path

class asteroid_list(ac.SpriteList):
    def __init__(self):
        super().__init__()
        
class explosion(ac.Sprite):
    def __init__(self, texture_list):
        super().__init__()
        self.textures = texture_list
        self.set_texture(0)
        self.texture_index = 0
        self.win_condition = True
        self.explosion_occurences = 0
        
    def update(self):
        super().update()
        if self.win_condition == False and self.texture_index <= len(self.textures) - 1:
            self.set_texture(self.texture_index)
            self.texture_index += 1