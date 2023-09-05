HS_FILE = 'hs_text.txt'  # 最高分文件


class GameStats:
    def __init__(self, ai_game):
        """游戏状态类初始化"""
        #  关联ai_game属性
        self.settings = ai_game.settings

        #  游戏状态
        self.ship_left = self.settings.ship_left  # 剩余飞船数
        self.game_active = False  # 游戏活跃状态
        self.score = 0  # 得分
        self.level = 1  # 等级
        self._init_highest_score()  # 最高分

    def reset_stats(self):
        """初始化游戏状态"""
        self.ship_left = self.settings.ship_left  # 初始化剩余飞船数
        self.game_active = False  # 游戏非活跃状态
        self.score = 0  # 得分归零
        self.level = 1  # 初始化等级

    def _init_highest_score(self):
        """初始化最高分"""
        with open(HS_FILE) as hs_file:
            self.highest_score = int(hs_file.read())

    def save_highest_score(self):
        """保存最高分"""
        self._check_highest_score()  # 更新最高分
        with open(HS_FILE, 'w') as hs_file:  # 写入文件
            hs_file.write(str(self.highest_score))

    def _check_highest_score(self):
        """更新最高分"""
        if self.highest_score < self.score:
            self.highest_score = self.score
