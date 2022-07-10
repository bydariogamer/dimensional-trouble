from operator import attrgetter
import sys
from itertools import cycle

import pygame

from src.globals import FPS, BACKGROUND, DISP_WID, DISP_HEI
from src.utils import text, load_json

from src.button import Button


class Menu:
    BACKGROUND = BACKGROUND

    def __init__(self, screen: pygame.Surface, clock: pygame.time.Clock, buttons):
        self.screen = screen
        self.clock = clock
        self.buttons = buttons
        self.dt = 0
        self.running = True

    def handle_events(self, events=None):
        if events is None:
            events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                sys.exit()

            for button in sorted(self.buttons, key=attrgetter("rect.right")):
                button.handle_event(event)

    def draw(self):
        self.screen.fill(self.BACKGROUND)
        for button in sorted(self.buttons, key=attrgetter("rect.left")):
            button.draw(self.screen)
        pygame.display.update()

    def update(self):
        self.dt = self.clock.tick(FPS)

    def loop(self):
        while self.running:
            self.handle_events()
            self.draw()
            self.update()

    def stop(self):
        self.running = False


class MainMenu(Menu):
    TITLE = text("EVOLUTIONIST", (30, 100, 30), 150)
    AUTHORS = text("by Emc235 & bydariogamer", (250, 40, 40), 30)

    def __init__(
        self,
        screen: pygame.Surface,
        clock: pygame.time.Clock,
        buttons: Button = None,
    ):
        if buttons is None:
            buttons = [
                Button(
                    (0, H / 2, 600, 100),
                    color=(100, 100, 250),
                    label="PLAY",
                    on_click=[lambda _: Game(screen, clock).run()],
                ),
                Button(
                    (0, H / 2 + 130, 600, 100),
                    color=(100, 100, 250),
                    label="EXIT",
                    on_click=[Button.put_exit],
                ),
            ]
        super().__init__(screen, clock, buttons)
        sheet = SpriteSheet(PATHS.SPRITESHEETS / "slime-green-right.png")
        data = load_json(PATHS.SPRITESHEETS / "slime-green-right.json")
        frames = [
            pygame.transform.scale(
                sheet.clip(data["frames"][str(i)]), (300, 300)
            ).convert_alpha()
            for i in range(1, 9)
        ]
        self.animation = cycle(frames)
        self.animation_limiter = cycle(range(4))
        self.last_anim = next(self.animation)

    def draw(self):
        self.screen.fill(self.BACKGROUND)
        self.screen.blit(self.TITLE, (15, 50))
        self.screen.blit(self.AUTHORS, (50, 230))
        if not next(self.animation_limiter):
            self.last_anim = next(self.animation)
        self.screen.blit(self.last_anim, (800, 250))
        for button in self.buttons:
            button.draw(self.screen)
        pygame.display.update()
