import pygame

from Assets.colors import WHITE, BLUE, GREEN, ORANGE, RED, YELLOW
from Classes.Utility.Qube import *

cell_length: int = 30
cell_spacing: int = 2
full_spacing: int = cell_length + cell_spacing
colors: dict = {1: RED, 2: BLUE, 3: WHITE, 4: GREEN, 5: YELLOW, 6: ORANGE}


class QubeRender3:
    def __init__(self, window: pygame.Surface, pos: tuple[int, int], net: bool = True):
        self.window: pygame.Surface = window
        self.pos: tuple[int, int] = pos  # Position is the center of front face
        self.net: bool = net
    
    def draw(self, qube: Qube3) -> None:
        front_tl: tuple[int, int] = self.pos[0] - int(1.5 * cell_length) - cell_spacing,\
                                    self.pos[1] - int(1.5 * cell_length) - cell_spacing
        if self.net:
            sides: tuple = qube.front, qube.up, qube.left, qube.right, qube.down, qube.back
            # Get top left of each face
            top_lefts: tuple = (
                front_tl,
                (front_tl[0], front_tl[0] - 3 * full_spacing - cell_spacing),
                (front_tl[0] - 3 * full_spacing - cell_spacing, front_tl[1]),
                (front_tl[0] + 3 * full_spacing + cell_spacing, front_tl[1]),
                (front_tl[0], front_tl[0] + 3 * full_spacing + cell_spacing),
                (front_tl[0] + 6 * full_spacing + 2 * cell_spacing, front_tl[1]),
            )
            
            for tl, side in zip(top_lefts, sides):
                for i, column in enumerate(zip(side.up(), side.mid_h(), side.down())):
                    pygame.draw.rect(self.window, colors[column[0]],
                                     pygame.Rect((i * full_spacing + tl[0], tl[1]),
                                                 (cell_length, cell_length)))
                    pygame.draw.rect(self.window, colors[column[1]],
                                     pygame.Rect((i * full_spacing + tl[0], tl[1] + full_spacing),
                                                 (cell_length, cell_length)))
                    pygame.draw.rect(self.window, colors[column[2]],
                                     pygame.Rect((i * full_spacing + tl[0], tl[1] + 2 * full_spacing),
                                                 (cell_length, cell_length)))
        return None
