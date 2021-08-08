import arcade
import random
import math
import os

#from arcade.experimental.camera import Camera2D

from arcade import Point, Vector
from arcade.utils import _Vec2

import time

import pyglet



from typing import cast
import pprint

import pyglet.input.base

# --- Constants ---
SCREEN_WIDTH = 1900
SCREEN_HEIGHT = 1000
IMAGE_WIDTH = 1900
IMAGE_HEIGHT= 1000

SCROLL_SPEED = 1.5




# //////////
TILE_SPRITE_SCALING = 0.5

# Constants
SCREEN_WIDTH = 1200 #1800 #1000
SCREEN_HEIGHT = 1000 #1000 #650
SCREEN_TITLE = "Rafale"

# Constants used to scale our sprites from their original size
CHARACTER_SCALING = 1
TILE_SCALING = 0.5
COIN_SCALING = 0.5
SCALE = 0.5

SPRITE_PIXEL_SIZE = 128
GRID_PIXEL_SIZE = (SPRITE_PIXEL_SIZE * TILE_SCALING)

# Movement speed of player, in pixels per frame
PLAYER_MOVEMENT_SPEED = 10
GRAVITY = 1
PLAYER_JUMP_SPEED = 20


LEFT_VIEWPORT_MARGIN = SCREEN_WIDTH // 2
RIGHT_VIEWPORT_MARGIN = SCREEN_WIDTH // 2
BOTTOM_VIEWPORT_MARGIN = SCREEN_HEIGHT // 2
TOP_VIEWPORT_MARGIN = SCREEN_HEIGHT // 2


MOVEMENT_SPEED = PLAYER_MOVEMENT_SPEED
MOVEMENT_SPEED_AMPHET = MOVEMENT_SPEED * 3


AMPHET_TIME_MAX = 60 * 10




HEALTHBAR_WIDTH = 50
HEALTHBAR_HEIGHT = 3
HEALTHBAR_OFFSET_Y = -30
LIFEBAR_Yoffset = 30

HEALTH_NUMBER_OFFSET_X = -10
HEALTH_NUMBER_OFFSET_Y = -25

ENEMY_MAX_HEALTH = 20

PLAYER_MAX_HEALTH = 141

LASER_DAMMAGE = 15
GRENADE_DAMMAGE = 150


MAX_DISTANCE_DOG_DETECTION = SCREEN_HEIGHT


LIVES_AT_START = 3


AMMO_MAX = 50
AMMO_GLOCK_START = 30

AMMO_GRENADE_START = 10

AMMO_GLOCK_PACK = 20
AMMO_GRENADE_PACK = 3

MEDIKIT_HEALTH_BOOST = PLAYER_MAX_HEALTH // 2

LEFT_MOUSE_BTN = 1
RIGHT_MOUSE_BTN = 4

SPRITE_SCALING_LASER = 0.8


ROCKET_SMOKE_TEXTURE = arcade.make_soft_circle_texture(15, arcade.color.GRAY)

CLOUD_TEXTURES = [
    arcade.make_soft_circle_texture(250, arcade.color.WHITE),
    arcade.make_soft_circle_texture(250, arcade.color.LIGHT_GRAY),
    arcade.make_soft_circle_texture(250, arcade.color.LIGHT_BLUE),
]


#MUSIC_INTRO = "resources/sounds/bb.mp3"

MUSIC_INTRO = "resources/sounds/airplane-landing_daniel_simion.wav"

MUSIC_GAMEOVER = "resources/sounds/player_gun.wav"

#MUSIC_INGAME = "resources/sounds/jet_sound.ogg"
# FileNotFoundError: Unable to load sound file: "resources/sounds/jet_sound.ogg". Exception: file does not start with RIFF id

MUSIC_INGAME = "resources/sounds/exp_01.wav"

DISPLAY_YOFFSET_SCORE = 150
DISPLAY_YOFFSET_AMMO = 175
DISPLAY_YOFFSET_GRENADE = 200


# *************************************************************

HEALTHBAR_WIDTH = 50
HEALTHBAR_HEIGHT = 3
HEALTHBAR_OFFSET_Y = -30
LIFEBAR_Yoffset = 30

HEALTH_NUMBER_OFFSET_X = -10
HEALTH_NUMBER_OFFSET_Y = -25


CROSSHAIR__RELATIVE_XOFFSET_SETUP = 0
CROSSHAIR__RELATIVE_YOFFSET_SETUP = 100

