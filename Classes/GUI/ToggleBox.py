import pygame

from Classes.GUI.Button import Button

element_size: tuple[int, int] = 30, 15


class ToggleBox(Button):
    def __init__(self, window: pygame.Surface, pos: tuple[int, int], color: pygame.Color, init: bool = False):
        super().__init__(window, pos, element_size)
        self.color: pygame.Color = color
        self.state: bool = init  # False is left
    
    def update(self) -> None:
        super().update()
        if self.clicked:
            self.state = not self.state  # i.e. Toggle
        return None
    
    def draw(self):
        pygame.draw.rect(self.window, self.color, self.rect, 1, 3)
        toggle_x = self.rect.x + (17 if self.state else 2)
        pygame.draw.rect(self.window, self.color, pygame.Rect((toggle_x, self.rect.y + 2), (11, 11)), border_radius=2)
        return None
