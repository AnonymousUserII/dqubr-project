from os.path import join

import pygame

from Classes.GUI.Button import Button
from Assets.colors import REST_BTN_COLOR, HOVER_BTN_COLOR, LIGHT_BLACK


class TextButton(Button):
    def __init__(self, window: pygame.Surface, pos: tuple[int, int], size: tuple[int, int], text: str, text_size: int):
        super().__init__(window, pos, size)
        self.label: pygame.Surface = pygame.font.Font(join("Assets", "od.otf"), text_size)\
            .render(text, True, LIGHT_BLACK)
        self.label_rect: pygame.Rect = self.label.get_rect(center=self.rect.center)
        self.color: pygame.Color = REST_BTN_COLOR
        self.hidden: bool = False
    
    def update(self) -> None:
        if self.hidden:
            return None
        super().update()
        self.color = HOVER_BTN_COLOR if self.hover else REST_BTN_COLOR
        return None
    
    def draw(self) -> None:
        if self.hidden:
            return None
        pygame.draw.rect(self.window, self.color, self.rect, border_radius=4)
        self.window.blit(self.label, self.label_rect)
        return None
