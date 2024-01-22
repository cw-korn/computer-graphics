import arcade
import random
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 650
SCREEN_TITLE = "My First Arcade Game"

PLAYER_MOVEMENT_SPEED = 5
CHARACTER_SCALING = 0.15
RIGHT_FACING = 0
LEFT_FACING = 1
UPDATES_PER_FRAME = 5

TILE_SCALING = 0.8
ITEM_SCALING = 0.1

def load_texture_pair(filename):
    return [arcade.load_texture(filename,flipped_horizontally=True),arcade.load_texture(filename)]


class PlayerCharacter(arcade.Sprite):
    def __init__(self):
        super().__init__()
        self.character_face_direction = RIGHT_FACING
        self.scale = CHARACTER_SCALING
        self.cur_texture = 0

        self.idle_texture_pair = load_texture_pair("week3/assets/otter1.png")
        self.walk_textures = [load_texture_pair("week3/assets/otter2.png"),load_texture_pair("week3/assets/otter1.png")]
        self.texture = self.idle_texture_pair[0]

    def update_animation (self, delta_time: float = 1/60):
        if self.change_x < 0 and self.character_face_direction == RIGHT_FACING:
            self.character_face_direction = LEFT_FACING
        elif self.change_x > 0 and self.character_face_direction == LEFT_FACING:
            self.character_face_direction = RIGHT_FACING

        if self.change_x == 0 and self.change_y ==0:
            self.texture=self.idle_texture_pair[self.character_face_direction]
            return

        self.cur_texture +=1
        if self.cur_texture > 2 * UPDATES_PER_FRAME:
            self.cur_texture = 0
        frame = self.cur_texture //UPDATES_PER_FRAME
        self.texture = self.walk_textures[frame - 1][self.character_face_direction]

class item(arcade.Sprite):
    def update(self):
        self.center_y -=1
        if self.top<0:
            self.reset_pos()

    def reset_pos(self):
        self.center_y = random.randrange(SCREEN_HEIGHT + 20, SCREEN_HEIGHT + 100)
        self.center_x = random.randrange(SCREEN_WIDTH)

class MyGame(arcade.Window):
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)
        arcade.set_background_color(arcade.csscolor.CORNFLOWER_BLUE)
        self.scene = None
        self.player_sprite = None
        self.physics_engine = None
        self.item_sprite_list =None
        self.collect_sound = arcade.load_sound(":resources:sounds/coin1.wav")
        self.gui_camera = arcade.Camera(self.width, self.height)
        self.score = 0
        self.life = 3  # Add a life counter here

    def setup(self):
        self.scene = arcade.Scene()
        image_source = 'week3/assets/otter1.png'
        #self.player_sprite = arcade.Sprite(image_source, CHARACTER_SCALING, flipped_horizontally=True)
        self.player_sprite = PlayerCharacter()
        self.player_sprite.center_x = 64
        self.player_sprite.center_y = 128
        self.scene.add_sprite("Player",self.player_sprite)
        self.physics_engine = arcade.PhysicsEngineSimple(
            self.player_sprite, walls=None
        )
        coordinate_list = [[512, 96], [256, 96], [768, 96], [512, 300], [256, 300], [768, 300], [512, 550], [256, 550],
                           [768, 550]]
        i = 0
        for coordinate in coordinate_list:
            i += 1
            # Add a crate on the ground
            rock = arcade.Sprite(
                f":resources:images/space_shooter/meteorGrey_big{1 + (i % 4)}.png", TILE_SCALING
            )
            rock.position = coordinate
            self.scene.add_sprite("obstacles", rock)

        self.physics_engine = arcade.PhysicsEngineSimple(
            self.player_sprite, walls=self.scene["obstacles"]
        )
        self.item_sprite_list = arcade.SpriteList()

        for i in range(20):
            shell = item("week3/assets/shell.png", ITEM_SCALING)
            #shell = arcade.Sprite("assets/shell.png", ITEM_SCALING)
            shell.center_x = random.randrange(SCREEN_WIDTH)
            shell.center_y = random.randrange(SCREEN_HEIGHT)
            self.item_sprite_list.append(shell)

    def on_draw(self):
        self.clear()
        self.scene.draw()
        self.item_sprite_list.draw()

        self.gui_camera.use()
        score_text = f"SCORE:{self.score}"
        arcade.draw_text (score_text, 10, 10, arcade.csscolor.BLUE_VIOLET, 18)

        lifetext = f"LIFE: {self.life}"
        arcade.draw_text(lifetext, 10, 600, arcade.csscolor.RED,24)

        if self.score ==20:
            arcade.draw_text("You Win", 400, 300,arcade.csscolor.GREEN,40)


    def on_key_press(self, key, modifiers):
        if key == arcade.key.UP or key == arcade.key.W:
            self.player_sprite.change_y = PLAYER_MOVEMENT_SPEED
        elif key == arcade.key.DOWN or key == arcade.key.S:
            self.player_sprite.change_y = -PLAYER_MOVEMENT_SPEED
        elif key == arcade.key.LEFT or key == arcade.key.A:
            self.player_sprite.change_x = -PLAYER_MOVEMENT_SPEED
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.player_sprite.change_x = PLAYER_MOVEMENT_SPEED

    def on_key_release(self, key, modifiers):
        if key == arcade.key.UP or key == arcade.key.W:
            self.player_sprite.change_y = 0
        elif key == arcade.key.DOWN or key == arcade.key.S:
            self.player_sprite.change_y = 0
        elif key == arcade.key.LEFT or key == arcade.key.A:
            self.player_sprite.change_x = 0
        elif key == arcade.key.RIGHT or key == arcade.key.D:
            self.player_sprite.change_x = 0

    def on_update(self, delta_time):
        self.physics_engine.update()
        item_hit_list = arcade.check_for_collision_with_list(
            self.player_sprite, self.item_sprite_list
        )
        for item in item_hit_list:
            item.remove_from_sprite_lists()
            arcade.play_sound(self.collect_sound)
        self.item_sprite_list.update()
        for item in item_hit_list:
            self.score +=1
        self.player_sprite.update_animation()


def main():
    window = MyGame()
    window.setup()
    arcade.run()

if __name__ == "__main__":
    main()
