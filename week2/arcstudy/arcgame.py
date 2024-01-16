import arcade

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 650
SCREEN_TITLE = "My First Arcade Game"
CHARACTER_SCALING = 0.5
TILE_SCALING = 0.5
COIN_SCALING = 0.2
PLAYER_MOVEMENT_SPEED = 5
PLAYER_JUMP_SPEED = 15
GRAVITY = 1

RIGHT_FACING = 0
LEFT_FACING = 1


def load_texture_pair(filename):
   return [
       arcade.load_texture(filename, flipped_horizontally=True),
       arcade.load_texture(filename)
   ]


class PlayerCharacter(arcade.Sprite):
   def __init__(self):
       super().__init__()
       self.character_face_direction = RIGHT_FACING
       self.scale = CHARACTER_SCALING
       self.idle_texture_pair = load_texture_pair("assets/aether_idle.png")
       self.walk_texture_pair = load_texture_pair("assets/aether.png")
       self.texture = self.idle_texture_pair[0]

   def update_animation(self, delta_time: float = 1 / 60):
       if self.change_x < 0 and self.character_face_direction == RIGHT_FACING:
           self.character_face_direction = LEFT_FACING
       elif self.change_x > 0 and self.character_face_direction == LEFT_FACING:
           self.character_face_direction = RIGHT_FACING
       if self.change_x == 0 and self.change_y == 0 and self.change_y < 200:
           self.texture = self.idle_texture_pair[self.character_face_direction]
           return
       self.texture = self.walk_texture_pair[self.character_face_direction]


class MyGame(arcade.Window):
   def __init__(self):
       super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
       arcade.set_background_color(arcade.csscolor.CORNFLOWER_BLUE)

       # Initialize player variables
       self.player_list = arcade.SpriteList()
       self.player_sprite = None

       # Initialize wall variables
       self.wall_list = arcade.SpriteList()

       # Initialize coin variables
       self.coin_list = arcade.SpriteList()

       # Our physics engine
       self.physics_engine = None

       # Camera
       self.camera = None

       # Sounds
       self.collect_coin_sound = arcade.load_sound(":resources:sounds/coin1.wav")
       self.jump_sound = arcade.load_sound(":resources:sounds/jump1.wav")

       # Score
       self.score = 0

   def setup(self):
       # Set up the game
       self.player_sprite = PlayerCharacter()
       self.player_sprite.center_x = 500
       self.player_sprite.center_y = 325
       self.player_list.append(self.player_sprite)

       # Add walls using the specified x coordinates
       for x in range(0, 1250, 64):
           wall = arcade.Sprite(":resources:images/tiles/grassMid.png", TILE_SCALING)
           wall.center_x = x
           wall.center_y = 32
           self.wall_list.append(wall)

       # Additional walls with specified coordinates
       coordinate_list = [[512, 96], [256, 96], [768, 96]]
       for coordinate in coordinate_list:
           wall = arcade.Sprite(":resources:images/tiles/boxCrate_double.png", TILE_SCALING)
           wall.position = coordinate
           self.wall_list.append(wall)

       # Create the 'physics engine'
       self.physics_engine = arcade.PhysicsEnginePlatformer(
           self.player_sprite, gravity_constant=GRAVITY, walls=self.wall_list
       )

       # Camera setup
       self.camera = arcade.Camera(self.width, self.height)

       # Add coins to the scene
       for x in range(128, 1250, 256):
           coin = arcade.Sprite("assets/primogem.png", COIN_SCALING)
           coin.center_x = x
           coin.center_y = 96
           self.coin_list.append(coin)

       # Reset the score
       self.score = 0

   def on_draw(self):
       # Draw everything using the camera
       self.camera.use()
       arcade.start_render()
       self.player_list.draw()
       self.wall_list.draw()
       self.coin_list.draw()

       # Draw the score on the screen
       score_text = f"Score: {self.score}"
       arcade.draw_text(score_text, 10, 10, arcade.csscolor.WHITE, 18)

   def on_key_press(self, key, modifiers):
       """Called whenever a key is pressed."""
       if key == arcade.key.UP or key == arcade.key.W:
           if self.physics_engine.can_jump():
               self.player_sprite.change_y = PLAYER_JUMP_SPEED
               arcade.play_sound(self.jump_sound)
       elif key == arcade.key.LEFT or key == arcade.key.A:
           self.player_sprite.change_x = -PLAYER_MOVEMENT_SPEED
       elif key == arcade.key.RIGHT or key == arcade.key.D:
           self.player_sprite.change_x = PLAYER_MOVEMENT_SPEED

   def on_key_release(self, key, modifiers):
       """Called whenever a key is released."""
       if key == arcade.key.LEFT or key == arcade.key.A or key == arcade.key.RIGHT or key == arcade.key.D:
           self.player_sprite.change_x = 0

   def on_update(self, delta_time):

       # Update character physics
       self.physics_engine.update()

       # Center camera to player
       self.center_camera_to_player()

       # Check for collisions with coins
       coin_hit_list = arcade.check_for_collision_with_list(self.player_sprite, self.coin_list)
       for coin in coin_hit_list:
           coin.remove_from_sprite_lists()  # Remove the coin
           arcade.play_sound(self.collect_coin_sound)  # Play a sound
           self.score += 1  # Add one to the score

       self.player_sprite.update_animation(delta_time)

   def center_camera_to_player(self):
       screen_center_x = self.player_sprite.center_x - (self.camera.viewport_width / 2)
       screen_center_y = self.player_sprite.center_y - (self.camera.viewport_height / 2)

       # Don't let camera travel past 0
       if screen_center_x < 0:
           screen_center_x = 0
       if screen_center_y < 0:
           screen_center_y = 0

       player_centered = screen_center_x, screen_center_y
       self.camera.move_to(player_centered)


def main():
   window = MyGame()
   window.setup()
   arcade.run()


if __name__ == "__main__":
   main()


