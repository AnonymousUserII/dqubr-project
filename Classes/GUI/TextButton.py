from os.path import join

import pygame

from Assets.colors import REST_BTN_COLOR, HOVER_BTN_COLOR, LIGHT_BLACK, LAYER2_COLOR
from Classes.GUI.Button import Button
from Classes.GUI.Tooltip import Tooltip


class TextButton(Button):
    def __init__(self, window: pygame.Surface, pos: tuple[int, int], size: tuple[int, int], text: str, text_size: int,
                 identifier: int | None = None,
                 tooltip: str | None = None, tooltip_size: tuple[int, int] | None = None):
        super().__init__(window, pos, size)
        self.was_hover: bool = False  # Holds hover state for previous frame
        
        self.label: pygame.Surface = pygame.font.Font(join("Assets", "fcm.otf"), text_size)\
            .render(text, True, LIGHT_BLACK)
        self.label_rect: pygame.Rect = self.label.get_rect(center=self.rect.center)
        self.color: pygame.Color = REST_BTN_COLOR
        self.hidden: bool = False
        self.identifier: int | None = identifier
        self.tooltip: str | None = tooltip
        self.tooltip_size: tuple[int, int] | None = tooltip_size
    
    def update(self) -> None:
        self.was_hover = self.hover
        super().update()
        if self.hidden:
            self.hover, self.clicked = False, False
            return None
        self.color = HOVER_BTN_COLOR if self.hover else REST_BTN_COLOR
        return None
    
    def draw(self) -> Tooltip | None:
        """
        Draws this element
        Returns a tooltip if applicable and is being hovered over
        """
        if self.hidden:
            return None
        pygame.draw.rect(self.window, self.color, self.rect, border_radius=4)
        self.window.blit(self.label, self.label_rect)
        if self.hover and self.tooltip:
            return Tooltip(self.window, pygame.mouse.get_pos(), self.tooltip_size, self.tooltip,
                           12, LIGHT_BLACK, LAYER2_COLOR)
        return None
