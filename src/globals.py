import pygame


pygame.init()


__all__ = [
    "DISP_ICO",
    "DISP_WID",
    "DISP_HEI",
    "DISP_TIT",
    "display",
    "font",
    "FPS",
    "clock",
    "config",
    "UP",
    "DOWN",
    "RIGHT",
    "LEFT",
    "PAUSE",
    "ACCEPT",
    "BACKGROUND",
    "JUMP"
]


########### Window Properties ###########

DISP_WID = 400
DISP_HEI = 240
DISP_TIT = "Dimensional Trouble Temporary Title"
DISP_ICO = "icon/path/still/to/determine"

font = pygame.font.Font("data/fonts/dogica.ttf", 40)

pygame.display.set_caption(DISP_TIT)

display = pygame.display.set_mode(
    (DISP_WID, DISP_HEI), pygame.RESIZABLE | pygame.SCALED
)

FPS = 60
clock = pygame.time.Clock()
game_mode = None

#################### Configurations ######################

config = {
    "key": {
        "up": pygame.K_w,
        "down": pygame.K_s,
        "left": pygame.K_a,
        "right": pygame.K_d,
        "pause": pygame.K_ESCAPE,
        "accept": pygame.K_RETURN,
        "jump": pygame.K_SPACE
    }
}

RIGHT = config["key"]["right"]
LEFT = config["key"]["left"]
UP = config["key"]["up"]
DOWN = config["key"]["down"]
PAUSE = config["key"]["pause"]
ACCEPT = config["key"]["accept"]
JUMP = config["key"]["jump"]

######################## Game Data ########################

game_data = dict(map=None, posX=64, posY=64, cam_x=0, cam_y=0, dialogResponses={})

#################### Colors ######################

BACKGROUND = pygame.Color(120, 150, 130)

