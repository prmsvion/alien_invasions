import sys

from time import  sleep

import pygame
from bullet import Bullet
from alien import Alien


def check_events(score,ai_settings, screen, ship, bullets, stats, play_button,aliens):
    '''响应按键和鼠标事件'''
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, ai_settings, screen, ship, bullets, aliens, stats,score)
        elif event.type == pygame.KEYUP:
            check_keyup_events(event,ship)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(score,stats, play_button, mouse_x, mouse_y,
                              ai_settings,screen,aliens, ship,bullets)

def check_keydown_events(event, ai_settings, screen, ship, bullets, aliens, stats,score):
    '''响应按键'''
    if event.key == pygame.K_RIGHT:
        ship.moving_right = 1
    elif event.key == pygame.K_LEFT:
        ship.moving_left = 1
    elif event.key == pygame.K_SPACE:
        fire_bullet(ai_settings, screen, ship, bullets)
    elif event.key == pygame.K_ESCAPE :
        sys.exit()
    elif event.key == pygame.K_p: #游戏开始，初始化代码拷贝自check_playbutton
        start_game(stats,ai_settings,screen, aliens, ship,bullets)
        # 重置游戏设置
        ai_settings.initialize_dynamic_settings()
        stats.reset_stats()

        # 显示记分板类里的属性，最高分，等级，当前分数，剩余飞船数目
        score.prep_high_score()
        score.prep_level()
        score.prep_score()
        score.prep_ships()

def check_keyup_events(event,ship):
    '''响应松开'''
    if event.key == pygame.K_RIGHT:
        ship.moving_right = 0
    elif event.key == pygame.K_LEFT:
        ship.moving_left = 0

def check_play_button(score,stats, play_button, mouse_x, mouse_y,
                      ai_settings,screen, aliens, ship,bullets):
    '''单击play按钮时启动游戏'''
    if play_button.rect.collidepoint(mouse_x, mouse_y) and not stats.game_active :
        start_game(stats,ai_settings,screen, aliens, ship,bullets)
        #重置游戏设置
        ai_settings.initialize_dynamic_settings()
        stats.reset_stats()

        #显示记分板类里的属性，最高分，等级，当前分数，剩余飞船数目
        score.prep_high_score()
        score.prep_level()
        score.prep_score()
        score.prep_ships()

def start_game(stats,ai_settings,screen, aliens, ship,bullets):
    pygame.mouse.set_visible(0)
    stats.game_active = 1
    bullets.empty()
    aliens.empty()
    # 重新生成外星人并重置飞船位置
    creat_fleet(ai_settings, screen, aliens, ship)
    ship.center_ship()
    # Pause
    sleep(0.5)
    stats.reset_stats()

def screen_update(ai_settings, screen, ship, aliens, bullets, stats, play_button, score):
    '''更新屏幕上图像,并切换到新屏幕'''
    #每次循环重绘屏幕
    screen.fill(ai_settings.bg_color)

    if stats.game_active:
        for bullet in bullets.sprites():
            bullet.draw_bullet()

    ship.blitme()
    aliens.draw(screen)
    score.show_score()

    if not stats.game_active:
        play_button.draw_button()

    #让最近绘制的屏幕可见
    pygame.display.flip()

def bullets_update(bullets,aliens,ai_settings, screen, ship, stats, score):
    '''更新子弹位置，并删除消失子弹'''
    #更新子弹
    bullets.update()
    # 删除消失的子弹
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)
    check_collisions(ai_settings, screen, aliens, bullets, ship, stats, score)

def check_collisions(ai_settings, screen, aliens, bullets, ship, stats, score):
    '''检测子弹与外星人的碰撞'''
    #检测是否有子弹击中外星人
    #删除碰撞的子弹与外星人
    collisions = pygame.sprite.groupcollide(bullets, aliens, 1, 1)
    if collisions :
        #当一个子弹与多个外星人碰撞时，可以正确计分
        for aliens in collisions.values():
            stats.score += ai_settings.alien_points * len(aliens)
            score.prep_score()
            check_high_score(stats, score)
    #检查外星人编组是否为空，是的话调用create重新生成
    if len(aliens) == 0:
        bullets.empty()
        #当消灭所有外星人后,等级提高1
        stats.level += 1
        score.prep_level()

        creat_fleet(ai_settings, screen, aliens, ship)
        ai_settings.increase_speed()


