from os.path import join
import pygame

from Classes.Button import Button
DARK_GREY: pygame.Color = pygame.Color(0x10, 0x10, 0x10)
FRAME_COLOR: pygame.Color = pygame.Color(0xAE, 0xDF, 0xFC)
REST_BTN_COLOR: pygame.Color = pygame.Color(0x8A, 0xD2, 0xFB)


class TabButton(Button):
    def __init__(self, window: pygame.Surface, pos: tuple[int, int], size: tuple[int, int], text: str):
        super().__init__(window, pos, size)
        self.bg_color, self.hover_color, self.color, self.text_color = \
            REST_BTN_COLOR, FRAME_COLOR, REST_BTN_COLOR, DARK_GREY
        
        self.label: pygame.Surface = pygame.font.Font(join("Assets", "od.otf"), 20).render(text, True, DARK_GREY)
        self.label_rect: pygame.Rect = self.label.get_rect(center=self.rect.center)
        # Offset different-colored label for text shadow
        shadow_rect: pygame.Rect = pygame.Rect(tuple(p + 2 for p in pos), size)
        shadow_color: pygame.Color = pygame.Color(0x6E, 0xAE, 0xEE)
        self.shadow: pygame.Surface = pygame.font.Font(join("Assets", "od.otf"), 20).render(text, True, shadow_color)
        self.shadow_rect: pygame.Rect = self.label.get_rect(center=shadow_rect.center)
        # Adjust labels to be slightly higher than center
        self.label_rect.top -= 3
        self.shadow_rect.top -= 3
    
    def update(self, active: bool = False) -> None:
        super().update_state()
        self.color = self.hover_color if self.hover or active else self.bg_color
        return None
    
    def draw(self) -> None:
        pygame.draw.rect(self.window, self.color, self.rect, border_radius=12)
        self.window.blit(self.shadow, self.shadow_rect)
        self.window.blit(self.label, self.label_rect)
        return None
