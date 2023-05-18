from os import path

import pygame

from Classes.GUI.TextBox import TextBox
from Assets.colors import DARK_GREY

MAX_HEIGHT: int = 12  # Leaderboard is 2 columns by MAX_HEIGHT rows


class Leaderboard:
    def __init__(self, window: pygame.Surface, pos: tuple[int, int], text_size: int, color: pygame.Color,
                 entries: list[tuple[str, str]] | None):
        self.window, self.pos, self.text_size, self.color = window, pos, text_size, color
        self.entries: tuple = tuple((entry[1], entry[0]) for entry in entries)  # Entered by PLR: TIME
        self.index: int = 0
    
    def add(self, entry: tuple[str, str]) -> None:
        """
        Receives (time, player) and adds to local and filed leaderboard
        """
        self.entries += {entry[1], entry[0]}
        with open(path.join("Data", "times.txt", 'a')) as file:
            file.write(f"{entry[0]} {entry[1]}\n")
        return None
    
    def draw(self) -> None:
        records: list[TextBox] = []
        for i, entry in enumerate(self.entries):
            # Do not draw records not on this page
            if i < 2 * MAX_HEIGHT * self.index:
                continue
            if 2 * MAX_HEIGHT * (self.index + 1) < i - 1:
                break
            
            rel_y: int = i - 2 * MAX_HEIGHT * self.index  # Relative index of record on its page
            rel_x: int = 0
            if rel_y > MAX_HEIGHT:
                rel_x = 180
                rel_y = (i - MAX_HEIGHT - 1) - 2 * MAX_HEIGHT * self.index
            records.append(TextBox(self.window, (self.pos[0] + rel_x, self.pos[1] + rel_y * int(1.5 * self.text_size)),
                                   self.text_size, f"{entry[1]:>10} {entry[0]:<7}", DARK_GREY, True, True))
        for record in records:
            record.draw()
        return None
    
