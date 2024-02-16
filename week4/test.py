import arcade

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 650
SCREEN_TITLE = "My first game"

CHARACTER_SCALE = 0.4
TILE_SCALE = 0.5
RIGHT_FACING = 0
LEFT_FACING = 1

PLAYER_SPEED = 5
GRAVITY = 1
PLAYER_JUMP_SPEED = 20


COIN_SCALE = 0.2

def load_texture_pair(filename):
    return [
        arcade.load_texture(filename, flipped_horizontally = True),
        arcade.load_texture(filename)
    ]


class PlayerCharacter(arcade.Sprite):
    def __init__(self):
        super().__init__()

        self.character_face_direction = RIGHT_FACING
        self.scale = CHARACTER_SCALE

        self.idle_texture_pair = load_texture_pair("assets/aether_idle.png")
        self.walk_texture_pair = load_texture_pair("assets/aether.png")
        self.texture = self.idle_texture_pair[0]

    def update_animation (self,delta_time: float = 1/60):
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

        self.scene = None
        self.player_sprite = None

        self.physics_engine = None
        self.camera = None
        self.gui_camera = None
        self.score = 0

        self.collect_sound = arcade.load_sound(":resources:sounds/coin1.wav")
        self.jump_sound = arcade.load_sound(":resources:sounds/jump1.wav")

    def setup(self):
        self.scene = arcade.Scene()
        self.camera = arcade.Camera(self.width, self.height)
        self.gui_camera = arcade.Camera(self.width, self.height)
        self.score = 0

        #image_path = ":resources:images/animated_characters/female_adventurer/femaleAdventurer_idle.png"
        #image_path = "Assets/aether.png"
        #self.player_sprite = arcade.Sprite(image_path, CHARACTER_SCALE, flipped_horizontally=True)
        self.player_sprite = PlayerCharacter()
        self.player_sprite.center_y = 128
        self.player_sprite.center_x = 64
        self.scene.add_sprite("Player",self.player_sprite)

        coordinate_list = [[512, 96], [256, 96], [768, 96]]
        for coordinate in coordinate_list:  #print walls 3 times
            wall = arcade.Sprite(":resources:images/tiles/boxCrate_double.png", TILE_SCALE)
            wall.position = coordinate
            self.scene.add_sprite("Walls", wall)

        for x in range(0,1500,64):
            floor = arcade.Sprite(":resources:images/tiles/grassMid.png", TILE_SCALE)
            floor.center_x = x
            floor.center_y = 32
            self.scene.add_sprite("Walls", floor)

        self.physics_engine = arcade.PhysicsEnginePlatformer(
            self.player_sprite, gravity_constant= GRAVITY, walls = self.scene.get_sprite_list("Walls")
            #self.player_sprite, self.scene.get_sprite_list("Walls")
        )

        for x in range(128, 1300, 256):
            coin = arcade.Sprite("Assets/primogem.png", COIN_SCALE)
            coin.center_y = 96
            coin.center_x = x
            self .scene.add_sprite("Coin", coin)


    def on_update(self, delta_time: float):
        self.physics_engine.update()
        self.scene.update_animation(delta_time, ["Player"])

        coin_hit = arcade.check_for_collision_with_list(self.player_sprite, self.scene.get_sprite_list("Coin"))
        for coin in coin_hit:
            coin.remove_from_sprite_lists()
            arcade.play_sound(self.collect_sound)
            self.score += 1

        self.center_camera_to_player()

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
        self.gui_camera.use()

        self.scene.draw()

        score_text = f"Score: {self.score}"
        arcade.draw_text(score_text, 10, 10, arcade.csscolor.WHITE, 18)
        #self.scene.draw()

    def center_camera_to_player(self):
        screen_center_x = self.player_sprite.center_x - (self.camera.viewport_width /2)
        screen_center_y = self.player_sprite.center_y - (self.camera.viewport_height /2)

        if screen_center_x < 0:
            screen_center_x = 0
        if screen_center_y < 0:
            screen_center_y = 0
        player_center = screen_center_x, screen_center_y
        self.camera.move_to(player_center)
def main():
    window = MyGame()
    window.setup()
    arcade.run()

if __name__ == "__main__":
    main()