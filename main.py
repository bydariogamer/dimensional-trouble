import pygame

from src.actors import *
from src.game import *
from src.globals import *


def start_game():
    game.game_mode = game_play
    p = GameMap("res/map/test_for_PGE.json")
    p.draw_tiles()

    new_actor(Tux, 160, 160, None, "actorlayer")

    game.cam_x = DISP_WID / 2 - 16
    game.cam_y = DISP_HEI / 2 - 16

    #new_actor(Slime, 300, 250, None, "actorlayer")

    running = True

    while running:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == JUMP:
                    game.game_player.jump()
                    # print("event jump")

        display.fill(BLACK)
        game.game_mode()
        game.run()

        pygame.display.update()


if __name__ == "__main__":
    start_game()
