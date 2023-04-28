from os import path
from enum import Enum
from contextlib import redirect_stdout
with redirect_stdout(None):
    import pygame

from Assets.colors import *
from Classes.GUI.TabButton import TabButton
from Classes.GUI.TextBox import TextBox
from Classes.GUI.ToggleBox import ToggleBox
from Classes.GUI.RadioButtons import RadioButtons
from Classes.GUI.ColoredBox import ColoredBox
from Classes.GUI.QubeRender import *
from Classes.Utility.Qube import *


class Tab(Enum):
    QUBE = 0
    CFOP = 1
    TIME = 2


class SFXChannel(Enum):
    TAB = 0
    GUI = 1
    ROTATE = 2


# Window Properties
_RES: tuple[int, int] = (1200, 900)
_TITLE: str = "dQubr Project"
_TICK_RATE: int = 120


def program_window():
    pygame.init()
    window: pygame.Surface = pygame.display.set_mode(_RES, pygame.DOUBLEBUF)
    window.fill(BG_COLOR)
    pygame.display.set_caption(_TITLE)
    
    clock: pygame.time.Clock = pygame.time.Clock()
    
    # Sounds
    tab_sound: pygame.mixer.Sound = pygame.mixer.Sound(path.join("Assets", "TabClick.wav"))
    pygame.mixer.Channel(SFXChannel.TAB.value).set_volume(0.4)
    
    # Tab buttons
    qube_tab_btn: TabButton = TabButton(window, (50, 10), (200, 60), "Virtual Qube")
    cfop_tab_btn: TabButton = TabButton(window, (260, 10), (200, 60), "CFOP Solver")
    time_tab_btn: TabButton = TabButton(window, (470, 10), (200, 60), "Times")
    active_tab: int = Tab.QUBE.value

    qube = Qube3()
    qube_size: int = 3
    is_qube_form: bool = False
    
    qube_renderers: tuple = (None, None, QubeRender3, None)
    
    # GUI elements of each tab
    qube_tab_gui: list = [TextBox(window, (500, 500), 60, "Turning and turning", DARK_GREY),
                          
                          TextBox(window, (1000, 100), 32, "Cube Size", DARK_GREY),
                          RadioButtons(window, (950, 150), ("1x1x1", "2x2x2", "3x3x3", "4x4x4"), DARK_GREY, 2),
                          
                          ColoredBox(window, (40, 80), (800, 600), LAYER1_COLOR),
                          TextBox(window, (120, 100), 24, "Cube Style", DARK_GREY),
                          TextBox(window, (75, 131), 18, "Net", DARK_GREY),
                          ToggleBox(window, (100, 125), DARK_GREY, False),
                          TextBox(window, (160, 132), 18, "Cube", DARK_GREY),
                          
                          QubeRender3(window, (400, 400), qube_size, is_qube_form)]
    cfop_tab_gui: tuple = (TextBox(window, (700, 300), 60, "Solving this and that", DARK_GREY),)
    time_tab_gui: tuple = (TextBox(window, (600, 600), 60, "Times are a\'changing", DARK_GREY),
                           TextBox(window, (400, 400), 60, "00", DARK_GREY))
    guis: tuple = qube_tab_gui, cfop_tab_gui, time_tab_gui
    
    fc, xc, yc, zc, rc, lc, uc, dc, bc, mc = False, False, False, False, False, False, False, False, False, False

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
                pygame.mixer.Channel(SFXChannel.TAB.value).play(tab_sound)
                
            tab_button.draw()
        
        if 1:
            # cst = "–––––––––––––––––––––––––––––––\n"\
            #       f"          {qube.up.up()}\n"\
            #       f"          {qube.up.mid_h()}\n"\
            #       f"          {qube.up.down()}\n"\
            #       f"{qube.left.up()} {qube.front.up()} {qube.right.up()} {qube.back.up()}\n"\
            #       f"{qube.left.mid_h()} {qube.front.mid_h()} {qube.right.mid_h()} {qube.back.mid_h()}\n"\
            #       f"{qube.left.down()} {qube.front.down()} {qube.right.down()} {qube.back.down()}\n"\
            #       f"          {qube.down.up()}\n"\
            #       f"          {qube.down.mid_h()}\n"\
            #       f"          {qube.down.down()}\n"
            
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

            if keys_pressed[pygame.K_r] and not rc:
                qube.r(keys_pressed[pygame.K_LSHIFT])
                rc = True
            elif not keys_pressed[pygame.K_r]:
                rc = False

            if keys_pressed[pygame.K_l] and not lc:
                qube.l(keys_pressed[pygame.K_LSHIFT])
                lc = True
            elif not keys_pressed[pygame.K_l]:
                lc = False

            if keys_pressed[pygame.K_u] and not uc:
                qube.u(keys_pressed[pygame.K_LSHIFT])
                uc = True
            elif not keys_pressed[pygame.K_u]:
                uc = False

            if keys_pressed[pygame.K_d] and not dc:
                qube.d(keys_pressed[pygame.K_LSHIFT])
                dc = True
            elif not keys_pressed[pygame.K_d]:
                dc = False
            
            if keys_pressed[pygame.K_b] and not bc:
                qube.b(keys_pressed[pygame.K_LSHIFT])
                bc = True
            elif not keys_pressed[pygame.K_b]:
                bc = False
            
            if keys_pressed[pygame.K_m] and not mc:
                qube.m(keys_pressed[pygame.K_LSHIFT])
                mc = True
            elif not keys_pressed[pygame.K_m]:
                mc = False
            
            if keys_pressed[pygame.K_F5]:
                qube.reset()
            
            # dst = "–––––––––––––––––––––––––––––––\n"\
            #       f"          {qube.up.up()}\n"\
            #       f"          {qube.up.mid_h()}\n"\
            #       f"          {qube.up.down()}\n"\
            #       f"{qube.left.up()} {qube.front.up()} {qube.right.up()} {qube.back.up()}\n"\
            #       f"{qube.left.mid_h()} {qube.front.mid_h()} {qube.right.mid_h()} {qube.back.mid_h()}\n"\
            #       f"{qube.left.down()} {qube.front.down()} {qube.right.down()} {qube.back.down()}\n"\
            #       f"          {qube.down.up()}\n"\
            #       f"          {qube.down.mid_h()}\n"\
            #       f"          {qube.down.down()}\n"
            #
            # if cst != dst:
            #     print(dst)
        
        pygame.draw.rect(window, FRAME_COLOR, pygame.Rect((20, 60), (1160, 820)), border_radius=12)  # Tab Background
        for element in guis[active_tab]:
            try:
                element.update()
                if type(element) == ToggleBox:
                    if active_tab == Tab.QUBE.value:
                        is_qube_form = element.state
                if type(element) == RadioButtons:
                    if active_tab == Tab.QUBE.value:
                        qube_size = element.selected + 1
            except AttributeError:  # Element is static
                pass
            
            # Update Qube Render
            qube_tab_gui[-1] = qube_renderers[qube_size - 1](window, qube_tab_gui[-1].pos, qube_size, is_qube_form)
            
            try:
                element.draw()
            except TypeError:  # Is QubeRenderer
                qube_tab_gui[-1].draw(qube)
        
        pygame.display.update()
        clock.tick(_TICK_RATE)


if __name__ == '__main__':
    program_window()
    pygame.quit()
