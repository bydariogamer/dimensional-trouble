from typing import *
import pygame
import json
import math
import sys
import functools

import src.globals


# colors have also alpha
BLACK = (0, 0, 0, 255)
WHITE = (255, 255, 255, 255)
BLUE = (30, 144, 255, 255)
TRUE_BLUE = (0, 0, 255, 255)
PURPLE = (155, 89, 182, 255)
RED = (255, 0, 0, 255)
GREEN = (60, 179, 113, 255)
DARK_GREEN = (46, 139, 87, 255)
ORANGE = (230, 140, 30, 255)
GREY = (128, 128, 128, 255)
LIGHT_GREY = (192, 192, 192, 255)
PINK = (255, 51, 153, 255)
FLASH_GREEN = (153, 255, 0, 255)
NAVY = (0, 0, 128, 255)
GOLD = (255, 214, 0, 255)
WHITESMOKE = (245, 245, 245, 255)
TURQUOISE = (26, 188, 156, 255)
YELLOW = (241, 196, 15, 255)
CONCRETE = (149, 165, 166, 255)
PUMPKIN = (211, 84, 0, 255)
NICE_BLUE = (52, 152, 219, 255)
MIDNIGHT_BLUE = (44, 62, 80, 255)


@functools.lru_cache
def load_image(path: str) -> pygame.surface.Surface:
    return pygame.image.load(path).convert()


@functools.lru_cache
def load_alpha_image(path: str) -> pygame.surface.Surface:
    return pygame.image.load(path).convert_alpha()


@functools.lru_cache
def resize_smooth_image(
    image: pygame.Surface, new_size: Tuple[int, int]
) -> pygame.surface.Surface:
    return pygame.transform.smoothscale(image, new_size)


@functools.lru_cache
def resize_image(
    image: pygame.Surface, new_size: Tuple[int, int]
) -> pygame.surface.Surface:
    return pygame.transform.scale(image, new_size)


@functools.lru_cache
def resize_image_ratio(
    image: pygame.Surface, new_size: Tuple[int, int]
) -> pygame.surface.Surface:
    ratio = new_size[0] / image.get_width()
    return pygame.transform.scale(
        image,
        (math.floor(image.get_width() * ratio), math.floor(image.get_height() * ratio)),
    )


@functools.lru_cache
def resizex(
    image: pygame.surface.Surface, amount: int or float
) -> pygame.surface.Surface:
    w, h = image.get_width(), image.get_height()
    return pygame.transform.scale(image, (w * amount, h * amount))


def is_left_click(event: pygame.event.Event) -> bool:
    return event.type == pygame.MOUSEBUTTONDOWN and event.button == 1


def is_middle_click(event: pygame.event.Event) -> bool:
    return event.type == pygame.MOUSEBUTTONDOWN and event.button == 2


def is_right_click(event: pygame.event.Event) -> bool:
    return event.type == pygame.MOUSEBUTTONDOWN and event.button == 3


@functools.lru_cache
def get_font(size, font=None) -> pygame.font.Font:
    if font is None:
        return src.globals.font
    else:
        return pygame.font.Font(font, size)


def wrap_multi_lines(
    text: str,
    font: pygame.font.Font,
    max_width: int,
    max_height: int = 0,
    antialias: bool = True,
) -> List:
    finished_lines = [""]

    for word in text.split(" "):
        w = font.render(word, antialias, BLACK).get_width()
        # check if one word is too long to fit in one line
        if w > max_width:
            sys.exit(
                f"""the word: "{word}" is too long to fit in a width of: {max_width}, out of bounds by: {w - max_width}pxls"""
            )

        if (
            font.render(finished_lines[-1] + word, antialias, BLACK).get_width()
            > max_width
        ):
            finished_lines.append(f"""{word}""")
        else:
            finished_lines[-1] += f""" {word}"""
    finished_lines[0] = finished_lines[0][1:]
    if max_height > 0:
        h = 0
        for line in finished_lines:
            h += font.render(line, antialias, BLACK).get_height()

        if h > max_height:
            sys.exit(
                f"""the lines: {finished_lines} are too long in the y axis by: {h - max_height}pxls"""
            )

    return finished_lines


def blit_multiple_lines(
    x: int,
    y: int,
    lines: list,
    display: pygame.surface.Surface,
    font: pygame.font.Font,
    centered_x=False,
    centered_x_pos: int = None,
    color: Tuple[int, int, int] = (0, 0, 0),
) -> None:
    if centered_x and not centered_x_pos:
        sys.exit("Missing 'centered_x_pos'")
    height = font.get_height()
    for i, text in enumerate(lines):
        rendered_text_surface = font.render(text, True, color)
        if centered_x:
            display.blit(
                rendered_text_surface,
                (
                    centered_x_pos - rendered_text_surface.get_width() / 2,
                    y + (i * height),
                ),
            )
        else:
            display.blit(rendered_text_surface, (x, y + (i * height)))


