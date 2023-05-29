from Assets.colors import WHITE, BLUE, GREEN, ORANGE, RED, YELLOW
from Classes.Utility.Qube import *
from Classes.Utility.Shapes import *

cell_lengths: tuple[int, int, int] = 120, 60, 40
cell_spacing: int = 3
colors: dict = {1: RED, 2: BLUE, 3: WHITE, 4: GREEN, 5: YELLOW, 6: ORANGE}


class QubeRender:
    def __init__(self, window: pygame.Surface, pos: tuple[int, int], size: int, is_cube_form: bool = False):
        self.window: pygame.Surface = window
        self.pos: tuple[int, int] = pos  # Position is the center of front face
        self.size: int = size
        self.is_cube_form: bool = is_cube_form
    
    def draw(self, qube: Qube1 | Qube2 | Qube3, back_view: bool = False, see_through: bool = False) -> None:
        cell_length: int = cell_lengths[self.size - 1]
        full_dim: int = cell_length + cell_spacing
        prlgrm_wh: tuple[int, int] = int(cell_length * 1.5), int(cell_length * 0.5)
        prlgrm_dim: int = prlgrm_wh[1] + cell_spacing
        sides: tuple = qube.front, qube.up, qube.left, qube.right, qube.down, qube.back
        if back_view:
            sides = qube.back, qube.down, qube.right, qube.left, qube.up, qube.front
            self.is_cube_form = True
        if self.is_cube_form:
            if self.size == 1:
                front_tl: tuple[int, int] = self.pos[0] - int(0.5 * cell_length) - (50 if see_through else 100), \
                                            self.pos[1] - int(0.5 * cell_length)
                # Draw front
                pygame.draw.rect(self.window, colors[sides[0].cell], pygame.Rect(front_tl, (cell_length, cell_length)))
                if back_view and see_through:
                    # Draw bottom
                    bottom_dl: tuple[int, int] = front_tl[0] - int(1/3 * prlgrm_wh[0]) - cell_spacing, \
                                                 front_tl[1] + full_dim + prlgrm_dim
                    draw_top_parallelogram(self.window, bottom_dl, cell_length, colors[sides[1].cell])
                    # Draw left
                    left_tl: tuple[int, int] = front_tl[0] - int(1/3 * prlgrm_wh[0]) - 2 * cell_spacing, \
                                               front_tl[1] + int(1/3 * prlgrm_wh[0])
                    draw_right_parallelogram(self.window, left_tl, cell_length, colors[sides[3].cell])
                elif back_view:
                    # Draw bottom
                    bottom_tl: tuple[int, int] = front_tl[0] + cell_spacing, front_tl[1] + full_dim + cell_spacing
                    draw_bottom_parallelogram(self.window, bottom_tl, cell_length, colors[sides[1].cell])
                    # Draw left
                    left_tr: tuple[int, int] = front_tl[0] + full_dim + cell_spacing, front_tl[1] + cell_spacing
                    draw_left_parallelogram(self.window, left_tr, cell_length, colors[sides[3].cell])
                else:
                    # Draw top
                    top_dl: tuple[int, int] = front_tl[0] + cell_spacing, front_tl[1] - 2 * cell_spacing
                    draw_top_parallelogram(self.window, top_dl, cell_length, colors[sides[1].cell])
                    # Draw right
                    right_tl: tuple[int, int] = front_tl[0] + full_dim + cell_spacing, front_tl[1] - cell_spacing
                    draw_right_parallelogram(self.window, right_tl, cell_length, colors[sides[3].cell])
            elif self.size == 2:
                front_tl: tuple[int, int] = self.pos[0] - int(0.5 * cell_spacing) - cell_length \
                                            - (50 if see_through else 100), \
                                            self.pos[1] - int(0.5 * cell_spacing) - cell_length
                # Draw front
                inc: int = -1 if see_through else 1
                for i, column in enumerate(zip(sides[0].up()[::inc], sides[0].down()[::inc])):
                    pygame.draw.rect(self.window, colors[column[0]],
                                     pygame.Rect((i * full_dim + front_tl[0], front_tl[1]),
                                                 (cell_length, cell_length)))
                    pygame.draw.rect(self.window, colors[column[1]],
                                     pygame.Rect((i * full_dim + front_tl[0], front_tl[1] + full_dim),
                                                 (cell_length, cell_length)))
                if back_view and see_through:
                    # Draw bottom
                    bottom_dl: tuple[int, int] = front_tl[0] - int(2 / 3 * prlgrm_wh[0]) - cell_spacing, \
                                                 front_tl[1] + 2 * (full_dim + prlgrm_dim)
                    for i, column in enumerate(zip(sides[1].up(), sides[1].down())):
                        draw_top_parallelogram(self.window,
                                               (bottom_dl[0] + i * full_dim, bottom_dl[1]),
                                               cell_length, colors[column[0]])
                        draw_top_parallelogram(self.window,
                                               (bottom_dl[0] + i * full_dim + int(0.5 * cell_length) + cell_spacing,
                                                bottom_dl[1] - prlgrm_dim),
                                               cell_length, colors[column[1]])
                    # Draw left
                    left_tl: tuple[int, int] = front_tl[0] - 2 * (int(1/3 * prlgrm_wh[0]) + 2 * cell_spacing), \
                                               front_tl[1] + 2 * (int(1/3 * prlgrm_wh[0]) + cell_spacing)
                    for i, column in enumerate(zip(sides[3].up()[::-1], sides[3].down()[::-1])):
                        draw_right_parallelogram(self.window,
                                                 (left_tl[0] + i * prlgrm_dim, left_tl[1] - i * prlgrm_dim),
                                                 cell_length, colors[column[0]])
                        draw_right_parallelogram(self.window,
                                                 (left_tl[0] + i * prlgrm_dim,
                                                  left_tl[1] - i * prlgrm_dim + full_dim),
                                                 cell_length, colors[column[1]])
                elif back_view:
                    # Draw bottom
                    bottom_tl: tuple[int, int] = (front_tl[0] + cell_spacing, front_tl[1] + 2 * full_dim + cell_spacing)
                    for i, column in enumerate(zip(sides[1].down()[::-1], sides[1].up()[::-1])):
                        draw_bottom_parallelogram(self.window,
                                                  (bottom_tl[0] + i * full_dim, bottom_tl[1]),
                                                  cell_length, colors[column[0]])
                        draw_bottom_parallelogram(self.window,
                                                  (bottom_tl[0] + i * full_dim + int(0.5 * cell_length) + cell_spacing,
                                                   bottom_tl[1] + prlgrm_dim), cell_length, colors[column[1]])
                    # Draw left
                    left_tl: tuple[int, int] = front_tl[0] + 2 * full_dim + cell_spacing, front_tl[1] + cell_spacing
                    for i, column in enumerate(zip(sides[3].up(), sides[3].down())):
                        draw_left_parallelogram(self.window,
                                                (left_tl[0] + i * prlgrm_dim, left_tl[1] + i * prlgrm_dim),
                                                cell_length, colors[column[0]])
                        draw_left_parallelogram(self.window,
                                                (left_tl[0] + i * prlgrm_dim, left_tl[1] + i * prlgrm_dim + full_dim),
                                                cell_length, colors[column[1]])
                else:
                    # Draw top
                    top_dl: tuple[int, int] = front_tl[0] + cell_spacing, front_tl[1] - 2 * cell_spacing
                    for i, column in enumerate(zip(sides[1].down(), sides[1].up())):
                        draw_top_parallelogram(self.window,
                                               (top_dl[0] + i * full_dim, top_dl[1]), cell_length, colors[column[0]])
                        draw_top_parallelogram(self.window,
                                               (top_dl[0] + i * full_dim + int(0.5 * cell_length) + cell_spacing,
                                                top_dl[1] - prlgrm_dim), cell_length, colors[column[1]])
                    # Draw right
                    right_tl: tuple[int, int] = front_tl[0] + 2 * full_dim + cell_spacing, front_tl[1] - cell_spacing
                    for i, column in enumerate(zip(sides[3].up(), sides[3].down())):
                        draw_right_parallelogram(self.window,
                                                 (right_tl[0] + i * prlgrm_dim, right_tl[1] - i * prlgrm_dim),
                                                 cell_length, colors[column[0]])
                        draw_right_parallelogram(self.window,
                                                 (right_tl[0] + i * prlgrm_dim,
                                                  right_tl[1] - i * prlgrm_dim + full_dim),
                                                 cell_length, colors[column[1]])
            elif self.size == 3:
                front_tl: tuple[int, int] = self.pos[0] - int(1.5 * cell_length) - cell_spacing \
                                            - (50 if see_through else 100), \
                                            self.pos[1] - int(1.5 * cell_length) - cell_spacing
                # Draw front
                inc: int = -1 if see_through else 1
                for i, column in enumerate(zip(sides[0].up()[::inc], sides[0].mid()[::inc], sides[0].down()[::inc])):
                    pygame.draw.rect(self.window, colors[column[0]],
                                     pygame.Rect((i * full_dim + front_tl[0], front_tl[1]),
                                                 (cell_length, cell_length)))
                    pygame.draw.rect(self.window, colors[column[1]],
                                     pygame.Rect((i * full_dim + front_tl[0], front_tl[1] + full_dim),
                                                 (cell_length, cell_length)))
                    pygame.draw.rect(self.window, colors[column[2]],
                                     pygame.Rect((i * full_dim + front_tl[0], front_tl[1] + 2 * full_dim),
                                                 (cell_length, cell_length)))
                if back_view and see_through:
                    # Draw bottom
                    bottom_dl: tuple[int, int] = front_tl[0] - prlgrm_wh[0] - 3 * cell_spacing, \
                                                 front_tl[1] + 3 * (full_dim + prlgrm_dim)
                    for i, column in enumerate(zip(sides[1].up(), sides[1].mid(), sides[1].down())):
                        draw_top_parallelogram(self.window,
                                               (bottom_dl[0] + i * full_dim, bottom_dl[1]),
                                               cell_length, colors[column[0]])
                        draw_top_parallelogram(self.window,
                                               (bottom_dl[0] + i * full_dim + int(0.5 * cell_length) + cell_spacing,
                                                bottom_dl[1] - prlgrm_dim),
                                               cell_length, colors[column[1]])
                        draw_top_parallelogram(self.window,
                                               (bottom_dl[0] + i * full_dim + cell_length + 2 * cell_spacing,
                                                bottom_dl[1] - 2 * prlgrm_dim),
                                               cell_length, colors[column[2]])
                    # Draw left
                    left_tl: tuple[int, int] = front_tl[0] - prlgrm_wh[0] - 5 * cell_spacing, \
                                               front_tl[1] + prlgrm_wh[0] + 3 * cell_spacing
                    for i, column in enumerate(zip(sides[3].up()[::-1], sides[3].mid()[::-1], sides[3].down()[::-1])):
                        draw_right_parallelogram(self.window,
                                                 (left_tl[0] + i * prlgrm_dim,
                                                  left_tl[1] - i * prlgrm_dim),
                                                 cell_length, colors[column[0]])
                        draw_right_parallelogram(self.window,
                                                 (left_tl[0] + i * prlgrm_dim,
                                                  left_tl[1] - i * prlgrm_dim + full_dim),
                                                 cell_length, colors[column[1]])
                        draw_right_parallelogram(self.window,
                                                 (left_tl[0] + i * prlgrm_dim,
                                                  left_tl[1] - i * prlgrm_dim + 2 * full_dim),
                                                 cell_length, colors[column[2]])
                elif back_view:
                    # Draw bottom
                    bottom_tl: tuple[int, int] = front_tl[0] + cell_spacing, front_tl[1] + 3 * full_dim + cell_spacing
                    for i, column in enumerate(zip(sides[1].down()[::-1], sides[1].mid()[::-1], sides[1].up()[::-1])):
                        draw_bottom_parallelogram(self.window,
                                                  (bottom_tl[0] + i * full_dim, bottom_tl[1]),
                                                  cell_length, colors[column[0]])
                        draw_bottom_parallelogram(self.window,
                                                  (bottom_tl[0] + i * full_dim + int(0.5 * cell_length) + cell_spacing,
                                                   bottom_tl[1] + prlgrm_dim),
                                                  cell_length, colors[column[1]])
                        draw_bottom_parallelogram(self.window,
                                                  (bottom_tl[0] + i * full_dim + cell_length + 2 * cell_spacing,
                                                   bottom_tl[1] + 2 * prlgrm_dim),
                                                  cell_length, colors[column[2]])
                    # Draw left
                    left_tl: tuple[int, int] = front_tl[0] + 3 * full_dim + cell_spacing, front_tl[1] + cell_spacing
                    for i, column in enumerate(zip(sides[3].up(), sides[3].mid(), sides[3].down())):
                        draw_left_parallelogram(self.window,
                                                (left_tl[0] + i * prlgrm_dim,
                                                 left_tl[1] + i * prlgrm_dim),
                                                cell_length, colors[column[0]])
                        draw_left_parallelogram(self.window,
                                                (left_tl[0] + i * prlgrm_dim,
                                                 left_tl[1] + i * prlgrm_dim + full_dim),
                                                cell_length, colors[column[1]])
                        draw_left_parallelogram(self.window,
                                                (left_tl[0] + i * prlgrm_dim,
                                                 left_tl[1] + i * prlgrm_dim + 2 * full_dim),
                                                cell_length, colors[column[2]])
                else:
                    # Draw top
                    top_dl: tuple[int, int] = front_tl[0] + cell_spacing, front_tl[1] - 2 * cell_spacing
                    for i, column in enumerate(zip(sides[1].down(), sides[1].mid(), sides[1].up())):
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
                    for i, column in enumerate(zip(sides[3].up(), sides[3].mid(), sides[3].down())):
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
        else:  # Render net form
            if self.size == 1:
                front_tl: tuple[int, int] = self.pos[0] - int(0.5 * cell_length), self.pos[1] - int(0.5 * cell_length)
                top_lefts: tuple = (
                    front_tl,
                    (front_tl[0], front_tl[1] - full_dim - cell_spacing),
                    (front_tl[0] - full_dim - cell_spacing, front_tl[1]),
                    (front_tl[0] + full_dim + cell_spacing, front_tl[1]),
                    (front_tl[0], front_tl[1] + full_dim + cell_spacing),
                    (front_tl[0] + 2 * (full_dim + cell_spacing), front_tl[1])
                )
                
                for tl, side in zip(top_lefts, sides):
                    pygame.draw.rect(self.window, colors[side.cell], pygame.Rect(tl, (cell_length, cell_length)))
            elif self.size == 2:
                front_tl: tuple[int, int] = self.pos[0] - int(0.5 * cell_spacing) - cell_length, \
                                            self.pos[1] - int(0.5 * cell_spacing) - cell_length
                # Top left of each face
                top_lefts: tuple = (
                    front_tl,
                    (front_tl[0], front_tl[0] - 2 * full_dim - cell_spacing),
                    (front_tl[0] - 2 * full_dim - cell_spacing, front_tl[1]),
                    (front_tl[0] + 2 * full_dim + cell_spacing, front_tl[1]),
                    (front_tl[0], front_tl[0] + 2 * full_dim + cell_spacing),
                    (front_tl[0] + 4 * full_dim + 2 * cell_spacing, front_tl[1])
                )
                
                for tl, side in zip(top_lefts, sides):
                    for i, column in enumerate(zip(side.up(), side.down())):
                        pygame.draw.rect(self.window, colors[column[0]],
                                         pygame.Rect((i * full_dim + tl[0], tl[1]),
                                                     (cell_length, cell_length)))
                        pygame.draw.rect(self.window, colors[column[1]],
                                         pygame.Rect((i * full_dim + tl[0], tl[1] + full_dim),
                                                     (cell_length, cell_length)))
            elif self.size == 3:
                front_tl: tuple[int, int] = self.pos[0] - int(1.5 * cell_length) - cell_spacing, \
                                            self.pos[1] - int(1.5 * cell_length) - cell_spacing
                # Get top left of each face
                top_lefts: tuple = (
                    front_tl,
                    (front_tl[0], front_tl[1] - 3 * full_dim - cell_spacing),
                    (front_tl[0] - 3 * full_dim - cell_spacing, front_tl[1]),
                    (front_tl[0] + 3 * full_dim + cell_spacing, front_tl[1]),
                    (front_tl[0], front_tl[1] + 3 * full_dim + cell_spacing),
                    (front_tl[0] + 6 * full_dim + 2 * cell_spacing, front_tl[1])
                )
    
                for tl, side in zip(top_lefts, sides):
                    for i, column in enumerate(zip(side.up(), side.mid(), side.down())):
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
