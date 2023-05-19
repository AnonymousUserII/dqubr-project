from os import path
from time import time
from enum import Enum
from contextlib import redirect_stdout
with redirect_stdout(None):
    import pygame

from Assets.colors import *
from Assets.sounds import *
from Classes.GUI.TabButton import TabButton
from Classes.GUI.TextBox import TextBox
from Classes.GUI.TextButton import TextButton
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
    TIME = 1


# Window Properties
_RES: tuple[int, int] = (1200, 660)
_TITLE: str = "dQubr Project"
_TICK_RATE: int = 120

# Program constants
HISTORY_OVERFLOW: int = 24


# Dictionary to hold arrow graphics for qube turning
moves: list[str] = []
for form in ("net", "cube"):
    for rotation in ('f', 'b', 'r', 'l', 'u', 'd', 'm', 'e', 's', 'x', 'y', 'z'):
        moves.append(f"{form}_{rotation}")
        moves.append(f"{form}_{rotation}p")
qube_arrows: dict[str, pygame.Surface] = {}
for move in moves:
    qube_arrows[move] = pygame.image.load(path.join("Assets", "QubeArrows", f"{move}.png"))

# Dictionary to hold keyboard graphics for the two-hand timer
keyboard_img: dict[str, pygame.Surface] = {"none": pygame.image.load(path.join("Assets", "keyboard_base.png")),
                                           "left": pygame.image.load(path.join("Assets", "keyboard_l.png")),
                                           "right": pygame.image.load(path.join("Assets", "keyboard_r.png")),
                                           "both": pygame.image.load(path.join("Assets", "keyboard_lr.png"))}

# Retrieve leaderboard times from file
with open(path.join("Data", "times.timmy")) as time_history:
    times: list = time_history.read().strip().split("\n")
    leaderboard: list = []
    for record in times:
        if not record:  # If the line is blank
            continue
        (player, score) = record.split()
        leaderboard.append((score, player))
leaderboard.sort()


