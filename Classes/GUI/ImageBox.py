import pygame


class ImageBox:
    def __init__(self, window: pygame.Surface, pos: tuple[int, int], size: tuple[int, int]):
        self.window: pygame.Surface = window
        self.rect = pygame.Rect(pos, size)
        self.image: pygame.Surface | None = None
    
    def update_state(self, image: pygame.Surface | None) -> None:
        self.image = image
        return None
        
    def draw(self) -> None:
        if self.image:
            self.window.blit(self.image, self.rect)
        return None
