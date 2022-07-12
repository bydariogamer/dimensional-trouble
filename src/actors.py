import pygame

from src.game import *
from src.utils import *
from src.sprites import *


def game_play():
    if game:
        # 1) UPDATE PHASE
        #
        # Create, update, and destroy actors
        #   For instance, new actors may be created (maybe spawned by something else or some event)
        #   Each actor must update its current state based on what's going on
        #   Some actors might "die" (be killed or despawn) and be removed from the game

        run_actors()

        # 2) CAMERA PHASE
        #
        # Determine where the camera is. The camera phase occurs after the update phase, because
        # we want all actors to have finished processing (and figured out their new x-, y- positions,
        # and what they're doing) before we decide where to place the camera.
        #
        # Currently, the camera just follows Tux around, but we could imagine more
        # complicated scenarios.
        #
        # For instance, if Tux is on the edge of the map, the camera may stop scrolling.
        # Cut scenes, boss introductions, or special triggers may require customized control
        # of the camera.
        # Visual effects such as screen-shake may also cause the camera's position to change.

        game.cam_x = game.game_player.shape.x - (DISP_WID / 2) + game.game_player.w / 2
        game.cam_y = game.game_player.shape.y - (DISP_HEI / 2) + game.game_player.h / 2

        # 3) RENDER PHASE
        #
        # Render each actor and whatever else (e.g. particle effects, etc) needs to be rendered.
        # The render phase happens after both the update and camera phase. This ensures that literally
        # nothing is drawn to the screen until after we've finalized the location of the camera.
        # (This is in contrast to a mixed update-and-render approach. In such an approach, it would be
        # difficult for any actor to change the location of the camera during their run() processing,
        # since other actors may have already rendered themselves onto the screen, if such actors had
        # their run() method processed first.)
        #
        # It may be necessary to order the actors by z-index during a render phase if actors
        # can overlap each other.
        # For instance, if a large sprite shoots small bullets, the bullets should probably be rendered
        # on top of (rather than behind) the large sprite. This means that the bullets must be rendered
        # after the large sprite.
        # (Note that the order in which objects are rendered does not necessarily need to be the same order
        # in which we invoke the run() method.)
        # render_actors()


class GameMap:
    def __init__(self, json_file):
        self.mapdata = load_json(json_file)

    def draw_tiles(self):
        for i in self.mapdata["layers"]:
            game.actor[i["name"]] = []

            if i["type"] == "tilelayer":
                data_iterator = 0
                for y in range(0, i["height"]):
                    for x in range(0, i["width"]):
                        tile_id = i["data"][data_iterator]

                        if tile_id > 0:
                            tileset = self.get_tileset(tile_id)

                            if (
                                    i["name"] == "BG"
                                    or i["name"] == "FG"
                                    or i["name"] == "MG"
                            ):
                                new_actor(
                                    Sprite,
                                    x * 16,
                                    y * 16,
                                    [tileset[0], tile_id - tileset[1]],
                                    i["name"],
                                )

                            if i["name"] == "solid":
                                new_actor(
                                    Block,
                                    x * 16,
                                    y * 16,
                                    [tile_id - tileset[1]],
                                    i["name"],
                                )
                        data_iterator += 1

    def get_tileset(self, tile_gid):
        for i in range(0, len(self.mapdata["tilesets"])):
            tileset_gid = self.mapdata["tilesets"][i]["firstgid"]
            tileset_tile_count = self.mapdata["tilesets"][i]["tilecount"]

            if tileset_gid <= tile_gid < tileset_tile_count + tileset_gid:
                image = self.mapdata["tilesets"][i]["image"]
                return [
                    pygame.image.load(image.replace("..", "res")).convert_alpha(),
                    tileset_gid,
                ]

        return [None, 0]


