from os.path import join
import pygame


class TextBox:
    def __init__(self, window: pygame.Surface, pos: tuple[int, int], height: int, text: str, color: pygame.Color,
                 left_aligned: bool = False):
        self.window: pygame.Surface = window
        self.label: pygame.Surface = pygame.font.Font(join("Assets", "od.otf"), height)\
            .render(text, True, color)
        self.label_rect: pygame.Rect = self.label.get_rect(midleft=pos) if left_aligned else \
            self.label.get_rect(center=pos)
    
    def draw(self) -> None:
        self.window.blit(self.label, self.label_rect)
        return None