def pixel_perfect_collision(
    image_1: pygame.surface.Surface,
    image_1_pos: Tuple[int, int],
    image_2: pygame.surface.Surface,
    image_2_pos: Tuple[int, int],
) -> bool:
    offset = [image_1_pos[0] - image_2_pos[0], image_1_pos[1] - image_2_pos[1]]
    mask_1 = pygame.mask.from_surface(image_1)
    mask_2 = pygame.mask.from_surface(image_2)
    result = mask_2.overlap(mask_1, offset)
    if result:
        return True
    return False


def load_json(path):
    return json.loads(open(path, "r").read())


def flatten(items):
    for item in items:
        if isinstance(item, list) or isinstance(item, tuple):
            for subitem in flatten(item):
                yield subitem
        else:
            yield item


@functools.lru_cache(5000)
def text(txt, color, size=20, font_name=None):
    """Render a text on a surface. Results are cached."""
    return get_font(size, font_name).render(str(txt), True, color)


def draw_text(font: pygame.font.Font, x, y, text, color):
    src.globals.display.blit(font.render(text, True, color), (x, y))


def blit_centered(screen, surface, rect):
    screen.blit(surface, surface.get_rect(center=rect.center))


@functools.lru_cache(100)
def ninepatch(surface: pygame.Surface, rect: tuple):
    rect = pygame.Rect(rect)
    result = pygame.Surface(rect.size, pygame.SRCALPHA)
    subsurf_w = surface.get_width() // 3
    subsurf_h = surface.get_height() // 3
    a1 = surface.subsurface(0, 0, subsurf_w, subsurf_h)
    a2 = surface.subsurface(subsurf_w, 0, subsurf_w, subsurf_h)
    a3 = surface.subsurface(2 * subsurf_w, 0, subsurf_w, subsurf_h)
    b1 = surface.subsurface(0, subsurf_h, subsurf_w, subsurf_h)
    b2 = surface.subsurface(subsurf_w, subsurf_h, subsurf_w, subsurf_h)
    b3 = surface.subsurface(2 * subsurf_w, subsurf_h, subsurf_w, subsurf_h)
    c1 = surface.subsurface(0, 2 * subsurf_h, subsurf_w, subsurf_h)
    c2 = surface.subsurface(subsurf_w, 2 * subsurf_h, subsurf_w, subsurf_h)
    c3 = surface.subsurface(2 * subsurf_w, 2 * subsurf_h, subsurf_w, subsurf_h)

    result.blit(a1, (0, 0))
    result.blit(pygame.transform.scale(a2, (rect.w - 2 * subsurf_w, subsurf_h)), (subsurf_w, 0))
    result.blit(a3, (rect.w - subsurf_w, 0))
    result.blit(pygame.transform.scale(b1, (subsurf_w, rect.h - 2 * subsurf_h)), (0, subsurf_h))
    result.blit(
        pygame.transform.scale(b2, (rect.w - 2 * subsurf_w, rect.h - 2 * subsurf_h)),
        (subsurf_w, subsurf_h),
    )
    result.blit(
        pygame.transform.scale(b3, (subsurf_w, rect.h - 2 * subsurf_h)),
        (rect.w - subsurf_w, subsurf_h),
    )
    result.blit(c1, (0, rect.h - subsurf_h))
    result.blit(
        pygame.transform.scale(c2, (rect.w - 2 * subsurf_w, subsurf_h)),
        (subsurf_w, rect.h - subsurf_h),
    )
    result.blit(c3, (rect.w - subsurf_w, rect.h - subsurf_h))

    return result


# ~~stolen~~ borrowed from https://github.com/pygame/pygame/pull/2929#issuecomment-1002342735
def vector2_move_towards(
        origin,
        target,
        speed: float
):
    """Moves towards the target Vector2 by the movement speed.

    Must be put in a loop until its reached its target.

    Parameters:
        origin: The original position
        target: The target position.
        speed: The movement speed.
    """
    delta = target - origin
    dist = delta.magnitude()

    if dist <= speed or dist == 0:
        return target

    return origin + delta / dist * speed


def number_format(n: int, l: int) -> str:
    ns = str(n)
    if len(ns) < l:
        return "0" * (l - len(ns)) + ns
    return ns


# dumb stuff to replace when I have time:


def draw_sprite(spr, frame, x, y):
    src.globals.display.blit(spr, (x, y), frame)
