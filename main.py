from enum import Enum
from contextlib import redirect_stdout
with redirect_stdout(None):
    import pygame

from Classes.TabButton import TabButton
from Classes.TextBox import TextBox


class Tab(Enum):
    QUBE = 0
    CFOP = 1
    TIME = 2


# Window Constants
_RES: tuple[int, int] = (1200, 900)
_TITLE: str = "dQubr Project"
_REFRESH_RATE: int = 60

# Standard Colors
DARK_GREY: pygame.Color = pygame.Color(0x10, 0x10, 0x10)
BG_COLOR: pygame.Color = pygame.Color(0x77, 0xC0, 0xF7)
FRAME_COLOR: pygame.Color = pygame.Color(0xAE, 0xDF, 0xFC)
REST_BTN_COLOR: pygame.Color = pygame.Color(0x8A, 0xD2, 0xFB)


def program_window():
    pygame.init()
    window: pygame.Surface = pygame.display.set_mode(_RES, pygame.DOUBLEBUF)
    window.fill(BG_COLOR)
    pygame.display.set_caption(_TITLE)
    clock: pygame.time.Clock = pygame.time.Clock()
    
    # GUI Elements
    qube_tab_btn: TabButton = TabButton(window, (100, 30), (200, 60), REST_BTN_COLOR, FRAME_COLOR,
                                        DARK_GREY, "Virtual Qube")
    cfop_tab_btn: TabButton = TabButton(window, (310, 30), (200, 60), REST_BTN_COLOR, FRAME_COLOR,
                                        DARK_GREY, "CFOP Solver")
    time_tab_btn: TabButton = TabButton(window, (520, 30), (200, 60), REST_BTN_COLOR, FRAME_COLOR,
                                        DARK_GREY, "Times")
    
    qube_tab_gui: tuple = (TextBox(window, (500, 500), 60, "Turning and turning", DARK_GREY),)
    cfop_tab_gui: tuple = (TextBox(window, (500, 500), 60, "Solving this and that", DARK_GREY),)
    time_tab_gui: tuple = (TextBox(window, (500, 500), 60, "Times are a\'changing", DARK_GREY),)
    guis: tuple = qube_tab_gui, cfop_tab_gui, time_tab_gui
    
    active_tab: int = Tab.QUBE.value
    
    running: bool = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break
        
        for i, tab_button in enumerate((qube_tab_btn, cfop_tab_btn, time_tab_btn)):
            if tab_button.update(i == active_tab):
                active_tab = i
            tab_button.draw()
            
        pygame.draw.rect(window, FRAME_COLOR, pygame.Rect((80, 80), (1040, 780)), border_radius=12)  # Tab Background
        for element in guis[active_tab]:
            element.draw()
        
        pygame.display.update()
        clock.tick(_REFRESH_RATE)


if __name__ == '__main__':
    program_window()