def fire_bullet(ai_settings, screen, ship, bullets):
    # 子弹数目小于设置的值时，创建子弹并将其添加在编组中
    if len(bullets) < ai_settings.bullets_allowed:
        new_bullet = Bullet(ai_settings, screen, ship)
        bullets.add(new_bullet)


def create_alien(ai_settings,screen,aliens,alien_number, row_number):
    alien = Alien(ai_settings, screen)
    alien_width = alien.rect.width
    alien.x = alien_width + 2 * alien_width * alien_number
    alien.rect.x = alien.x
    alien.rect.y = alien.rect.height + 2*alien.rect.height*row_number
    aliens.add(alien)

def creat_fleet(ai_settings, screen, aliens, ship):
    '''创建外星人群'''
    alien = Alien(ai_settings, screen)
    number_aliens_x = get_number_aliens_x(ai_settings, alien.rect.width)
    number_rows = get_number_rows(ai_settings, ship.rect.height, alien.rect.height, )
    #Creat aliens on the first line
    for row_number in range(number_rows):
        for alien_number in range(number_aliens_x):
            #Creat a new alien and put it in the line
            create_alien(ai_settings,screen,aliens,alien_number,row_number)

def get_number_aliens_x(ai_settings, alien_width):
    '''计算每行可容纳的外星人数量'''
    # 外星人之间的间距等于其宽度
    avaliable_space_x = ai_settings.screen_width - 2 * alien_width
    number_aliens_x = int(avaliable_space_x / alien_width / 2)
    return number_aliens_x

def get_number_rows(ai_settings, ship_height, alien_height, ):
    '''计算每行可容纳的外星人数量'''
    # 外星人之间的间距等于其宽度
    avaliable_space_y = ai_settings.screen_height - 3 * alien_height - ship_height
    number_rows = int(avaliable_space_y / alien_height / 2)
    return number_rows

def check_fleet_edges(ai_settings, aliens):
    """有外星人到达边缘时采取相应的措施"""
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(ai_settings, aliens)
            break

def change_fleet_direction(ai_settings, aliens):
    """将整群外星人下移，并改变它们的方向"""
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.fleet_drop_speed
    ai_settings.fleet_direction *= -1

def check_aliens_bottom( ai_settings,aliens, ship, screen,stats,bullets,score):
    '''检查是否有外星人到达屏幕底端'''
    for alien in aliens.sprites():
        screen_rect = screen.get_rect()
        if alien.rect.bottom >= screen_rect.bottom:
            #与撞击飞船时处理相同
            ship_hit(ai_settings,aliens, ship, screen,stats,bullets,score)
            break

def aliens_update(ai_settings,aliens, ship, screen,stats,bullets,score):
    """
    检查是否有外星人位于屏幕边缘，并更新整群外星人的位置
    """
    # 更新外星人
    check_fleet_edges(ai_settings, aliens,)
    aliens.update()
    #检测外星人与飞船的collision
    if pygame.sprite.spritecollideany(ship,aliens):
        ship_hit(ai_settings,aliens, ship, screen,stats,bullets, score)
    #检查外星人是否到达屏幕底端
    check_aliens_bottom(ai_settings,aliens, ship, screen,stats,bullets,score)

def ship_hit(ai_settings,aliens, ship, screen,stats,bullets, score):
    '''响应外星人与飞船的碰撞'''

    #飞船剩余数目减1
    if stats.ship_left > 1:
        stats.ship_left -= 1
        score.prep_ships()
        #清空子弹与外星人
        bullets.empty()
        aliens.empty()
        #重新生成外星人并重置飞船位置
        creat_fleet(ai_settings, screen, aliens, ship)
        ship.center_ship()
        #Pause
        sleep(0.5)
    else:
        stats.game_active = 0
        pygame.mouse.set_visible(1)

def check_high_score(stats, score):
    '''检查最高分'''
    with open('high_score.txt','r+') as f:
        if stats.score > stats.high_score:
            stats.high_score = stats.score
            f.write(str(stats.high_score))
            score.prep_high_score()
