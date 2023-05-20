from os.path import join
from time import time

import pygame

from Classes.GUI.Button import Button

ascii_set: str = "1234567890abcdefghijklmnopqrstuvwxyz=-+_!@#$%^&*()"


class InputBox(Button):
    def __init__(self, window: pygame.Surface, pos: tuple[int, int], size: tuple[int, int], text_height: int,
                 bg_color: pygame.Color | None, active_color: pygame.Color | None,
                 text_color: pygame.Color, max_length: int, accepted_keys: str = ascii_set):
        super().__init__(window, pos, size)
        self.text_height, self.bg_color, self.active_color, self.text_color, self.max_length = \
            text_height, bg_color, active_color, text_color, max_length
        self.color: pygame.Color = bg_color
        self.text: str = ""
        self.font: pygame.font = pygame.font.Font(join("Assets", "fcm.otf"), text_height)
        self.accepted: str = accepted_keys
        self.enabled: bool = False
        self.changed_enabled: bool = False
    
    def update_field(self, events: list[pygame.event]) -> bool:
        super().update()
        old_enabled: bool = self.enabled
        if self.clicked:
            self.enabled = True
        elif pygame.mouse.get_pressed()[0] and not self.hover:
            self.enabled = False
        
        for event in events:
            if event.type == pygame.KEYDOWN and self.enabled:
                try:
                    if event.key in (pygame.K_ESCAPE, pygame.K_RETURN, pygame.K_KP_ENTER):
                        self.enabled = False
                    elif event.key == pygame.K_BACKSPACE:
                        if len(self.text) > 0:
                            self.text = self.text[:-1]
                    elif event.unicode.lower() in self.accepted:
                        if len(self.text) < self.max_length:
                            self.text += event.unicode.upper()
                except AttributeError:  # If there is no ASCII for the "input" key
                    pass
        
        self.changed_enabled = old_enabled != self.enabled
        self.color = self.active_color if self.enabled else self.bg_color
        return self.enabled
    
    def draw(self) -> None:
        if self.color:
            pygame.draw.rect(self.window, self.color, self.rect, border_radius=5)
        
        label: pygame.Surface = self.font.render(self.text, True, self.text_color)
        label_rect: pygame.Rect = label.get_rect(midleft=self.rect.midleft)
        label_rect.x += 5
        self.window.blit(label, label_rect)
        
        # Blinking cursor
        if self.enabled and int(time() * 2) % 2:  # Blink rate is 500ms
            cursor_pos: tuple[int, int] = label_rect.right, label_rect.top + 3
            pygame.draw.rect(self.window, self.text_color, pygame.Rect(cursor_pos, (2, self.text_height)))
        
        return None
