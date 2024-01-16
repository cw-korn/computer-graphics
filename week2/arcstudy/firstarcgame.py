import arcade

# creating game platform
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 650
SCREEN_TITLE = "My First Arcade Game"

CHARACTER_SCALING = 0.4
TILE_SCALING = 0.5
PLAYER_MOVEMENT_SPEED = 5
GRAVITY = 1
PLAYER_JUMP_SPEED = 20
COIN_SCALING = 1

class MyGame(arcade.Window):
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
        arcade.set_background_color(arcade.csscolor.CORNFLOWER_BLUE)
        self.player_list = arcade.SpriteList()
        self.player_sprite = None
        self.scene = None
        self.player_sprite = None
        self.physics_engine = None
        self.camera = None
        self.collect_coin_sound = arcade.load_sound(":resources:sounds/coin1.wav")
        self.jump_sound = arcade.load_sound(":resources:sounds/jump1.wav")
        self.score = 0


    def on_draw(self):
        self.clear()

    def setup(self):
        self.player_sprite = PlayerCharacter()

    def on_update(self, delta_time: float):
        self.scene.update_animation(delta_time, ["Player"])

def main():
    window = MyGame()
    window.setup()
    arcade.run()


if __name__ == "__main__":
    main()

####################################################################################################


def setup(self):
    image_source = ":resources:images/animated_characters/female_adventurer/ femaleAdventurer_idle.png"
    self.player_sprite = arcade.Sprite(image_source, CHARACTER_SCALING, flipped_horizontally=True)
    self.player_sprite.center_x = 500
    self.player_sprite.center_y = 325
    self.player_list.append(self.player_sprite)


def on_draw(self):
    self.player_list.draw()


#############################################################################
# add sprite to scene object


def setup(self):
    self.scene = arcade.Scene()
    self.scene.add_sprite_list("Player")
    self.scene.add_sprite("Player", self.player_sprite)

def on_draw(self):
    self.scene.draw()

# add sprite to scene object
def setup(self):
    self.scene = arcade.Scene()
    coordinate_list = [[512, 96], [256, 96], [768, 96]]
    for coordinate in coordinate_list:
        wall = arcade.Sprite(":resources:images/tiles/boxCrate_double.png", TILE_SCALING)
        wall.position = coordinate
        self.scene.add_sprite("Walls", wall)
    self.scene.add_sprite("Walls", wall)


def on_draw(self):
    self.scene.draw()

################################################################
# add floor to scene object
def setup(self):
    self.scene = arcade.Scene()

    for x in range(0, 1250, 64):
        wall = arcade.Sprite(":resources:images/tiles/grassMid.png", TILE_SCALING)
        wall.center_x = x
        wall.center_y = 32
        self.scene.add_sprite("Walls", wall)


def on_draw(self):
    self.scene.draw()
################################################################
# add custom sprite
    image_source = 'assets/aether.png'
    self.player_sprite = arcade.Sprite(image_source, CHARACTER_SCALING)
###############################################################


# add user control
PLAYER_MOVEMENT_SPEED = 5


# get keyboard input
def on_key_press(self, key, modifiers):
    if key == arcade.key.UP or key == arcade.key.W:
        self.player_sprite.change_y = PLAYER_MOVEMENT_SPEED
    elif key == arcade.key.DOWN or key == arcade.key.S:
        self.player_sprite.change_y = -PLAYER_MOVEMENT_SPEED
    elif key == arcade.key.LEFT or key == arcade.key.A:
        self.player_sprite.change_x = -PLAYER_MOVEMENT_SPEED
    elif key == arcade.key.RIGHT or key == arcade.key.D:
        self.player_sprite.change_x = PLAYER_MOVEMENT_SPEED


# update character location when release keyboard input
def on_key_release(self, key, modifiers):
    if key == arcade.key.UP or key == arcade.key.W:
        self.player_sprite.change_y = 0
    elif key == arcade.key.DOWN or key == arcade.key.S:
        self.player_sprite.change_y = 0
    elif key == arcade.key.LEFT or key == arcade.key.A:
        self.player_sprite.change_x = 0
    elif key == arcade.key.RIGHT or key == arcade.key.D:
        self.player_sprite.change_x = 0


##############################################################################################################################
# add user control physics



def setup(self):
    self.physics_engine = arcade.PhysicsEngineSimple(
        self.player_sprite, self.scene.get_sprite_list("Walls")
    )

    self.physics_engine = arcade.PhysicsEngineSimple(
    self.player_sprite, self.scene.get_sprite_list("Walls")
)

#update character physics

def on_update(self, delta_time):
    self.physics_engine.update()

##########################################################
# add player gravity
GRAVITY = 1
PLAYER_JUMP_SPEED = 20

def setup(self):
    # Create the 'physics engine'
    self.physics_engine = arcade.PhysicsEnginePlatformer(
        self.player_sprite, gravity_constant=GRAVITY, walls=self.scene["Walls"]
    )


def on_key_press(self, key, modifiers):
    """Called whenever a key is pressed."""
    if key == arcade.key.UP or key == arcade.key.W:
        if self.physics_engine.can_jump():
            self.player_sprite.change_y = PLAYER_JUMP_SPEED
    elif key == arcade.key.LEFT or key == arcade.key.A:
        self.player_sprite.change_x = -PLAYER_MOVEMENT_SPEED
    elif key == arcade.key.RIGHT or key == arcade.key.D:
        self.player_sprite.change_x = PLAYER_MOVEMENT_SPEED

##########################################################
# add camera follow player



def setup(self):
    self.camera = arcade.Camera(self.width, self.height)


def on_draw(self):
    self.camera.use()


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


def on_update(self, delta_time):
    self.center_camera_to_player()


# add interaction objects and sound
COIN_SCALING = 0.2




def setup(self):

    for x in range(128, 1250, 256):
        coin = arcade.Sprite("assets/primogem.png", COIN_SCALING)
        coin.center_x = x
        coin.center_y = 96
        self.scene.add_sprite("Coins", coin)


def on_key_press(self, key, modifiers):
    if key == arcade.key.UP or key == arcade.key.W:
        if self.physics_engine.can_jump():
            self.player_sprite.change_y = PLAYER_JUMP_SPEED
            arcade.play_sound(self.jump_sound)


def on_update(self, delta_time):
    coin_hit_list = arcade.check_for_collision_with_list(self.player_sprite, self.scene["Coins"])
    for coin in coin_hit_list:
        coin.remove_from_sprite_lists()  # Remove the coin
        arcade.play_sound(self.collect_coin_sound)  # Play a sound

##############################################################################################################################
# add text gui



def setup(self):
    self.score = 0

def on_draw(self):
    score_text = f"Score: {self.score}"
    arcade.draw_text(score_text, 10, 10, arcade.csscolor.WHITE, 18, )

def on_update(self, delta_time):
    coin_hit_list = arcade.check_for_collision_with_list(self.player_sprite, self.scene["Coins"])
    for coin in coin_hit_list:
        coin.remove_from_sprite_lists()  # Remove the coin
        arcade.play_sound(self.collect_coin_sound)  # Play a sound
        self.score += 1  # Add one to the score


# control texture
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

        self.idle_texture_pair = load_texture_pair("Assets/aether_idle.png")
        self.walk_texture_pair = load_texture_pair("Assets/aether.png")
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


#############################################
# add custom sprite to scene object
class MyGame(arcade.Window):

    def setup(self):
        self.player_sprite = PlayerCharacter()

    def on_update(self, delta_time: float):
        self.scene.update_animation(delta_time, ["Player"])


