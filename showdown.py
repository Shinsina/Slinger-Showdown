import pygame
import pygame.gfxdraw
import sys

from racecar import Racecar
from scoreboard import Scoreboard


class Showdown:

    # Main class to manage game assets and behaviorm

    def __init__(self):
        # Initialization of base elements for game
        pygame.init()
        self.image = pygame.image.load('track.png')
        pygame.mixer.music.load('BackgroundMusic.mp3')
        pygame.mixer.music.play(-1, 0.0)
        WINDOWWIDTH = self.image.get_rect().width
        WINDOWHEIGHT = self.image.get_rect().height
        self.screen = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))

        # Setting up elements related to the timer
        self.clock = pygame.time.Clock()
        self.timer = 30
        self.dt = 0
        self.font = pygame.font.Font(None, 40)

        # Variable to tell if the game is currently active
        self.game_active = False

        # Variable for if the player has a continue they can use
        self.continue_allowed = True

        # Audio objects for the boost sound
        self.boostchannel = pygame.mixer.Channel(3)
        self.boostsound = pygame.mixer.Sound('Boost.mp3')

        # Setting the window caption to the game title
        pygame.display.set_caption("Slinger Showdown")

        # Setting references to game objects and pushing the first frame to the screen
        self.racecar = Racecar(self)
        self.sb = Scoreboard(self)
        self._update_screen()

    def _update_screen(self):
        # Redraw the screen during each pass through the loop
        # Make the most recently drawn screen visible
        # See each method for details as to what they do
        self.racecar.blitme()
        self.sb.prep_score()
        self.sb.prep_timeboosts()
        self.sb.prep_lapcount()
        self.sb.show_score()
        self._update_timer()
        pygame.display.flip()

    def _update_timer(self):
        # Handles events based on current value of the timer
        if self.timer <= 0:
            self.txt = self.font.render(
                'Game Over', True, (0, 0, 0), (230, 230, 230))
            self.screen.blit(self.txt, (450, 335))
            self.game_active = False
            pygame.mixer.music.stop()
            if self.racecar.lapcount > 0 and self.continue_allowed == True:
                self.txt = self.font.render(
                    'Continue?', True, (0, 0, 0), (230, 230, 230))
                self.screen.blit(self.txt, (450, 335))
        else:
            self.txt = self.font.render(
                'Timer: ' + str(round(self.timer, 2)), True, (0, 0, 0), (230, 230, 230))
            self.screen.blit(self.txt, (450, 335))

    def _check_events(self):
        # Respond to keypresses and mouse events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)

    def _check_keydown_events(self, event):
        # Handles events for when a particular key is hit given respective conditions for each

        # Gameplay Controls
        if event.key == pygame.K_w:
            if self.game_active:
                self.racecar.is_moving = True
                self.racecar.chan1.play(self.racecar.enginenoise)
        elif event.key == pygame.K_q:
            sys.exit()
        elif event.key == pygame.K_ESCAPE:
            if self.game_active:
                self.game_active = False
                pygame.mixer.music.stop()
            elif self.game_active == False:
                self.game_active = True
                pygame.mixer.music.play(-1, 0.0)
        elif event.key == pygame.K_SPACE:
            if (self.game_active == True and self.racecar.is_moving == False):
                if self.racecar.timeboosts > 0:
                    self.racecar.timeboosts -= 1
                    self.boostchannel.play(self.boostsound)
                    self.timer += 1
        elif event.key == pygame.K_RETURN:
            if (self.game_active == False and self.timer <= 0 and self.continue_allowed == True):
                self.timer = (self.racecar.lapcount) * 5
                self.racecar.lapcount = 0
                self.racecar.timeboosts = 0
                self.continue_allowed = False

        # Audio Controls
        elif event.key == pygame.K_e:
            if self.racecar.chan1.get_volume() > 0:
                self.racecar.chan1.set_volume(0)
            elif self.racecar.chan1.get_volume() == 0:
                self.racecar.chan1.set_volume(1)
        elif event.key == pygame.K_m:
            if pygame.mixer.music.get_volume() > 0:
                pygame.mixer.music.set_volume(0)
            elif pygame.mixer.music.get_volume() == 0:
                pygame.mixer.music.set_volume(1)
        elif event.key == pygame.K_c:
            if self.racecar.chan2.get_volume() > 0:
                self.racecar.chan2.set_volume(0)
            elif self.racecar.chan2.get_volume() == 0:
                self.racecar.chan2.set_volume(1)
        elif event.key == pygame.K_b:
            if self.boostchannel.get_volume() > 0:
                self.boostchannel.set_volume(0)
            elif self.boostchannel.get_volume() == 0:
                self.boostchannel.set_volume(1)

    def _check_keyup_events(self, event):
        # Check when a key is released
        if event.key == pygame.K_w:
            self.racecar.is_moving = False

    def run_game(self):
        # Start the main loop for the game
        while True:
            # Watch for keyboard and mouse events
            self.screen.blit(self.image, (0, 0))
            self.racecar.blitme()
            self._check_events()
            if self.game_active:
                self.racecar.update()
                self.timer -= self.dt
            self._update_screen()
            self.dt = self.clock.tick(150) / 1000


if __name__ == "__main__":
    sd = Showdown()
    sd.run_game()
