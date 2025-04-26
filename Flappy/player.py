import math
import pygame

import global_var
import rect_utils

KEYDOWN = 768
KEYUP = 769
K_w = 119
K_UP = 1073741906
MOUSEBUTTONDOWN = 1025

screen_center_x = 960
screen_center_y = 540

def coords2pygame(x_offset=0, y_offset=0):
    return {
        "x": screen_center_x + x_offset,
        "y": screen_center_y - y_offset,
    }

class Player:
    def __init__(self):
        self.xpos = -800
        self.ypos = 0
        self.angle = 0

    def tick(self):
        self.time = global_var.get("time")

        self.ypos = math.cos(self.time * 3) * 15
        self.angle = 0

        hb = pygame.Rect(
            coords2pygame(x_offset=self.xpos, y_offset=self.ypos)["x"] - 50,
            coords2pygame(x_offset=self.xpos, y_offset=self.ypos)["y"] - 35,
            100, 100,
        )
        global_var.set("player_hb", rect_utils.rect2dict(hb))

        # check if dead by pipes
        player_hb = rect_utils.dict2rect(global_var.get("player_hb"))
        pipe_hbs = [rect_utils.dict2rect(i) for i in global_var.get("pipe_hb")]
        for pipe_hb in pipe_hbs:
            if player_hb.colliderect(pipe_hb):
                if global_var.get("score") > global_var.get("best"):
                    global_var.set("best", global_var.get("score"))
                global_var.set("menu", "home")
        
        # check if dead by floor
        if abs(self.ypos) > 510:
            if global_var.get("score") > global_var.get("best"):
                global_var.set("best", global_var.get("score"))
            global_var.set("menu", "home")