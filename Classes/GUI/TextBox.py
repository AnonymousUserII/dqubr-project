from os.path import join
import pygame


class TextBox:
    def __init__(self, window: pygame.Surface, pos: tuple[int, int], height: int, text: str, color: pygame.Color,
                 left_aligned: bool = False, mono_font: bool = False):
        self.window: pygame.Surface = window
        self.pos, self.height, self.color, self.left_aligned = pos, height, color, left_aligned
        self.font = join("Assets", "fcm.ttf" if mono_font else "od.otf")
        self.label: pygame.Surface = pygame.font.Font(self.font, height)\
            .render(text, True, color)
        self.label_rect: pygame.Rect = self.label.get_rect(midleft=pos) if left_aligned else \
            self.label.get_rect(center=pos)
    
    def update_text(self, text: str) -> None:
        self.label: pygame.Surface = pygame.font.Font(self.font, self.height) \
            .render(text, True, self.color)
        self.label_rect: pygame.Rect = self.label.get_rect(midleft=self.pos) if self.left_aligned else \
            self.label.get_rect(center=self.pos)
        return None
    
    def draw(self) -> None:
        self.window.blit(self.label, self.label_rect)
        return None
