import pygame
from settings import *

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, game):
        super().__init__()
        self.game = game

        self.image = pygame.Surface((TILE_SIZE, TILE_SIZE))
        self.image.fill(BLUE)

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        self.speed = 5
        self.jump_force = -15
        self.gravity = 1
        self.fall_speed = 10

        self.vel_y = 0
        self.jumping = False
        self.on_ground = False
        self.facing_right = True
        self.state = "idle"

        self.invulnerable = False
        self.invulnerable_timer = 0

        self.load_animations()

    def load_animations(self):
        self.animations = {
            "idle": [self.image],
            "run": [self.image],
            "jump": [self.image],
            "fall": [self.image]
        }

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if (event.key in [pygame.K_w, pygame.K_UP, pygame.K_SPACE]) and self.on_ground:
                self.jump()

    def jump(self):
        self.vel_y = self.jump_force
        self.jumping = True
        self.on_ground = False

        if 'jump' in self.game.sounds:
            self.game.sounds['jump'].play()

    def hit(self):
        self.invulnerable = True
        self.invulnerable_timer = pygame.time.get_ticks()

    def update(self):
        now = pygame.time.get_ticks()
        if self.invulnerable and now - self.invulnerable_timer > 2000:
            self.invulnerable = False

        self.handle_movement()
        self.apply_gravity()
        self.check_collisions()
        self.animate()

    def handle_movement(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            self.speed = -5
            self.rect.x += self.speed
            self.facing_right = False
            self.state = "run"
        elif keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            self.speed = 5
            self.rect.x += self.speed
            self.facing_right = True
            self.state = "run"
        else:
            if self.on_ground:
                self.state = "idle"

    def apply_gravity(self):
        self.vel_y += self.gravity
        if self.vel_y > self.fall_speed:
            self.vel_y = self.fall_speed

        self.rect.y += self.vel_y

        if self.vel_y > 0 and not self.on_ground:
            self.state = "fall"
        elif self.vel_y < 0:
            self.state = "jump"

    def check_collisions(self):
        self.on_ground = False
        hits = pygame.sprite.spritecollide(self, self.game.platforms, False)

        for platform in hits:
            if self.vel_y > 0 and self.rect.bottom > platform.rect.top and self.rect.bottom < platform.rect.bottom:
                self.rect.bottom = platform.rect.top
                self.vel_y = 0
                self.on_ground = True
                self.jumping = False
            elif self.vel_y < 0 and self.rect.top < platform.rect.bottom:
                self.rect.top = platform.rect.bottom
                self.vel_y = 0
          

    def animate(self):
            if self.state == "idle":
               self.image = pygame.image.load("assets/sprites/rocket_up.png").convert_alpha()
            elif self.state == "jump":
               self.image = pygame.image.load("assets/sprites/rocket_up.png").convert_alpha()
            elif self.speed > 0:
               self.image = pygame.image.load("assets/sprites/rocket_right.png").convert_alpha()
            elif self.speed < 0:
                self.image = pygame.image.load("assets/sprites/rocket_left.png").convert_alpha() 
