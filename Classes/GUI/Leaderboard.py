import pygame

from Classes.GUI.TextBox import TextBox
from Assets.colors import DARK_GREY


class Leaderboard:
    def __init__(self, window: pygame.Surface, pos: tuple[int, int], text_size: int, color: pygame.Color,
                 entries: tuple[tuple[str, str]] | None):
        self.window, self.pos, self.text_size, self.color = window, pos, text_size, color
        self.entries: dict = {entry[1]: entry[0] for entry in entries}  # Entered by PLR: TIME
    
    def add(self, entry: tuple[str, str]) -> None:
        self.entries += {entry[1], entry[0]}
        return None
    
    def draw(self) -> None:
        records: list[TextBox] = []
        for i, entry in enumerate(sorted(self.entries.items())):
            records.append(TextBox(self.window, (self.pos[0], self.pos[1] + i * int(1.5 * self.text_size)),
                                   self.text_size, "{:<7} {}".format(entry[1], entry[0]), DARK_GREY, True))
        for record in records:
            record.draw()
        return None
    
