import pygame


class ColoredBox:
    def __init__(self, window: pygame.Surface, pos: tuple[int, int], size: tuple[int, int], color: pygame.Color):
        self.window: pygame.Surface = window
        self.rect: pygame.Rect = pygame.Rect(pos, size)
        self.color: pygame.Color = color
    
    def draw(self) -> None:
        pygame.draw.rect(self.window, self.color, self.rect, border_radius=12)
        return None