XRESPAWN = SCREEN_WIDTH // 2
YRESPAWN = SCREEN_HEIGHT // 2


RADAR_RADIUS_DETECTION = 512

ECLOSION_TIME_INTERVAL = 15.0
ECLOSION_MAX_WAVES = 3

GUNBTN = 0  # A


JOY_DEADZONE = 0.2


BULLET_COOLDOWN_TICKS = 10
# /////////

print("Visit   https://www.kenney.nl/   for pixel art  ")
print(" Visit   https://opengameart.org/   for resources   ")
print("   https://opengameart.org/content/ui-pack-space-extension   ")

# https://movilab.org/wiki/Tiled_Map_Editor



class GameView(arcade.View):

#class MyGame(arcade.View):
    
    def __init__(self, fullscreen = True):
    #def __init__(self, width, height, fullscreen = True):
    #def __init__(self, width = SCREEN_WIDTH, height = SCREEN_HEIGHT, fullscreen = True):
        #super().__init__(width, height)
        #super().__init__(width = SCREEN_WIDTH, height = SCREEN_HEIGHT)
        super().__init__()

        arcade.set_viewport(0, SCREEN_WIDTH - 1, 0, SCREEN_HEIGHT - 1)



        file_path = os.path.dirname(os.path.abspath(__file__))
        os.chdir(file_path)




        self.tick = 0
        self.bullet_cooldown = 0
        self.joy = None

        self.tile_map = None

        self.window.set_mouse_visible(False)

        self.topleft_corner = None

        # Cameras
        self.camera = None
        self.gui_camera = None

        self.shake_offset_1 = 0
        self.shake_offset_2 = 0
        self.shake_vel_1 = 0
        self.shake_vel_2 = 0


        self.datamusic = arcade.load_sound(MUSIC_INGAME)

        self.datamusic.get_length()

        self.player_music_ingame = None

        self.explosion_images = []


        self.mouse_pos = 0, 0
    
        
        #self.set_mouse_visible(True)
        self.window.set_mouse_visible(False)

       
        self.frame_count = 0


        #self.coin_list = None
        #self.wall_list = None

        self.startposition_list = None
        
        
        
        #self.dont_touch_list = None
        self.player_list = None
        self.life_list = None

        self.enemy_list = None


        # Used to keep track of our scrolling
        self.view_bottom = 0
        self.view_left = 0

        # Keep track of the score
        self.score = 0
        self.lives = 0


        self.ammo = 0
        self.ammo_text = None # ????????????????????

        

        # Load sounds. Sounds from kenney.nl
        self.gun_sound = arcade.sound.load_sound("resources/sounds/player_gun.wav")
        self.hit_sound = arcade.sound.load_sound("resources/sounds/player_gun.wav")
        self.death_sound = arcade.load_sound("resources/sounds/player_gun.wav")

        # Where is the right edge of the map?
        self.end_of_map = 0

        # Level
        self.level = 1

        # Load sounds
        self.collect_coin_sound = arcade.load_sound("resources/sounds/player_gun.wav")
        self.jump_sound = arcade.load_sound("resources/sounds/player_gun.wav")
        self.game_over = arcade.load_sound("resources/sounds/player_gun.wav")




    def load_level(self, level):
        # Read in the tiled map
        #my_map = arcade.tilemap.read_tmx(f":resources:tmx_maps/level_{level}.tmx")

        map_name = f"./resources/maps/level_{level}.json"

        

        layer_options = {"Topleft_corner_layer": {"use_spatial_hash": True},"Startposition_layer": {"use_spatial_hash": True}, "Cloud_thunder_layer": {"use_spatial_hash": True}, "Mi35_layer": {"use_spatial_hash": True}, "Back_image": {"use_spatial_hash": True}}


        self.tile_map = arcade.load_tilemap(map_name, scaling=TILE_SPRITE_SCALING,layer_options=layer_options)

        self.scene = arcade.Scene.from_tilemap(self.tile_map)

        # --- Walls ---

        # Calculate the right edge of the my_map in pixels
        #self.end_of_map = my_map.map_size.width * GRID_PIXEL_SIZE

        self.end_of_map = self.tile_map.width * GRID_PIXEL_SIZE


        self.view_left = 0
        self.view_bottom = 0



    def on_resize(self, width, height):
        self.camera.resize(width, height)
        self.gui_camera.resize(width, height)




    def setup(self, level):


        self.background_list = arcade.SpriteList()

        for i in range(0,9):
            self.background_list.append(arcade.Sprite(f"resources/images/backgrounds/Background_{i}.jpg"))

            curent_background = self.background_list[i]

            curent_background.center_x = SCREEN_WIDTH // 2

            curent_background.center_y = SCREEN_HEIGHT // 2 + IMAGE_HEIGHT * i

            curent_background.change_y = -SCROLL_SPEED


        # --------------------------------------------------------------------------------
        """ Set up the game here. Call this function to restart the game. """

        #self.eclosion_remaining_waves = ECLOSION_MAX_WAVES

        #arcade.schedule(self.krontab, ECLOSION_TIME_INTERVAL)


        

        # Keep track of the score
        self.score = 0

        if self.level == 1:
            self.lives = LIVES_AT_START
        

        self.ammo = AMMO_GLOCK_START

        self.startposition_list = arcade.SpriteList()
        
        # Create the Sprite lists
        self.player_list = arcade.SpriteList()
        self.enemy_list =  arcade.SpriteList()

       
        self.life_list = arcade.SpriteList()



        for i in range(32):  
        
                        
            texture_name = f"resources/images/explosion/explosion{i:04d}.png"
            self.explosion_images.append(arcade.load_texture(texture_name))

        self.explosion_list = arcade.SpriteList()


        self.wall_list = arcade.SpriteList(use_spatial_hash=True, spatial_hash_cell_size=128)

        self.coin_list = arcade.SpriteList()

        
        self.macadam_list = arcade.SpriteList()
        self.pave_list = arcade.SpriteList()

        #......................................................................

        

        #.................................
        # --- Load in a map from the tiled editor ---

        # Name of the layer in the file that has our platforms/walls
        startposition_layer_name = 'Startposition'

        

        # Name of the layer in the file that has our platforms/walls
        platforms_layer_name = 'Platforms'
        # Name of the layer that has items for pick-up
        #coins_layer_name = 'Coins'
        # Name of the layer that has items for foreground
        #foreground_layer_name = 'Foreground'
        # Name of the layer that has items for background
        #background_layer_name = 'Background'
        # Name of the layer that has items we shouldn't touch
        #dont_touch_layer_name = "Don't Touch"


        stairs_layer_name = "Stairs"

        back_image_layer_name = "Back_image"

        # Map name
  
        #map_name = f"resources/tmx_maps/easymap1_level_{level}.tmx"

        map_name = f"./resources/maps/level_{level}.json"

        # Read in the tiled map
        #my_map = arcade.tilemap.read_tmx(map_name)  !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

        #self.tile_map = arcade.load_tilemap(
            
        #    f"./resources/maps/level_{level}.json", scaling=TILE_SPRITE_SCALING,layer_options=layer_options
        #)

        self.load_level(self.level)

        

        # Calculate the right edge of the my_map in pixels
        #self.end_of_map = my_map.map_size.width * GRID_PIXEL_SIZE
        self.end_of_map = self.tile_map.width * GRID_PIXEL_SIZE
        

        # -- startposition ------------------------------------------------------------------------------------------------------------------------------------------------
        #self.startposition_list = arcade.tilemap.process_layer(map_object=my_map,
        #                                              layer_name=startposition_layer_name,
        #                                              scaling=TILE_SCALING,
        #                                              use_spatial_hash=True)

        #print("---> ", self.startposition_list[0])
        #print(" X ", self.startposition_list[0].center_x)
        #print(" Y ", self.startposition_list[0].center_y)

        #start_XY = tuple((self.startposition_list[0].center_x,self.startposition_list[0].center_y))
        start_XY = tuple((666,666))




        #image_source = "resources/00/rafale_logo.png"

        image_source = "resources/images/Ships/ship0.png"

        
        #self.player_sprite = arcade.Sprite(image_source, CHARACTER_SCALING)
        self.player_sprite = SpriteWithHealth(image_source, CHARACTER_SCALING, max_health = PLAYER_MAX_HEALTH)


        self.player_sprite.center_x = start_XY[0]
        self.player_sprite.center_y = start_XY[1]


        #self.player_list.append(self.player_sprite)
        self.scene.add_sprite("Player", self.player_sprite)

        # *******************************************************************************************
        #self.life_list.append(life)

        for i in range(self.lives):
                life = arcade.Sprite("resources/images/HUD/head_128.png", SCALE)
                self.life_list.append(life)


        #----------------------------------------------------------------------------------------

        #self.crosshair_list = arcade.SpriteList()

        #self.crosshair_sprite = arcade.Sprite("resources/images/HUD/crosshair061.png", 0.4)

        #self.crosshair_relative_xoffset = CROSSHAIR__RELATIVE_XOFFSET_SETUP
        #self.crosshair_relative_yoffset = CROSSHAIR__RELATIVE_YOFFSET_SETUP
      

        #self.crosshair_sprite.center_x = self.player_sprite.center_x + CROSSHAIR__RELATIVE_XOFFSET_SETUP
        #self.crosshair_sprite.center_y = self.player_sprite.center_y + CROSSHAIR__RELATIVE_YOFFSET_SETUP

        #self.crosshair_list.append(self.crosshair_sprite)
        # ///////////

        

        # Used to keep track of our scrolling
        self.view_bottom = 0
        self.view_left = 0

        #self.camera = arcade.Camera(self.window, SCREEN_WIDTH, SCREEN_HEIGHT)           Creating the camera expects width, height, then an optional window parameter. This error occurs when the window is passed in as a size.
        #self.gui_camera = arcade.Camera(self.window, SCREEN_WIDTH, SCREEN_HEIGHT)

        self.camera = arcade.Camera(SCREEN_WIDTH, SCREEN_HEIGHT, self.window)
        self.gui_camera = arcade.Camera(SCREEN_WIDTH, SCREEN_HEIGHT, self.window)

        # Center camera on user
        self.pan_camera_to_user()


    def on_show(self):
        

        # Reset the viewport, necessary if we have a scrolling game and we need
        # to reset the viewport back to the start so we can see what we draw.
        arcade.set_viewport(0, SCREEN_WIDTH - 1, 0, SCREEN_HEIGHT - 1)
        

    def on_draw(self):

        self.camera.use()
        #self.clear()
        self.window.clear()


        arcade.start_render()

        arcade.set_viewport(0, SCREEN_WIDTH - 1, 0, SCREEN_HEIGHT - 1)


        self.background_list.draw()


        self.scene.draw()

        #self.center_on_player()    AttributeError: 'GameView' object has no attribute 'center_on_player'
        #self.camera.center_on_player() # AttributeError: 'Camera' object has no attribute 'center_on_player'


        self.gui_camera.use()

    def update(self, delta_time):

        for background in self.background_list:


            #reset the images when they go past the screen
            if background.bottom == -IMAGE_HEIGHT:
                background.center_y = SCREEN_HEIGHT + IMAGE_WIDTH // 2
        

        self.background_list.update()


    def on_key_press(self, key, modifiers):
        """Called whenever a key is pressed. """
        #if self.player_sprite.amphet_excited is False:
        

        if key == arcade.key.UP:
            self.player_sprite.change_y = MOVEMENT_SPEED
        elif key == arcade.key.DOWN:
            self.player_sprite.change_y = -MOVEMENT_SPEED
        elif key == arcade.key.LEFT:
            self.player_sprite.change_x = -MOVEMENT_SPEED
        elif key == arcade.key.RIGHT:
            self.player_sprite.change_x = MOVEMENT_SPEED


        elif key == arcade.key.ESCAPE:
            raise Exception("\n\n      See You soon, fork it share it !")



 

    def on_key_release(self, key, modifiers):
        """Called when the user releases a key. """

        if key == arcade.key.UP or key == arcade.key.DOWN:
            self.player_sprite.change_y = 0
        elif key == arcade.key.LEFT or key == arcade.key.RIGHT:
            self.player_sprite.change_x = 0


    def pan_camera_to_user(self, panning_fraction: float = 1.0):
        """
        Manage Scrolling
        :param panning_fraction: Number from 0 to 1. Higher the number, faster we
                                 pan the camera to the user.
        """

        print("\n ------->   ")


        print(type(self.camera.viewport_width))


        print(dir(self.camera.viewport_width))

        # This spot would center on the user
        screen_center_x = self.player_sprite.center_x - (self.camera.viewport_width / 2)
        screen_center_y = self.player_sprite.center_y - (
            self.camera.viewport_height / 2
        )
        if screen_center_x < 0:
            screen_center_x = 0
        if screen_center_y < 0:
            screen_center_y = 0
        user_centered = screen_center_x, screen_center_y

        self.camera.move_to(user_centered, panning_fraction)







