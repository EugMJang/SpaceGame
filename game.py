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
    SPAWN_EVENT = pygame.USEREVENT + 1
    pygame.time.set_timer(SPAWN_EVENT, 1000)
    while running:
        game_clock.tick(60)
        screen.fill((0, 0, 0))
        draw_stars(star_positions)
        player.draw(screen)
        player.update()
        enemies.draw(screen)
        enemies.update()
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == SPAWN_EVENT:
                enemies.add(Enemy(main_player))
            if event.type == pygame.QUIT:
                running = False

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
    
    def update(self):
        self.point_to_cursor()
        print(self.health)
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

        self.player = player

        self.image = pygame.Surface((self.size, self.size), pygame.SRCALPHA, 32).convert_alpha()
        pygame.draw.circle(self.image, (175, 0, 0), (10, 10), 10)

        self.rect = self.image.get_rect()
        which_side = random.randint(0, 1000)
        if which_side % 2 == 0:
            self.rect.center = (-10, random.randint(10, height - 10))
        else:
            self.rect.center = (width + 10, random.randint(10, height - 10))
    
    def update(self):
        if (not pygame.sprite.collide_mask(self, self.player)):
            self.move_to_player()
        else:
            self.player.health -= 0.25

    def move_to_player(self):
        rel_pos = rel_x, rel_y = self.rect.centerx - self.player.rect.centerx, self.rect.centery - self.player.rect.centery
        distance_to_player = int(dist([0, 0], rel_pos))
        self.rect = self.rect.move(self.speed * rel_x / distance_to_player, self.speed * rel_y / distance_to_player)

def draw_stars(positions):
    for x, y in positions:
        pygame.draw.rect(screen, (255, 255, 255), pygame.Rect(x, y, 2, 2))

game_clock = pygame.time.Clock()

main()
    