class Settings():
    '''存储游戏所有设置的一个类'''

    def __init__(self):
        '''游戏初始化设置'''
        #屏幕相关设置
        self.screen_width = 960
        self.screen_height = 600
        self.bg_color=(230,230,230)

        #存储飞船属性
        #self.ship_speed_factor = 1.5
        self.ship_limit = 1

        #存储子弹属性设置
        self.bullet_width = 222
        self.bullet_height = 12
        self.bullet_color = 60,60,60
        #self.bullet_speed_factor = 1.5
        self.bullets_allowed = 3

        self.fleet_drop_speed = 15
        #外星人移动加速系数
        self.speedup_scale = 1.1
        #得分增加的系数
        self.score_scale = 1.5

        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        '''动态属性初始化函数，集中放置随游戏进程改变的参数的初始值，用于重启游戏时进行初始化'''
        self.alien_speed_factor = 1
        self.ship_speed_factor = 1.5
        self.bullet_speed_factor = 1.5
        #外星人初始移动方向，1表示向右，-1表示左移
        self.fleet_direction = 1
        #消灭一个外星人的奖励分数
        self.alien_points = 50

    def increase_speed(self):
        self.alien_speed_factor *= self.speedup_scale
        self.ship_speed_factor *= self.speedup_scale
        self.bullet_speed_factor *= self.speedup_scale
        self.alien_points = int(self.score_scale * self.alien_points)
        #print(self.alien_points)