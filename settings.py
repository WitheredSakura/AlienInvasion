class Settings:
    def __init__(self):
        """静态设置"""
        #  屏幕设置
        self.screen_width = 1000  # 屏幕宽度
        self.screen_height = 500  # 屏幕高度
        self.bg_color = (230, 230, 230)  # 背景颜色

        #  游戏设置
        #  1.飞船
        self.ship_left = 3  # 飞船初始生命数
        self.init_ship_speed = 0.3  # 飞船初始速度

        # 2.子弹
        self.bullet_width = 3  # 子弹宽度
        self.bullet_length = 15  # 子弹长度
        self.bullet_color = (60, 60, 60)  # 子弹颜色
        self.init_bullet_speed = 0.5  # 子弹初始速度

        # 3.外星人
        self.create_gap = 0.25  # 外星人生成间隔
        self.init_alien_speed = 0.15  # 外星人初始速度
        self.init_alien_scores = 10  # 外星人初始分数

        # 4.加速设置
        self.init_speedup_scale = float(1.1)  # 移动加速
        self.init_scores_scale = float(1.5)  # 得分加速

        #  按钮设置
        self.button_width = 200  # 按钮宽度
        self.button_height = 50  # 按钮高度
        self.text_color = (255, 255, 255)  # 字体颜色
        self.button_color = (0, 255, 0)  # 按钮颜色
        self.font_size = 48  # 字体大小
        self.font_name = None  # 字体名称

        #  得分字体设置
        self.score_text_color = (30, 30, 30)
        self.score_font_name = None
        self.score_font_size = 48
        self.highest_score_font_size = 48

        """动态设置"""
        self.alien_speed = self.init_alien_speed  # 外星人速度
        self.alien_scores = self.init_alien_scores  # 外星人分数
        self.bullet_speed = self.init_bullet_speed  # 子弹速度
        self.ship_speed = self.init_ship_speed  # 飞船速度
        self.speedup_scale = self.init_speedup_scale  # 加速速度
        self.scores_scale = self.init_scores_scale  # 加速得分
        self.level = 1  # 等级

    def initialize_dynamic_settings(self):
        """初始化动态设置"""
        self.alien_speed = self.init_alien_speed
        self.alien_scores = self.init_alien_scores
        self.bullet_speed = self.init_bullet_speed
        self.ship_speed = self.init_ship_speed
        self.speedup_scale = self.init_speedup_scale

    def increase_speed(self):
        """加速"""
        self.alien_speed *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale
        self.ship_speed *= self.speedup_scale
        self.alien_scores = int(self.alien_scores * self.scores_scale)
