import pygame
from pygame.sprite import Sprite

class Alien(Sprite):
    def __init__(self,ai_settings,screen):
        '''初始化外星人并设置其位置'''
        super().__init__()
        self.screen = screen
        self.ai_settings = ai_settings

        # 加载外星人图像并获取其外接矩形
        self.image = pygame.image.load(r'images\alien.bmp')
        self.rect = self.image.get_rect()

        #设置外星人初始位置
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        #存储外星人准确位置（小数)
        self.x = float(self.rect.x)

    def check_edges(self):
        '''外星人位于屏幕边缘时,返回1'''
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right:
            return 1
        elif self.rect.left <= 0:
            return 1

    def update(self, ):
        '''向左或右移动外星人'''
        self.x += self.ai_settings.alien_speed_factor * self.ai_settings.fleet_direction
        self.rect.x = self.x

    def blitme(self):
        '''指定位置绘制👽'''
        self.screen.blit(self.image, self.rect)