import arcade
import os

# --- Constants ---
SCREEN_WIDTH = 1900
SCREEN_HEIGHT = 1000
IMAGE_WIDTH = 1900
IMAGE_HEIGHT= 1000

SCROLL_SPEED = 1.5


print("Visit   https://www.kenney.nl/   for pixel art  ")
print(" Visit   https://opengameart.org/   for resources   ")



class MyGame(arcade.Window):
    def __init__(self, width, height, fullscreen = True):
        super().__init__(width, height)

        file_path = os.path.dirname(os.path.abspath(__file__))
        os.chdir(file_path)

    def setup(self):

        #first background image
        self.background_list = arcade.SpriteList()

        for i in range(0,9):
            self.background_list.append(arcade.Sprite(f"resources/images/backgrounds/Background_{i}.jpg"))

            curent_background = self.background_list[i]

            curent_background.center_x = SCREEN_WIDTH // 2

            curent_background.center_y = SCREEN_HEIGHT // 2 + IMAGE_HEIGHT * i

            curent_background.change_y = -SCROLL_SPEED

        

    def on_draw(self):
        arcade.start_render()
        self.background_list.draw()

    def update(self, delta_time):

        for background in self.background_list:


            #reset the images when they go past the screen
            if background.bottom == -IMAGE_HEIGHT:
                background.center_y = SCREEN_HEIGHT + IMAGE_WIDTH // 2

        

        self.background_list.update()

def main():
    window = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT)
    window.setup()
    arcade.run()

if __name__ == "__main__":
    main()


"""

def update(self, delta_time):

        #reset the images when they go past the screen
        if self.background_sprite.bottom == -IMAGE_HEIGHT:
            self.background_sprite.center_y = SCREEN_HEIGHT + IMAGE_WIDTH // 2

        if self.background_sprite_2.bottom == -IMAGE_HEIGHT:
            self.background_sprite_2.center_y = SCREEN_HEIGHT + IMAGE_WIDTH // 2

        self.background_list.update()


"""




"""
def setup(self):

        #first background image
        self.background_list = arcade.SpriteList()

        self.background_sprite = arcade.Sprite("resources/images/backgrounds/image5.jpg")

        self.background_sprite.center_x = SCREEN_WIDTH // 2
        self.background_sprite.center_y = SCREEN_HEIGHT // 2
        #self.background_sprite.change_x = -SCROLL_SPEED
        self.background_sprite.change_y = -SCROLL_SPEED


        self.background_list.append(self.background_sprite)

        #second background image
        self.background_sprite_2 = arcade.Sprite("resources/images/backgrounds/back.png")

        self.background_sprite_2.center_x = SCREEN_WIDTH // 2
        self.background_sprite_2.center_y = SCREEN_HEIGHT // 2 + IMAGE_HEIGHT
        #self.background_sprite_2.change_x = -SCROLL_SPEED
        self.background_sprite_2.change_y = -SCROLL_SPEED

        self.background_list.append(self.background_sprite_2)
"""












"""
def update(self, delta_time):

        #reset the images when they go past the screen
        if self.background_sprite.left == -IMAGE_WIDTH:
            self.background_sprite.center_x = SCREEN_WIDTH + IMAGE_WIDTH // 2

        if self.background_sprite_2.left == -IMAGE_WIDTH:
            self.background_sprite_2.center_x = SCREEN_WIDTH + IMAGE_WIDTH // 2

        self.background_list.update()
"""