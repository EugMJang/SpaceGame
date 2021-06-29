import pygame, random, sys
from math import atan2, degrees, dist

pygame.init()

size = width, height = 500, 500
screen = pygame.display.set_mode(size)

game_state = "main"

def main():
    running = True
    star_positions = [(random.randint(0, width), random.randint(0, height)) for i in range(100)]

    player = pygame.sprite.Group()
    main_player = MainPlayer()
    player.add(main_player)

    enemies = pygame.sprite.Group()
    enemies.add(Enemy(main_player))

    bullets = pygame.sprite.Group()

    SPAWN_EVENT = pygame.USEREVENT + 1
    pygame.time.set_timer(SPAWN_EVENT, 500)

    start_ticks = pygame.time.get_ticks()
    while running:
        game_clock.tick(60)
        screen.fill((0, 0, 0))
        draw_stars(star_positions)
        player.draw(screen)
        player.update()

        enemies.draw(screen)
        enemies.update()

        bullets.draw(screen)
        bullets.update()

        time_since_start = (pygame.time.get_ticks() - start_ticks) / 1000
        font = pygame.font.SysFont("Arial", 25)
        time_text = font.render(str(time_since_start) + " seconds", 1, (255, 255, 255))
        screen.blit(time_text, (30, 30))

        pygame.display.flip()

        collisions = pygame.sprite.groupcollide(bullets, enemies, True, False)
        if collisions:
            for enemy in collisions.values():
                enemy[0].health -= 50

        for event in pygame.event.get():
            if event.type == SPAWN_EVENT:
                enemies.add(Enemy(main_player))
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                bullets.add(Bullet(main_player))

class MainPlayer(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        self.side = 70

        self.health = 100

        self.image = pygame.Surface((self.side, self.side), pygame.SRCALPHA, 32).convert_alpha()
        self.draw_player()
        self.original_image = self.image

        self.rect = self.image.get_rect()
        self.rect.center = (width / 2, height / 2)

        self.health_bar = HealthBar((self.rect.centerx, self.rect.bottom + 10), self.side, (175, 0, 0), (0, 175, 0))
    
    def update(self):
        self.point_to_cursor()
        self.health_bar.draw(self.health, (self.rect.centerx, self.rect.bottom + 10))
        if self.health <= 0:
            sys.exit()

    def draw_player(self):
        pygame.draw.circle(self.image, (0, 0, 175), (self.side / 2, self.side / 2), 25)
        pygame.draw.rect(self.image, (0, 0, 100), (31, 31, 39, 8))
    
    def point_to_cursor(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        rel_x, rel_y = mouse_x - self.rect.centerx, mouse_y - self.rect.centery

        angle = degrees(atan2(rel_y, rel_x))
        self.rotate_image(-angle)
    
    def rotate_image(self, angle):
        self.image = pygame.transform.rotate(self.original_image, angle)
        self.rect = self.image.get_rect(center = self.original_image.get_rect(center = (width / 2, height / 2)).center)

class Enemy(pygame.sprite.Sprite):
    def __init__(self, player):
        pygame.sprite.Sprite.__init__(self)

        self.size = 20
        self.speed = -3

        self.health = 100.0

        self.player = player

        self.image = pygame.Surface((self.size, self.size), pygame.SRCALPHA, 32).convert_alpha()
        pygame.draw.circle(self.image, (175, 0, 0), (10, 10), 10)

        self.rect = self.image.get_rect()
        which_side = random.randint(0, 1000)
        if which_side % 2 == 0:
            if which_side % 4 == 0:
                self.rect.center = (-10, random.randint(10, height / 2 - 75))
            else:
                self.rect.center = (-10, random.randint(height / 2 + 75, height + 10))
        else:
            if which_side % 4 == 3:
                self.rect.center = (width + 10, random.randint(10, height / 2 - 75))
            else:
                self.rect.center = (width + 10, random.randint(height / 2 + 75, height + 10))

        self.health_bar = HealthBar((self.rect.centerx, self.rect.bottom + 10), self.size, (0, 0, 0), (175, 0, 0))
    
    def update(self):
        self.health_bar.draw(self.health, (self.rect.centerx, self.rect.bottom + 10))
        if not pygame.sprite.collide_mask(self, self.player):
            self.move_to_player()
        else:
            self.player.health -= 0.25
        if self.health <= 0:
            self.kill()
            del self

    def move_to_player(self):
        rel_pos = rel_x, rel_y = self.rect.centerx - self.player.rect.centerx, self.rect.centery - self.player.rect.centery
        distance_to_player = int(dist([0, 0], rel_pos))
        self.rect = self.rect.move(self.speed * rel_x / distance_to_player, self.speed * rel_y / distance_to_player)

class Bullet(pygame.sprite.Sprite):
    def __init__(self, player):
        pygame.sprite.Sprite.__init__(self)

        self.size = 10
        
        self.speed = 7

        self.image = pygame.Surface((self.size, self.size))
        pygame.draw.circle(self.image, (200, 200, 200), (self.size / 2, self.size / 2), self.size / 2)

        self.rect = self.image.get_rect()
        self.rect.center = player.rect.center
        
        self.destx, self.desty = pygame.mouse.get_pos()
        rel_pos = self.rel_x, self.rel_y = self.destx - self.rect.centerx, self.desty - self.rect.centery
        self.distance_to_player = int(dist([0, 0], rel_pos))

    def update(self):
        self.move_in_direction()
        if self.rect.center > (width, height) or self.rect.center < (0, 0):
            self.kill()
            del self

    def move_in_direction(self):
        self.rect = self.rect.move(self.speed * self.rel_x / self.distance_to_player, self.speed * self.rel_y / self.distance_to_player)

class HealthBar():
    def __init__(self, pos, width, color, health_color):
        self.pos, self.width, self.color, self.health_color = pos, width, color, health_color

        self.image = pygame.Surface((width, 5))
        pygame.draw.rect(self.image, color, (0, 0, width, 5))
        pygame.draw.rect(self.image, health_color, (0, 0, width, 5))

        self.rect = self.image.get_rect()
        self.rect.center = pos
    def draw(self, health, pos):
        pygame.draw.rect(self.image, self.color, (0, 0, self.width, 5))
        pygame.draw.rect(self.image, self.health_color, (0, 0, self.width * health / 100.0, 5))
        
        self.rect = self.image.get_rect()
        self.rect.center = pos
        screen.blit(self.image, self.rect)

def draw_stars(positions):
    for x, y in positions:
        pygame.draw.rect(screen, (255, 255, 255), pygame.Rect(x, y, 2, 2))

game_clock = pygame.time.Clock()

main()
    