def process_time(t: float) -> tuple[int, int, int]:
    """
    Takes time in seconds
    Returns time in minutes:seconds:centiseconds
    """
    t = min(t, 99 * 60 + 99.99)  # Set a maximum possible time of 99:99:99
    minutes: int = int(t // 60)
    t -= minutes * 60
    seconds: int = int(t)
    t -= seconds
    centiseconds: int = int(t * 100)
    return minutes, seconds, centiseconds


def program_window():
    pygame.init()
    window: pygame.Surface = pygame.display.set_mode(_RES, pygame.DOUBLEBUF)
    window.fill(BG_COLOR)
    pygame.display.set_caption(_TITLE)
    
    clock: pygame.time.Clock = pygame.time.Clock()
    
    # Sound Channels
    pygame.mixer.Channel(0).set_volume(0.1)  # TabButtons
    pygame.mixer.Channel(1).set_volume(0.3)  # TextButtons
    pygame.mixer.Channel(2).set_volume(0.4)  # Cube Turns
    
    # Tab buttons
    qube_tab_btn: TabButton = TabButton(window, (50, 10), (200, 60), "Virtual Qube")
    time_tab_btn: TabButton = TabButton(window, (260, 10), (200, 60), "Times")
    active_tab: int = Tab.TIME.value

    qube = Qube3()
    qube_size: int = 3
    qube_types: tuple = Qube1, Qube2, Qube3
    is_cube_form: bool = False
    hide_rotation_tips: bool = False
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
    nums: str = "0123456789"
    
    # GUI elements of each tab
    qube_tab_gui: tuple = (TextBox(window, (1100, 600), 8, "Turning and turning...", HIDDEN_BLUE),
                           # Settings
                           TextBox(window, (850, 200), 24, "Cube Size", DARK_GREY, True),
                           RadioButtons(window, (870, 240), ("1x1x1", "2x2x2", "3x3x3"), DARK_GREY, 2),
                           TextBox(window, (850, 360), 24, "Cube Style", DARK_GREY, True),
                           TextBox(window, (865, 397), 18, "Net", DARK_GREY, True),
                           ToggleBox(window, (905, 391), DARK_GREY, 0, False),
                           TextBox(window, (965, 398), 18, "Cube", DARK_GREY),
                           TextBox(window, (850, 100), 24, "Show Rotation Tips", DARK_GREY, True),
                           TextBox(window, (880, 131), 18, "Yes", DARK_GREY),
                           ToggleBox(window, (905, 125), DARK_GREY, 1, False),
                           TextBox(window, (955, 132), 18, "No", DARK_GREY),
                           
                           # Cube Rendering Division
                           ColoredBox(window, (40, 80), (780, 540), LAYER1_COLOR),
                           QubeButton(window, (328, 150), (300, 170), "L\'", 2),
                           QubeButton(window, (370, 150), (342, 170), "M\'", 3),
                           QubeButton(window, (412, 150), (384, 170), "R", 2),
                           QubeButton(window, (328, 590), (228, 520), "L", 2),
                           QubeButton(window, (370, 590), (270, 520), "M", 3),
                           QubeButton(window, (412, 590), (312, 520), "R\'", 2),
                           
                           QubeButton(window, (150, 328), (120, 328), "U", 2),
                           QubeButton(window, (150, 370), (120, 370), "E\'", 3),
                           QubeButton(window, (150, 412), (120, 412), "D\'", 2),
                           QubeButton(window, (720, 328), (490, 258), "U\'", 2),
                           QubeButton(window, (720, 370), (490, 300), "E", 3),
                           QubeButton(window, (720, 412), (490, 342), "D", 2),
                           
                           QubeButton(window, (505, 196), (410, 400), "B\'", 2),
                           QubeButton(window, (485, 238), (380, 430), "S", 3),
                           QubeButton(window, (465, 280), (350, 460), "F", 2),
                           QubeButton(window, (280, 280), (180, 290), "F\'", 2),
                           QubeButton(window, (260, 238), (210, 260), "S\'", 3),
                           QubeButton(window, (240, 196), (240, 230), "B", 2),

                           QubeButton(window, (90, 130), None, "x", 1),
                           QubeButton(window, (132, 130), None, "y", 1),
                           QubeButton(window, (174, 130), None, "z", 1),
                           QubeButton(window, (90, 172), None, "x\'", 1),
                           QubeButton(window, (132, 172), None, "y\'", 1),
                           QubeButton(window, (174, 172), None, "z\'", 1),
                           
                           TextButton(window, (610, 100), (80, 40), "Reset", 18),
                           TextButton(window, (700, 100), (100, 40), "Scramble", 18),
                           
                           TextBox(window, (680, 230), 28, "", DARK_GREY),
                           QubeRender(window, (740, 330), qube_size, is_cube_form),
                           
                           ColoredBox(window, (565, 480), (600, 140), LAYER1_COLOR, True),
                           TextButton(window, (1080, 490), (70, 40), "Undo", 18),
                           TextBox(window, (492, 580), 14, "", DARK_GREY, True),  # Shows message when scrambled
                           TextBox(window, (492, 510), 36, "Move History", DARK_GREY, True),
                           TextBox(window, (495, 550), 16, "", DARK_GREY, True),  # Move history chain

                           QubeRender(window, (370, 370), qube_size, is_cube_form),
                           ImageBox(window, (170, 170), (530, 400)))
    time_tab_gui: tuple = (TextBox(window, (400, 190), 9, "Times are a\'changing", HIDDEN_BLUE),
                           TextBox(window, (50, 100), 40, "Name:", DARK_GREY, True),
                           InputBox(window, (200, 75), (200, 50), 40, LAYER1_COLOR, LAYER2_COLOR, DARK_GREY, 7),
                           
                           ColoredBox(window, (800, 75), (365, 400), LAYER1_COLOR),
                           TextBox(window, (990, 110), 36, "Leaderboard", DARK_GREY),
                           Leaderboard(window, (820, 150), 14, DARK_GREY, leaderboard),
                           
                           # Add a time section
                           TextBox(window, (900, 520), 32, "Add a time", DARK_GREY),
                           InputBox(window, (810, 540), (50, 40), 32, LAYER1_COLOR, LAYER2_COLOR, DARK_GREY, 2, nums),
                           InputBox(window, (880, 540), (50, 40), 32, LAYER1_COLOR, LAYER2_COLOR, DARK_GREY, 2, nums),
                           InputBox(window, (950, 540), (50, 40), 32, LAYER1_COLOR, LAYER2_COLOR, DARK_GREY, 2, nums),
                           TextBox(window, (835, 590), 12, "MIN", DARK_GREY),
                           TextBox(window, (905, 590), 12, "SEC", DARK_GREY),
                           TextBox(window, (975, 590), 12, "CS", DARK_GREY),
                           TextBox(window, (870, 558), 18, ':', DARK_GREY),
                           TextBox(window, (940, 558), 18, '.', DARK_GREY),
                           TextButton(window, (1030, 542), (36, 36), '+', 36, 2),
                           TextBox(window, (850, 615), 18, "", WARN_RED, True),  # Prompt to fill in all fields
                           
                           # Prompts to save player times
                           TextButton(window, (250, 380), (300, 50), "Save to Leaderboard", 24, 1),
                           TextBox(window, (400, 450), 18, "", WARN_RED),  # Prompt below button
                           TextBox(window, (300, 140), 18, "", WARN_RED),  # Prompt next to name
                           
                           # Keyboard Graphic
                           ImageBox(window, (250, 500), (288, 69)),
                           TextBox(window, (390, 600), 18, "Ready timer by holding a key on both sides", DARK_GREY),
                           
                           # Timer shown
                           ColoredBox(window, (100, 200), (600, 160), LAYER1_COLOR),
                           TextBox(window, (300, 270), 100, ":", DARK_GREY),
                           TextBox(window, (500, 275), 100, ".", DARK_GREY),
                           TextBox(window, (200, 285), 100, "00", DARK_GREY, False, True),  # Minutes
                           TextBox(window, (400, 285), 100, "00", DARK_GREY, False, True),  # Seconds
                           TextBox(window, (600, 285), 100, "00", DARK_GREY, False, True))  # Centiseconds
    guis: tuple = qube_tab_gui, time_tab_gui
    
    # Start with specific elements hidden
    time_tab_gui[-11].hidden = True
    
    # Cooldowns for keyboard shortcuts
    fc, xc, yc, zc, rc, lc, uc, dc, bc, mc, ec, sc = (False for _ in range(12))
    undo_cool = False
    timer_cool = False
    tab_cool = False
    prev_cool, next_cool = False, False
    
    formatted_time: list = ["00", "00", "00"]  # Holds the minutes, seconds, and centiseconds of timer as strings
    input_box_active: bool = False  # Records when an input box is active on the times tab
    
    running: bool = True
    while running:
        events: list[pygame.event] = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                running = False
                break
        keys_pressed: pygame.key.ScancodeWrapper = pygame.key.get_pressed()
        
        for i, tab_button in enumerate((qube_tab_btn, time_tab_btn)):
            tab_button.update(active_tab == i)  # Sets button to hover color if its tab is active
            if tab_button.clicked and not active_tab == i:  # Prevent sound from playing if tab already selected
                active_tab = i
                pygame.mixer.Channel(0).play(TAB_CLICK)
                
            tab_button.draw()
        
        if active_tab == Tab.QUBE.value:
            primed: bool = keys_pressed[pygame.K_LSHIFT] | keys_pressed[pygame.K_RSHIFT]
            try:  # Rotation keyboard shortcuts
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
                if keys_pressed[pygame.K_BACKQUOTE] and not undo_cool or qube_tab_gui[-6].clicked:
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
            
            # Scramble system
            if keys_pressed[pygame.K_F8] or qube_tab_gui[-10].clicked:
                random_move_attempts: int = 20
                qube.reset()
                scramble = generate_shuffle(qube_size, random_move_attempts)
                qube.apply_moves(scramble)
                move_history = scramble
                scrambled = True
                qube_tab_gui[-4].update_text("Moves to Scramble")
            
            if fc | xc | yc | zc | rc | lc | uc | dc | bc | mc | undo_cool:  # If a keyboard shortcut was used to turn
                scrambled = False
            
            history_length: int = len(move_history)
            if not history_length:  # If move_history is empty
                qube_tab_gui[-4].update_text("")  # Hide move history textbox
                qube_tab_gui[-5].update_text("")
                qube_tab_gui[-6].hidden = True  # Hide undo button
                qube_tab_gui[-7].hidden = True  # Hide move history box
                qube_tab_gui[-11].hidden = True  # Hide reset button
            else:
                length_text: str = f" ({history_length})" if history_length > HISTORY_OVERFLOW else ""
                qube_tab_gui[-4].update_text("Moves to Scramble" if scrambled else "Move History" + length_text)
                qube_tab_gui[-5].update_text("Start with WHITE front, RED top" if scrambled else "")
                qube_tab_gui[-6].hidden = False  # Show undo button
                qube_tab_gui[-7].hidden = False  # Show move history box
                qube_tab_gui[-11].hidden = False  # Show reset button
            
            # Return qube to solved state
            if keys_pressed[pygame.K_F5] or qube_tab_gui[-11].clicked:
                qube.reset()
                move_history.clear()
            
            # Show back view label only if cube form shown
            qube_tab_gui[-9].update_text("Back View" if is_cube_form else "")
            
            # Update Move History text
            reverse_history: int = 1 if scrambled else -1
            qube_tab_gui[-3].update_text(", ".join((move_history[:HISTORY_OVERFLOW * reverse_history:reverse_history]))
                                         + (", ..." if len(move_history) > HISTORY_OVERFLOW else ""))
        elif active_tab == Tab.TIME.value:
            if keys_pressed[pygame.K_TAB] and not tab_cool:  # Tab switching
                shifted: bool = keys_pressed[pygame.K_LSHIFT] | keys_pressed[pygame.K_RSHIFT]
                if not shifted:
                    for i in range(3):
                        if time_tab_gui[7 + i].enabled:
                            time_tab_gui[7 + i].enabled = False
                            time_tab_gui[(i + 1) % 3 + 7].enabled = True
                            break
                else:
                    for i in range(2, -1, -1):
                        if time_tab_gui[7 + i].enabled:
                            time_tab_gui[7 + i].enabled = False
                            time_tab_gui[(i - 1) % 3 + 7].enabled = True
                            break
                tab_cool = True
            elif not keys_pressed[pygame.K_TAB]:
                tab_cool = False
            
            # To skip keyboard hits when an inbox box is active
            input_box_active = time_tab_gui[2].update_field(events) | \
                               time_tab_gui[7].update_field(events) | \
                               time_tab_gui[8].update_field(events) | \
                               time_tab_gui[9].update_field(events)
            if time_tab_gui[8].text:
                if int(time_tab_gui[8].text) >= 60:  # If inputted seconds is greater than 60
                    time_tab_gui[8].text = "59"
                    
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
                
                # Leaderboard page change keyboard shortcut
                if keys_pressed[pygame.K_RIGHT] and not next_cool:
                    time_tab_gui[5].increment_page()
                    next_cool = True
                elif not keys_pressed[pygame.K_RIGHT]:
                    next_cool = False
                
                if keys_pressed[pygame.K_LEFT] and not prev_cool:
                    time_tab_gui[5].decrement_page()
                    prev_cool = True
                elif not keys_pressed[pygame.K_LEFT]:
                    prev_cool = False
                
                # Update keyboard graphic
                selected: str = "none"
                if left_activated and right_activated:
                    selected = "both"
                elif left_activated:
                    selected = "left"
                elif right_activated:
                    selected = "right"
                time_tab_gui[-8].update_state(keyboard_img[selected])
                
                if not timer_running:
                    if left_activated and right_activated and not timer_cool:
                        is_ready = True
                        current_time = start_time
                        time_tab_gui[-7].update_text("Release to start timer")
                        time_tab_gui[-11].hidden = True
                    else:
                        if is_ready:
                            is_ready = False
                            timer_running = True
                            start_time = time()
                            current_time = start_time
                            time_tab_gui[-7].update_text("Press a key on both sides to stop timer")
                        elif not (left_activated and right_activated):
                            timer_cool = False
                            time_tab_gui[-7].update_text("Ready timer by pressing a key on both sides")
                else:
                    current_time = time()
                    if left_activated and right_activated:
                        timer_running = False
                        timer_cool = True
                        time_tab_gui[-7].update_text("Timer stopped")
                        time_tab_gui[-11].hidden = False
            
            # Update timer
            display_time: tuple = process_time(current_time - start_time)
            formatted_time = ["%02d" % display_time[i] for i in range(3)]
            time_tab_gui[-3].update_text(formatted_time[0])
            time_tab_gui[-2].update_text(formatted_time[1])
            time_tab_gui[-1].update_text(formatted_time[2])
        
        hovered_btn: str = ""
        pygame.draw.rect(window, FRAME_COLOR, pygame.Rect((20, 60), (1160, 580)), border_radius=20)  # Tab Background
        for element in guis[active_tab]:  # Draw rest of GUI elements for the tab
            # Update GUI Elements
            try:
                if type(element) == QubeButton:
                    if active_tab == Tab.QUBE.value:
                        move: str | None = element.update_state(qube_size, is_cube_form)
                        if element.hidden:
                            continue
                        
                        if element.hover and not pygame.mouse.get_pressed()[0]:
                            hovered_btn = element.text
                        if move is not None:
                            qube.apply_moves((move,))
                            move_history.append(move)
                            scrambled = False
                            pygame.mixer.Channel(2).play(ROTATE)
                
                element.update()
                
                if type(element) == ToggleBox:
                    if element.clicked:
                        pygame.mixer.Channel(1).play(CLICK)
                    if active_tab == Tab.QUBE.value:
                        if element.id == 0:
                            is_cube_form = element.state
                        elif element.id == 1:
                            hide_rotation_tips = element.state
                elif type(element) == RadioButtons:
                    if element.changed:
                        pygame.mixer.Channel(1).play(CLICK)
                    if active_tab == Tab.QUBE.value:
                        old_q_size: int = qube_size
                        qube_size = element.selected + 1
                        # Update Qube Render
                        qube_tab_gui[-2].size = qube_size
                        qube_tab_gui[-8].size = qube_size
                        qube_tab_gui[-2].is_cube_form = is_cube_form
                        if old_q_size != qube_size:
                            qube = qube_types[qube_size - 1]()
                            move_history.clear()
                elif type(element) == TextButton:
                    if element.clicked:
                        pygame.mixer.Channel(1).play(CLICK)
                        if element.identifier == 1:
                            if len(time_tab_gui[2].text):  # If there is name, then add time to leaderboard
                                time_string: str = f"{formatted_time[0]}:{formatted_time[1]}.{formatted_time[2]}"
                                time_tab_gui[5].add((time_string, time_tab_gui[2].text))
                            else:  # Then prompt user for name
                                time_tab_gui[-10].update_text("Please fill in a name to save this time")
                                time_tab_gui[-9].update_text("Fill in name here")
                        elif element.identifier == 2:  # Same thing for adding a time
                            if len(time_tab_gui[7].text) and len(time_tab_gui[8].text) and len(time_tab_gui[9].text):
                                if len(time_tab_gui[2].text):  # Check for name
                                    mins, sec, cs = time_tab_gui[7].text, time_tab_gui[8].text, time_tab_gui[9].text
                                    mins, sec, cs = ("%02d" % unit for unit in (int(mins), int(sec), int(cs)))
                                    time_string: str = f"{mins}:{sec}.{cs}"
                                    time_tab_gui[5].add((time_string, time_tab_gui[2].text))
                                else:
                                    time_tab_gui[-9].update_text("Fill in name here")
                            else:
                                time_tab_gui[16].update_text("Please fill in all fields")
                elif type(element) == Leaderboard:
                    if element.changed:
                        pygame.mixer.Channel(1).play(CLICK)
                elif type(element) == InputBox:
                    if element.changed_enabled:
                        pygame.mixer.Channel(1).play(CLICK)
            except (AttributeError, TypeError):  # Element is static or requires an argument
                if type(element) == ImageBox:
                    if active_tab == Tab.QUBE.value and not hide_rotation_tips:  # Show corresponding arrows
                        form: str = "cube" if is_cube_form else "net"
                        rotation: str = hovered_btn.replace("\'", 'p').lower()
                        image_name: str = f"{form}_{rotation}"
                        element.update_state(qube_arrows[image_name] if hovered_btn else None)
                pass
            
            if len(time_tab_gui[2].text):  # If there is a name for the timer, hide warning prompts
                time_tab_gui[-10].update_text("")
                time_tab_gui[-9].update_text("")
            if len(time_tab_gui[7].text) and len(time_tab_gui[8].text) and len(time_tab_gui[9].text):  # Adding a time
                time_tab_gui[16].update_text("")
            
            # Draw GUI Elements
            try:
                element.draw()
            except TypeError:  # Is QubeRenderer
                qube_tab_gui[-2].draw(qube)
                if is_cube_form:
                    qube_tab_gui[-8].draw(qube, back_view=True)
        
        pygame.display.update()
        _TICK_RATE = 480 if timer_running and active_tab == Tab.TIME.value and not input_box_active else 120
        clock.tick(_TICK_RATE)


if __name__ == '__main__':
    program_window()
    pygame.quit()
