from os import path

import pygame


class Tooltip:
    def __init__(self, window: pygame.Surface, pos: tuple[int, int], box_size: tuple[int, int], text: str,
                 text_size: int, text_color: pygame.Color, box_color: pygame.Color):
        self.window: pygame.Surface = window
        self.rect: pygame.Rect = pygame.Rect(pos, box_size)
        self.label: pygame.Surface = pygame.font.Font(path.join("Assets", "fcm.otf"), text_size)\
            .render(text, True, text_color)
        self.label_rect: pygame.Rect = self.label.get_rect(center=self.rect.center)
        self.box_color: pygame.Color = box_color
    
    def draw(self) -> None:
        pygame.draw.rect(self.window, self.box_color, self.rect, border_radius=5)
        self.window.blit(self.label, self.label_rect)
        return None