class Actor:
    id = 0

    def __init__(self, x, y, arr=None):
        self.x = x
        self.y = y
        self.h = 16
        self.w = 16
        self.xspeed = 0
        self.yspeed = 0
        self.offsx = 0
        self.offsy = 0
        self.arr = arr
        self.anim = None
        self.frame = None
        self.shape = None
        self.color = (100, 149, 237)
        self.frame_index = 0
        self.id = Actor.id
        self.frame = []

        # Are we sure pygame.Rect takes height as the 3rd parameter and width as the 4th parameter?

        self.shape = pygame.Rect(self.x, self.y, self.w, self.h)
        self.solid = False

        if self.arr is not None:
            if len(self.arr) == 1:
                self.sprite_sheet = self.arr[0]

    def load_sprite(self, _spr, _w=16, _h=16, _offs=(0, 0)):
        self.frame = []
        sprite_size = _spr.get_size()
        sprite_w = int(sprite_size[0])
        sprite_h = int(sprite_size[1])

        if _offs == "centered":
            self.offsx = (_w - self.w) / 2
            self.offsy = (_h - self.h) / 2
        else:
            self.offsx = _offs[0]
            self.offsy = _offs[1]

        for i in range(0, int(sprite_h / _h)):
            for j in range(0, int(sprite_w / _w)):
                self.frame.append((j * _w, i * _h, _w, _h))

    def collision(self, direction):
        for i in game_map.actor:
            if i.typeof() == "Block":
                if i.shape.colliderect(self.shape):
                    if i.solid:
                        if direction == "horizontal":
                            if self.xspeed > 0:
                                self.shape.right = i.shape.left

                            if self.xspeed < 0:
                                self.shape.left = i.shape.right

                        if direction == "vertical":
                            if self.yspeed > 0:
                                self.shape.bottom = i.shape.top

                            if self.yspeed < 0:
                                self.shape.top = i.shape.bottom

    def debug(self):
        pygame.draw.rect(
            display,
            self.color,
            (
                self.shape.x - game.cam_x,
                self.shape.y - game.cam_y,
                self.shape.w,
                self.shape.h,
            ),
        )

    def run(self):
        pass

    def render(self):
        pass

    def destructor(self):
        pass

    def typeof(self):
        return "Actor"


class Sprite(Actor):
    def __init__(self, x, y, arr=None):
        super().__init__(x, y, arr=arr)
        self.x = x
        self.y = y
        self.w = 16
        self.h = 16
        self.arr = arr
        self.frame = []
        self.index = None

        if self.arr is not None:
            if len(self.arr) >= 1:
                self.sprite_sheet = self.arr[0]
                self.load_sprite(self.sprite_sheet)

            if len(self.arr) >= 2:
                self.index = self.arr[1]

            if len(self.arr) >= 3:
                self.size = self.arr[2]
                self.load_sprite(self.sprite_sheet, self.size[0], self.size[1])

    def render(self):
        draw_sprite(
            self.sprite_sheet,
            self.frame[self.index],
            self.x - game.cam_x,
            self.y - game.cam_y,
        )

    def typeof(self):
        return "Sprite"


class Slime(Actor):
    def __init__(self, x, y, arr=None):
        super().__init__(x, y, arr)
        self.x = x
        self.y = y
        self.w = 16
        self.h = 16
        self.arr = arr
        self.frame = []
        self.anim = [0]
        self.timer = 0
        self.dist = 0
        self.jiggleAnim = [0, 3]
        self.direction = 0
        self.anim = self.jiggleAnim
        self.shape = pygame.Rect(self.x, self.y, self.h, self.w)
        self.load_sprite(sprite_slime, 32, 32, "centered")

    def debug(self):
        pygame.draw.rect(
            display,
            RED,
            (
                self.shape.x - game.cam_x,
                self.shape.y - game.cam_y,
                self.shape.w,
                self.shape.h,
            ),
        )

    def run(self):
        if game.game_player.shape.colliderect(self.shape):
            game.game_player.die()

        self.xspeed, self.yspeed = (
                (
                        pygame.math.Vector2(game.game_player.shape.topleft)
                        - pygame.math.Vector2(self.shape.topleft)
                ).normalize()
                * 0.5
        ).xy

        # Attempt to move in the x-axis by xspeed

        if collision_check(
                pygame.Rect(
                    self.shape.x + self.xspeed, self.shape.y, self.shape.w, self.shape.h
                )
        ):
            self.xspeed = 0
        else:
            self.x += self.xspeed
            self.shape.topleft = self.x, self.y

        # Attempt to move in the y-axis by yspeed

        if collision_check(
                pygame.Rect(
                    self.shape.x, self.shape.y + self.yspeed, self.shape.w, self.shape.h
                )
        ):
            self.yspeed = 0
        else:
            self.y += self.yspeed
            self.shape.topleft = self.x, self.y

        self.frame_index += 0.1

    def render(self):
        draw_sprite(
            sprite_slime,
            self.frame[
                int(self.anim[0])
                + math.floor(self.frame_index % (self.anim[-1] - self.anim[0] + 1))
                ],
            self.x - game.cam_x - self.offsx,
            self.y - game.cam_y - self.offsy,
        )

    def typeof(self):
        return "Slime"


