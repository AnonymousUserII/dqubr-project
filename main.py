from os import path
from enum import Enum
from contextlib import redirect_stdout
with redirect_stdout(None):
    import pygame

from Classes.TabButton import TabButton
from Classes.TextBox import TextBox
from Classes.Qube import *


class Tab(Enum):
    QUBE = 0
    CFOP = 1
    TIME = 2


class Channel(Enum):
    TAB = 0
    GUI = 1
    ROTATE = 2


# Window Properties
_RES: tuple[int, int] = (1200, 900)
_TITLE: str = "dQubr Project"
_TICK_RATE: int = 120

# Standardized Colors
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
    
    # Sounds
    tab_sound: pygame.mixer.Sound = pygame.mixer.Sound(path.join("Assets", "TabClick.wav"))
    pygame.mixer.Channel(Channel.TAB.value).set_volume(0.4)
    
    # Tab buttons
    qube_tab_btn: TabButton = TabButton(window, (50, 10), (200, 60), "Virtual Qube")
    cfop_tab_btn: TabButton = TabButton(window, (260, 10), (200, 60), "CFOP Solver")
    time_tab_btn: TabButton = TabButton(window, (470, 10), (200, 60), "Times")
    
    # GUI elements of each tab
    qube_tab_gui: tuple = (TextBox(window, (500, 500), 60, "Turning and turning", DARK_GREY),)
    cfop_tab_gui: tuple = (TextBox(window, (700, 300), 60, "Solving this and that", DARK_GREY),)
    time_tab_gui: tuple = (TextBox(window, (600, 600), 60, "Times are a\'changing", DARK_GREY),)
    guis: tuple = qube_tab_gui, cfop_tab_gui, time_tab_gui
    
    active_tab: int = Tab.QUBE.value
    
    qube = Qube3()
    
    fc, xc, yc, zc = False, False, False, False

    running: bool = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break
        
        for i, tab_button in enumerate((qube_tab_btn, cfop_tab_btn, time_tab_btn)):
            tab_button.update(active_tab == i)  # Sets button to hover color if its tab is active
            if tab_button.clicked and not active_tab == i:  # Prevent sound from playing if tab already selected
                active_tab = i
                pygame.mixer.Channel(Channel.TAB.value).play(tab_sound)
                
            tab_button.draw()
        
        if 1:
            cst = "–––––––––––––––––––––––––––––––\n"\
                  f"          {qube.up.up()}\n"\
                  f"          {qube.up.mid_h()}\n"\
                  f"          {qube.up.down()}\n"\
                  f"{qube.left.up()} {qube.front.up()} {qube.right.up()} {qube.back.up()}\n"\
                  f"{qube.left.mid_h()} {qube.front.mid_h()} {qube.right.mid_h()} {qube.back.mid_h()}\n"\
                  f"{qube.left.down()} {qube.front.down()} {qube.right.down()} {qube.back.down()}\n"\
                  f"          {qube.down.up()}\n"\
                  f"          {qube.down.mid_h()}\n"\
                  f"          {qube.down.down()}\n"
            
            keys_pressed: pygame.key.ScancodeWrapper = pygame.key.get_pressed()
            if keys_pressed[pygame.K_f] and not fc:
                qube.f(keys_pressed[pygame.K_LSHIFT])
                fc = True
            elif not keys_pressed[pygame.K_f]:
                fc = False
            
            if keys_pressed[pygame.K_x] and not xc:
                qube.x(keys_pressed[pygame.K_LSHIFT])
                xc = True
            elif not keys_pressed[pygame.K_x]:
                xc = False
            
            if keys_pressed[pygame.K_y] and not yc:
                qube.y(keys_pressed[pygame.K_LSHIFT])
                yc = True
            elif not keys_pressed[pygame.K_y]:
                yc = False
            
            if keys_pressed[pygame.K_z] and not zc:
                qube.z(keys_pressed[pygame.K_LSHIFT])
                zc = True
            elif not keys_pressed[pygame.K_z]:
                zc = False
            
            dst = "–––––––––––––––––––––––––––––––\n"\
                  f"          {qube.up.up()}\n"\
                  f"          {qube.up.mid_h()}\n"\
                  f"          {qube.up.down()}\n"\
                  f"{qube.left.up()} {qube.front.up()} {qube.right.up()} {qube.back.up()}\n"\
                  f"{qube.left.mid_h()} {qube.front.mid_h()} {qube.right.mid_h()} {qube.back.mid_h()}\n"\
                  f"{qube.left.down()} {qube.front.down()} {qube.right.down()} {qube.back.down()}\n"\
                  f"          {qube.down.up()}\n"\
                  f"          {qube.down.mid_h()}\n"\
                  f"          {qube.down.down()}\n"
            
            if cst != dst:
                print(dst)
        
        pygame.draw.rect(window, FRAME_COLOR, pygame.Rect((20, 60), (1160, 820)), border_radius=12)  # Tab Background
        for element in guis[active_tab]:
            element.draw()
        
        pygame.display.update()
        clock.tick(_TICK_RATE)


if __name__ == '__main__':
    program_window()
    pygame.quit()
