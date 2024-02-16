import arcade

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 650
SCREEN_TITLE = "My Arcade Exam"
CHARACTER_SCALE = 0.4
TILE_SCALE = 0.5
RIGHT_FACING = 0
LEFT_FACING = 1
PLAYER_SPEED = 5
PLAYER_JUMP_SPEED = 20
GRAVITY = 1
TILE_SCALE = 0.5

class MyGame(arcade.Window):
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
        arcade.set_background_color(arcade.csscolor.CORNFLOWER_BLUE)

        self.scene = None
        self.physics_engine = None
        self.camera = None
        self.gui_camera = None
        self.score = 0
        self.collect_sound = arcade.load_sound(":resources:sounds/coin1.wav")
        self.jump_sound = arcade.load_sound(":resources:sounds/jump1.wav")

    def center_camera_to_player(self):
        screen_center_x = self.player_sprite.center_x - (self.camera.viewport_width /2)
        screen_center_y = self.player_sprite.center_y - (self.camera.viewport_height /2)

        if screen_center_x < 0:
            screen_center_x = 0
        if screen_center_y < 0:
            screen_center_y = 0
        player_center = screen_center_x, screen_center_y
        self.camera.move_to(player_center)    

    def setup(self):
        #camera setup
        self.scene = arcade.Scene()
        self.camera = arcade.Camera(self.width, self.height)
        self.gui_camera = arcade.Camera(self.width, self.height)
        self.score = 0

        #scene and player setup
        self.scene = arcade.Scene()
        self.player_sprite = PlayerCharacter()
        self.player_sprite.center_y = 128
        self.player_sprite.center_x = 64
        self.scene.add_sprite("Player",self.player_sprite)
        
        
        for x in range(0,1500, 64):
            floor = arcade.Sprite(":resources:images/tiles/grassMid.png",TILE_SCALE)
            floor.center_x = x
            floor.center_y = 32
            self.scene.add_sprite("Walls", floor)
        #add gravity
        self.physics_engine = arcade.PhysicsEnginePlatformer(
            self.player_sprite, gravity_constant= GRAVITY, walls = self.scene.get_sprite_list("Walls")
            #self.player_sprite, self.scene.get_sprite_list("Walls")
        )


        for y in range(0, 700, 64):
            wall = arcade.Sprite(":resources:images/tiles/boxCrate_double.png", TILE_SCALE, center_x=0, center_y= y)
            self.scene.add_sprite("Walls", wall)
            wall = arcade.Sprite(":resources:images/tiles/boxCrate_double.png", TILE_SCALE, center_x=1500, center_y= y)
            self.scene.add_sprite("Walls", wall)

        for x in range(320,640, 64):
            floor = arcade.Sprite(":resources:images/tiles/grassHalf_mid.png",TILE_SCALE)
            floor.center_x = x
            floor.center_y = 200
            self.scene.add_sprite("Walls", floor)

        for x in range(720,1000, 64):
            floor = arcade.Sprite(":resources:images/tiles/grassHalf_mid.png",TILE_SCALE)
            floor.center_x = x
            floor.center_y = 320
            self.scene.add_sprite("Walls", floor)

        coordinate_list = [[1240, 96], [512, 280], [768, 400]]
        for coordinate in coordinate_list:
            star = arcade.Sprite(":resources:images/items/star.png", 0.5)
            star.position = coordinate
            self.scene.add_sprite("Collect", star)

        flag = arcade.Sprite(":resources:images/items/flagRed2.png", 0.5)
        flag.center_y = 96
        flag.center_x = 1024
        self.scene.add_sprite("Flag", flag)

    def on_update(self, delta_time: float):
        self.center_camera_to_player()
        self.physics_engine.update()
        self.scene.update_animation(delta_time, ["Player"])

        star_hit = arcade.check_for_collision_with_list(self.player_sprite, self.scene.get_sprite_list("Collect"))
        for star in star_hit:
            star.remove_from_sprite_lists()
            arcade.play_sound(self.collect_sound)
            self.score += 1
        
        flag_hit = arcade.check_for_collision_with_list(self.player_sprite, self.scene.get_sprite_list("Flag"))
        for flag in flag_hit:
            if self.score == 3:
                #self.has_won = True  # Set the flag to True when the condition is met
    

    def on_key_press(self, key, modifiers):
        if key == arcade.key.UP or key == arcade.key.W:
            if self.physics_engine.can_jump():
                self.player_sprite.change_y = PLAYER_JUMP_SPEED
                arcade.play_sound(self.jump_sound)
        elif key == arcade.key.DOWN or key == arcade.key.S:
            self.player_sprite.change_y = -PLAYER_SPEED
        elif key == arcade.key.LEFT or key == arcade.key.A:
            self.player_sprite.change_x = -PLAYER_SPEED
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.player_sprite.change_x = PLAYER_SPEED

    def on_key_release(self, key, modifiers):
        if key == arcade.key.UP or key == arcade.key.W:
            self.player_sprite.change_y = 0
        elif key == arcade.key.DOWN or key == arcade.key.S:
            self.player_sprite.change_y = 0
        elif key == arcade.key.LEFT or key == arcade.key.A:
            self.player_sprite.change_x = 0
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.player_sprite.change_x = 0

    def on_draw(self):
        self.clear()
        self.camera.use()
        self.scene.draw()
        self.gui_camera.use()
        score_text = f"STAR:{self.score}"
        arcade.draw_text (score_text, 10, 10, arcade.csscolor.BLUE_VIOLET, 18)

        #if self.has_won:
        #    arcade.draw_text("You Win", 400, 300, arcade.csscolor.GREEN, 40)



#this function is created for player character class loading files
def load_texture_pair(filename):
    return [arcade.load_texture(filename,flipped_horizontally=True),arcade.load_texture(filename)]

#import from lab
class PlayerCharacter(arcade.Sprite):
    def __init__(self):
        super().__init__()

        self.character_face_direction = RIGHT_FACING
        self.scale = CHARACTER_SCALE
    
        self.idle_texture_pair = load_texture_pair("computer-graphics/week4/assets/aether_idle.png")
        self.walk_texture_pair = load_texture_pair("computer-graphics/week4/assets/aether_walk0.png")
        self.texture = self.idle_texture_pair[0]
        self.win_trigger = 1

    def update_animation (self,delta_time: float = 1/60):
        if self.change_x < 0 and self.character_face_direction == RIGHT_FACING:
            self.character_face_direction = LEFT_FACING
        elif self.change_x > 0 and self.character_face_direction == LEFT_FACING:
            self.character_face_direction = RIGHT_FACING

        if self.change_x == 0 and self.change_y == 0 and self.change_y < 200:
            self.texture = self.idle_texture_pair[self.character_face_direction]
            return
        self.texture = self.walk_texture_pair[self.character_face_direction] 

def main():
    window = MyGame()
    window.setup()
    arcade.run()

if __name__ == "__main__":
    main()