import sys
import pygame
import threading
from settings import Settings
from ship import Ship
from bullet import Bullet
from alien import Alien
from time import sleep
from game_stats import GameStats
from button import Button
from scoreboard import ScoreBoard


class AlienInvasion:
    def __init__(self):
        """游戏初始化"""
        pygame.init()  # pygame初始化
        self.settings = Settings()  # 设置初始化
        self.game_stats = GameStats(self)  # 游戏状态初始化

        #  屏幕
        self.screen = pygame.display.set_mode(
            (self.settings.screen_width, self.settings.screen_height)
        )  # 屏幕初始化
        self.bg_color = self.settings.bg_color  # 背景颜色初始化
        pygame.display.set_caption("Alien Invasion")  # 字幕

        #  飞船
        self.ship = Ship(self)

        #  子弹
        self.bullets = pygame.sprite.Group()

        #  外星人
        self.aliens = pygame.sprite.Group()
        self.create_cancel = True

        #  按钮
        self.play_button = Button(self, 'PLAY')

        #  计分板
        self.score_board = ScoreBoard(self)

    def _check_events_down(self, event):
        """检测按键事件"""
        if event.key == pygame.K_RIGHT:  # 飞船右移
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:  # 飞船左移
            self.ship.moving_left = True
        elif event.key == pygame.K_SPACE and\
                self.game_stats.game_active:  # 开火
            self._fire_bullet()
        elif event.key == pygame.K_q:  # 退出
            self.create_cancel = True  # 终止外星人生成子线程
            sys.exit()  # 结束主线程

    def _fire_bullet(self):
        """开火"""
        new_bullet = Bullet(self)  # 创建新子弹
        self.bullets.add(new_bullet)  # 添加到子弹组

    def _check_events_up(self, event):
        """检测松键事件"""
        if event.key == pygame.K_RIGHT:  # 飞船停止右移
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:  # 飞船停止左移
            self.ship.moving_left = False

    def _check_collision(self):
        """检测碰撞"""
        self._bullet_alien_collision()  # 子弹击中外星人
        self._ship_alien_collision()  # 飞船与外星人碰撞

    def _bullet_alien_collision(self):
        """子弹击中外星人"""
        #  删除发生碰撞的子弹和外星人
        collision = pygame.sprite.groupcollide(
            self.bullets, self.aliens, True, True
        )
        #  发生碰撞
        if collision:
            #  得分
            self.game_stats.score += self.settings.alien_scores
            #  升级
            if self.game_stats.level * 100 < self.game_stats.score:
                self.game_stats.level += 1  # 升级
                self.settings.increase_speed()  # 游戏速度加快

    def _ship_alien_collision(self):
        """飞船与外星人碰撞"""
        #  检测飞船与外星人碰撞
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            #  终止外星人生成子线程
            self.create_cancel = True  # 阻止子线程递归调用
            sleep(1)  # 等待子线程终止

            self.game_stats.ship_left -= 1  # 飞船生命-1
            self.score_board.update_ships(self)  # 飞船组更新
            self.ship.center_ship()  # 飞船居中
            self.aliens.empty()  # 清空外星人
            self.bullets.empty()  # 清空子弹

            #  判断游戏是否继续
            if self.game_stats.ship_left > 0:  # 游戏继续
                #  重新启用外星人生成子线程
                self.create_cancel = False
                self._create_fleet()
            else:  # 游戏终止
                self.game_stats.save_highest_score()  # 保存最高分
                self.score_board.update_highset_score_image()  # 更新最高分图片
                self.game_stats.reset_stats()  # 游戏状态初始化
                self.settings.initialize_dynamic_settings()  # 动态设置初始化
                self.score_board.update_ships(self)  # 飞船组初始化
                pygame.mouse.set_visible(True)  # 鼠标可见

    def _check_play_button(self, mos_pos):
        """检测开始游戏按钮"""
        #  检测鼠标点击
        if self.play_button.rect.collidepoint(mos_pos):
            self.game_stats.game_active = True  # 游戏设置为活跃状态
            self.create_cancel = False  # 启用外星人生成子线程
            self._create_fleet()
            pygame.mouse.set_visible(False)  # 鼠标不可见

    def _check_events(self):
        """事件检测"""
        for event in pygame.event.get():  # 获取所有事件

            if event.type == pygame.QUIT:  # 关闭窗口
                self.create_cancel = True  # 终止外星人生成子线程
                sys.exit()  # 终止主线程

            elif event.type == pygame.MOUSEBUTTONDOWN\
                    and not self.game_stats.game_active:  # 鼠标点击事件
                self._check_play_button(pygame.mouse.get_pos())  # 检测游戏开始按钮

            elif event.type == pygame.KEYDOWN:  # 按键事件
                self._check_events_down(event)

            elif event.type == pygame.KEYUP:  # 松键事件
                self._check_events_up(event)

    def _update_screen(self):
        """屏幕刷新"""
        #  屏幕元素刷新
        self.screen.fill(self.bg_color)  # 背景颜色填充
        self.ship.blitme()  # 飞船图像生成
        for bullet in self.bullets.sprites():  # 子弹图像生成
            bullet.draw_bullet()
        for alien in self.aliens.sprites():  # 外星人图像生成
            alien.blitme()
        if not self.game_stats.game_active:  # PLAY按钮生成（游戏非活跃状态）
            self.play_button.draw_button()
        self.score_board.show_score()  # 分数显示
        self.score_board.show_highest_score()  # 最高分显示
        self.score_board.show_ships()  # 飞船组显示
        #  屏幕重新显示
        pygame.display.flip()

    def _update_bullets(self):
        """子弹位置更新"""
        self.bullets.update()  # 更新所有子弹位置
        for bullet in self.bullets.copy():  # 移除屏幕外子弹
            if bullet.rect.y < 0:
                self.bullets.remove(bullet)

    def _create_fleet(self):
        """创建外星人群"""
        if not self.create_cancel:
            self._create_alien()
            threading.Timer(self.settings.create_gap,
                            self._create_fleet).start()  # 子线程递归调用

    def _create_alien(self):
        """创建外星人"""
        new_alien = Alien(self)
        self.aliens.add(new_alien)

    def _delete_alien(self, alien):
        """删除外星人"""
        self.aliens.remove(alien)

    def _update_aliens(self):
        """外星人位置更新"""
        self.aliens.update()  # 更新所有外星人位置
        for alien in self.aliens.copy():  # 移除所有屏幕外外星人
            if alien.rect.y > self.settings.screen_height:
                self._delete_alien(alien)

    def run_game(self):
        """主线程：游戏运行"""
        self._update_screen()  # 初始化屏幕
        while True:
            self._check_events()  # 检测事件
            if self.game_stats.game_active:  # 游戏活跃状态
                self.ship.update()  # 更新飞船位置
                self._update_bullets()  # 更新子弹位置
                self._update_aliens()  # 更新外星人位置
                self._check_collision()  # 检测碰撞
                self._update_screen()  # 刷新屏幕


ai = AlienInvasion()
ai.run_game()
