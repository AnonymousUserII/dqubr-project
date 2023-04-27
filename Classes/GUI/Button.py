import pygame


class Button:
    def __init__(self, window: pygame.Surface, pos: tuple[int, int], size: tuple[int, int]):
        self.window, self.pos, self.size = window, pos, size
        self.rect: pygame.Rect = pygame.Rect(self.pos, self.size)
        self.hover, self.clicked, self.click_cooldown = False, False, False
    
    def update(self) -> None:
        self.hover = self.rect.collidepoint(pygame.mouse.get_pos())
        lmb_clicked: bool = pygame.mouse.get_pressed()[0]
        self.clicked = self.hover and lmb_clicked and not self.click_cooldown
        self.click_cooldown = lmb_clicked or self.clicked  # Requires mouse to be released before clicking again
        return None
