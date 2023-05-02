import pygame

from Classes.GUI.Button import Button


class SpriteButton(Button):
    def __init__(self, window: pygame.Surface, pos: tuple[int, int], size: tuple[int, int],
                 rest_sprite: pygame.Surface, hover_sprite: pygame.Surface | None):
        super().__init__(window, pos, size)
        self.rest_sprite, self.sprite = rest_sprite, rest_sprite
        self.hover_sprite: pygame.Surface = hover_sprite if hover_sprite else rest_sprite
        
    def update(self) -> None:
        super().update()
        self.sprite = self.hover_sprite if self.hover else self.rest_sprite
        return None
    
    def draw(self) -> None:
        self.window.blit(self.sprite, self.rect)
        return None
