import pygame.font
from pygame.sprite import Group

from racecar import Racecar


class Scoreboard:
    # A class to report scoring information

    def __init__(self, sd_game):
        # Initialize scorekeeping attributes
        self.sd_game = sd_game
        self.screen = sd_game.screen
        self.screen_rect = self.screen.get_rect()

        # Font settings for scoring information
        self.text_color = (30, 30, 30)
        self.font = pygame.font.SysFont(None, 48)

        # Prepare the initial score image
        self.prep_score()
        self.prep_timeboosts()
        self.prep_lapcount()

    def prep_score(self):
        # Turn the score into a rendered image
        rounded_score = self.sd_game.racecar.distancetotal
        # print(rounded_score)
        score_str = 'Score: ' + "{:,}".format(rounded_score)
        self.score_image = self.font.render(
            score_str, True, self.text_color, (230, 230, 230))

        # Display the score at the top right of the screen
        self.score_rect = self.score_image.get_rect()
        self.score_rect.center = self.screen_rect.center
        self.score_rect.top = 250

    def prep_timeboosts(self):
        # Turn the timeboost count into a rendered image
        timeboosts_total = 'Boosts: ' + str(self.sd_game.racecar.timeboosts)
        self.tb_image = self.font.render(
            timeboosts_total, True, self.text_color, (230, 230, 230))

        # Position the count below the score
        self.tb_rect = self.tb_image.get_rect()
        self.tb_rect.right = self.score_rect.right
        self.tb_rect.top = self.score_rect.bottom + 10

    def prep_lapcount(self):
        lapcount = 'Lap Count:' + str(self.sd_game.racecar.lapcount)
        self.lc_image = self.font.render(
            lapcount, True, self.text_color, (230, 230, 230))

        # Position the count below other count
        self.lc_rect = self.lc_image.get_rect()
        self.lc_rect.right = self.score_rect.right
        self.lc_rect.top = self.tb_rect.bottom + 50

    def show_score(self):
        # Draw score and timeboost count on screen
        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.tb_image, self.tb_rect)
        self.screen.blit(self.lc_image, self.lc_rect)
