import random
import pygame
import math

import global_var
import rect_utils

screen_center_x = 960
screen_center_y = 540

def coords2pygame(x_offset=0, y_offset=0):
    return {
        "x": screen_center_x + x_offset,
        "y": screen_center_y - y_offset,
    }

class Pipe:
    def __init__(self, x):
        self.xpos = x
        self.ypos_start = random.randint(-150, 150)
        self.type = random.randint(1, 2)
        self.passed = False
        self.speed = 0
    
    def tick(self):
        self.xpos -= global_var.get("speed")
        if self.xpos < -1100:
            self.xpos = 1100
            self.ypos_start = random.randint(-150, 150)
            if global_var.get("score") < 11:
                self.type = random.randint(1, 2)
            elif global_var.get("score") < 21:
                self.type = random.randint(1, 3)
            elif global_var.get("score") < 31:
                if random.randint(0, 1):
                    self.type = 3
                else:
                    self.type = random.randint(1, 2)
            elif global_var.get("score" < 41):
                self.type = 3
            else:
                if random.randint(0, 1):
                    self.type = 3
                else:
                    self.type = random.randint(1, 3)
            self.passed = False
        if self.type == 1:
            self.ypos = self.ypos_start + global_var.get("mouse_y")
        elif self.type == 2:
            self.ypos = self.ypos_start - global_var.get("mouse_y")
        elif self.type == 3:
            self.ypos = self.ypos_start + global_var.get("mouse_y") + math.sin(global_var.get("time") * 2) * 120
        
        if self.xpos < -800 and self.passed == False:
            self.passed = True
            global_var.set("score", global_var.get("score") + 1)
            if global_var.get("speed") < 40:
                global_var.set("speed", global_var.get("speed") + 0.5)

        hb1 = pygame.Rect(
            coords2pygame(x_offset=self.xpos, y_offset=self.ypos)["x"] - 100,
            coords2pygame(x_offset=self.xpos, y_offset=self.ypos + 810)["y"],
            200, 600,
        )
        hb2 = pygame.Rect(
            coords2pygame(x_offset=self.xpos, y_offset=self.ypos)["x"] - 100,
            coords2pygame(x_offset=self.xpos, y_offset=self.ypos - 145)["y"],
            200, 600,
        )
        current_hitboxes = global_var.get("pipe_hb")
        current_hitboxes.append(rect_utils.rect2dict(hb1))
        current_hitboxes.append(rect_utils.rect2dict(hb2))
        global_var.set("pipe_hb", current_hitboxes)