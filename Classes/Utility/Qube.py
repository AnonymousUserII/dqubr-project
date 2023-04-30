from random import random, choice

from Classes.Utility.Face import *


def generate_shuffle(size: int, moves: int = 40, contract_doubles: bool = False) -> list[str]:
    possible_moves: list = ['R', 'L', 'U', 'D', 'F', 'B']  # Default
    if size == 1:
        possible_moves = ['x', 'y', 'z']
    elif size == 3:
        possible_moves.append('M')
    elif size == 4:
        possible_moves += ['r', 'l', 'u', 'd', 'f', 'b']
        possible_moves += []
    random_moveset: list[str] = []
    for _ in range(moves):
        random_moveset.append(choice(possible_moves))
        if round(random()) == 1:
            random_moveset[-1] += "\'"  # 50/50 for move to be primed
    
    # Check for redundant moves
    move_string: str = '&'.join(random_moveset)
    for move in possible_moves:
        # Remove four-in-a-row
        while f"{move}&{move}&{move}&{move}" in move_string:
            move_string = move_string.replace(f"{move}&{move}&{move}&{move}", "")
            move_string.replace("&&", "&")
        while f"{move}\'&{move}\'&{move}\'&{move}\'" in move_string:
            move_string = move_string.replace(f"{move}\'&{move}\'&{move}\'&{move}\'", "")
            move_string.replace("&&", "&")
        
        # Remove consecutive reversals, e.g. D&D'
        while f"{move}&{move}\'" in move_string:
            move_string = move_string.replace(f"{move}&{move}\'", "")
            move_string.replace("&&", "&")
        while f"{move}\'&{move}" in move_string:
            move_string = move_string.replace(f"{move}\'&{move}", "")
            move_string.replace("&&", "&")
        
        # Contract triples then doubles
        while f"{move}&{move}&{move}" in move_string:
            move_string = move_string.replace(f"{move}&{move}&{move}", "")
            move_string.replace("&&", "&")
        while f"{move}\'&{move}\'&{move}\'" in move_string:
            move_string = move_string.replace(f"{move}\'&{move}\'&{move}\'", "")
            move_string.replace("&&", "&")
        
        if contract_doubles:
            while f"{move}&{move}" in move_string:
                move_string = move_string.replace(f"{move}&{move}", f"{move}2")
                move_string.replace("&&", "&")
            while f"{move}\'&{move}\'" in move_string:
                move_string = move_string.replace(f"{move}\'&{move}\'", f"{move}2\'")
                move_string.replace("&&", "&")
        
        while "&&" in move_string:  # Remove extra separators
            move_string = move_string.replace("&&", "&")
    generated_moves = move_string.split('&')
    # Remove empty moves
    while "" in generated_moves:
        generated_moves.remove("")
    while "\'" in generated_moves:
        generated_moves.remove("\'")
    
    return generated_moves


class Qube1:
    def __init__(self):
        self.up: Face1 = Face1(1)
        self.left: Face1 = Face1(2)
        self.front: Face1 = Face1(3)
        self.right: Face1 = Face1(4)
        self.back: Face1 = Face1(5)
        self.down: Face1 = Face1(6)
    
    def reset(self) -> None:
        self.__init__()
        return None
    
    def x(self, prime: bool = False) -> None:
        """
        Rotate entire cube by x-axis (left-to-right), not prime meaning clockwise as viewed from right
        """
        if prime:
            self.front, self.down, self.back, self.up = self.up, self.front, self.down, self.back
        else:
            self.front, self.up, self.back, self.down = self.down, self.front, self.up, self.back
    
    def y(self, prime: bool = False) -> None:
        """
        Rotate entire cube by y-axis (top-to-bottom), not prime meaning clockwise as viewed from top
        """
        if prime:
            self.front, self.right, self.back, self.left = self.left, self.front, self.right, self.back
        else:
            self.front, self.left, self.back, self.right = self.right, self.front, self.left, self.back
        return None

    def z(self, prime: bool = False) -> None:
        """
        Rotate entire cube by z-axis (front-to-back), not prime meaning clockwise as viewed from front
        """
        if prime:
            self.up, self.left, self.down, self.right = self.right, self.up, self.left, self.down
        else:
            self.up, self.right, self.down, self.left = self.left, self.up, self.right, self.down
        return None
    
    def apply_moves(self, moves: list | tuple) -> None:
        """
        Accepts an iterable sequence of moves in character form.
        """
        for move in moves:
            prime: bool = '\'' in move
            if 'x' in move:
                self.x(prime)
            elif 'y' in move:
                self.y(prime)
            elif 'z' in move:
                self.z(prime)
        return None


