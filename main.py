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
    qube_types: tuple = Qube1, Qube2, Qube3
    is_cube_form: bool = False
    move_history: list[str] = []
    
    # GUI elements of each tab
    qube_tab_gui: list = [TextBox(window, (500, 500), 60, "Turning and turning", DARK_GREY),

                          TextBox(window, (1000, 100), 32, "Cube Size", DARK_GREY),
                          RadioButtons(window, (950, 150), ("1x1x1", "2x2x2", "3x3x3", "4x4x4"), DARK_GREY, 2),

                          ColoredBox(window, (40, 80), (800, 600), LAYER1_COLOR),
                          TextBox(window, (120, 100), 24, "Cube Style", DARK_GREY),
                          TextBox(window, (75, 131), 18, "Net", DARK_GREY),
                          ToggleBox(window, (100, 125), DARK_GREY, False),
                          TextBox(window, (160, 132), 18, "Cube", DARK_GREY),

                          TextBox(window, (160, 710), 36, "Move History", DARK_GREY),
                          TextBox(window, (160, 750), 16, "", DARK_GREY, True),

                          QubeRender(window, (400, 400), qube_size, is_cube_form)]
    cfop_tab_gui: tuple = (TextBox(window, (700, 300), 60, "Solving this and that", DARK_GREY),)
    time_tab_gui: tuple = (TextBox(window, (600, 600), 60, "Times are a\'changing", DARK_GREY),
                           TextBox(window, (400, 400), 60, "00", DARK_GREY))
    guis: tuple = qube_tab_gui, cfop_tab_gui, time_tab_gui
    
    fc, xc, yc, zc, rc, lc, uc, dc, bc, mc = False, False, False, False, False, False, False, False, False, False
    undo_cool = False

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
            keys_pressed: pygame.key.ScancodeWrapper = pygame.key.get_pressed()
            primed: bool = keys_pressed[pygame.K_LSHIFT] | keys_pressed[pygame.K_RSHIFT]
            old_m_history: int = len(move_history)
            try:
                if keys_pressed[pygame.K_f] and not fc:
                    qube.f(primed)
                    move_history.append("F" + ("\'" if primed else ""))
                    fc = True
                elif not keys_pressed[pygame.K_f]:
                    fc = False
                
                if keys_pressed[pygame.K_x] and not xc:
                    qube.x(primed)
                    move_history.append("x" + ("\'" if primed else ""))
                    xc = True
                elif not keys_pressed[pygame.K_x]:
                    xc = False
                
                if keys_pressed[pygame.K_y] and not yc:
                    qube.y(primed)
                    move_history.append("y" + ("\'" if primed else ""))
                    yc = True
                elif not keys_pressed[pygame.K_y]:
                    yc = False
                
                if keys_pressed[pygame.K_z] and not zc:
                    qube.z(primed)
                    move_history.append("z" + ("\'" if primed else ""))
                    zc = True
                elif not keys_pressed[pygame.K_z]:
                    zc = False
    
                if keys_pressed[pygame.K_r] and not rc:
                    qube.r(primed)
                    move_history.append("R" + ("\'" if primed else ""))
                    rc = True
                elif not keys_pressed[pygame.K_r]:
                    rc = False
    
                if keys_pressed[pygame.K_l] and not lc:
                    qube.l(primed)
                    move_history.append("L" + ("\'" if primed else ""))
                    lc = True
                elif not keys_pressed[pygame.K_l]:
                    lc = False
    
                if keys_pressed[pygame.K_u] and not uc:
                    qube.u(primed)
                    move_history.append("U" + ("\'" if primed else ""))
                    uc = True
                elif not keys_pressed[pygame.K_u]:
                    uc = False
    
                if keys_pressed[pygame.K_d] and not dc:
                    qube.d(primed)
                    move_history.append("D" + ("\'" if primed else ""))
                    dc = True
                elif not keys_pressed[pygame.K_d]:
                    dc = False
                
                if keys_pressed[pygame.K_b] and not bc:
                    qube.b(primed)
                    move_history.append("B" + ("\'" if primed else ""))
                    bc = True
                elif not keys_pressed[pygame.K_b]:
                    bc = False
                
                if keys_pressed[pygame.K_m] and not mc:
                    qube.m(primed)
                    move_history.append("M" + ("\'" if primed else ""))
                    mc = True
                elif not keys_pressed[pygame.K_m]:
                    mc = False
            except AttributeError:
                pass
            
            try:  # Temporary undo system
                if keys_pressed[pygame.K_BACKQUOTE] and not undo_cool:
                    prime: bool = "\'" not in move_history[-1]
                    if 'R' in move_history[-1]:
                        qube.r(prime)
                    elif 'L' in move_history[-1]:
                        qube.l(prime)
                    elif 'F' in move_history[-1]:
                        qube.f(prime)
                    elif 'B' in move_history[-1]:
                        qube.b(prime)
                    elif 'U' in move_history[-1]:
                        qube.u(prime)
                    elif 'D' in move_history[-1]:
                        qube.d(prime)
                    elif 'M' in move_history[-1]:
                        qube.m(prime)
                    elif 'E' in move_history[-1]:
                        qube.e(prime)
                    elif 'S' in move_history[-1]:
                        qube.s(prime)
                    elif 'x' in move_history[-1]:
                        qube.x(prime)
                    elif 'y' in move_history[-1]:
                        qube.y(prime)
                    elif 'z' in move_history[-1]:
                        qube.z(prime)
                    move_history.pop(-1)
                    undo_cool = True
                elif not keys_pressed[pygame.K_BACKQUOTE]:
                    undo_cool = False
            except IndexError:  # No recorded moves
                pass
            
            if old_m_history != len(move_history):  # If a move was made
                # Set textbox to original (from scramble sequence)
                qube_tab_gui[-3] = TextBox(window, (37, 710), 36, "Move History", DARK_GREY, True)
            
            if keys_pressed[pygame.K_F8]:
                random_move_attempts: int = 40
                qube.reset()
                scramble = generate_shuffle(qube_size, random_move_attempts)
                qube.apply_moves(scramble)
                move_history = scramble
                qube_tab_gui[-3] = TextBox(window, (37, 710), 36, "Moves to Scramble", DARK_GREY, True)
            
            if keys_pressed[pygame.K_F5]:
                qube.reset()
                move_history.clear()
        
        pygame.draw.rect(window, FRAME_COLOR, pygame.Rect((20, 60), (1160, 820)), border_radius=20)  # Tab Background
        for element in guis[active_tab]:
            try:
                element.update()
                if type(element) == ToggleBox:
                    if active_tab == Tab.QUBE.value:
                        is_cube_form = element.state
                if type(element) == RadioButtons:
                    if active_tab == Tab.QUBE.value:
                        old_q_size: int = qube_size
                        qube_size = element.selected + 1
                        if old_q_size != qube_size:
                            qube = qube_types[qube_size - 1]()
                            move_history.clear()
            except AttributeError:  # Element is static
                pass
            
            # Update Move History
            qube_tab_gui[-2] = TextBox(window, (40, 750), 16, ", ".join((move_history[:-35:-1])), DARK_GREY, True)
            
            # Update Qube Render
            qube_tab_gui[-1].size = qube_size
            qube_tab_gui[-1].is_cube_form = is_cube_form
            
            try:
                element.draw()
            except TypeError:  # Is QubeRenderer
                qube_tab_gui[-1].draw(qube)
        
        pygame.display.update()
        clock.tick(_TICK_RATE)


if __name__ == '__main__':
    program_window()
    pygame.quit()
