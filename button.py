import pygame.font


class Button:
    def __init__(self, ai_game, msg):
        """按钮类初始化"""
        #  关联ai_game属性
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()
        self.settings = ai_game.settings

        #  按钮图像
        self.width = self.settings.button_width  # 按钮宽度设置
        self.height = self.settings.button_height  # 按钮高度设置
        self.button_color = self.settings.button_color  # 按钮颜色设置

        #  按钮位置
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.midbottom = self.screen_rect.center

        #  文本图像
        self.font = pygame.font.Font(self.settings.font_name,
                                     self.settings.font_size)  # 字体设置
        self.text_color = self.settings.text_color  # 文字颜色设置
        self._prepare_msg(msg)  # 生成文字图像

    def _prepare_msg(self, msg):
        """生成文字图像"""
        self.msg_image = self.font.render(msg, True, self.text_color,
                                          self.button_color)  # 生成文字图像
        self.msg_image_rect = self.msg_image.get_rect()  # 设置文字图像位置
        self.msg_image_rect.center = self.rect.center

    def draw_button(self):
        """绘制按钮"""
        self.screen.fill(self.button_color, self.rect)  # 填充按钮区域颜色
        self.screen.blit(self.msg_image, self.msg_image_rect)  # 生成文字图像
