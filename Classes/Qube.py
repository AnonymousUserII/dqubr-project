from Classes.Face import Face3


class Qube3:
    def __init__(self):
        self.up: Face3 = Face3(tuple(1 for _ in range(9)))
        self.left: Face3 = Face3(tuple(2 for _ in range(9)))
        self.front: Face3 = Face3(tuple(3 for _ in range(9)))
        self.right: Face3 = Face3(tuple(4 for _ in range(9)))
        self.back: Face3 = Face3(tuple(5 for _ in range(9)))
        self.down: Face3 = Face3(tuple(6 for _ in range(9)))
    
    def f(self, prime: bool = False) -> None:
        """
        Rotate the 8 pieces around the front face, not prime meaning clockwise
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
        
        # Move four main faces
        if prime:
            ((f.ul, f.u, f.ur), (f.l, f.c, f.r), (f.dl, f.d, f.dr)), \
                ((d.ul, d.u, d.ur), (d.l, d.c, d.r), (d.dl, d.d, d.dr)), \
                ((b.ul, b.u, b.ur), (b.l, b.c, b.r), (b.dl, b.d, b.dr)), \
                ((u.ul, u.u, u.ur), (u.l, u.c, u.r), (u.dl, u.d, u.dr)) = \
                (u.up(), u.mid_h(), u.down()), (f.up(), f.mid_h(), f.down()), (d.down(), d.mid_h(), d.up()), \
                (b.down(), b.mid_h(), b.up())
        else:
            ((f.ul, f.u, f.ur), (f.l, f.c, f.r), (f.dl, f.d, f.dr)), \
                ((u.ul, u.u, u.ur), (u.l, u.c, u.r), (u.dl, u.d, u.dr)), \
                ((b.ul, b.u, b.ur), (b.l, b.c, b.r), (b.dl, b.d, b.dr)), \
                ((d.ul, d.u, d.ur), (d.l, d.c, d.r), (d.dl, d.d, d.dr)) = \
                (d.up(), d.mid_h(), d.down()), (f.up(), f.mid_h(), f.down()), (u.down(), u.mid_h(), u.up()), \
                (b.down(), b.mid_h(), b.up())
        
        self.front, self.up, self.back, self.down = f, u, b, d
        return None
    
    def y(self, prime: bool = False) -> None:
        """
        Rotate entire cube by y-axis (top-to-bottom), not prime meaning clockwise as viewed from top
        """
        # Rotate side faces
        self.up.rotate(prime)
        self.down.rotate(not prime)
        
        # Move four main faces
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
        r: Face3 = self.right
        d: Face3 = self.down
        l: Face3 = self.left
        
        # Rotate side faces
        self.front.rotate(prime)
        self.back.rotate(not prime)
        
        # Move four main faces
        if prime:
            ((u.ul, u.u, u.ur), (u.l, u.c, u.r), (u.dl, u.d, u.dr)), \
                ((l.ul, l.u, l.ur), (l.l, l.c, l.r), (l.dl, l.d, l.dr)), \
                ((d.ul, d.u, d.ur), (d.l, d.c, d.r), (d.dl, d.d, d.dr)), \
                ((r.ul, r.u, r.ur), (r.l, r.c, r.r), (r.dl, r.d, r.dr)) = \
                r.rotated(), u.rotated(), l.rotated(), d.rotated()
        else:
            ((u.ul, u.u, u.ur), (u.l, u.c, u.r), (u.dl, u.d, u.dr)), \
                ((r.ul, r.u, r.ur), (r.l, r.c, r.r), (r.dl, r.d, r.dr)), \
                ((d.ul, d.u, d.ur), (d.l, d.c, d.r), (d.dl, d.d, d.dr)), \
                ((l.ul, l.u, l.ur), (l.l, l.c, l.r), (l.dl, l.d, l.dr)) = \
                l.rotated(), u.rotated(), r.rotated(), d.rotated()
        
        return None
    
    """The other rotations are combinations of the above 3"""
    
    def r(self, prime: int | bool = False) -> None:
        self.y()
        self.f(prime)
        self.y(True)
        return None
    
    def l(self, prime: int | bool = False) -> None:
        self.y(True)
        self.f(prime)
        self.y()
        return None
    
    def u(self, prime: int | bool = False) -> None:
        self.x(True)
        self.f(prime)
        self.x()
        return None
    
    def d(self, prime: int | bool = False) -> None:
        self.x()
        self.f(prime)
        self.x(True)
        return None
    
    def b(self, prime: int | bool = False) -> None:
        self.y()
        self.y()
        self.f(prime)
        self.y(True)
        self.y(True)
        return None
