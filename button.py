import pygame.font
class Button():
    def __init__(self, ai_settings, screen, msg,  ):
        '''初始化按钮属性'''
        self.screen = screen
        self.screen_rect = self.screen.get_rect()#自己修改的

        # 设置按钮属性
        self.width = 200
        self.height = 50
        self.button_color = 0,255,0
        self.text_color = 255,255,255
        self.font = pygame.font.SysFont(None, 48)
        #创建按钮对应的rect
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = self.screen_rect.center
        #创建按钮标签
        self.prep_msg(msg)

    def prep_msg(self, msg):
        self.msg_image = self.font.render(msg, 1, self.text_color, self.button_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center

    def draw_button(self):
        self.screen.fill(self.button_color, self.rect)
        self.screen.blit(self.msg_image, self.msg_image_rect)