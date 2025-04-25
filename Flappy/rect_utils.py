import pygame

def rect2dict(a):
    return {
        "x" : a.x,
        "y" : a.y,
        "width" : a.width,
        "height" : a.height
    }

def dict2rect(a):
    return pygame.Rect(
        a['x'],
        a['y'],
        a['width'],
        a['height']
    )