import pygame

from Assets.colors import WHITE, BLUE, GREEN, ORANGE, RED, YELLOW
from Classes.Utility.Qube import *
from Classes.Utility.Shapes import *

cell_length: int = 50
prlgrm_wh: tuple[int, int] = int(cell_length * 1.5), int(cell_length * 0.5)
cell_spacing: int = 2
full_dim: int = cell_length + cell_spacing
prlgrm_dim: int = prlgrm_wh[1] + cell_spacing
colors: dict = {1: RED, 2: BLUE, 3: WHITE, 4: GREEN, 5: YELLOW, 6: ORANGE}


class QubeRender3:
    def __init__(self, window: pygame.Surface, pos: tuple[int, int], size: int, is_qube_form: bool = False):
        self.window: pygame.Surface = window
        self.pos: tuple[int, int] = pos  # Position is the center of front face
        self.size: int = size
        self.is_qube_form: bool = is_qube_form
    
    def draw(self, qube: Qube3) -> None:
        front_tl: tuple[int, int] = self.pos[0] - int(1.5 * cell_length) - cell_spacing, \
                                    self.pos[1] - int(1.5 * cell_length) - cell_spacing
        sides: tuple = qube.front, qube.up, qube.left, qube.right, qube.down, qube.back
        if self.is_qube_form:
            if self.size == 3:
                # Draw front
                for i, column in enumerate(zip(sides[0].up(), sides[0].mid_h(), sides[0].down())):
                    pygame.draw.rect(self.window, colors[column[0]],
                                     pygame.Rect((i * full_dim + front_tl[0], front_tl[1]),
                                                 (cell_length, cell_length)))
                    pygame.draw.rect(self.window, colors[column[1]],
                                     pygame.Rect((i * full_dim + front_tl[0], front_tl[1] + full_dim),
                                                 (cell_length, cell_length)))
                    pygame.draw.rect(self.window, colors[column[2]],
                                     pygame.Rect((i * full_dim + front_tl[0], front_tl[1] + 2 * full_dim),
                                                 (cell_length, cell_length)))
                # Draw top
                top_dl: tuple[int, int] = front_tl[0] + cell_spacing, front_tl[1] - 2 * cell_spacing
                for i, column in enumerate(zip(sides[1].down(), sides[1].mid_h(), sides[1].up())):
                    draw_top_parallelogram(self.window,
                                           (top_dl[0] + i * full_dim, top_dl[1]),
                                           cell_length, colors[column[0]])
                    draw_top_parallelogram(self.window,
                                           (top_dl[0] + i * full_dim + int(0.5 * cell_length) + cell_spacing,
                                            top_dl[1] - prlgrm_dim),
                                           cell_length, colors[column[1]])
                    draw_top_parallelogram(self.window,
                                           (top_dl[0] + i * full_dim + cell_length + 2 * cell_spacing,
                                            top_dl[1] - 2 * prlgrm_dim),
                                           cell_length, colors[column[2]])
                # Draw right
                right_tl: tuple[int, int] = front_tl[0] + 3 * full_dim + cell_spacing, front_tl[1] - cell_spacing
                for i, column in enumerate(zip(sides[3].up(), sides[3].mid_h(), sides[3].down())):
                    draw_right_parallelogram(self.window,
                                             (right_tl[0] + i * prlgrm_dim,
                                              right_tl[1] - i * prlgrm_dim),
                                             cell_length, colors[column[0]])
                    draw_right_parallelogram(self.window,
                                             (right_tl[0] + i * prlgrm_dim,
                                              right_tl[1] - i * prlgrm_dim + full_dim),
                                             cell_length, colors[column[1]])
                    draw_right_parallelogram(self.window,
                                             (right_tl[0] + i * prlgrm_dim,
                                              right_tl[1] - i * prlgrm_dim + 2 * full_dim),
                                             cell_length, colors[column[2]])
        else:
            if self.size == 3:
                # Get top left of each face
                top_lefts: tuple = (
                    front_tl,
                    (front_tl[0], front_tl[0] - 3 * full_dim - cell_spacing),
                    (front_tl[0] - 3 * full_dim - cell_spacing, front_tl[1]),
                    (front_tl[0] + 3 * full_dim + cell_spacing, front_tl[1]),
                    (front_tl[0], front_tl[0] + 3 * full_dim + cell_spacing),
                    (front_tl[0] + 6 * full_dim + 2 * cell_spacing, front_tl[1]),
                )
    
                for tl, side in zip(top_lefts, sides):
                    for i, column in enumerate(zip(side.up(), side.mid_h(), side.down())):
                        pygame.draw.rect(self.window, colors[column[0]],
                                         pygame.Rect((i * full_dim + tl[0], tl[1]),
                                                     (cell_length, cell_length)))
                        pygame.draw.rect(self.window, colors[column[1]],
                                         pygame.Rect((i * full_dim + tl[0], tl[1] + full_dim),
                                                     (cell_length, cell_length)))
                        pygame.draw.rect(self.window, colors[column[2]],
                                         pygame.Rect((i * full_dim + tl[0], tl[1] + 2 * full_dim),
                                                     (cell_length, cell_length)))
        return None
