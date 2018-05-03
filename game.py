import logging
import pygame
import sys

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)

# Konstanter
FPS = 60
SCREEN_SIZE = (1200, 1000)
CAPTION = "Nice god"

COLOR = {'ship': pygame.Color('#FF00FF'),
         'ship_fill': pygame.Color('#FF00FF'),
         'bg': pygame.Color('#FFFF00'),
         'thruster': pygame.Color('#008000'),
         'colorman': pygame.Color('#008000'),
         'bg_pause': pygame.Color('#a142f4'),
         'text_color': pygame.Color('#000705'),

}

# Game states
STATE_PREGAME = 1
STATE_RUNNING = 2
STATE_GAMEOVER = 3

class Controller():
    """Game controller."""

    def __init__(self):
        """Initialize game controller."""
        self.fps = FPS

        pygame.init()
        self.screen = pygame.display.set_mode(SCREEN_SIZE)
        pygame.display.set_caption(CAPTION)
        self.clock = pygame.time.Clock()

        self.player = Player(self.screen)

        # Initialize game state
        self.game_state = STATE_PREGAME
        self.Large_text = pygame.font.SysFont("", 115)


    def run(self):
        """Main game loop."""
        while True:
            # Hantera event
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    # ALT + F4 or icon in upper right corner.
                    self.quit()

                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    # Escape key pressed.
                    self.quit()

                if self.game_state == STATE_PREGAME:
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        self.game_state = STATE_RUNNING

                if self.game_state == STATE_RUNNING:
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_w:
                        self.player.engine_on()

                    if event.type == pygame.KEYUP and event.key == pygame.K_w:
                        self.player.engine_off()

                    if event.type == pygame.KEYDOWN and event.key == pygame.K_a:
                        self.player.right_thruster_on()

                    if event.type == pygame.KEYUP and event.key == pygame.K_a:
                        self.player.right_thruster_off()

                    if event.type == pygame.KEYDOWN and event.key == pygame.K_d:
                        self.player.left_thruster_on()

                    if event.type == pygame.KEYUP and event.key == pygame.K_d:
                        self.player.left_thruster_off()

            # Hantera speltillstånd
            if self.game_state == STATE_PREGAME:
                pass

            if self.game_state == STATE_RUNNING:
                self.player.tick()

                if self.player.y > SCREEN_SIZE[1] - 10 or self.player.y < 10:
#                    logger.debug('OUT OF BOUNDS!')
                    self.game_state = STATE_GAMEOVER

                self.screen.fill(COLOR['bg'])
                self.player.draw()

            if self.game_state == STATE_GAMEOVER:
                self.quit()  # Gör något bättre.
            if self.game_state == STATE_PREGAME:
                self.screen.fill(COLOR['bg_pause'])
                text = self.Large_text.render("Nacho", True, COLOR['text_color'])
                pos = (SCREEN_SIZE[0] / 2 - text.get_width() / 2,
                        SCREEN_SIZE[1] / 2 - text.get_height() / 2)
                self.screen.blit(text, pos)

            pygame.display.flip()

            self.clock.tick(self.fps)

    def quit(self):
        logging.info('You are a doer of the losing, noob')
        pygame.quit()
        sys.exit()


class Player():
    def __init__(self, screen):
        self.x = SCREEN_SIZE[0] / 2
        self.y = SCREEN_SIZE[1] / 2
        self.screen = screen
        self.engine = False
        self.left_thruster = False
        self.right_thruster = False
        self.x_speed = 0
        self.y_speed = 0
        self.gravity = 1
        self.fuel = 1195

    def draw(self):
        surface = pygame.Surface((2100, 2100))
        surface.fill(COLOR['bg'])
#        pygame.draw.line(surface, COLOR['ship'], (10, 0), (15, 20))
#        pygame.draw.line(surface, COLOR['ship'], (10, 0), (5, 20))
        pygame.draw.polygon(surface, COLOR['ship_fill'], ((10, 0), (15, 15), (5, 15)), 0)
        pygame.draw.polygon(surface, COLOR['ship'], ((10, 0), (15, 15), (5, 15)), 1)

        if self.engine:
            pygame.draw.polygon(surface, COLOR['thruster'], ((13, 16), (10, 19), (7, 16)), 0)

        if self.left_thruster:
            pygame.draw.polygon(surface, COLOR['thruster'], ((6, 12), (5, 14), (2, 13), (6, 12), 0))

        if self.right_thruster:
            pygame.draw.polygon(surface, COLOR['thruster'], ((14, 12), (15, 14), (18, 13), (14, 12), 0))

        pygame.draw.lines(self.screen, COLOR['colorman'], 0, [(5,30), (self.fuel, 30)], 40)

        self.screen.blit(surface, (self.x - 25, self.y - 10))

    def tick(self):
        # -- Y-axis control
        if self.engine:
            self.y_speed -= 0.03
        else:
            self.y_speed += 0.01

        self.y = self.y + self.y_speed + self.gravity

        # -- X-axis control
        if self.left_thruster:
            self.x_speed += 0.01

        if self.right_thruster:
            self.x_speed -= 0.01

        self.x_speed = self.x_speed * 0.99

        self.x = self.x + self.x_speed
        if self.engine == True:
            self.fuel -= 2.50

        if self.fuel <0:
            self.engine = False


    def engine_on(self):
        self.engine = True

    def engine_off(self):
        self.engine = False

    def left_thruster_on(self):
        self.left_thruster = True

    def left_thruster_off(self):
        self.left_thruster = False

    def right_thruster_on(self):
        self.right_thruster = True

    def right_thruster_off(self):
        self.right_thruster = False

if __name__ == "__main__":
    logger.info('Starting...')
    c = Controller()
    c.run()
