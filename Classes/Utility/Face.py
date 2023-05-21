class Face1:
    def __init__(self, starting_cell: int):
        self.cell: int = starting_cell


class Face2:
    def __init__(self, starting_cells: tuple | list):
        """
        Starting cells format:
        (ul, ur, dl, dr)
        ul ur
        dl dr
        """
        self.ul, self.ur, self.dl, self.dr = starting_cells

    def up(self) -> tuple:
        return self.ul, self.ur

    def left(self) -> tuple:
        return self.ul, self.dl

    def right(self) -> tuple:
        return self.ur, self.dr

    def down(self) -> tuple:
        return self.dl, self.dr
    
    def rotated(self, counterclockwise: bool = False) -> tuple:
        """
        Returns face as if it had been rotated
        """
        return (self.right(), self.left()) if counterclockwise else (self.left()[::-1], self.right()[::-1])
    
    def rotate(self, counterclockwise: bool = False) -> None:
        """
        Rotates this face
        """
        if counterclockwise:
            (self.ul, self.ur), (self.dl, self.dr) = self.right(), self.left()
        else:
            (self.ur, self.ul), (self.dr, self.dl) = self.left(), self.right()
        return None


class Face3:
    def __init__(self, starting_cells: tuple | list):
        """
        Starting cells format:
        (ul, u, ur, l, c, r, dl, d, dr)
        ul u ur
        l  c  r
        dl d dr
        """
        self.ul, self.u, self.ur, self.l, self.c, self.r, self.dl, self.d, self.dr = starting_cells
    
    def up(self) -> tuple:
        return self.ul, self.u, self.ur
    
    def left(self) -> tuple:
        return self.ul, self.l, self.dl
    
    def right(self) -> tuple:
        return self.ur, self.r, self.dr
    
    def down(self) -> tuple:
        return self.dl, self.d, self.dr
    
    def mid(self) -> tuple:
        return self.l, self.c, self.r
    
    def rotated(self, counterclockwise: bool = False) -> tuple[tuple, tuple, tuple]:
        """
        Returns the face (in form (ul, u, ur), (l, c, r), (dl, d, dr)) as if it had been rotated
        """
        return (self.right(), (self.u, self.c, self.d), self.left()) if counterclockwise else \
            (self.left()[::-1], (self.d, self.c, self.u), self.right()[::-1])
    
    def rotate(self, counterclockwise: bool = False) -> None:
        """
        Rotates this face
        """
        if counterclockwise:
            (self.ul, self.u, self.ur), self.l, (self.dl, self.d, self.dr), self.r = \
                self.right(), self.u, self.left(), self.d
        else:
            (self.ur, self.u, self.ul), self.r, (self.dr, self.d, self.dl), self.l = \
                self.left(), self.u, self.right(), self.d
        return None
