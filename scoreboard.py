import pygame.font
import pygame.sprite
from ship import Ship


class ScoreBoard:
    def __init__(self, ai_game):
        """计分板类初始化"""
        #  关联ai_game属性
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()
        self.settings = ai_game.settings
        self.game_stats = ai_game.game_stats

        #  字体图像
        self.text_color = self.settings.score_text_color  # 字体颜色
        self.font = pygame.font.Font(self.settings.score_font_name,
                                     self.settings.score_font_size)  # 得分字体
        self.highest_score_font = pygame.font.Font(
            self.settings.score_font_name,
            self.settings.highest_score_font_size
        )  # 最高分字体
        self._pre_score()  # 生成得分图像
        self._pre_highest_score()  # 生成最高分图像

        #  飞船
        self.ships = pygame.sprite.Group()  # 初始化飞船组
        self._pre_ships(ai_game)

    def _pre_score(self):
        """生成得分图像"""
        score_str = str(self.game_stats.score)  # 获取得分
        self.score_image = self.font.render(
            score_str, True, self.text_color, self.settings.bg_color
        )  # 生成得分图像

        #  设置得分图像位置
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - 20
        self.score_rect.top = 20

    def _pre_highest_score(self):
        """生成最高分图像"""
        highest_score_str = str(self.game_stats.highest_score)  # 获取最高分
        self.highest_score_image = self.font.render(
            highest_score_str, True, self.text_color, self.settings.bg_color
        )  # 生成最高分图像

        #  设置最高分图像位置
        self.highest_score_rect = self.highest_score_image.get_rect()
        self.highest_score_rect.midtop = self.screen_rect.midtop
        self.highest_score_rect.top = 20

    def show_score(self):
        """显示得分"""
        self._pre_score()  # 重新生成得分图像
        self.screen.blit(self.score_image, self.score_rect)  # 显示得分

    def show_highest_score(self):
        """显示最高分"""
        self.screen.blit(self.highest_score_image, self.highest_score_rect)

    def update_highset_score_image(self):
        """重新生成最高分图像"""
        self._pre_highest_score()

    def _pre_ships(self, ai_game):
        """准备飞船组"""
        self.ships.empty()
        for ship_num in range(self.game_stats.ship_left):  # 根据剩余飞船数创建飞船
            ship = Ship(ai_game)  # 创建新飞船
            ship.rect.left = self.screen_rect.left + ship_num * ship.rect.width
            ship.rect.top = self.screen_rect.top  # 设置飞船位置
            self.ships.add(ship)  # 加入飞船组

    def update_ships(self, ai_game):
        """更新飞船组"""
        self._pre_ships(ai_game)  # 重新准备飞船组

    def show_ships(self):
        """显示飞船组"""
        for ship in self.ships.sprites():
            ship.blitme()
