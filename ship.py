import pygame
from pygame.sprite import Sprite

class Ship( Sprite ):

    def __init__(self,ai_settings,screen):
        '''初始化飞船并设置其位置'''
        super().__init__()
        self.screen = screen
        self.ai_settings = ai_settings

        #加载飞船图像并获取其外接矩形
        self.image = pygame.image.load('images\ship.bmp')
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()

        #将每艘飞船放在屏幕底部中央
        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom

        #飞船center属性中存储小数值
        self.center = float (self.rect.centerx )

        #飞船移动标志
        self.moving_right = 0
        self.moving_left = 0


    def update(self):
        '''根据标志位调整飞船位置'''
        #更新飞船的center值，而不是rect
        if self.moving_right and self.rect.right < self.screen_rect.right :
            self.center += self.ai_settings.ship_speed_factor
        if self.moving_left and self.rect.left > 0 :
            self.center -= self.ai_settings.ship_speed_factor

        #根据center属性更新rect对象
        self.rect.centerx = self.center

    def blitme(self):
        '''指定位置绘制飞船'''
        self.screen.blit(self.image, self.rect)

    def center_ship(self):
        self.center = self.screen_rect.centerx
        #self.rect.bottom = self.screen_rect.bottom


