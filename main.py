import pygame
from sys      import exit
from settings import *
from tiles    import *
from level    import Level

FPS=60

pygame.init()
screen = pygame.display.set_mode((screen_width,screen_height), pygame.NOFRAME)
clock = pygame.time.Clock()
level = Level(level_map, screen)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit(0)

    screen.fill('black')

    #font = pygame.font.Font('assets/roboto.ttf', 30)
    #text = font.render(str(int(clock.get_fps())), 1, pygame.Color("red"))
    #screen.blit(text, (0,0))

    level.run()

    pygame.display.update()
    clock.tick(FPS)


