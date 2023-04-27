import pygame

from Classes.GUI.Button import Button
from Classes.GUI.TextBox import TextBox

button_radius: int = 12
text_size: int = 16
label_offset: int = 8
rb_spacing: int = 8


class RadioButton(Button):
    def __init__(self, window: pygame.Surface, pos: tuple[int, int], label: str, color: pygame.Color):
        box_pos: tuple[int, int] = pos[0] - button_radius, pos[1]
        label_pos: tuple[int, int] = box_pos[0] + (2 * button_radius) + label_offset, pos[1]
        self.label: TextBox = TextBox(window, label_pos, text_size, label, color, left_aligned=True)
        
        box_size: tuple[int, int] = \
            (2 * button_radius + label_offset + self.label.label.get_width(), max(2 * button_radius, text_size))
        
        super().__init__(window, (box_pos[0], pos[1] - button_radius), box_size)
        self.color: pygame.Color = color
        
    def draw(self, selected: bool) -> None:
        circle_center: tuple[int, int] = self.pos[0] + button_radius, self.pos[1] + button_radius
        pygame.draw.circle(self.window, self.color, circle_center, button_radius, 1)
        if selected:
            pygame.draw.circle(self.window, self.color, circle_center, button_radius - 3)
        self.label.draw()
        return None


class RadioButtons:
    def __init__(self, window: pygame.Surface, pos: tuple[int, int], labels: tuple, color: pygame.Color, init: int = 0):
        self.first_pos: tuple[int, int] = pos
        self.buttons: list[RadioButton] = []
        self.selected: int = init
        
        for i, label in enumerate(labels):
            b_pos = pos[0], pos[1] + i * (max(2 * button_radius, text_size) + rb_spacing)
            self.buttons.append(RadioButton(window, b_pos, label, color))
    
    def update(self) -> None:
        for i, button in enumerate(self.buttons):
            button.update()
            if button.clicked:
                self.selected = i
        return None
    
    def draw(self) -> None:
        for i, button in enumerate(self.buttons):
            button.draw(self.selected == i)
        return None

