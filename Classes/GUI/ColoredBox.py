import pygame


class ColoredBox:
    def __init__(self, window: pygame.Surface, pos: tuple[int, int], size: tuple[int, int], color: pygame.Color,
                 hidden: bool = False):
        self.window: pygame.Surface = window
        self.rect: pygame.Rect = pygame.Rect(pos, size)
        self.color: pygame.Color = color
        self.hidden: bool = hidden
    
    def draw(self) -> None:
        if not self.hidden:
            pygame.draw.rect(self.window, self.color, self.rect, border_radius=12)
        return None
