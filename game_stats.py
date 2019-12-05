class GameStats():
    '''跟踪游戏的统计信息 '''

    def __init__(self,ai_settings):
        self.ai_settings = ai_settings
        self.game_active = 0
        self.reset_stats()
        self.load_high_score()
        #self.high_score = 0

    def reset_stats(self):
        '''初始化游戏过程中可能变化的信息'''
        self.ship_left = self.ai_settings.ship_limit
        self.score = 0
        self.level = 1

    def load_high_score(self):
        with open('high_score.txt', 'r') as f:
            if f.read().rstrip():
                #在读取文件之后，一定一定记得在下次读取前将指针放在文件的开始位置，f.seek()
                f.seek(0)
                self.high_score = f.read()
                #debug使用
                try:
                    self.high_score = int(self.high_score.strip())
                except ValueError:
                    print(self.high_score+'!!!')
                    self.high_score = 0
            else:
                self.high_score = 0
