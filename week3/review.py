import arcade
import random

#global variables
#setting up the window 
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 650
SCREEN_TITLE = "otter recreate"
UPDATES_PER_FRAME = 5

#object value setup
PLAYER_MOVEMENT_SPEED = 5
CHARACTER_SCALING = 0.15
RIGHT_FACING = 0
LEFT_FACING = 1

#object scaling
TILE_SCALING = 0.8
ITEM_SCALING = 0.1
SLIME_SCALING = 0.3

#this function is created for player character class loading files
def load_texture_pair(filename):
    return [arcade.load_texture(filename,flipped_horizontally=True),arcade.load_texture(filename)]

#playercharacter setup--------------------------------------------------------------------------------------------------
class PlayerCharacter(arcade.Sprite): 
    def __init__(self):
        super().__init__()
        self.character_face_direction = RIGHT_FACING
        self.scale = CHARACTER_SCALING
        self.cur_texture = 0
        self.idle_texture_pair = load_texture_pair("computer-graphics/week3/assets/otter1.png") 
        self.walk_textures = [load_texture_pair("computer-graphics/week3/assets/otter2.png"),load_texture_pair("computer-graphics/week3/assets/otter1.png")]   
        self.texture = self.idle_texture_pair[0]
        
            
    def update_animation (self,delta_time: float = 1/60):
        #when character is changing direction
        if self.change_x < 0 and self.character_face_direction == RIGHT_FACING:
            self.character_face_direction = LEFT_FACING
        elif self.change_x > 0 and self.character_face_direction == LEFT_FACING:
            self.character_face_direction = RIGHT_FACING        
        #when the character is not moving
        if self.change_x == 0 and self.change_y ==0:
            self.texture=self.idle_texture_pair[self.character_face_direction]
            return
        self.cur_texture +=1 #updating current texture index
        # Check if the current texture index exceeds the limit for walking animation
        if self.cur_texture > 2 * UPDATES_PER_FRAME:
            self.cur_texture = 0
        # Calculate the frame number for the walking animation
        frame = self.cur_texture //UPDATES_PER_FRAME
        # Set the texture based on the walking animation frame and character direction
        self.texture = self.walk_textures[frame - 1][self.character_face_direction]
        

#item setup--------------------------------------------------------------------------------------------------
class item(arcade.Sprite):
    def update(self):
        self.center_y -=1
        #when item go under the screen then reset position
        if self.top<0:
            self.reset_pos()
    #reset positions to on top of the screen with buffer    
    def reset_pos(self):
        self.center_y = random.randrange(SCREEN_HEIGHT + 20, SCREEN_HEIGHT + 100)
        self.center_x = random.randrange(SCREEN_WIDTH)   
        
#enemy setup--------------------------------------------------------------------------------------------------
class Enemy (arcade.Sprite):
    def update(self):
        self.center_x -= 2
        if self.left < 0:
            self.reset_pos()

    def reset_pos(self):
        self.center_x = random.randrange(SCREEN_WIDTH,SCREEN_WIDTH +100)
        self.center_y = random.randrange(SCREEN_HEIGHT)

#game set up--------------------------------------------------------------------------------------------------
class MyGame(arcade.Window):
    def __init__(self):
        super().__init__(SCREEN_WIDTH, SCREEN_HEIGHT,SCREEN_TITLE)
        arcade.set_background_color(arcade.csscolor.CORNFLOWER_BLUE)
        self.scene = None
        self.physics_engine = None
        self.physics_engine = None
        self.item_sprite_list =None
        self.collect_sound = arcade.load_sound(":resources:sounds/coin1.wav")
        self.hit_sound = arcade.load_sound(":resources:sounds/hurt4.wav")
        self.gui_camera = arcade.Camera(self.width, self.height)
        self.score = 0
        self.life = 3  # Add a life counter here

    def setup(self):
        self.scene = arcade.Scene()
        self.player_sprite = PlayerCharacter() #From character class--> import player
        self.player_sprite
        self.player_sprite.center_x = 64
        self.player_sprite.center_y = 128
        self.scene.add_sprite("Player", self.player_sprite)
        self.gui_camera = arcade.Camera(self.width, self.height)
        self.score = 0

        #add rocks on the scene
        coordinate_list = [[512, 96], [256, 96], [768, 96], [512, 300], [256, 300], [768, 300], [512, 550], [256, 550], [768, 550]]
        i = 0
        for coordinate in coordinate_list:
            i += 1
            rock = arcade.Sprite(
                f":resources:images/space_shooter/meteorGrey_big{1 + (i % 4)}.png", TILE_SCALING
            )
            rock.position = coordinate
            self.scene.add_sprite("obstacles", rock)

        #add physics into the game make player can't go through rocks   
        self.physics_engine = arcade.PhysicsEngineSimple(
            self.player_sprite, walls=self.scene["obstacles"]
        )

        #spawing shells from the top
        self.item_sprite_list = arcade.SpriteList()
        for i in range(20):
            shell = item("computer-graphics/week3/assets/shell.png", ITEM_SCALING)
            shell.center_x = random.randrange(SCREEN_WIDTH)
            shell.center_y = random.randrange(SCREEN_HEIGHT)
            self.item_sprite_list.append(shell)

        #spawning random slimes
        self.enemy_sprite_list = arcade.SpriteList()
        for i in range(7):
            slime = Enemy(f"computer-graphics/week3/assets/slime{i}.png", SLIME_SCALING)
            slime.center_x = random.randrange(SCREEN_WIDTH)
            slime.center_y = random.randrange(SCREEN_HEIGHT)
            self.enemy_sprite_list.append(slime)

    def on_draw(self):
        #clear cashe?
        self.clear()
        #make scene
        self.scene.draw()
        #make shell
        self.item_sprite_list.draw()
        #make enemy
        self.enemy_sprite_list.draw()
        #display life and score
        self.gui_camera.use()
        score_text = f"SCORE:{self.score}"
        arcade.draw_text (score_text, 10, 10, arcade.csscolor.BLUE_VIOLET, 18)

        lifetext = f"LIFE: {self.life}"
        arcade.draw_text(lifetext, 10, 600, arcade.csscolor.RED,24)

        if self.score ==20:
            self.enemy_sprite_list.clear()
            self.item_sprite_list.clear()            
            arcade.draw_text("You Win", 400, 300,arcade.csscolor.GREEN,40)
        elif self.life == 0: 
            self.enemy_sprite_list.clear()
            self.item_sprite_list.clear()
            arcade.draw_text("You Lose", 400, 300,arcade.csscolor.DARK_RED,40)

    def on_key_press(self,key,modifiers):
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

    def on_update(self,delta_time):
        self.physics_engine.update()
        self.item_sprite_list.update()
        self.player_sprite.update_animation()

        item_hit_list = arcade.check_for_collision_with_list(
            self.player_sprite, self.item_sprite_list
        )
        #when hit with shell remove that shell
        for item in item_hit_list:
            item.remove_from_sprite_lists()
            arcade.play_sound(self.collect_sound)
        #increase score
        for item in item_hit_list:
            self.score += 1

        #when hit with enemy remove that shell
        self.enemy_sprite_list.update()
        slime_hit = arcade.check_for_collision_with_list(
            self.player_sprite, self.enemy_sprite_list
        )
        for slime in slime_hit:
            slime.remove_from_sprite_lists()
            arcade.play_sound(self.hit_sound)
        #decrease score
        for slime in slime_hit:
            self.life -= 1
# for running the game--------------------------------------------------------------------------------------------------
def main():
    window = MyGame()
    window.setup()
    arcade.run()

if __name__ == "__main__":
    main()