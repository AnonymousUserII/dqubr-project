from os import path
from time import perf_counter as time
from contextlib import redirect_stdout

with redirect_stdout(None):  # Load PyGame without welcome message
    import pygame

from Assets.colors import *
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

# Window Properties
_RES: tuple[int, int] = (1200, 660)
_TITLE: str = "dQubr Project"
_ICON: pygame.Surface = pygame.image.load(path.join("Assets", "dqube.png"))
_TICK_RATE: int = 240
# Constants
HISTORY_OVERFLOW: int = 24
INSPECTION_TIME: int = 15

# Dictionary to hold arrow graphics for qube turning
moves: list[str] = []
for form in ("net", "cube"):
    for rotation in ('f', 'b', 'r', 'l', 'u', 'd', 'm', 'e', 's', 'x', 'y', 'z'):
        moves.append(f"{form}_{rotation}")
        moves.append(f"{form}_{rotation}p")
qube_arrows: dict[str, pygame.Surface] = {}
pygame.display.init()
for move in moves:
    qube_arrows[move] = pygame.image.load(path.join("Assets", "QubeArrows", f"{move}.png"))
    qube_arrows[move].set_alpha(180)  # Set translucent

# Dictionary to hold keyboard graphics for the two-hand timer
keyboard_img: dict[str, pygame.Surface] = {}
for perm in ("none", "left", "right", "both"):
    keyboard_img[perm] = pygame.image.load(path.join("Assets", f"keyboard_{perm}.png"))

# Keyboard graphics for keyboard rotation shortcuts
keyboard_shortcuts: dict[str, pygame.Surface] = {
    "lettered": pygame.image.load(path.join("Assets", "keyboard_lettered.png")),
    "alternative": pygame.image.load(path.join("Assets", "keyboard_alternative.png"))
}