class InstructionView(arcade.View):

    def __init__(self):
        
        super().__init__()

        arcade.set_viewport(0, SCREEN_WIDTH - 1, 0, SCREEN_HEIGHT - 1)

        self.background = arcade.load_texture("./resources/images/backgrounds/raf_pilot.jpg")

        
        self.music_intro = arcade.load_sound(MUSIC_INTRO)

        self.looping_music = False



        print("type(self.music_intro)   : ", type(self.music_intro))


        self.player_music_intro = None

    
    
    def on_show(self):
        """ This is run once when we switch to this view """
        arcade.set_background_color(arcade.csscolor.DARK_SLATE_BLUE)

        # Reset the viewport, necessary if we have a scrolling game and we need
        # to reset the viewport back to the start so we can see what we draw.
        arcade.set_viewport(0, SCREEN_WIDTH - 1, 0, SCREEN_HEIGHT - 1)

        
        

        #self.player_music_intro.EOS_LOOP = 'loop'
        self.player_music_intro = arcade.play_sound(self.music_intro)
        

        print("type(self.player_music_intro)   : ", type(self.player_music_intro))


    def on_draw(self):
        """ Draw this view """
        arcade.start_render()

        arcade.draw_lrwh_rectangle_textured(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, self.background)



        arcade.draw_text("Instructions Screen", SCREEN_WIDTH / 2, SCREEN_HEIGHT *0.75+200,
                         arcade.color.WHITE, font_size=50, anchor_x="center")
        arcade.draw_text("Click to advance", SCREEN_WIDTH / 2, SCREEN_HEIGHT *0.75+100,
                         arcade.color.WHITE, font_size=20, anchor_x="center")


        


    def on_mouse_press(self, _x, _y, _button, _modifiers):
        """ If the user presses the mouse button, start the game. """
        game_view = GameView()
        game_view.setup(level=1)
        arcade.set_background_color(arcade.csscolor.BLACK)


        try:
            self.music_intro.stop(self.player_music_intro)
        except ValueError:
            print("music already finished")  # ValueError: list.remove(x): x not in list   media.Source._players.remove(player)

        self.window.show_view(game_view)


    def on_update(self, delta_time):
        """ Movement and game logic """
        pass










