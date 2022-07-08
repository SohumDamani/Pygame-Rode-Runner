import pygame
from sys import exit

#starts pygame
pygame.init()

width=800
height=400

screen = pygame.display.set_mode((width,height))
pygame.display.set_caption("Active")
clock = pygame.time.Clock()

sky = pygame.image.load('graphics/Sky.png').convert()
snail_surface = pygame.image.load('graphics/snail/snail1.png').convert_alpha() #this removes the whitespace of snail
snail_rect = snail_surface.get_rect(midbottom=(600,300))

while True:
    for event in pygame.event.get():
        # check if x button of window is clicked or not
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.MOUSEMOTION:
            #print(event.pos)
            if snail_rect.collidepoint(event.pos):
                print("Collision")


    screen.blit(sky, (0, 0))
    screen.blit(snail_surface,snail_rect)
    """
    to covert it into moving image update x position and 
    take care snail does not disappear
    """
    snail_rect.x-=5
    if snail_rect.right<0:
        snail_rect.left=800

    """
    Check if mouse is over the snail or not
    i.e get mouse position
    """
    # mouse = pygame.mouse.get_pos()
    # if snail_rect.collidepoint(mouse):
    #     print("Collision :",mouse)

    pygame.display.update()
    #While loop does not run faster than 60 times per sec
    #60fps
    clock.tick(60)