# Retrieve leaderboard times from file
with open(path.join("Assets", "times.timmy"), 'r') as time_history:
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
    t = min(t, 99 * 60 + 99.99)  # Maximum possible time of 99:99:99
    t = max(t, 0)  # Minimum possible 00:00:00
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
    pygame.display.set_icon(_ICON)
    
    clock: pygame.time.Clock = pygame.time.Clock()
    
    # Sounds
    click: pygame.mixer.Sound = pygame.mixer.Sound(path.join("Assets", "Sounds", "click.wav"))
    tab_click: pygame.mixer.Sound = pygame.mixer.Sound(path.join("Assets", "Sounds", "tab_click.wav"))
    rotate: pygame.mixer.Sound = pygame.mixer.Sound(path.join("Assets", "Sounds", "turn.wav"))
    error: pygame.mixer.Sound = pygame.mixer.Sound(path.join("Assets", "Sounds", "bass.wav"))
    
    pygame.mixer.Channel(0).set_volume(0.1)  # TabButtons
    pygame.mixer.Channel(1).set_volume(0.3)  # TextButtons
    pygame.mixer.Channel(2).set_volume(0.4)  # Cube Turns
    pygame.mixer.Channel(3).set_volume(0.6)  # Error sound
    
    # Tab buttons
    qube_tab_btn: TabButton = TabButton(window, (50, 10), (200, 60), "Virtual Qube", "Play with a virtual qube")
    time_tab_btn: TabButton = TabButton(window, (260, 10), (200, 60), "Times", "Use a real cube to set personal times")
    active_tab: int = 0
    
    qube_size: int = 3
    qube_types: tuple = Qube1, Qube2, Qube3
    qube = qube_types[qube_size - 1]()
    is_cube_form: bool = True
    ghost_back_view: bool = True
    hide_rotation_tips: bool = False
    move_history: list[str] = []
    scrambled: bool = False  # If qube is freshly scrambled and no moves applied yet
    alt_layout: bool = False  # False = Lettered, True = alternative rotation keyboard shortcuts
    
    is_ready: bool = False
    timer_running: bool = False
    start_time: float = time()
    current_time: float = start_time
    
    # Sets of keys for the timer
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
                           TextBox(window, (850, 340), 24, "Cube Size", DARK_GREY, True),
                           RadioButtons(window, (870, 380), ("1x1x1", "2x2x2", "3x3x3"), DARK_GREY, qube_size - 1),
    
                           TextBox(window, (1000, 340), 24, "Cube Form", DARK_GREY, True),
                           TextBox(window, (1015, 377), 18, "Net", DARK_GREY, True),
                           ToggleBox(window, (1055, 371), DARK_GREY, 0, is_cube_form),
                           TextBox(window, (1115, 378), 18, "Cube", DARK_GREY),
    
                           TextBox(window, (850, 100), 24, "Hover Rotation Tips", DARK_GREY, True),
                           TextBox(window, (880, 131), 18, "Yes", DARK_GREY),
                           ToggleBox(window, (905, 125), DARK_GREY, 1, False),
                           TextBox(window, (955, 132), 18, "No", DARK_GREY),
    
                           TextBox(window, (850, 180), 24, "Keybind Rotation Layout", DARK_GREY, True),
                           TextBox(window, (900, 211), 18, "Lettered", DARK_GREY),
                           ToggleBox(window, (950, 205), DARK_GREY, 2, False),
                           TextBox(window, (990, 212), 18, "Alternative", DARK_GREY, True),
                           ImageBox(window, (850, 230), (250, 82)),
    
                           ColoredBox(window, (40, 80), (780, 540), LAYER1_COLOR),
                           TextButton(window, (570, 170), (190, 30), "Toggle back view", 14, 3),
                           # Qube Turning Buttons
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
    
                           TextBox(window, (132, 105), 16, "Rotate whole qube", DARK_GREY),
                           QubeButton(window, (90, 140), None, "x", 1),
                           QubeButton(window, (132, 140), None, "y", 1),
                           QubeButton(window, (174, 140), None, "z", 1),
                           QubeButton(window, (90, 182), None, "x\'", 1),
                           QubeButton(window, (132, 182), None, "y\'", 1),
                           QubeButton(window, (174, 182), None, "z\'", 1),
    
                           TextButton(window, (610, 100), (80, 40), "Reset", 18),
                           TextButton(window, (700, 100), (100, 40), "Scramble", 18),
    
                           TextBox(window, (660, 230), 28, "", DARK_GREY),
                           QubeRender(window, (740, 330), qube_size, is_cube_form),
    
                           ColoredBox(window, (565, 480), (600, 140), LAYER1_COLOR, True),
                           TextButton(window, (1080, 490), (70, 40), "Undo", 18),
                           TextBox(window, (492, 580), 14, "", DARK_GREY, True),  # Shows message when scrambled
                           TextBox(window, (492, 510), 36, "Move History", DARK_GREY, True),
                           TextBox(window, (495, 550), 16, "", DARK_GREY, True),  # Move history chain
    
                           QubeRender(window, (370, 370), qube_size, is_cube_form),
                           ImageBox(window, (170, 170), (530, 400)))
    time_tab_gui: tuple = (TextBox(window, (400, 190), 9, "Times are a\'changing", HIDDEN_BLUE),
                           # Name input
                           TextBox(window, (50, 100), 40, "Name:", DARK_GREY, True),
                           InputBox(window, (200, 75), (200, 50), 40, LAYER1_COLOR, LAYER2_COLOR, DARK_GREY, 7),
    
                           # Leaderboard
                           ColoredBox(window, (800, 75), (365, 400), LAYER1_COLOR),
                           TextBox(window, (990, 110), 36, "Leaderboard", DARK_GREY),
                           Leaderboard(window, (820, 150), 14, DARK_GREY, leaderboard),
    
                           # Add a time section
                           TextBox(window, (900, 510), 32, "Add a time", DARK_GREY),
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
    
                           # Hover elements for time preparation
                           TextBox(window, (590, 85), 18, "Hover for Preparation", DARK_GREY),
                           TextButton(window, (450, 105), (120, 30), "Scramble", 14, 3, "", (600, 30)),
                           TextButton(window, (580, 105), (180, 30), f"Inspection ({INSPECTION_TIME}s)",
                                      14, 4, "", (120, 40)),
                           TextBox(window, (400, 400), 24, "", WARN_RED),  # Prompt for inspection timeout
    
                           # Prompts to save player times
                           TextButton(window, (250, 380), (300, 50), "Save to Leaderboard", 24, 1, saving=True),
                           TextBox(window, (400, 450), 18, "", WARN_RED),  # Prompt below button
                           TextBox(window, (300, 140), 18, "", WARN_RED),  # Prompt next to name
    
                           # Keyboard Graphic
                           ImageBox(window, (230, 470), (350, 115)),
                           TextBox(window, (400, 610), 18, "Ready timer by holding a key on both sides", DARK_GREY),
    
                           # Timer shown
                           ColoredBox(window, (100, 200), (600, 160), LAYER1_COLOR),
                           TextBox(window, (300, 270), 100, ":", DARK_GREY),
                           TextBox(window, (500, 275), 100, ".", DARK_GREY),
                           # Minutes, seconds, centiseconds
                           TextBox(window, (200, 285), 100, "00", DARK_GREY, False, True),
                           TextBox(window, (400, 285), 100, "00", DARK_GREY, False, True),
                           TextBox(window, (600, 285), 100, "00", DARK_GREY, False, True)
                           )
    guis: tuple = qube_tab_gui, time_tab_gui
    time_tab_gui[-11].hidden = True  # Start with button to save time hidden
    
    # Cooldowns for keyboard shortcuts
    fc, xc, yc, zc, rc, lc, uc, dc, bc, mc, ec, sc = (False for _ in range(12))
    fpc, xpc, ypc, zpc, rpc, lpc, upc, dpc, bpc, mpc, epc, spc = (False for _ in range(12))  # Prime cooldowns
    undo_cool = False
    timer_cool = False
    tab_cool = False
    prev_cool, next_cool = False, False
    
    undo_start: float | None = None  # Records when the undo button is first pressed
    inspection_start: float = time()  # Records when inspection time starts
    inspection_running: bool = False  # States when the inspection timer takes over the normal timer
    inspection_remaining: float = INSPECTION_TIME  # Holds amount of inspection time left
    unaddressed_error: dict[str, bool] = {"name": False, "fields": False}  # Holds if error for adding time is addressed
    
    formatted_time: list = ["00", "00", "00"]  # Holds the minutes, seconds, and centiseconds of timer as strings
    input_box_active: bool  # Records when an input box is active on the times tab
    
    running: bool = True
    while running:
        events: list[pygame.event] = pygame.event.get()
        time_of_frame: float = time()
        for event in events:
            if event.type == pygame.QUIT:
                running = False
                break
        keys_pressed: pygame.key.ScancodeWrapper = pygame.key.get_pressed()
        
        for i, tab_button in enumerate((qube_tab_btn, time_tab_btn)):
            tab_button.update(active_tab == i)  # Sets button to hover color if its tab is active
            if tab_button.clicked and active_tab != i:  # Prevent sound from playing if tab already selected
                active_tab = i
                pygame.mixer.Channel(0).play(tab_click)
        
        if active_tab == 0:  # Virtual Qube tab (Update Qube)
            # Rotation keyboard shortcuts
            if not alt_layout:
                primed: bool = keys_pressed[pygame.K_LSHIFT] | keys_pressed[pygame.K_RSHIFT]
                try:
                    if keys_pressed[pygame.K_f] and not fc:
                        qube.f(primed)
                        pygame.mixer.Channel(2).play(rotate)
                        move_history.append("F" + ("\'" if primed else ""))
                        fc = True
                    elif not keys_pressed[pygame.K_f]:
                        fc = False
                    
                    if keys_pressed[pygame.K_x] and not xc:
                        qube.x(primed)
                        pygame.mixer.Channel(2).play(rotate)
                        move_history.append("x" + ("\'" if primed else ""))
                        xc = True
                    elif not keys_pressed[pygame.K_x]:
                        xc = False
                    
                    if keys_pressed[pygame.K_y] and not yc:
                        qube.y(primed)
                        pygame.mixer.Channel(2).play(rotate)
                        move_history.append("y" + ("\'" if primed else ""))
                        yc = True
                    elif not keys_pressed[pygame.K_y]:
                        yc = False
                    
                    if keys_pressed[pygame.K_z] and not zc:
                        qube.z(primed)
                        pygame.mixer.Channel(2).play(rotate)
                        move_history.append("z" + ("\'" if primed else ""))
                        zc = True
                    elif not keys_pressed[pygame.K_z]:
                        zc = False
                    
                    if keys_pressed[pygame.K_r] and not rc:
                        qube.r(primed)
                        pygame.mixer.Channel(2).play(rotate)
                        move_history.append("R" + ("\'" if primed else ""))
                        rc = True
                    elif not keys_pressed[pygame.K_r]:
                        rc = False
                    
                    if keys_pressed[pygame.K_l] and not lc:
                        qube.l(primed)
                        pygame.mixer.Channel(2).play(rotate)
                        move_history.append("L" + ("\'" if primed else ""))
                        lc = True
                    elif not keys_pressed[pygame.K_l]:
                        lc = False
                    
                    if keys_pressed[pygame.K_u] and not uc:
                        qube.u(primed)
                        pygame.mixer.Channel(2).play(rotate)
                        move_history.append("U" + ("\'" if primed else ""))
                        uc = True
                    elif not keys_pressed[pygame.K_u]:
                        uc = False
                    
                    if keys_pressed[pygame.K_d] and not dc:
                        qube.d(primed)
                        pygame.mixer.Channel(2).play(rotate)
                        move_history.append("D" + ("\'" if primed else ""))
                        dc = True
                    elif not keys_pressed[pygame.K_d]:
                        dc = False
                    
                    if keys_pressed[pygame.K_b] and not bc:
                        qube.b(primed)
                        pygame.mixer.Channel(2).play(rotate)
                        move_history.append("B" + ("\'" if primed else ""))
                        bc = True
                    elif not keys_pressed[pygame.K_b]:
                        bc = False
                    
                    if keys_pressed[pygame.K_m] and not mc:
                        qube.m(primed)
                        pygame.mixer.Channel(2).play(rotate)
                        move_history.append("M" + ("\'" if primed else ""))
                        mc = True
                    elif not keys_pressed[pygame.K_m]:
                        mc = False
                    
                    if keys_pressed[pygame.K_e] and not ec:
                        qube.e(primed)
                        pygame.mixer.Channel(2).play(rotate)
                        move_history.append("E" + ("\'" if primed else ""))
                        ec = True
                    elif not keys_pressed[pygame.K_e]:
                        ec = False
                    
                    if keys_pressed[pygame.K_s] and not sc:
                        qube.s(primed)
                        pygame.mixer.Channel(2).play(rotate)
                        move_history.append("S" + ("\'" if primed else ""))
                        sc = True
                    elif not keys_pressed[pygame.K_s]:
                        sc = False
                except AttributeError:  # Move not available for size of cube
                    pass
            else:
                try:
                    if keys_pressed[pygame.K_u] and not fc:
                        qube.f()
                        pygame.mixer.Channel(2).play(rotate)
                        move_history.append("F")
                        fc = True
                    elif not keys_pressed[pygame.K_u]:
                        fc = False
                    
                    if keys_pressed[pygame.K_r] and not fpc:
                        qube.f(True)
                        pygame.mixer.Channel(2).play(rotate)
                        move_history.append("F\'")
                        fpc = True
                    elif not keys_pressed[pygame.K_r]:
                        fpc = False
                    
                    if keys_pressed[pygame.K_i] and not sc:
                        qube.s()
                        pygame.mixer.Channel(2).play(rotate)
                        move_history.append("S")
                        sc = True
                    elif not keys_pressed[pygame.K_i]:
                        sc = False
                    
                    if keys_pressed[pygame.K_e] and not spc:
                        qube.s(True)
                        pygame.mixer.Channel(2).play(rotate)
                        move_history.append("S\'")
                        spc = True
                    elif not keys_pressed[pygame.K_e]:
                        spc = False
                    
                    if keys_pressed[pygame.K_o] and not bpc:
                        qube.b(True)
                        pygame.mixer.Channel(2).play(rotate)
                        move_history.append("B\'")
                        bpc = True
                    elif not keys_pressed[pygame.K_o]:
                        bpc = False
                    
                    if keys_pressed[pygame.K_w] and not bc:
                        qube.b()
                        pygame.mixer.Channel(2).play(rotate)
                        move_history.append("B")
                        bc = True
                    elif not keys_pressed[pygame.K_w]:
                        bc = False
                    
                    if keys_pressed[pygame.K_j] and not uc:
                        qube.u()
                        pygame.mixer.Channel(2).play(rotate)
                        move_history.append("U")
                        uc = True
                    elif not keys_pressed[pygame.K_j]:
                        uc = False
                    
                    if keys_pressed[pygame.K_f] and not upc:
                        qube.u(True)
                        pygame.mixer.Channel(2).play(rotate)
                        move_history.append("U\'")
                        upc = True
                    elif not keys_pressed[pygame.K_f]:
                        upc = False
                    
                    if keys_pressed[pygame.K_k] and not epc:
                        qube.e(True)
                        pygame.mixer.Channel(2).play(rotate)
                        move_history.append("E\'")
                        epc = True
                    elif not keys_pressed[pygame.K_k]:
                        epc = False
                    
                    if keys_pressed[pygame.K_d] and not ec:
                        qube.e()
                        pygame.mixer.Channel(2).play(rotate)
                        move_history.append("E")
                        ec = True
                    elif not keys_pressed[pygame.K_d]:
                        ec = False
                    
                    if keys_pressed[pygame.K_l] and not dpc:
                        qube.d(True)
                        pygame.mixer.Channel(2).play(rotate)
                        move_history.append("D\'")
                        dpc = True
                    elif not keys_pressed[pygame.K_l]:
                        dpc = False
                    
                    if keys_pressed[pygame.K_s] and not dc:
                        qube.d()
                        pygame.mixer.Channel(2).play(rotate)
                        move_history.append("D")
                        dc = True
                    elif not keys_pressed[pygame.K_s]:
                        dc = False
                    
                    if keys_pressed[pygame.K_m] and not rc:
                        qube.r()
                        pygame.mixer.Channel(2).play(rotate)
                        move_history.append("R")
                        rc = True
                    elif not keys_pressed[pygame.K_m]:
                        rc = False
                    
                    if keys_pressed[pygame.K_n] and not rpc:
                        qube.r(True)
                        pygame.mixer.Channel(2).play(rotate)
                        move_history.append("R\'")
                        rpc = True
                    elif not keys_pressed[pygame.K_n]:
                        rpc = False
                    
                    if keys_pressed[pygame.K_8] and not mc:
                        qube.m()
                        pygame.mixer.Channel(2).play(rotate)
                        move_history.append("M")
                        mc = True
                    elif not keys_pressed[pygame.K_8]:
                        mc = False
                    
                    if keys_pressed[pygame.K_3] and not mpc:
                        qube.m(True)
                        pygame.mixer.Channel(2).play(rotate)
                        move_history.append("M\'")
                        mpc = True
                    elif not keys_pressed[pygame.K_3]:
                        mpc = False
                    
                    if keys_pressed[pygame.K_c] and not lpc:
                        qube.l(True)
                        pygame.mixer.Channel(2).play(rotate)
                        move_history.append("L\'")
                        lpc = True
                    elif not keys_pressed[pygame.K_c]:
                        lpc = False
                    
                    if keys_pressed[pygame.K_v] and not lc:
                        qube.l()
                        pygame.mixer.Channel(2).play(rotate)
                        move_history.append("L")
                        lc = True
                    elif not keys_pressed[pygame.K_v]:
                        lc = False
                    
                    if keys_pressed[pygame.K_COMMA] and not xc:
                        qube.x()
                        pygame.mixer.Channel(2).play(rotate)
                        move_history.append("x")
                        xc = True
                    elif not keys_pressed[pygame.K_COMMA]:
                        xc = False
                    
                    if keys_pressed[pygame.K_x] and not xpc:
                        qube.x(True)
                        pygame.mixer.Channel(2).play(rotate)
                        move_history.append("x\'")
                        xpc = True
                    elif not keys_pressed[pygame.K_x]:
                        xpc = False
                    
                    if keys_pressed[pygame.K_h] and not yc:
                        qube.y()
                        pygame.mixer.Channel(2).play(rotate)
                        move_history.append("y")
                        yc = True
                    elif not keys_pressed[pygame.K_h]:
                        yc = False
                    
                    if keys_pressed[pygame.K_g] and not ypc:
                        qube.y(True)
                        pygame.mixer.Channel(2).play(rotate)
                        move_history.append("y\'")
                        ypc = True
                    elif not keys_pressed[pygame.K_g]:
                        ypc = False
                    
                    if keys_pressed[pygame.K_y] and not zc:
                        qube.z()
                        pygame.mixer.Channel(2).play(rotate)
                        move_history.append("z")
                        zc = True
                    elif not keys_pressed[pygame.K_y]:
                        zc = False
                    
                    if keys_pressed[pygame.K_t] and not zpc:
                        qube.z(True)
                        pygame.mixer.Channel(2).play(rotate)
                        move_history.append("z\'")
                        zpc = True
                    elif not keys_pressed[pygame.K_t]:
                        zpc = False
                
                except AttributeError:  # Move not available for size of cube
                    pass
            
            # Undo button clicking and holding
            if qube_tab_gui[-6].clicked:  # Initial click
                undo_start = time_of_frame
            elif undo_start and pygame.mouse.get_pressed()[0]:  # Button is still being held
                time_since_start: float = time_of_frame - undo_start
                if time_since_start > 0.3:  # If held for more than 300 milliseconds
                    qube_tab_gui[-6].clicked = True
                    undo_start = time_of_frame
            else:
                undo_start = None
            
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
                    pygame.mixer.Channel(1).play(click)
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
                pygame.mixer.Channel(2).set_volume(0.7)
                pygame.mixer.Channel(2).play(rotate)
                pygame.mixer.Channel(2).set_volume(0.4)
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
            
            # Show certain parts if is_cube_form is true
            if is_cube_form:
                qube_tab_gui[-9].update_text("Internal Back View" if ghost_back_view else "Rotated Back View")
                qube_tab_gui[17].hidden = False
            else:
                qube_tab_gui[-9].update_text("")
                qube_tab_gui[17].hidden = True

            # Update Move History text
            reverse_history: int = 1 if scrambled else -1
            qube_tab_gui[-3].update_text(", ".join((move_history[:HISTORY_OVERFLOW * reverse_history:reverse_history]))
                                         + (", ..." if len(move_history) > HISTORY_OVERFLOW else ""))
        elif active_tab == 1:  # Times tab (Update Timer)
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
            input_box_active = time_tab_gui[2].update_field(events) | time_tab_gui[7].update_field(events) \
                               | time_tab_gui[8].update_field(events) | time_tab_gui[9].update_field(events)
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
                        inspection_running = False
                        is_ready = True
                        current_time = start_time
                        time_tab_gui[-7].update_text("Release to start timer")
                        time_tab_gui[-11].hidden = True
                    else:
                        if is_ready:
                            is_ready = False
                            timer_running = True
                            start_time = time_of_frame
                            current_time = start_time
                            time_tab_gui[-7].update_text("Press a key on both sides to stop timer")
                        elif not (left_activated and right_activated):
                            timer_cool = False
                            time_tab_gui[-7].update_text("Ready timer by pressing a key on both sides")
                else:
                    current_time = time_of_frame
                    if left_activated and right_activated:
                        timer_running = False
                        timer_cool = True
                        time_tab_gui[-7].update_text("Timer stopped")
                        time_tab_gui[-11].hidden = False
            
            # Update timer
            display_time: tuple = process_time(current_time - start_time)
            
            if inspection_running:
                inspection_remaining = INSPECTION_TIME - (time_of_frame - inspection_start)
                inspect_formatted = process_time(inspection_remaining)
                mins, sec, cs = inspect_formatted
                mins, sec, cs = ("%02d" % unit for unit in (int(mins), int(sec), int(cs)))
                time_tab_gui[-3].update_text(mins)
                time_tab_gui[-2].update_text(sec)
                time_tab_gui[-1].update_text(cs)
                time_tab_gui[-11].hidden = True
            else:
                formatted_time = ["%02d" % display_time[i] for i in range(3)]
                time_tab_gui[-3].update_text(formatted_time[0])
                time_tab_gui[-2].update_text(formatted_time[1])
                time_tab_gui[-1].update_text(formatted_time[2])
            
            time_tab_gui[20].update_text("Inspection time expired" if inspection_remaining <= 0 and inspection_running
                                         else "")
        
        window.fill(BG_COLOR)
        tooltips: list = [qube_tab_btn.draw(), time_tab_btn.draw()]
        pygame.draw.rect(window, FRAME_COLOR, pygame.Rect((20, 60), (1160, 580)), border_radius=20)  # Tab Background
        hovered_btn: str = ""  # Holds the text of a hovered QubeButton
        
        for element in guis[active_tab]:  # Draw GUI elements for the tab
            # Update GUI Elements
            try:
                if type(element) == QubeButton:
                    if active_tab == 0:
                        btn_label: str | None = element.update_state(qube_size, is_cube_form)
                        if element.hidden:
                            continue
                        
                        if element.hover and not pygame.mouse.get_pressed()[0]:
                            hovered_btn = element.text
                        if btn_label is not None:
                            qube.apply_moves((btn_label,))  # A tuple of 1 element
                            move_history.append(btn_label)
                            scrambled = False
                            pygame.mixer.Channel(2).play(rotate)
                
                element.update()
                
                if type(element) == ToggleBox:
                    if element.clicked:
                        pygame.mixer.Channel(1).play(click)
                    if active_tab == 0:
                        if element.id == 0:
                            is_cube_form = element.state
                        elif element.id == 1:
                            hide_rotation_tips = element.state
                        elif element.id == 2:
                            alt_layout = element.state
                elif type(element) == RadioButtons:
                    if element.changed:
                        pygame.mixer.Channel(1).play(click)
                    if active_tab == 0:
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
                        pygame.mixer.Channel(1).play(click)
                        if element.identifier == 1:
                            if len(time_tab_gui[2].text):  # If there is name, then add time to leaderboard
                                time_string: str = f"{formatted_time[0]}:{formatted_time[1]}.{formatted_time[2]}"
                                time_tab_gui[5].add((time_string, time_tab_gui[2].text))
                            else:  # Then prompt user for name
                                pygame.mixer.Channel(3).play(error)
                                time_tab_gui[-10].update_text("Please fill in a name to save this time")
                                time_tab_gui[-9].update_text("Fill in name here")
                        elif element.identifier == 2:  # Same thing for manually adding a time
                            if len(time_tab_gui[7].text) and len(time_tab_gui[8].text) and len(time_tab_gui[9].text):
                                if len(time_tab_gui[2].text):  # Check for name
                                    mins, sec, cs = time_tab_gui[7].text, time_tab_gui[8].text, time_tab_gui[9].text
                                    mins, sec, cs = ("%02d" % unit for unit in (int(mins), int(sec), int(cs)))
                                    time_string: str = f"{mins}:{sec}.{cs}"
                                    time_tab_gui[5].add((time_string, time_tab_gui[2].text))
                                else:
                                    pygame.mixer.Channel(3).play(error)
                                    unaddressed_error["name"] = True
                                    time_tab_gui[-9].update_text("Fill in name here")
                                    time_tab_gui[16].update_text("Please fill in a name to save this time")
                            else:
                                pygame.mixer.Channel(3).play(error)
                                unaddressed_error["fields"] = True
                                time_tab_gui[16].update_text("Please fill in all fields")
                        elif element.identifier == 3:  # Toggle back view type
                            ghost_back_view = not ghost_back_view
                    if element.hover:
                        if element.identifier == 3:
                            if element.clicked or not element.was_hover:  # If it is a new hover or clicked
                                element.tooltip = ", ".join(generate_shuffle(2, 20, True))
                        if element.identifier == 4:
                            if not timer_running and element.clicked:
                                inspection_start = time_of_frame
                                inspection_running = True
                            else:
                                if timer_running or is_ready:
                                    element.tooltip = "Timer running"
                                else:
                                    element.tooltip = "Start time" if not inspection_running else "Reset time"
                elif type(element) == Leaderboard:
                    if element.changed:
                        pygame.mixer.Channel(1).play(click)
                elif type(element) == InputBox:
                    if timer_running:  # Hinder input field activation while timer is running
                        element.enabled = False
                    elif element.changed_enabled:
                        pygame.mixer.Channel(1).play(click)
            except (AttributeError, TypeError):  # Element is static or requires an argument
                if type(element) == ImageBox:
                    if active_tab == 0 and not hide_rotation_tips:  # Show corresponding arrows
                        shape: str = "cube" if is_cube_form else "net"
                        rot_type: str = hovered_btn.replace("\'", 'p').lower()
                        image_name: str = f"{shape}_{rot_type}"
                        element.update_state(qube_arrows[image_name] if hovered_btn else None)
                pass
            
            if len(time_tab_gui[2].text) or timer_running or is_ready:
                # Hide warning prompts for missing name
                unaddressed_error["name"] = False
                time_tab_gui[-10].update_text("")
                time_tab_gui[-9].update_text("")
            if len(time_tab_gui[7].text) and len(time_tab_gui[8].text) and len(time_tab_gui[9].text):  # Adding a time
                unaddressed_error["fields"] = False
            time_tab_gui[16].update_text("Please fill in all fields" if unaddressed_error["fields"]
                                         else "Please fill in a name" if unaddressed_error["name"] else "")
            qube_tab_gui[15].update_state(keyboard_shortcuts["alternative" if alt_layout else "lettered"])
            
            # Draw GUI Elements
            try:
                tooltips.append(element.draw())  # Some elements will return a tooltip
            except TypeError:  # Is QubeRenderer
                qube_tab_gui[-2].draw(qube)
                if is_cube_form:
                    qube_tab_gui[-8].draw(qube, back_view=True, see_through=ghost_back_view)
        
        for tooltip in tooltips:  # Draw the tooltips last
            if tooltip:
                tooltip.draw()
        
        pygame.display.update()
        clock.tick(_TICK_RATE)


if __name__ == '__main__':
    program_window()
    pygame.quit()