"""
def main():
    window = MyGame(SCREEN_WIDTH, SCREEN_HEIGHT)
    window.setup()
    arcade.run()
"""







class JoyConfigView(arcade.View):
    """A View that allows a user to interactively configure their joystick"""
    REGISTRATION_PAUSE = 1.5
    NO_JOYSTICK_PAUSE = 2.0
    JOY_ATTRS = ("x", "y", "z", "rx", "ry", "rz")

    def __init__(self, joy_method_names, joysticks, next_view, width, height):
        super().__init__()
        self.next_view = next_view
        self.width = width
        self.height = height
        self.msg = ""
        self.script = self.joy_config_script()
        self.joys = joysticks
        #arcade.set_background_color(arcade.color.WHITE)

        self.background = arcade.load_texture("./resources/images/backgrounds/raf_paysage.jpg")


        if len(joysticks) > 0:
            self.joy = joysticks[0]
            self.joy_method_names = joy_method_names
            self.axis_ranges = {}

    def config_axis(self, joy_axis_label, method_name):
        self.msg = joy_axis_label
        self.axis_ranges = {a: 0.0 for a in self.JOY_ATTRS}
        while max([v for k, v in self.axis_ranges.items()]) < 0.85:
            for attr, farthest_val in self.axis_ranges.items():
                cur_val = getattr(self.joy, attr)
                if abs(cur_val) > abs(farthest_val):
                    self.axis_ranges[attr] = abs(cur_val)
            yield

        max_val = 0.0
        max_attr = None
        for attr, farthest_val in self.axis_ranges.items():
            if farthest_val > max_val:
                max_attr = attr
                max_val = farthest_val
        self.msg = f"Registered!"

        setattr(pyglet.input.base.Joystick, method_name, property(lambda that: getattr(that, max_attr), None))

        # pause briefly after registering an axis
        yield from self._pause(self.REGISTRATION_PAUSE)

    def joy_config_script(self):
        if len(self.joys) == 0:
            self.msg = "No joysticks found!  Use keyboard controls."
            yield from self._pause(self.NO_JOYSTICK_PAUSE)
            return

        for joy_axis_label, method_name in self.joy_method_names:
            yield from self.config_axis(joy_axis_label, method_name)

    def on_update(self, delta_time):
        try:
            next(self.script)
        except StopIteration:
            self.window.show_view(self.next_view)

    def on_draw(self):
        arcade.start_render()
        



        arcade.draw_lrwh_rectangle_textured(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT, self.background)

        #rcade.draw_text("Configure your joystick", self.width/2, self.height/2+100,
        #                 arcade.color.YELLOW, font_size=32, anchor_x="center")

        arcade.draw_text("Configure your joystick", self.width/2, self.height*0.75+100,
                         arcade.color.YELLOW, font_size=32, anchor_x="center")

        arcade.draw_text(self.msg, self.width/2, self.height*0.75,
                         arcade.color.GREEN, font_size=24, anchor_x="center")

    def _pause(self, delay):
        """Block a generator from advancing for the given delay. Call with 'yield from self._pause(1.0)"""
        start = time.time()
        end = start + delay
        while time.time() < end:
            yield




