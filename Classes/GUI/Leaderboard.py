from os import path

import pygame

from Assets.colors import DARK_GREY, REST_BTN_COLOR, HOVER_BTN_COLOR, WARN_RED, FADED_GREY
from Classes.GUI.Button import Button
from Classes.GUI.TextBox import TextBox
from Classes.GUI.TextButton import TextButton
from Classes.GUI.Tooltip import Tooltip
from Classes.Utility.Shapes import draw_left_triangle, draw_right_triangle

MAX_HEIGHT: int = 12  # Leaderboard is 2 columns by MAX_HEIGHT rows


class ArrowButton(Button):
    def __init__(self, window: pygame.Surface, pos: tuple[int, int], size: int, direction: str):
        super().__init__(window, pos, (size, size))
        self.rest_color, self.hover_color, self.color = REST_BTN_COLOR, HOVER_BTN_COLOR, REST_BTN_COLOR
        self.direction: str = direction
    
    def update(self) -> None:
        super().update()
        self.color = self.hover_color if self.hover else self.rest_color
        return None
    
    def draw(self) -> None:
        if self.direction.lower().startswith('r'):
            draw_right_triangle(self.window, self.pos, self.size[0], self.color)
        else:
            draw_left_triangle(self.window, self.pos, self.size[0], self.color)
        return None


class TextBoxButton(TextBox):
    def __init__(self, window: pygame.Surface, pos: tuple[int, int], height: int, text: str, color: pygame.Color,
                 delete_mode: bool = False):
        super().__init__(window, pos, height, text, color, True, True)
        self.delete_mode: bool = delete_mode
        self.hover: bool = False
    
    def update(self) -> bool:
        self.hover: bool = self.label_rect.collidepoint(pygame.mouse.get_pos())
        return self.hover and pygame.mouse.get_pressed()[0]  # If clicked
        
    def draw(self) -> None:
        if self.delete_mode:
            if self.hover:
                pygame.draw.rect(self.window, WARN_RED, self.label_rect)
        super().draw()
        return None


class Leaderboard:
    def __init__(self, window: pygame.Surface, pos: tuple[int, int], text_size: int, color: pygame.Color,
                 entries: list[tuple[str, str]] | None):
        self.window, self.pos, self.text_size, self.color = window, pos, text_size, color
        self.entries: list = [(entry[1], entry[0]) for entry in entries]  # Entered by PLR: TIME
        self.index: int = 0
        self.total_pages: int = 0
        self.refresh()
        
        self.empty_prompt: TextBox = TextBox(self.window, (self.pos[0] + 160, self.pos[1] + 30), 14,
                                             "Your saved times will appear here", FADED_GREY, False, True)
        self.page_records: list = []
        paging_pos: tuple[int, int] = self.pos[0] + 180, self.pos[1] + int(1.8 * MAX_HEIGHT) * text_size
        self.page_text: TextBox = TextBox(window, paging_pos, 16, f"Page {1} of {self.total_pages + 1}", DARK_GREY)
        self.decrement_btn: ArrowButton = ArrowButton(self.window, (paging_pos[0] - 70, paging_pos[1] - 8), 15, "left")
        self.increment_btn: ArrowButton = ArrowButton(self.window, (paging_pos[0] + 60, paging_pos[1] - 8), 15, "right")
        
        self.delete_mode_btn: TextButton = TextButton(self.window, (paging_pos[0] - 170, paging_pos[1] - 15), (80, 30),
                                                      "", 18, None, "Delete entries by clicking", (200, 30))
        self.delete_btn_label: TextBox = TextBox(self.window, (paging_pos[0] - 130, paging_pos[1]), 16,
                                                 "Remove", DARK_GREY)
        self.delete_prompt: TextBox = TextBox(self.window, (paging_pos[0], paging_pos[1] - 35), 16, "", WARN_RED)
        self.delete_mode: bool = False
        self.click_cool: bool = False
        self.changed: bool = False
    
    def increment_page(self) -> bool:
        old_index: int = self.index
        self.index = min(self.index + 1, self.total_pages)
        return old_index != self.index  # Returns if page changed
    
    def decrement_page(self) -> bool:
        old_index: int = self.index
        self.index = max(self.index - 1, 0)
        return old_index != self.index  # Returns if page changed
    
    def refresh(self) -> None:
        """
        Refresh number of pages and edits the leaderboard file
        """
        self.total_pages = (len(self.entries) - 1) // (2 * MAX_HEIGHT)
        self.index = min(self.index, self.total_pages)
        self.index = max(0, self.index)
        self.entries.sort(key=lambda entry: entry[1])
        with open(path.join("Assets", "times.timmy"), 'w') as file:
            file.write("\n".join(f"{name} {time}" for name, time in self.entries))
        return None
    
    def add(self, entry: tuple[str, str]) -> None:
        """
        Receives (time, player) and adds to local leaderboard and leaderboard file
        """
        self.entries.append((entry[1], entry[0]))
        self.refresh()
        return None
    
    def update(self) -> None:
        self.changed = False
        
        if len(self.entries):  # If there are entries on the leaderboard
            self.decrement_btn.update()
            self.increment_btn.update()
            if self.decrement_btn.clicked:
                if self.decrement_page():
                    self.changed = True
            if self.increment_btn.clicked:
                if self.increment_page():
                    self.changed = True
            
            if not pygame.mouse.get_pressed()[0]:
                self.click_cool = False
            
            self.delete_mode_btn.update()
            if self.delete_mode_btn.clicked:  # Then toggle delete mode
                self.delete_mode = not self.delete_mode
                self.changed = True
        else:
            self.delete_mode = False
        
        self.delete_mode_btn.tooltip = "Finish deleting entries" if self.delete_mode else "Delete entries by clicking"
        self.delete_btn_label.update_text("Done" if self.delete_mode else "Edit")
        self.delete_prompt.update_text("Click on a time to remove it" if self.delete_mode else "")

        # Update the shown records on the leaderboard
        self.page_records.clear()
        for i, entry in enumerate(self.entries[self.index * 2 * MAX_HEIGHT:(self.index + 1) * 2 * MAX_HEIGHT]):
            # Relative positions to leaderboard
            rel_x: int = 0 if i < MAX_HEIGHT else 180
            rel_y: int = (i % MAX_HEIGHT) * int(1.5 * self.text_size)
            self.page_records.append(TextBoxButton(self.window, (self.pos[0] + rel_x, self.pos[1] + rel_y),
                                                   self.text_size, f"{entry[1]:>8} {entry[0]:<7}",
                                                   DARK_GREY, self.delete_mode))
        for i, record in enumerate(self.page_records):
            clicked_entry: bool = record.update()
            if clicked_entry and not self.click_cool:
                self.click_cool = True
                self.changed = True
                if self.delete_mode:
                    self.entries.pop(2 * MAX_HEIGHT * self.index + i)
                    self.refresh()
        return None
    
    def draw(self) -> Tooltip | None:
        """
        Draws the leaderboard entries of this page, page manipulators, and delete mode button
        Returns the tooltip of the delete mode button, if given
        """
        tooltip: Tooltip | None = None
        for record in self.page_records:
            record.draw()
        if len(self.entries):
            self.page_text.update_text(f"Page {self.index + 1} of {self.total_pages + 1}")
            self.page_text.draw()
            self.decrement_btn.draw()
            self.increment_btn.draw()
            tooltip = self.delete_mode_btn.draw()
            self.delete_btn_label.draw()
            self.delete_prompt.draw()
        else:
            self.empty_prompt.draw()
        return tooltip
    
