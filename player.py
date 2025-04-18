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

        self.vel_x = 0
        self.vel_y = 0
        self.acceleration = PLAYER_ACCELERATION
        self.friction = PLAYER_FRICTION

        self.jumping = False
        self.facing_right = True
        self.on_ground = False

        self.current_frame = 0
        self.last_update = 0
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
            if (event.key == pygame.K_w or event.key == pygame.K_UP or event.key == pygame.K_SPACE) and self.on_ground:
                self.jump()

    def jump(self):
        self.vel_y = PLAYER_JUMP_FORCE
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
        print("Player velocity:", self.vel_x, self.vel_y)

        self.apply_physics()
        self.check_collisions()
        self.animate()

    def handle_movement(self):
        self.vel_x *= self.friction/4
       # self.rect.x= int(self.rect.x)+(2*self.vel_x)

        keys = pygame.key.get_pressed()
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            self.vel_x -= self.acceleration
            self.facing_right = False
            self.state = "run"

        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            self.vel_x += self.acceleration
            self.facing_right = True
            self.state = "run"

        if abs(self.vel_x) < 0.5:
            self.vel_x = 0
            if self.on_ground:
                self.state = "idle"

    def apply_physics(self):
        self.vel_y += GRAVITY

        if self.vel_y > MAX_FALL_SPEED:
            self.vel_y = MAX_FALL_SPEED

        self.rect.x += (self.vel_x)
        self.rect.y += (self.vel_y)

        if self.vel_y > 0 and not self.on_ground:
            self.state = "fall"
        elif self.vel_y < 0:
            self.state = "jump"
        print(self.state)
    def check_collisions(self):
        self.on_ground = False

        hits = pygame.sprite.spritecollide(self, self.game.platforms, False)
        for platform in hits:
            if self.vel_y > 0 and self.rect.bottom > platform.rect.top and self.rect.bottom < platform.rect.bottom:
                self.rect.bottom = platform.rect.top
                self.vel_y = 0
                self.on_ground = True
                self.jumping = False
            elif self.vel_y < 0 and self.rect.top < platform.rect.bottom and self.rect.top > platform.rect.top:
                self.rect.top = platform.rect.bottom
                self.vel_y = 0
            elif self.vel_x > 0 and self.rect.right > platform.rect.left+1 and self.rect.right < platform.rect.right-1:
                self.rect.right = platform.rect.left
                self.vel_x = 0
            elif self.vel_x < 0 and self.rect.left < platform.rect.right and self.rect.left > platform.rect.left:
                self.rect.left = platform.rect.right
                self.vel_x = 0

    def animate(self):
        if self.invulnerable:
            now = pygame.time.get_ticks()
            if (now // 200) % 2 == 0:
                self.image.fill(BLUE)
            else:
                self.image.fill((0, 0, 0, 0))  # Transparent
        else:
            self.image.fill(BLUE)
