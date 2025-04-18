import pygame
from settings import *
from player import Player
from platforms import Platform
from collectibles import Coin
from enemies import Enemy
from utils import load_image, load_sound
from camera import Camera
import os

class Game:
    def __init__(self):
        self.game_state = STATE_PLAYING
        self.level_index = 0
        self.score = 0
        self.lives = 3

        # Sprite grupları
        self.all_sprites = pygame.sprite.Group()
        self.platforms = pygame.sprite.Group()
        self.collectibles = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()

        # Asset klasörlerini oluştur
        os.makedirs(SPRITES_DIR, exist_ok=True)
        os.makedirs(SOUNDS_DIR, exist_ok=True)

        # Sesleri yükle
        self.sounds = {
            'coin': load_sound('coin.wav'),
            'hurt': load_sound('hurt.wav'),
            'level_complete': load_sound('level_complete.wav')
        }

        # Font ve kamera
        self.font = pygame.font.SysFont('Arial', 24)
        self.camera = Camera(WIDTH, HEIGHT)

        # Level yükle
        self.load_level(self.level_index)

    def load_level(self, level_index):
        self.all_sprites.empty()
        self.platforms.empty()
        self.collectibles.empty()
        self.enemies.empty()

        level = LEVELS[level_index]

        for y, row in enumerate(level):
            for x, col in enumerate(row):
                pos_x = x * TILE_SIZE
                pos_y = y * TILE_SIZE

                if col == "X":
                    platform = Platform(pos_x, pos_y)
                    self.platforms.add(platform)
                    self.all_sprites.add(platform)
                elif col == "P":
                    self.player = Player(pos_x, pos_y, self)
                    self.all_sprites.add(self.player)
                elif col == "C":
                    coin = Coin(pos_x, pos_y)
                    self.collectibles.add(coin)
                    self.all_sprites.add(coin)
                elif col == "E":
                    enemy = Enemy(pos_x, pos_y, self)
                    self.enemies.add(enemy)
                    self.all_sprites.add(enemy)

    def handle_event(self, event):
        if self.game_state == STATE_PLAYING:
            self.player.handle_event(event)
        elif self.game_state in (STATE_MENU, STATE_GAME_OVER, STATE_LEVEL_COMPLETE):
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                if self.game_state == STATE_GAME_OVER:
                    self.__init__()
                elif self.game_state == STATE_LEVEL_COMPLETE:
                    self.level_index += 1
                    if self.level_index < len(LEVELS):
                        self.load_level(self.level_index)
                        self.game_state = STATE_PLAYING
                    else:
                        self.game_state = STATE_MENU
                        self.level_index = 0
                self.game_state = STATE_PLAYING

    def update(self):
        if self.game_state == STATE_PLAYING:
            self.all_sprites.update()
            self.camera.update(self.player)

            coins_collected = pygame.sprite.spritecollide(self.player, self.collectibles, True)
            for coin in coins_collected:
                self.score += 10
                self.sounds['coin'].play()

            enemy_hits = pygame.sprite.spritecollide(self.player, self.enemies, False)
            if enemy_hits and not self.player.invulnerable:
                self.lives -= 1
                self.player.hit()
                self.sounds['hurt'].play()

                if self.lives <= 0:
                    self.game_state = STATE_GAME_OVER

            if len(self.collectibles) == 0:
                self.game_state = STATE_LEVEL_COMPLETE
                self.sounds['level_complete'].play()

            if self.player.rect.top > HEIGHT:
                self.lives -= 1
                if self.lives <= 0:
                    self.game_state = STATE_GAME_OVER
                else:
                    self.load_level(self.level_index)

    def draw(self, screen):
        if self.game_state == STATE_PLAYING:
            for sprite in self.all_sprites:
                screen.blit(sprite.image, self.camera.apply(sprite))
            self.draw_hud(screen)
        elif self.game_state == STATE_MENU:
            self.draw_menu(screen)
        elif self.game_state == STATE_GAME_OVER:
            self.draw_game_over(screen)
        elif self.game_state == STATE_LEVEL_COMPLETE:
            self.draw_level_complete(screen)

    def draw_hud(self, screen):
        score_text = self.font.render(f"Score: {self.score}", True, WHITE)
        screen.blit(score_text, (10, 10))

        lives_text = self.font.render(f"Lives: {self.lives}", True, WHITE)
        screen.blit(lives_text, (10, 40))

        level_text = self.font.render(f"Level: {self.level_index + 1}", True, WHITE)
        screen.blit(level_text, (WIDTH - 120, 10))

    def draw_menu(self, screen):
        title_text = pygame.font.SysFont('Arial', 48).render("PIXEL PLATFORMER", True, WHITE)
        screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, HEIGHT // 3))

        instructions = self.font.render("Press ENTER to start", True, WHITE)
        screen.blit(instructions, (WIDTH // 2 - instructions.get_width() // 2, HEIGHT // 2))

        controls = self.font.render("Controls: WASD or Arrow Keys", True, WHITE)
        screen.blit(controls, (WIDTH // 2 - controls.get_width() // 2, HEIGHT // 2 + 40))

    def draw_game_over(self, screen):
        game_over_text = pygame.font.SysFont('Arial', 48).render("GAME OVER", True, RED)
        screen.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 3))

        final_score = self.font.render(f"Final Score: {self.score}", True, WHITE)
        screen.blit(final_score, (WIDTH // 2 - final_score.get_width() // 2, HEIGHT // 2))

        restart = self.font.render("Press ENTER to play again", True, WHITE)
        screen.blit(restart, (WIDTH // 2 - restart.get_width() // 2, HEIGHT // 2 + 40))

    def draw_level_complete(self, screen):
        level_complete = pygame.font.SysFont('Arial', 48).render("LEVEL COMPLETE!", True, GREEN)
        screen.blit(level_complete, (WIDTH // 2 - level_complete.get_width() // 2, HEIGHT // 3))

        score_text = self.font.render(f"Score: {self.score}", True, WHITE)
        screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, HEIGHT // 2))

        continue_text = self.font.render("Press ENTER to continue", True, WHITE)
        screen.blit(continue_text, (WIDTH // 2 - continue_text.get_width() // 2, HEIGHT // 2 + 40))