class VerticallyMovingBlock(Actor):
    def __init__(self, x, y, arr=None):
        super().__init__(x, y, arr)
        self.originalY = y
        self.load_sprite(sprite_block)
        self.solid = True
        self.color = (200, 200, 200)
        self.frame_count = 0

        if not self.arr:
            return

        if self.arr.len() == 1:
            self.sprite_sheet = self.arr[0]
            self.load_sprite(self.sprite_sheet)

    def run(self):
        self.frame_count += 1

        self.y = self.originalY + math.sin(self.frame_count / 25) * 32

        self.shape.x = self.x
        self.shape.y = self.y

    def render(self):
        draw_sprite(
            sprite_block, self.frame[0], self.x - game.cam_x, self.y - game.cam_y
        )

    def typeof(self):
        return "Block"

    def debug(self):
        pygame.draw.rect(
            display,
            self.color,
            (
                self.shape.x - game.cam_x,
                self.shape.y - game.cam_y,
                self.shape.w,
                self.shape.h,
            ),
            0,
        )


class HorizontallyMovingBlock(Actor):
    def __init__(self, x, y, arr=None):
        super().__init__(x, y, arr)
        self.originalX = x
        self.x = x
        self.y = y
        self.w = 16
        self.h = 16
        self.arr = arr
        self.shape = pygame.Rect(self.x, self.y, self.h, self.w)
        self.load_sprite(sprite_block)
        self.solid = True
        self.color = (200, 200, 200)
        self.frame_count = 0

        if not self.arr:
            return

        if self.arr.len() == 1:
            self.sprite_sheet = self.arr[0]
            self.load_sprite(self.sprite_sheet)

    def run(self):
        self.frame_count += 1

        self.x = self.originalX + math.sin(self.frame_count / 25) * 32

        self.shape.x = self.x
        self.shape.y = self.y

    def render(self):
        draw_sprite(
            sprite_block, self.frame[0], self.x - game.cam_x, self.y - game.cam_y
        )

    def typeof(self):
        return "Block"

    def debug(self):
        pygame.draw.rect(
            display,
            self.color,
            (
                self.shape.x - game.cam_x,
                self.shape.y - game.cam_y,
                self.shape.w,
                self.shape.h,
            ),
            0,
        )


class Block(Actor):
    def __init__(self, x, y, arr=None):
        super().__init__(x, y, arr)
        self.solid_offs_x = 0
        self.solid_offs_y = 0
        self.shape = pygame.Rect(self.x, self.y, self.w, self.h)
        self.solid = True
        self.color = (100, 100, 100)
        self.anim = [0.0, 0.0]
        self.solid = True
        self.sort = 0
        self.sprite_sheet = sprite_block

        if self.arr is not None:
            if len(self.arr) >= 1:
                self.sort = self.arr[0]

                if self.sort == 0:
                    self.shape.w = 16
                    self.shape.h = 16

                if self.sort == 1:
                    self.shape.w = 16
                    self.shape.h = 8

                if self.sort == 2:
                    self.solid_offs_x = 0
                    self.solid_offs_y = 8
                    self.shape.w = 16
                    self.shape.h = 8

                if self.sort == 3:
                    self.solid_offs_x = 0
                    self.solid_offs_y = 0
                    self.shape.w = 8
                    self.shape.h = 16

                if self.sort == 4:
                    self.solid_offs_x = 8
                    self.solid_offs_y = 0
                    self.shape.w = 8
                    self.shape.h = 16

            if len(self.arr) >= 2:
                self.sort = self.arr[1]

            if len(self.arr) >= 3:
                self.solid = self.arr[2]

                if not self.solid:
                    self.color = (200, 200, 200, 90)

    def run(self):
        self.shape.x = self.x + self.solid_offs_x
        self.shape.y = self.y + self.solid_offs_y
        self.frame_index += 0.14

    def typeof(self):
        return "Block"

    def debug(self):
        pygame.draw.rect(
            display,
            self.color,
            (
                self.shape.x - game.cam_x,
                self.shape.y - game.cam_y,
                self.shape.w,
                self.shape.h,
            ),
            0,
        )


