import pygame.font
from pygame.sprite import Group

from ship import Ship

class ScoreBoard():
    '''显示得分的类'''

    def __init__(self, screen, ai_settings, stats):
        self.screen = screen
        self.screen_rect = self.screen.get_rect()  # 自己修改的
        self.ai_settings = ai_settings
        self.stats = stats

        self.text_color = 30,30,30
        self.font = pygame.font.SysFont(None, 48)

        self.prep_score()
        self.prep_high_score()
        self.prep_level()
        self.prep_ships()

    def prep_score(self):
        '''将表示得分的文本转变成图像'''

        #round（number, n）n表示精确到小数后点几位，n为负时表示圆整到10，100 ...
        rounded_score = int(round(self.stats.score, -1))
        score_str = '{:,}'.format(rounded_score)
        self.score_image = self.font.render(score_str, 1, self.text_color, self.ai_settings.bg_color)

        #将得分放在屏幕右上角
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - 20
        self.score_rect.top = 15

    def prep_high_score(self):
        '''将最高分的文本形式转变为图像放在右上角'''
        high_score = int(round(self.stats.high_score, -1))
        high_score_str = '{:,}'.format(high_score)
        self.high_score_image = self.font.render(high_score_str, 1, self.text_color, self.ai_settings.bg_color)

        # 将得分放在屏幕右上角
        self.high_score_rect = self.high_score_image.get_rect()
        self.high_score_rect.centerx = self.screen_rect.centerx
        self.high_score_rect.top = self.score_rect.top

    def prep_level(self):
        '''将等级由文本形式转变为图像形式'''
        self.level_image = self.font.render(str(self.stats.level), 1, self.text_color,
                                            self.ai_settings.bg_color)

        # 将等级放在得分下面
        self.level_rect = self.level_image.get_rect()
        self.level_rect.right = self.score_rect.right
        self.level_rect.top = self.score_rect.bottom + 8

    def prep_ships(self,):
        '''显示剩余飞船数目'''
        self.ships = Group()
        for ship_number in range(self.stats.ship_left):
            ship = Ship(self.ai_settings, self.screen)
            ship.rect.x = 10 + ship_number * ship.rect.width
            ship.rect.y = 10
            self.ships.add(ship)

    def show_score(self):
        '''在屏幕上显示得分'''
        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.high_score_image, self.high_score_rect)
        self.screen.blit(self.level_image, self.level_rect)
        self.ships.draw(self.screen)