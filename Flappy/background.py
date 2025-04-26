import global_var

class Background:
    def __init__(self, x, y):
        self.xpos = x
        self.ypos = y
    
    def tick(self):
        self.xpos -= global_var.get("speed") / 4
        if self.xpos < -1600:
            self.xpos = 1600