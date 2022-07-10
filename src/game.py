from src.globals import *
from src.utils import *


class Game:
    def __init__(self):
        self.game_mode = None
        self.cam_x = 0
        self.cam_y = 0
        self.map = None
        self.game_player = None
        self.uw = 500
        self.uh = 500
        self.debug_mode = False
        self.actor = {"None": []}
        self.unused_actors = {}
        self.attacks = []
        self.health = 100
        self.hurt_timer = 0
        self.frame = []

    def load_sprite(self, sprite):
        sprite_size = sprite.get_size()
        sprite_w = int(sprite_size[0])
        sprite_h = int(sprite_size[1])

        for i in range(0, int(sprite_h / 16)):
            for j in range(0, int(sprite_w / 16)):
                self.frame.append((j * 16, i * 16, 16, 16))

        return self.frame

    def run(self):
        if self.hurt_timer > 0:
            self.hurt_timer -= 1

        draw_text(font, 20, 20, str(round(clock.get_fps(), 1)), RED)


class Map:
    def __init__(self, _a):
        self.actlast = 0
        self.actor = []
        self.actor_empty = {}
        self.a = _a


game = Game()

game_map = Map(5)

solid_tiles = [
    18,
    19,
    21,
    22,
    23,
    24,
    25,
    26,
    27,
    28,
    29,
    30,
    31,
    32,
    33,
    34,
    35,
    36,
    37,
    38,
    39,
    40,
    41,
]

map_dict = [
    [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2],
    [7, 8, 8, 8, 8, 8, 8, 3, 8, 8, 8, 8, 8, 9],
    [7, 8, 3, 8, 8, 8, 3, 8, 8, 8, 10, 15, 15, 16],
    [7, 8, 8, 8, 8, 8, 8, 8, 10, 15, 16, 22, 22, 23],
    [7, 8, 8, 8, 8, 10, 15, 15, 16, 22, 23, 29, 29, 30],
    [14, 15, 15, 15, 15, 16, 22, 22, 23, 29, 30, 36, 36, 37],
    [28, 22, 22, 22, 22, 23, 29, 29, 30, 29, 37, 6, 6, 6],
    [28, 29, 29, 29, 29, 30, 29, 29, 37, 6, 6, 6, 6, 6],
    [35, 36, 36, 36, 36, 37, 6, 6, 6, 6, 6, 6, 6, 6],
]


def new_actor(actor_type, x, y, arr=None, layer="None"):
    na = actor_type(x, y, arr)
    na.id = game_map.actlast
    game.actor[layer].append(na)
    game_map.actlast += 1


def run_actors():
    for i in game.actor.values():
        for j in i:
            j.render()

            if game.debug_mode:
                j.debug()

            j.run()


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