class Qube2:
    def __init__(self):
        self.up: Face2 = Face2((1, 1, 1, 1))
        self.left: Face2 = Face2((2, 2, 2, 2))
        self.front: Face2 = Face2((3, 3, 3, 3))
        self.right: Face2 = Face2((4, 4, 4, 4))
        self.back: Face2 = Face2((5, 5, 5, 5))
        self.down: Face2 = Face2((6, 6, 6, 6))
    
    def reset(self) -> None:
        self.__init__()
        return None
    
    def f(self, prime: bool = False) -> None:
        """
        Rotate the front face and adjacent cells, not prime meaning clockwise
        """
        l: Face2 = self.left
        u: Face2 = self.up
        r: Face2 = self.right
        d: Face2 = self.down
        
        self.front.rotate(prime)
        if prime:
            (u.dl, u.dr), (l.dr, l.ur), (d.ul, d.ur), (r.dl, r.ul) = r.left(), u.down(), l.right(), d.up()
        else:
            (u.dr, u.dl), (r.ul, r.dl), (d.ur, d.ul), (l.ur, l.dr) = l.right(), u.down(), r.left(), d.up()
        return None
    
    def x(self, prime: bool = False) -> None:
        """
        Rotate entire cube by x-axis (left-to-right), not prime meaning clockwise as viewed from right
        """
        f: Face2 = self.front
        u: Face2 = self.up
        b: Face2 = self.back
        d: Face2 = self.down
        
        # Rotate side faces
        self.right.rotate(prime)
        self.left.rotate(not prime)
        
        # Move four main faces
        if prime:
            (((f.ul, f.ur), (f.dl, f.dr)),
             ((d.ul, d.ur), (d.dl, d.dr)),
             ((b.ul, b.ur), (b.dl, b.dr)),
             ((u.ul, u.ur), (u.dl, u.dr))) = \
                ((u.up(), u.down()),
                 (f.up(), f.down()),
                 (d.down()[::-1], d.up()[::-1]),
                 (b.down()[::-1], b.up()[::-1]))
        else:
            (((f.ul, f.ur), (f.dl, f.dr)),
             ((u.ul, u.ur), (u.dl, u.dr)),
             ((b.ul, b.ur), (b.dl, b.dr)),
             ((d.ul, d.ur), (d.dl, d.dr))) = \
                ((d.up(), d.down()),
                 (f.up(), f.down()),
                 (u.down()[::-1], u.up()[::-1]),
                 (b.down()[::-1], b.up()[::-1]))
        return None
    
    def y(self, prime: bool = False) -> None:
        """
        Rotate entire cube by y-axis (top-to-bottom), not prime meaning clockwise as viewed from top
        """
        # Rotate side faces
        self.up.rotate(prime)
        self.down.rotate(not prime)
        
        # Translate four main faces
        if prime:
            self.front, self.right, self.back, self.left = self.left, self.front, self.right, self.back
        else:
            self.front, self.left, self.back, self.right = self.right, self.front, self. left, self.back
        return None
    
    def z(self, prime: bool = False) -> None:
        """
        Rotate entire cube by z-axis (front-to-back), not prime meaning clockwise as viewed from front
        """
        u: Face2 = self.up
        l: Face2 = self.left
        r: Face2 = self.right
        d: Face2 = self.down
    
        # Rotate side faces
        self.front.rotate(prime)
        self.back.rotate(not prime)
    
        # Move four main faces, rotating like a windmill
        if prime:
            (((u.ul, u.ur), (u.dl, u.dr)),
             ((l.ul, l.ur), (l.dl, l.dr)),
             ((d.ul, d.ur), (d.dl, d.dr)),
             ((r.ul, r.ur), (r.dl, r.dr))) = \
                (r.rotated(prime),
                 u.rotated(prime),
                 l.rotated(prime),
                 d.rotated(prime))
        else:
            (((u.ul, u.ur), (u.dl, u.dr)),
             ((r.ul, r.ur), (r.dl, r.dr)),
             ((d.ul, d.ur), (d.dl, d.dr)),
             ((l.ul, l.ur), (l.dl, l.dr))) = \
                (l.rotated(),
                 u.rotated(),
                 r.rotated(),
                 d.rotated())
        return None

    """The other rotations are combinations of the above 3"""

    def r(self, prime: bool = False) -> None:
        self.y()
        self.f(prime)
        self.y(True)
        return None

    def l(self, prime: bool = False) -> None:
        self.y(True)
        self.f(prime)
        self.y()
        return None

    def u(self, prime: bool = False) -> None:
        self.x(True)
        self.f(prime)
        self.x()
        return None

    def d(self, prime: bool = False) -> None:
        self.x()
        self.f(prime)
        self.x(True)
        return None

    def b(self, prime: bool = False) -> None:
        self.y()
        self.y()
        self.f(prime)
        self.y(True)
        self.y(True)
        return None
    
    def apply_moves(self, moves: list | tuple) -> None:
        """
        Accepts an iterable sequence of moves in character form.
        """
        for move in moves:
            prime: bool = '\'' in move
            if 'R' in move:
                self.r(prime)
            elif 'L' in move:
                self.l(prime)
            elif 'F' in move:
                self.f(prime)
            elif 'B' in move:
                self.b(prime)
            elif 'U' in move:
                self.u(prime)
            elif 'D' in move:
                self.d(prime)
        return None