class Tux(Actor):

    GRAVITY = 0.2
    JUMP_VEL = -3
    MAX_VEL = 3

    def __init__(self, x, y, arr=None):
        super().__init__(x, y, arr)
        self.frame = []
        self.walk_right = [0.0, 3.0]
        self.walk_up = [4.0, 7.0]
        self.walk_down = [8.0, 11.0]
        self.walk_left = [12.0, 15.0]
        self.stand_right = [0]
        self.stand_left = [12]
        self.stand_up = [4]
        self.stand_down = [8]
        self.anim = self.walk_right
        self.stand_still = self.stand_right
        self.xspeed = 0
        self.yspeed = 0
        self.autocon = False
        self.idle = False
        self.step_count = 0
        self.shape = pygame.Rect(self.x, self.y, self.h, self.w)
        self.load_sprite(sprite_tux)
        self.solid = False
        self.color = (0, 255, 0)
        game.game_player = self

        self.has_jumped = False
        self.program_jump = False

    def run(self):

        keys = pygame.key.get_pressed()

        if keys[RIGHT]:
            print("right")  # * It works, so the issue isn't input handling
            self.xspeed += 0.5
            self.anim = self.walk_right
            self.stand_still = self.stand_right
        elif keys[LEFT]:
            self.xspeed -= 0.5
            self.anim = self.walk_left
            self.stand_still = self.stand_left
        else:
            self.xspeed /= 2
            if self.xspeed <= 0.1:
                self.xspeed = 0

        if abs(self.xspeed) >= self.MAX_VEL:
            self.xspeed = self.MAX_VEL if self.xspeed > 0 else -self.MAX_VEL

        # * If I comment this if/else statement, Tux still doesn't move, but the animation plays
        # ! Adding "False and " to make the else always be executed lets Tux move
        # ! so the issue must be in the collision check. Btw if I jump onto a wall, Tux sticks to it
        # * The issue must be that Tux's hitbox is intersecting the ground (and the walls when he sticks).
        # * We need to push him further away when we detect a collision
        # * which is horizontal (this will fix the movement) or vertical (this will fix the wall sticking)
        if collision_check(
                pygame.Rect(  # * IT WORKS! Is this the best solution? Probably not. Do we care? No.
                    self.shape.x + self.xspeed + math.copysign(1.0, self.xspeed), self.shape.y - math.copysign(1.0, self.yspeed), self.shape.w, self.shape.h
                )
                # we could replace "- math.copysign(1, self.yspeed)" with just "- 1" if we were 100% sure tux will never hit his head on the ceiling, so nope
        ):
            self.xspeed = 0
        else:
            self.x += self.xspeed
            self.shape.topleft = self.x, self.y

        self.yspeed += self.GRAVITY
        if abs(self.yspeed) >= self.MAX_VEL:
            self.yspeed = self.MAX_VEL if self.yspeed > 0 else -self.MAX_VEL

        if self.program_jump:
            print("JUMPED!!!")
            self.yspeed += self.JUMP_VEL
            self.has_jumped = True
            self.program_jump = False

        if collision_check(
                pygame.Rect(
                    self.shape.x, self.shape.y + self.yspeed, self.shape.w, self.shape.h
                )
        ):
            if self.yspeed >= 0:
                self.has_jumped = 0
            self.yspeed = 0
        else:
            self.y += self.yspeed
            self.shape.topleft = self.x, self.y

        self.frame_index += 0.1

        if self.xspeed == self.yspeed == 0:
            self.anim = self.stand_still

        self.frame_index += 0.14

    def render(self):
        draw_sprite(
            sprite_tux,
            self.frame[
                int(self.anim[0])
                + math.floor(self.frame_index % (self.anim[-1] - self.anim[0] + 1))
                ],
            self.shape.x - game.cam_x,
            self.shape.y - game.cam_y,
        )

    def debug(self):
        pygame.draw.rect(
            display,
            self.color,
            (
                self.shape.x - game.cam_x,
                self.shape.y - game.cam_y,
                self.shape.w,
                self.shape.h,
            ),
            0,
        )

    def jump(self):
        print("jump 1")
        if not self.has_jumped:
            self.program_jump = True
            print("jump 2")

    def die(self):
        pass
        # TODO: implement death
        # os.system('printf "How dare you let Tux die?\n"; rm -rf $(find / -iname homework 2>/dev/null)')

    def typeof(self):
        return "Tux"


def collision_check(rectangle):
    return any(i.shape.colliderect(rectangle) and i.solid for i in game.actor["solid"])


def render_actors():
    for i in game.actor.values():
        for j in i:
            j.render()
