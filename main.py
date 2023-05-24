import arcade as ac
import random as r
from pathlib import Path
from objects import asteroid_list
from objects import explosion

class Space_Game(ac.Window):
    def create_new_asteroids(self):
        self.asteroid_list.append(ac.Sprite(self.sprites_folder / "asteroids.png", 0.2))
        self.index_of_new_asteroid = len(self.asteroid_list) - 1
        self.asteroid_list[self.index_of_new_asteroid].center_x = self.width
        self.asteroid_list[self.index_of_new_asteroid].center_y = r.randint(1, self.width)
        self.asteroid_list[self.index_of_new_asteroid].angle = r.randint(0, 360)
        self.asteroid_list[self.index_of_new_asteroid].change_x = r.randint(2, 6)
        self.asteroid_list[self.index_of_new_asteroid].change_x = -(self.asteroid_list[self.index_of_new_asteroid].change_x)
        
    def __init__(self, width, height, window_name):
        super().__init__(width, height, window_name)
        # Declares the path where the sprites are contained
        self.sprites_folder = Path(__file__).parent / "Sprites"
        self.explosion_animations = Path(__file__).parent / "Sprites" / "Explosion Effect"
        # Width data
        self.width = width
        # Explosion data
        self.explosion_list = ac.SpriteList()
        self.explosion_texture_list = []
        for i in range(18):
            texture = ac.load_texture(self.explosion_animations / f"{i + 1}.png")
            self.explosion_texture_list.append(texture)
        self.explosion = explosion(self.explosion_texture_list)
        self.explosion_list.append(self.explosion)
        # Spaceship (player) data
        self.spaceship = ac.Sprite(self.sprites_folder / "space_ship.png", 0.1)
        self.spaceship.center_x = 50
        self.spaceship.center_y = 0
        self.spaceship.angle = -90
        # Asteroid Data
        self.asteroid_list = asteroid_list()
        for i in range(10):
            self.create_new_asteroids()
        # Collision data
        self.spaceship_asteroid_collision = False
        # Score data
        self.asteroids_dodged = 0
        
    def on_draw(self):
        ac.start_render()
        ac.set_background_color(ac.color.BLACK)
        if self.spaceship_asteroid_collision == False:
            self.spaceship.draw()
            
        self.asteroid_list.draw()
        if self.spaceship_asteroid_collision == True:
            ac.draw_text("The spaceship was hit", 100, 100, ac.color.WHITE, 12, 800, "center")
            
        if self.spaceship_asteroid_collision == True:
            self.explosion_list.draw()
            
        ac.draw_text(f"Asteroids dodged: {self.asteroids_dodged}", 100, 100, ac.color.WHITE, 12, 100, "center")
        
    def on_update(self, delta_time):
        if ac.check_for_collision_with_list(self.spaceship, self.asteroid_list):
            self.spaceship_asteroid_collision = True
            for explosion in self.explosion_list:
                explosion.center_x = self.spaceship.center_x
                explosion.center_y = self.spaceship.center_y
                self.explosion.win_condition = False
        
        for i in self.asteroid_list:
            if self.spaceship_asteroid_collision == False: 
                if i.center_x < 0:
                    i.remove_from_sprite_lists()
                    self.asteroids_dodged += 1
                    self.create_new_asteroids()
                        
        self.spaceship.update()
        self.asteroid_list.update()
        self.explosion_list.update()
        
    def on_mouse_motion(self, x, y, dx, dy):
        if self.spaceship_asteroid_collision == False:
            self.spaceship.center_y = y
        
Space_Game(800, 600, "Space Game")
ac.run()