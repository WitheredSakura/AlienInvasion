import pygame
import random
from pygame.sprite import Sprite


class Alien(Sprite):
    def __init__(self, ai_game):
        """初始化外星人类"""
        #  父类Sprite初始化
        super().__init__()

        #  关联ai_game属性
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()
        self.settings = ai_game.settings

        #  外星人图像
        self.image = pygame.image.load('ufo-g36b355dbc_640.png')
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(
            self.rect.width,
            self.settings.screen_width - self.rect.width)

        #  移动
        self.rect.y = 0
        self.y = float(self.rect.y)
        self.alien_speed = self.settings.alien_speed

    def update(self):
        """更新外星人位置"""
        self.y += self.alien_speed
        self.rect.y = self.y  # self.y为float，调整位置幅度更小

    def blitme(self):
        """显示外星人图像"""
        self.screen.blit(self.image, self.rect)
