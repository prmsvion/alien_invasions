import sys

import pygame
from pygame.sprite import Group

from scoreboard import ScoreBoard
from button import Button
from game_stats import GameStats
from setting import Settings
from ship import Ship
#from alien import Alien
import  game_functions as gf

def run_game():
    # 初始化游戏并创建一个屏幕对象
    pygame.init()
    ai_settings = Settings()
    screen= pygame.display.set_mode\
    (
        (ai_settings.screen_width, ai_settings.screen_height)
    )
    pygame.display.set_caption("Alien Invasion")
    #创建GameStats实例用于跟踪统计信息
    stats = GameStats(ai_settings)
    #创建一艘飞船
    ship = Ship(ai_settings,screen,)
    #创建一个编组存储子弹
    bullets = Group()
    #创建一个外星人
    aliens = Group()
    #生成外星人编组
    gf.creat_fleet(ai_settings, screen, aliens, ship)
    #创建开始按钮
    play_button = Button( ai_settings, screen, 'play')
    #创建记分牌
    score = ScoreBoard(screen, ai_settings, stats)

    #开始游戏的主循环
    while True:
        #监视键盘和鼠标事件
        gf.check_events(score,ai_settings, screen, ship, bullets, stats, play_button,aliens)
        # 游戏活跃时更新飞船与子弹
        if stats.game_active == 1:
            ship.update()
            gf.bullets_update(bullets,aliens,ai_settings, screen, ship, stats, score)
            gf.aliens_update(ai_settings,aliens, ship, screen,stats,bullets,score)
        # 每次循环重新绘制屏幕,保存最近绘制的屏幕可见
        gf.screen_update(ai_settings, screen, ship, aliens, bullets,stats,
                         play_button, score)

run_game()