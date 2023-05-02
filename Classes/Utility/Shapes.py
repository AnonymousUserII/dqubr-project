import pygame


parallelogram_top_vectors: tuple = (0, 0), (1, 0), (1.5, -0.5), (0.5, -0.5)  # From bottom-right, counterclockwise
parallelogram_bottom_vectors: tuple = (0, 0), (0.5, 0.5), (1.5, 0.5), (1, 0)  # From top-left, counterclockwise
parallelogram_right_vectors: tuple = (0, 0), (0, 1), (0.5, 0.5), (0.5, -0.5)  # From top-left, clockwise
parallelogram_left_vectors: tuple = (0, 0), (0, 1), (0.5, 1.5), (0.5, 0.5)  # From top-left, clockwise


def draw_top_parallelogram(window: pygame.Surface, pos: tuple[int, int], length: int, color: pygame.Color) -> None:
    shape_points: tuple = tuple((x * length + pos[0], y * length + pos[1]) for x, y in parallelogram_top_vectors)
    pygame.draw.polygon(window, color, shape_points)
    return None


def draw_right_parallelogram(window: pygame.Surface, pos: tuple[int, int], length: int, color: pygame.Color) -> None:
    shape_points: tuple = tuple((x * length + pos[0], y * length + pos[1]) for x, y in parallelogram_right_vectors)
    pygame.draw.polygon(window, color, shape_points)
    return None


def draw_bottom_parallelogram(window: pygame.Surface, pos: tuple[int, int], length: int, color: pygame.Color) -> None:
    shape_points: tuple = tuple((x * length + pos[0], y * length + pos[1]) for x, y in parallelogram_bottom_vectors)
    pygame.draw.polygon(window, color, shape_points)
    return None


def draw_left_parallelogram(window: pygame.Surface, pos: tuple[int, int], length: int, color: pygame.Color) -> None:
    shape_points: tuple = tuple((x * length + pos[0], y * length + pos[1]) for x, y in parallelogram_left_vectors)
    pygame.draw.polygon(window, color, shape_points)
    return None