class SpriteWithHealth(arcade.Sprite):
    """ Sprite with hit points """

    def __init__(self, image, scale, max_health):
        super().__init__(image, scale)

        # Add extra attributes for health
        self.max_health = max_health
        self.cur_health = max_health

        # Load sounds. Sounds from kenney.nl
        self.gun_sound = arcade.load_sound("resources/sounds/player_gun.wav")
        self.hit_sound = arcade.load_sound("resources/sounds/player_gun.wav")
        self.death_sound = arcade.load_sound("resources/sounds/player_gun.wav")

        self.respawning = 0


    def respawn(self, xrespawn, yrespawn):
        """
        Called when we die and need to make a new ship.
        'respawning' is an invulnerability timer.
        """
        # If we are in the middle of respawning, this is non-zero.
        self.respawning = 1
        #self.center_x = SCREEN_WIDTH / 2
        #self.center_y = SCREEN_HEIGHT / 2

        self.center_x = xrespawn
        self.center_y = yrespawn

        self.angle = 0

        self.cur_health = self.max_health


    def draw_health_number(self):
        """ Draw how many hit points we have """

        health_string = f"{self.cur_health}/{self.max_health}"
        arcade.draw_text(health_string,
                         start_x=self.center_x + HEALTH_NUMBER_OFFSET_X,
                         start_y=self.center_y + HEALTH_NUMBER_OFFSET_Y,
                         font_size=12,
                         color=arcade.color.WHITE)

    def draw_health_bar(self):
        """ Draw the health bar """

        # Draw the 'unhealthy' background
        if self.cur_health < self.max_health:
            arcade.draw_rectangle_filled(center_x=self.center_x,
                                         center_y=self.center_y + HEALTHBAR_OFFSET_Y,
                                         width=HEALTHBAR_WIDTH,
                                         height=3,
                                         color=arcade.color.RED)

        # Calculate width based on health
        health_width = HEALTHBAR_WIDTH * (self.cur_health / self.max_health)

        arcade.draw_rectangle_filled(center_x=self.center_x - 0.5 * (HEALTHBAR_WIDTH - health_width),
                                     center_y=self.center_y - LIFEBAR_Yoffset,
                                     width=health_width,
                                     height=HEALTHBAR_HEIGHT,
                                     color=arcade.color.GREEN)





def main():

    #window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE, fullscreen=False)
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE, fullscreen=True)

    

    #start_view = GameView()
    #window.show_view(start_view)
    
    #start_view.setup()
    #start_view.setup(level=1)

    start_view = InstructionView()
    #start_view = GameView()

    window.show_view(start_view)









    window.joys = arcade.get_joysticks()
    for j in window.joys:
        j.open()
    joy_config_method_names = (
        #("Move the movement stick left    < ", "move_stick_left"),
        #("Move the movement stick up      ^", "move_stick_up"),
        #("Move the movement stick right   >  ", "move_stick_right"),
        #("Move the movement stick down    V", "move_stick_down"),
        #("Move the shooting stick up or down", "shoot_stick_y"),
        ("Move the movement stick left or right", "move_stick_x"),
        ("Move the movement stick up or down", "move_stick_y"),
    )
    game = InstructionView()
    window.show_view(JoyConfigView(joy_config_method_names, window.joys, game, SCREEN_WIDTH, SCREEN_HEIGHT))

    
    arcade.run()

if __name__ == "__main__":
    main()
