import pygame
from pygame.sprite import Sprite


class Bullet(Sprite):
    def __init__(self, ai_game):
        """子弹类初始化"""
        #  父类Sprite初始化
        super().__init__()

        #  关联ai_game属性
        self.screen = ai_game.screen
        self.settings = ai_game.settings

        #  子弹图像
        self.color = self.settings.bullet_color  # 子弹颜色
        self.rect = pygame.Rect(0, 0, self.settings.bullet_width,
                                self.settings.bullet_length)  # 子弹位置
        self.rect.midtop = ai_game.ship.rect.midtop  # 关联飞船位置

        #  子弹移动
        self.y = float(self.rect.y)
        self.bullet_speed = self.settings.bullet_speed

    def update(self):
        """更新子弹位置"""
        self.y -= self.bullet_speed
        self.rect.y = self.y

    def draw_bullet(self):
        """绘制子弹"""
        pygame.draw.rect(self.screen, self.settings.bullet_color, self.rect)
