from os import path

import pygame

from Assets.colors import LIGHT_BLACK
from Classes.GUI.TextButton import TextButton


class QubeButton(TextButton):
    def __init__(self, window: pygame.Surface, net_pos: tuple[int, int], cube_pos: tuple[int, int] | None,
                 text: str, min_cube_size: int):
        super().__init__(window, net_pos, (30, 30), text, 16)
        self.label: pygame.Surface = pygame.font.Font(path.join("Assets", "od.otf"), 16) \
            .render(text, True, LIGHT_BLACK)
        self.label_rect: pygame.Rect = self.label.get_rect(center=self.rect.center)
        self.net_pos, self.cube_pos = net_pos, cube_pos if cube_pos is not None else net_pos
        self.rect.center = self.label_rect.center = net_pos  # Button position centered at given coordinate
        self.text: str = text
        self.min_cube_size: int = min_cube_size  # At what cube size will the button be visible
    
    def update_state(self, cube_size: bool, cube_form: bool) -> str | None:
        self.hidden = cube_size < self.min_cube_size
        if self.hidden:
            return None
        super().update()
        self.rect.center = self.label_rect.center = self.cube_pos if cube_form else self.net_pos
        return self.text if self.clicked else None
    
    def draw(self) -> None:
        if self.hidden:
            return
        pygame.draw.rect(self.window, self.color, self.rect, border_radius=4)
        self.window.blit(self.label, self.label_rect)
        return None
