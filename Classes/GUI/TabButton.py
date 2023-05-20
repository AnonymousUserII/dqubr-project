from os.path import join
import pygame

from Assets.colors import DARK_GREY, FRAME_COLOR, REST_TAB_COLOR, LAYER2_COLOR
from Classes.GUI.Button import Button
from Classes.GUI.Tooltip import Tooltip


class TabButton(Button):
    def __init__(self, window: pygame.Surface, pos: tuple[int, int], size: tuple[int, int], text: str, tooltip: str):
        super().__init__(window, pos, size)
        self.bg_color, self.hover_color, self.color, self.text_color = \
            REST_TAB_COLOR, FRAME_COLOR, REST_TAB_COLOR, DARK_GREY
        
        self.label: pygame.Surface = pygame.font.Font(join("Assets", "od.otf"), 20).render(text, True, DARK_GREY)
        self.label_rect: pygame.Rect = self.label.get_rect(center=self.rect.center)
        # Offset different-colored label for text shadow
        shadow_rect: pygame.Rect = pygame.Rect(tuple(p + 2 for p in pos), size)
        shadow_color: pygame.Color = pygame.Color(0x6E, 0xAE, 0xEE)
        self.shadow: pygame.Surface = pygame.font.Font(join("Assets", "od.otf"), 20).render(text, True, shadow_color)
        self.shadow_rect: pygame.Rect = self.label.get_rect(center=shadow_rect.center)
        # Adjust labels to be slightly higher than the center of its rect
        self.label_rect.top -= 3
        self.shadow_rect.top -= 3
        
        self.tooltip: str = tooltip
    
    def update(self, active: bool = False) -> None:
        super().update()
        self.color = self.hover_color if self.hover or active else self.bg_color
        return None
    
    def draw(self) -> Tooltip | None:
        """
        Draws this element and returns a tooltip if it is hovered over
        """
        pygame.draw.rect(self.window, self.color, self.rect, border_radius=12)
        self.window.blit(self.shadow, self.shadow_rect)
        self.window.blit(self.label, self.label_rect)
        if self.hover:
            return Tooltip(self.window, pygame.mouse.get_pos(), (300, 30), self.tooltip, 12, DARK_GREY, LAYER2_COLOR)
        return None
