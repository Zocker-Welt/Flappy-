import pygame
import math

import global_var
import rect_utils

from player import Player
from background import Background
from pipe import Pipe

pygame.init()
pygame.mixer.init()

sound = pygame.mixer.Sound("tomp3.wav")
sound.play(-1)

width, height = 1920, 1080
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Flappy?")

screen_center_x = screen.get_width() // 2
screen_center_y = screen.get_height() // 2

def event_to_dict(event):
    return {
        'type': event.type,
        'dict': dict(event.__dict__)
    }

def coords2pygame(button_image, x_offset=0, y_offset=0):
    return {
        "x": screen_center_x - button_image.get_width() // 2 + x_offset,
        "y": screen_center_y - button_image.get_height() // 2 - y_offset,
    }

def render_image(image, x=0, y=0):
    image_position = coords2pygame(image, x_offset=x, y_offset=y)
    screen.blit(
        image,
        (image_position["x"], image_position["y"])
    )

def set_size(image, size):
    return pygame.transform.scale(image, (image.get_width() * size, image.get_height() * size))

def render_text(text, font_size, x, y, color=(0, 0, 0)):
    font = pygame.font.SysFont("Comic Sans MS", font_size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.center = (screen_center_x + x, screen_center_y - y)
    screen.blit(text_surface, text_rect)

class Main:
    def __init__(self):
        global_var.set("menu", "home")
        global_var.set("score", 0)

        self.player_textures = {
            "1alive" : pygame.image.load("1alive.png"),
            "2alive" : pygame.image.load("2alive.png"),
            "3alive" : pygame.image.load("3alive.png"),
            "4alive" : pygame.image.load("4alive.png"),
            "5alive" : pygame.image.load("5alive.png"),
            "6alive" : pygame.image.load("6alive.png"),
            "7alive" : pygame.image.load("7alive.png"),
            "8alive" : pygame.image.load("8alive.png")
        }
        self.background_texture = pygame.image.load("background.png")
        self.pipe_texture = pygame.image.load("pipe1.png")
        self.pipe_textures = {
            1 : pygame.image.load("pipe1.png"),
            2 : pygame.image.load("pipe2.png"),
            3 : pygame.image.load("pipe3.png")
        }
        self.logo_texture = pygame.image.load("logo.png")
        self.play_texture = pygame.image.load("play.png")
        self.cover_texture = pygame.image.load("cover.png")
        self.left_texture = pygame.image.load("left.png")
        self.right_texture = pygame.image.load("right.png")

        self.player_obj = Player()
        self.background_obj1 = Background(-500, -450)
        self.background_obj2 = Background(600, -450)
        self.background_obj3 = Background(1700, -450)
        self.pipe_obj1 = Pipe(x=600)
        self.pipe_obj2 = Pipe(x=1200)
        self.pipe_obj3 = Pipe(x=1700)
        self.pipe_obj4 = Pipe(x=2200)

        self.clock = pygame.time.Clock()

        self.play_size = 1.00
        self.left_size = 1.00
        self.right_size = 1.00
        global_var.set("speed", 10)
        global_var.set("player_icon", "1")
    
    def handle(self):
        self.running = True
        while self.running:
            self.mouse_down_event = False
            self.events = pygame.event.get()
            for event in self.events:
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.mouse_down_event = True
            json_events = [event_to_dict(event) for event in self.events]
            global_var.set("events", json_events)
            
            screen.fill((130, 255, 251))
            
            self.time = pygame.time.get_ticks() / 1000.0
            global_var.set("time", self.time)
            self.mouse_x, self.mouse_y = pygame.mouse.get_pos()
            global_var.set("mouse_x", self.mouse_x - 960)
            global_var.set("mouse_y", 540 - self.mouse_y)
            self.mouse_down = pygame.mouse.get_pressed()[0]
            self.tick()
            
            """
            if self.mouse_down_event:
                print(self.mouse_x, self.mouse_y)
            """

            pygame.display.flip()
            self.clock.tick(60)

        pygame.quit()
    
    def tick(self):
        if global_var.get("menu") == "game":
            global_var.set("pipe_hb", [])
            self.background_obj1.tick()
            self.background_obj2.tick()
            self.background_obj3.tick()
            self.pipe_obj1.tick()
            self.pipe_obj2.tick()
            self.pipe_obj3.tick()
            self.pipe_obj4.tick()
            self.player_obj.tick()

            render_image(
                self.background_texture,
                x=self.background_obj1.xpos, y=self.background_obj1.ypos
            )
            render_image(
                self.background_texture,
                x=self.background_obj2.xpos, y=self.background_obj2.ypos
            )
            render_image(
                self.background_texture,
                x=self.background_obj3.xpos, y=self.background_obj3.ypos
            )

            render_image(
                set_size(self.pipe_textures[self.pipe_obj1.type], 1.5),
                x=self.pipe_obj1.xpos, y=self.pipe_obj1.ypos
            )

            render_image(
                set_size(self.pipe_textures[self.pipe_obj2.type], 1.5),
                x=self.pipe_obj2.xpos, y=self.pipe_obj2.ypos
            )

            render_image(
                set_size(self.pipe_textures[self.pipe_obj3.type], 1.5),
                x=self.pipe_obj3.xpos, y=self.pipe_obj3.ypos
            )

            render_image(
                set_size(self.pipe_textures[self.pipe_obj4.type], 1.5),
                x=self.pipe_obj4.xpos, y=self.pipe_obj4.ypos
            )

            render_image(
                set_size(pygame.transform.rotate(self.player_textures[f"{global_var.get("player_icon")}alive"], self.player_obj.angle), 1.2),
                x=self.player_obj.xpos, y=self.player_obj.ypos
            )

            render_image(
                set_size(self.cover_texture, 0.5),
                x=0, y=0
            )
            render_text(f"{global_var.get("score")}", 100, 0, 460, (255, 215, 0) if global_var.get("score") > global_var.get("best") else (102, 165, 255))
            """
            for rect in global_var.get("pipe_hb"):
                pygame.draw.rect(screen, (255, 0, 0), rect_utils.dict2rect(rect))
            pygame.draw.rect(screen, (0, 255, 0), rect_utils.dict2rect(global_var.get("player_hb")))
            """
        
        elif global_var.get("menu") == "home":
            self.background_obj1.tick()
            self.background_obj2.tick()
            self.background_obj3.tick()

            if 784 < self.mouse_x and self.mouse_x < 1129 and 835 < self.mouse_y and self.mouse_y < 967:
                self.play_size = (3.50 - self.play_size) / 2
                if self.mouse_down_event:
                    self.pipe_obj1.xpos = 200
                    self.pipe_obj2.xpos = 800
                    self.pipe_obj3.xpos = 1300
                    self.pipe_obj4.xpos = 1800
                    self.player_obj.ypos = 0
                    self.player_obj.yvel = 0
                    global_var.set("score", 0)
                    global_var.set("menu", "game")
                    """
                    self.pipe_obj1 = Pipe(x=1100)
                    self.pipe_obj2 = Pipe(x=1700)
                    self.pipe_obj3 = Pipe(x=2200)
                    self.pipe_obj4 = Pipe(x=2700)
                    """
            else:
                self.play_size += (1.00 - self.play_size) / 2
            
            if 697 < self.mouse_x and self.mouse_x < 813 and 463 < self.mouse_y and self.mouse_y < 605:
                self.left_size = (3.20 - self.left_size) / 2   
                if self.mouse_down_event:
                    icon = int(global_var.get("player_icon")) - 1
                    if icon == 0: icon = 8
                    global_var.set("player_icon", icon)
            else:
                self.left_size += (1.00 - self.left_size) / 2
            
            if 1098 < self.mouse_x and self.mouse_x < 1221 and 463 < self.mouse_y and self.mouse_y < 605:
                self.right_size = (3.20 - self.right_size) / 2
                if self.mouse_down_event:
                    icon = int(global_var.get("player_icon")) + 1
                    if icon == 9: icon = 1
                    global_var.set("player_icon", icon)
            else:
                self.right_size += (1.00 - self.right_size) / 2
            
            render_image(
                self.player_textures[f"{global_var.get("player_icon")}alive"],
                x=0, y=0
            )
            
            render_image(
                self.background_texture,
                x=self.background_obj1.xpos, y=self.background_obj1.ypos
            )

            render_image(
                self.background_texture,
                x=self.background_obj2.xpos, y=self.background_obj2.ypos
            )

            render_image(
                self.background_texture,
                x=self.background_obj3.xpos, y=self.background_obj3.ypos
            )

            render_image(
                self.logo_texture,
                x=0, y=300 + math.cos(self.time * 3) * 21
            )

            render_image(
                set_size(self.play_texture, self.play_size),
                x=0, y=-360
            )

            render_image(
                set_size(self.cover_texture, 0.5),
                x=0, y=0
            )

            render_image(
                set_size(self.left_texture, self.left_size),
                x=-200, y=0
            )

            render_image(
                set_size(self.right_texture, self.right_size),
                x=200, y=0
            )

            render_text(f"score: {global_var.get("score")}, best: {global_var.get("best")}", 100, 0, 460, (102, 165, 255))
            render_text("Use your mouse to move the pipes", 50, 0, -175 + math.sin(self.time * 2.5 + 2) * 10, (146, 195, 184))

main = Main()
main.handle()