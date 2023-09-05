import pygame
from pygame.sprite import Sprite


class Ship(Sprite):
    def __init__(self, ai_game):
        """飞船类初始化"""
        #  父类Sprite初始化
        super().__init__()

        #  关联ai_game属性
        self.settings = ai_game.settings
        self.screen = ai_game.screen
        self.screen_rect = ai_game.screen.get_rect()

        #  飞船图像
        self.image = pygame.image.load('airline-gfe73b1990_1280.png')  # 获取图像
        self.rect = self.image.get_rect()  # 设置显示位置
        self.rect.midbottom = self.screen_rect.midbottom
        self.x = float(self.rect.centerx)

        #  飞船移动状态
        self.moving_right = False
        self.moving_left = False
        self.ship_speed = self.settings.ship_speed

    def blitme(self):
        """显示飞船图像"""
        self.screen.blit(self.image, self.rect)

    def update(self):
        """更新飞船位置"""
        if self.moving_right:
            self.x += self.ship_speed
        elif self.moving_left:
            self.x -= self.ship_speed

        self.rect.x = self.x  # self.x为float，调整位置幅度更小

    def center_ship(self):
        """使飞船居中"""
        self.rect.midbottom = self.screen_rect.midbottom
        self.x = float(self.rect.x)
