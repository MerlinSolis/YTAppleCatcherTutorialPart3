from raylib import *
from pyray import *
from os.path import join
from random import randint,uniform

class Apple:
    def __init__(self,texture,position,max_vel):
        self.texture = texture
        self.position = position
        self.direction = Vector2(0,1)
        self.max_vel = max_vel
        self.y_velocity = 0
        self.acceleration_rate = randint(10,400)
        self.active = True
        self.visible = False

    def update(self,delta_time):
        self.y_velocity += self.acceleration_rate * delta_time

        self.position.y += self.y_velocity * delta_time * self.direction.y

        if self.position.y > get_screen_height():
            self.active = False

        if self.position.y > 0 and self.position.y < get_screen_height():
            self.visible = True
        else:
            self.visible = False


    def draw(self):
        if self.visible:
            draw_texture_v(self.texture,self.position,WHITE)

class Player:
    def __init__(self,texture,position,speed):
        self.texture = texture
        self.position = position
        self.speed = speed
        self.direction = Vector2()

    def update(self,delta_time):

        # if is_key_down(KEY_A):
        #     self.direction.x = -1
        # elif is_key_down(KEY_D):
        #     self.direction.x = 1
        # else:
        #     self.direction.x = 0

        self.direction.x = is_key_down(KEY_D) - is_key_down(KEY_A)


        self.position.x += self.speed * self.direction.x * delta_time

        if self.position.x < 0:
            self.position.x = 0
        elif self.position.x + self.texture.width > get_screen_width():
            self.position.x = get_screen_width() - self.texture.width


    def draw(self):
        draw_texture_v(self.texture,self.position,WHITE)

class Game:
    def __init__(self):
        self.screen_width = 1600
        self.screen_height = 900
        self.title = "Apple Catcher Game"
        self.fps_cap = 60
        init_window(self.screen_width,self.screen_height,self.title)
        set_target_fps(self.fps_cap)

        player_texture = load_texture(join("assets","images","basket.png"))
        player_texture.width //= 2
        player_texture.height //= 2

        self.player_basket = Player(player_texture,Vector2(self.screen_width/2 - player_texture.width/2,self.screen_height * 0.85),self.screen_width)

        bg_texture = load_texture(join("assets","images","bg_forest_image.png"))
        # self.bg_texture.width = self.screen_width
        # self.bg_texture.height = self.screen_height
        temp_img = load_image_from_texture(bg_texture)
        image_resize_nn(temp_img,self.screen_width,self.screen_height)
        self.bg_texture_resized = load_texture_from_image(temp_img)


        apple_image = load_image(join("assets","images","apple_1.png"))
        image_resize_nn(apple_image,42,40)
        self.apple_texture = load_texture_from_image(apple_image)
        # self.apple_texture = load_texture(join("assets","images","apple_1.png"))
        # self.apple_test = Apple(self.apple_texture,Vector2(self.screen_width/2,0),2*self.screen_height)

        self.apple_list = []
        self.max_apple = 5
        self.apple_last_spawn_time = 0
        self.apple_spawn_interval = uniform(0.5,2.5)


    def apple_spawner(self):

        if len(self.apple_list) < 5:
            if get_time() > self.apple_last_spawn_time + self.apple_spawn_interval:
                rand_x = randint(0,self.screen_width - self.apple_texture.width)
                rand_y = randint(-self.screen_height,0)
                self.apple_list.append(Apple(self.apple_texture,Vector2(rand_x,rand_y),2*self.screen_height))
                self.apple_last_spawn_time = get_time()
                self.apple_spawn_interval = uniform(0.5,2.5)


    def apple_despawner(self):
        self.apple_list = [apple for apple in self.apple_list if apple.active]


    def update_all_apples(self,delta_time):
        for apple in self.apple_list:
            apple.update(delta_time)


    def draw_all_apples(self):
        for apple in self.apple_list:
            apple.draw()


    def draw_background(self):
        draw_texture(self.bg_texture_resized,0,0,WHITE)

    def update(self):
        delta_time = get_frame_time()
        # print(delta_time)
        self.player_basket.update(delta_time)
        # self.apple_test.update(delta_time)

        self.apple_spawner()
        self.update_all_apples(delta_time)


        self.apple_despawner()


    def draw(self):
        begin_drawing()
        clear_background(PURPLE)
        self.draw_background()
        self.player_basket.draw()

        self.draw_all_apples()

        # draw_text(str(len(self.apple_list)),10,10,40,GREEN)
        # if self.apple_list:
        #     draw_text(str(self.apple_list[0].y_velocity),10,10,40,GREEN)
        # self.apple_test.draw()
        # draw_fps(100,100)
        end_drawing()

    def run(self):
        while not window_should_close():
            self.update()
            self.draw()
            

        unload_texture(self.bg_texture_resized)
        for apple in self.apple_list:
            unload_texture(apple.texture)
        close_window()




if __name__ == "__main__":
    game = Game()
    game.run()