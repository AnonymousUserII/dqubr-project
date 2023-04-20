from os.path import join
import pygame

from Classes.Button import Button


class TabButton(Button):
    def __init__(self, window: pygame.Surface, pos: tuple[int, int], size: tuple[int, int],
                 bg_color: pygame.Color, hover_color: pygame.Color, text_color: pygame.Color, text: str):
        super().__init__(window, pos, size)
        self.bg_color, self.hover_color, self.color, self.text_color = bg_color, hover_color, bg_color, text_color
        
        self.label: pygame.Surface = pygame.font.Font(join("Assets", "od.otf"), 20).render(text, True, text_color)
        self.label_rect: pygame.Rect = self.label.get_rect(center=self.rect.center)
        
        shadow_rect: pygame.Rect = pygame.Rect(tuple(p + 2 for p in pos), size)
        shadow_color: pygame.Color = pygame.Color(0x6E, 0xAE, 0xEE)
        self.label_b: pygame.Surface = pygame.font.Font(join("Assets", "od.otf"), 20).render(text, True, shadow_color)
        self.label_b_rect: pygame.Rect = self.label.get_rect(center=shadow_rect.center)
    
    def update(self, active: bool = False) -> bool:
        super().update_state()
        self.color = self.hover_color if self.hover or active else self.bg_color
        return self.clicked
    
    def draw(self) -> None:
        pygame.draw.rect(self.window, self.color, self.rect, border_radius=12)
        self.window.blit(self.label_b, self.label_b_rect)
        self.window.blit(self.label, self.label_rect)
        return None
