from os import path
from time import time
from enum import Enum
from contextlib import redirect_stdout
with redirect_stdout(None):
    import pygame

from Assets.colors import *
from Classes.GUI.TabButton import TabButton
from Classes.GUI.TextBox import TextBox
from Classes.GUI.ToggleBox import ToggleBox
from Classes.GUI.InputBox import InputBox
from Classes.GUI.RadioButtons import RadioButtons
from Classes.GUI.ColoredBox import ColoredBox
from Classes.GUI.Leaderboard import Leaderboard
from Classes.GUI.QubeRender import QubeRender
from Classes.GUI.ImageBox import ImageBox
from Classes.GUI.QubeButton import QubeButton
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


def process_time(time: float) -> tuple[int, int, int]:
    time = min(time, 99 * 60 + 99.99)  # Set a maximum possible time of 99:99:99
    minutes: int = int(time // 60)
    time -= minutes * 60
    seconds: int = int(time)
    time -= seconds
    centiseconds: int = int(time * 100)
    return minutes, seconds, centiseconds


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
    scrambled: bool = False
    
    is_ready: bool = False
    timer_running: bool = False
    start_time: float = time()
    current_time: float = start_time
    left_keys: set = {pygame.K_q, pygame.K_w, pygame.K_e, pygame.K_r,
                      pygame.K_a, pygame.K_s, pygame.K_d, pygame.K_f,
                      pygame.K_z, pygame.K_x, pygame.K_c, pygame.K_v}
    right_keys: set = {pygame.K_u, pygame.K_i, pygame.K_o, pygame.K_p,
                       pygame.K_j, pygame.K_k, pygame.K_l, pygame.K_SEMICOLON,
                       pygame.K_m, pygame.K_COMMA, pygame.K_PERIOD, pygame.K_SLASH}
    dummy_times: tuple = (("PLR", "00:58.21"), ("PLR", "00:30.00"), ("PLR", "00:47.60"), ("PLR", "01:08.75"))
    
    # GUI elements of each tab
    qube_tab_gui: tuple = (TextBox(window, (900, 800), 40, "Turning and turning...", DARK_GREY),
                           TextBox(window, (960, 850), 40, "here and there...", DARK_GREY),

                           TextBox(window, (1000, 100), 32, "Cube Size", DARK_GREY),
                           RadioButtons(window, (950, 150), ("1x1x1", "2x2x2", "3x3x3"), DARK_GREY, 2),
                           

                           ColoredBox(window, (40, 80), (800, 600), LAYER1_COLOR),
                           TextBox(window, (120, 100), 24, "Cube Style", DARK_GREY),
                           TextBox(window, (75, 131), 18, "Net", DARK_GREY),
                           ToggleBox(window, (100, 125), DARK_GREY, False),
                           TextBox(window, (160, 132), 18, "Cube", DARK_GREY),
                           
                           QubeButton(window, (358, 180), (330, 200), "L\'", 2),
                           QubeButton(window, (400, 180), (372, 200), "M\'", 3),
                           QubeButton(window, (442, 180), (414, 200), "R", 2),
                           QubeButton(window, (358, 620), (258, 550), "L", 2),
                           QubeButton(window, (400, 620), (300, 550), "M", 3),
                           QubeButton(window, (442, 620), (342, 550), "R\'", 2),
                           
                           QubeButton(window, (180, 358), (150, 358), "U", 2),
                           QubeButton(window, (180, 400), (150, 400), "E\'", 3),
                           QubeButton(window, (180, 442), (150, 442), "D\'", 2),
                           QubeButton(window, (750, 358), (520, 288), "U\'", 2),
                           QubeButton(window, (750, 400), (520, 330), "E", 3),
                           QubeButton(window, (750, 442), (520, 372), "D", 2),
                           
                           QubeButton(window, (535, 226), (380, 490), "B\'", 2),
                           QubeButton(window, (515, 268), (410, 460), "S", 3),
                           QubeButton(window, (495, 310), (440, 430), "F", 2),
                           QubeButton(window, (310, 310), (210, 320), "F\'", 2),
                           QubeButton(window, (290, 268), (240, 290), "S\'", 3),
                           QubeButton(window, (270, 226), (270, 260), "B", 2),

                           QubeButton(window, (100, 180), None, "x", 1),
                           QubeButton(window, (142, 180), None, "y", 1),
                           QubeButton(window, (184, 180), None, "z", 1),
                           QubeButton(window, (100, 222), None, "x\'", 1),
                           QubeButton(window, (142, 222), None, "y\'", 1),
                           QubeButton(window, (184, 222), None, "z\'", 1),
                           
                           ImageBox(window, (200, 200), (530, 400)),
                           TextBox(window, (690, 230), 28, "", DARK_GREY),
                           QubeRender(window, (750, 330), qube_size, is_cube_form),
                           
                           TextBox(window, (37, 780), 14, "", DARK_GREY, True),
                           TextBox(window, (37, 710), 36, "Move History", DARK_GREY, True),
                           TextBox(window, (40, 750), 16, "", DARK_GREY, True),

                           QubeRender(window, (400, 400), qube_size, is_cube_form))
    cfop_tab_gui: tuple = (TextBox(window, (700, 300), 60, "Solving this and that", DARK_GREY),)
    time_tab_gui: tuple = (TextBox(window, (400, 750), 60, "Times are a\'changing", DARK_GREY),
                           TextBox(window, (50, 100), 40, "Name:", DARK_GREY, True),
                           InputBox(window, (200, 75), (250, 50), 40, LAYER1_COLOR, LAYER2_COLOR, DARK_GREY, 7),
                           
                           ColoredBox(window, (800, 75), (365, 600), LAYER1_COLOR),
                           TextBox(window, (990, 110), 36, "Leaderboard", DARK_GREY),
                           Leaderboard(window, (820, 150), 16, DARK_GREY, dummy_times),
                           
                           ColoredBox(window, (100, 200), (600, 160), LAYER1_COLOR),
                           TextBox(window, (300, 275), 100, ":", DARK_GREY),
                           TextBox(window, (500, 275), 100, ".", DARK_GREY),
                           TextBox(window, (200, 280), 100, "00", DARK_GREY),
                           TextBox(window, (400, 280), 100, "00", DARK_GREY),
                           TextBox(window, (600, 280), 100, "00", DARK_GREY),)
    guis: tuple = qube_tab_gui, cfop_tab_gui, time_tab_gui
    
    # Cooldowns
    fc, xc, yc, zc, rc, lc, uc, dc, bc, mc, ec, sc = tuple(False for _ in range(12))
    undo_cool = False
    timer_cool = False

    running: bool = True
    while running:
        events: list[pygame.event] = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                running = False
                break
        keys_pressed: pygame.key.ScancodeWrapper = pygame.key.get_pressed()
        
        for i, tab_button in enumerate((qube_tab_btn, cfop_tab_btn, time_tab_btn)):
            tab_button.update(active_tab == i)  # Sets button to hover color if its tab is active
            if tab_button.clicked and not active_tab == i:  # Prevent sound from playing if tab already selected
                active_tab = i
                pygame.mixer.Channel(SFXChannel.TAB.value).play(tab_sound)
                
            tab_button.draw()
        
        if active_tab == Tab.QUBE.value:
            primed: bool = keys_pressed[pygame.K_LSHIFT] | keys_pressed[pygame.K_RSHIFT]
            try:  # Keyboard moving system
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
                
                if keys_pressed[pygame.K_e] and not ec:
                    qube.e(primed)
                    move_history.append("E" + ("\'" if primed else ""))
                    ec = True
                elif not keys_pressed[pygame.K_e]:
                    ec = False
                
                if keys_pressed[pygame.K_s] and not sc:
                    qube.s(primed)
                    move_history.append("S" + ("\'" if primed else ""))
                    sc = True
                elif not keys_pressed[pygame.K_s]:
                    sc = False
            except AttributeError:
                pass
            
            try:  # Undo system
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

            if keys_pressed[pygame.K_F8]:
                random_move_attempts: int = 20
                qube.reset()
                scramble = generate_shuffle(qube_size, random_move_attempts)
                qube.apply_moves(scramble)
                move_history = scramble
                scrambled = True
                qube_tab_gui[-3].update_text("Moves to Scramble")
            
            if fc | xc | yc | zc | rc | lc | uc | dc | bc | mc | undo_cool:  # If any move has been made
                scrambled = False
                # Set textbox to original text
                qube_tab_gui[-3].update_text("Move History")
            
            if not len(move_history):  # If move_history is empty
                # Hide move history textbox
                qube_tab_gui[-3].update_text("")
            else:
                qube_tab_gui[-3].update_text("Moves to Scramble" if scrambled else "Move History")
                qube_tab_gui[-4].update_text("Start with WHITE front, RED top" if scrambled else "")
            
            if keys_pressed[pygame.K_F5]:
                qube.reset()
                move_history.clear()
            
            qube_tab_gui[-6].update_text("Back View" if is_cube_form else "")
            
            # Update Move History text
            reverse_history: int = 1 if scrambled else -1
            qube_tab_gui[-2].update_text(", ".join((move_history[:35 * reverse_history:reverse_history])))
        elif active_tab == Tab.TIME.value:
            # Update name input
            input_box_active: bool = time_tab_gui[2].update_field(events)
            
            if not input_box_active:
                left_activated, right_activated = False, False
                for key in left_keys:
                    if keys_pressed[key]:
                        left_activated = True
                        break
                for key in right_keys:
                    if keys_pressed[key]:
                        right_activated = True
                        break
                
                if not timer_running:
                    if left_activated and right_activated and not timer_cool:
                        is_ready = True
                        current_time = start_time
                    else:
                        if is_ready:
                            is_ready = False
                            timer_running = True
                            start_time = time()
                            current_time = start_time
                        elif not (left_activated and right_activated):
                            timer_cool = False
                else:
                    current_time = time()
                    if left_activated and right_activated:
                        timer_running = False
                        timer_cool = True
            
            # Update timer
            display_time: tuple = process_time(current_time - start_time)
            time_tab_gui[-3].update_text("%02d" % display_time[0])
            time_tab_gui[-2].update_text("%02d" % display_time[1])
            time_tab_gui[-1].update_text("%02d" % display_time[2])
        
        pygame.draw.rect(window, FRAME_COLOR, pygame.Rect((20, 60), (1160, 820)), border_radius=20)  # Tab Background
        for element in guis[active_tab]:  # Draw rest of GUI elements for the tab
            try:
                if type(element) == QubeButton:
                    if active_tab == Tab.QUBE.value:
                        move: str | None = element.update_state(qube_size, is_cube_form)
                        if move is not None:
                            qube.apply_moves((move,))
                            move_history.append(move)
                else:
                    element.update()
                    if type(element) == ToggleBox:
                        if active_tab == Tab.QUBE.value:
                            is_cube_form = element.state
                    if type(element) == RadioButtons:
                        if active_tab == Tab.QUBE.value:
                            old_q_size: int = qube_size
                            qube_size = element.selected + 1
                            # Update Qube Render
                            qube_tab_gui[-1].size = qube_size
                            qube_tab_gui[-5].size = qube_size
                            qube_tab_gui[-1].is_cube_form = is_cube_form
                            if old_q_size != qube_size:
                                qube = qube_types[qube_size - 1]()
                                move_history.clear()
            except (AttributeError, TypeError):  # Element is static or requires an argument
                pass
            
            try:
                element.draw()
            except TypeError:  # Is QubeRenderer
                qube_tab_gui[-1].draw(qube)
                if is_cube_form:
                    qube_tab_gui[-5].draw(qube, back_view=True)
        
        pygame.display.update()
        clock.tick(_TICK_RATE)


if __name__ == '__main__':
    program_window()
    pygame.quit()
