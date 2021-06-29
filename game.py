import pygame, random, sys
from math import atan2, degrees

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

    while running:
        game_clock.tick(60)
        screen.fill((0, 0, 0))
        draw_stars(star_positions)
        player.draw(screen)
        player.update()
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

class MainPlayer(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        self.side = 70

        self.image = pygame.Surface((self.side, self.side))
        self.draw_player()
        self.original_image = self.image

        self.rect = self.image.get_rect()
        self.rect.topleft = (0, height / 2 - self.side / 2)
    
    def update(self):
        self.point_to_cursor()

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
        self.rect = self.image.get_rect(center = self.original_image.get_rect(topleft = (0, height / 2 - self.side / 2)).center)

def draw_stars(positions):
    for x, y in positions:
        pygame.draw.rect(screen, (255, 255, 255), pygame.Rect(x, y, 2, 2))

game_clock = pygame.time.Clock()

main()
    