class Qube3:
    def __init__(self):
        self.up: Face3 = Face3(tuple(1 for _ in range(9)))
        self.left: Face3 = Face3(tuple(2 for _ in range(9)))
        self.front: Face3 = Face3(tuple(3 for _ in range(9)))
        self.right: Face3 = Face3(tuple(4 for _ in range(9)))
        self.back: Face3 = Face3(tuple(5 for _ in range(9)))
        self.down: Face3 = Face3(tuple(6 for _ in range(9)))
    
    def reset(self) -> None:
        self.__init__()
        return None
    
    def f(self, prime: bool = False) -> None:
        """
        Rotate the front face and adjacent cells, not prime meaning clockwise
        """
        l: Face3 = self.left
        u: Face3 = self.up
        r: Face3 = self.right
        d: Face3 = self.down
        
        self.front.rotate(prime)
        if prime:
            (u.dl, u.d, u.dr), (l.dr, l.r, l.ur), (d.ul, d.u, d.ur), (r.dl, r.l, r.ul) = \
                r.left(), u.down(), l.right(), d.up()
        else:
            (u.dr, u.d, u.dl), (r.ul, r.l, r.dl), (d.ur, d.u, d.ul), (l.ur, l.r, l.dr) = \
                l.right(), u.down(), r.left(), d.up()
        
        return None
    
    def x(self, prime: bool = False) -> None:
        """
        Rotate entire cube by x-axis (left-to-right), not prime meaning clockwise as viewed from right
        """
        f: Face3 = self.front
        u: Face3 = self.up
        b: Face3 = self.back
        d: Face3 = self.down
        
        # Rotate side faces
        self.right.rotate(prime)
        self.left.rotate(not prime)
        
        # Move four main faces, minding that back face is flipped compared to the others
        if prime:
            (((f.ul, f.u, f.ur), (f.l, f.c, f.r), (f.dl, f.d, f.dr)),
             ((d.ul, d.u, d.ur), (d.l, d.c, d.r), (d.dl, d.d, d.dr)),
             ((b.ur, b.u, b.ul), (b.r, b.c, b.l), (b.dr, b.d, b.dl)),
             ((u.ur, u.u, u.ul), (u.r, u.c, u.l), (u.dr, u.d, u.dl))) = \
                ((u.up(), u.mid_h(), u.down()),
                 (f.up(), f.mid_h(), f.down()),
                 (d.down(), d.mid_h(), d.up()),
                 (b.down(), b.mid_h(), b.up()))
        else:
            (((f.ul, f.u, f.ur), (f.l, f.c, f.r), (f.dl, f.d, f.dr)),
             ((u.ul, u.u, u.ur), (u.l, u.c, u.r), (u.dl, u.d, u.dr)),
             ((b.ur, b.u, b.ul), (b.r, b.c, b.l), (b.dr, b.d, b.dl)),
             ((d.ur, d.u, d.ul), (d.r, d.c, d.l), (d.dr, d.d, d.dl))) = \
                ((d.up(), d.mid_h(), d.down()),
                 (f.up(), f.mid_h(), f.down()),
                 (u.down(), u.mid_h(), u.up()),
                 (b.down(), b.mid_h(), b.up()))
        
        self.front, self.up, self.back, self.down = f, u, b, d
        return None
    
    def y(self, prime: bool = False) -> None:
        """
        Rotate entire cube by y-axis (top-to-bottom), not prime meaning clockwise as viewed from top
        """
        # Rotate side faces
        self.up.rotate(prime)
        self.down.rotate(not prime)
        
        # Move four main faces, simple translation
        if prime:
            self.front, self.right, self.back, self.left = self.left, self.front, self.right, self.back
        else:
            self.front, self.left, self.back, self.right = self.right, self.front, self.left, self.back
        
        return None
    
    def z(self, prime: bool = False) -> None:
        """
        Rotate entire cube by z-axis (front-to-back), not prime meaning clockwise as viewed from front
        """
        u: Face3 = self.up
        l: Face3 = self.left
        r: Face3 = self.right
        d: Face3 = self.down
        
        # Rotate side faces
        self.front.rotate(prime)
        self.back.rotate(not prime)
        
        # Move four main faces, rotating like a windmill
        if prime:
            (((u.ul, u.u, u.ur), (u.l, u.c, u.r), (u.dl, u.d, u.dr)),
             ((l.ul, l.u, l.ur), (l.l, l.c, l.r), (l.dl, l.d, l.dr)),
             ((d.ul, d.u, d.ur), (d.l, d.c, d.r), (d.dl, d.d, d.dr)),
             ((r.ul, r.u, r.ur), (r.l, r.c, r.r), (r.dl, r.d, r.dr))) = \
                (r.rotated(prime),
                 u.rotated(prime),
                 l.rotated(prime),
                 d.rotated(prime))
        else:
            (((u.ul, u.u, u.ur), (u.l, u.c, u.r), (u.dl, u.d, u.dr)),
             ((r.ul, r.u, r.ur), (r.l, r.c, r.r), (r.dl, r.d, r.dr)),
             ((d.ul, d.u, d.ur), (d.l, d.c, d.r), (d.dl, d.d, d.dr)),
             ((l.ul, l.u, l.ur), (l.l, l.c, l.r), (l.dl, l.d, l.dr))) = \
                (l.rotated(),
                 u.rotated(),
                 r.rotated(),
                 d.rotated())
        
        self.up, self.left, self.right, self.down = u, l, r, d
        return None
    
    """The other rotations are combinations of the above 3"""
    
    def r(self, prime: bool = False) -> None:
        self.y()
        self.f(prime)
        self.y(True)
        return None
    
    def l(self, prime: bool = False) -> None:
        self.y(True)
        self.f(prime)
        self.y()
        return None
    
    def u(self, prime: bool = False) -> None:
        self.x(True)
        self.f(prime)
        self.x()
        return None
    
    def d(self, prime: bool = False) -> None:
        self.x()
        self.f(prime)
        self.x(True)
        return None
    
    def b(self, prime: bool = False) -> None:
        self.y()
        self.y()
        self.f(prime)
        self.y(True)
        self.y(True)
        return None
    
    def m(self, prime: bool = False) -> None:
        self.l(not prime)
        self.r(prime)
        self.x(not prime)
        return None
    
    def e(self, prime: bool = False) -> None:
        self.u(prime)
        self.d(not prime)
        self.y(not prime)
        return None
    
    def s(self, prime: bool = False) -> None:
        self.f(not prime)
        self.b(prime)
        self.z(prime)
        return None
    
    def apply_moves(self, moves: list | tuple) -> None:
        """
        Accepts an iterable sequence of moves in character form.
        """
        for move in moves:
            prime: bool = '\'' in move
            if 'R' in move:
                self.r(prime)
            elif 'L' in move:
                self.l(prime)
            elif 'F' in move:
                self.f(prime)
            elif 'B' in move:
                self.b(prime)
            elif 'U' in move:
                self.u(prime)
            elif 'D' in move:
                self.d(prime)
            elif 'M' in move:
                self.m(prime)
            elif 'E' in move:
                self.e(prime)
            elif 'S' in move:
                self.s(prime)
        return None
