import pygame
from sys import exit
from random import randint,choice

#starts pygame
pygame.init()

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        player_walk_1 = pygame.image.load('graphics/Player/player_walk_1.png').convert_alpha()
        player_walk_2 = pygame.image.load('graphics/Player/player_walk_2.png').convert_alpha()
        self.player_walk = [player_walk_1,player_walk_2] 
        self.player_index = 0
        self.player_jump = pygame.image.load('graphics/Player/jump.png').convert_alpha()

        self.image = self.player_walk[self.player_index]
        self.rect = self.image.get_rect(midbottom = (100,300))
        self.gravity = 0
        self.jump_sound = pygame.mixer.Sound('audio/jump.mp3')

    def player_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.rect.bottom>=300:
            self.gravity = -20
            self.jump_sound.play(fade_ms=1000)
            self.jump_sound.set_volume(0.3)

    def apply_gravity(self):
        self.gravity+=1
        self.rect.y +=self.gravity
        if self.rect.bottom>=300:
            self.rect.bottom=300

    def animation(self):
        if self.rect.bottom<300:
            self.image=self.player_jump
        else:
            self.player_index +=0.1
            if self.player_index>len(self.player_walk):
                self.player_index=0
            self.image = self.player_walk[int(self.player_index)]

    def update(self):
        self.player_input()
        self.apply_gravity()
        self.animation()

class Obstacle(pygame.sprite.Sprite):
    def __init__(self,type):
        super().__init__()
        if type=='fly':
            fly_1 = pygame.image.load('graphics/Fly/Fly1.png').convert_alpha()
            fly_2 = pygame.image.load('graphics/Fly/Fly2.png').convert_alpha()
            self.frames = [fly_1, fly_2]
            y_pos = 210
        else:
            snail_1 = pygame.image.load('graphics/snail/snail1.png').convert_alpha()
            snail_2 = pygame.image.load('graphics/snail/snail2.png').convert_alpha()
            self.frames = [snail_1, snail_2]
            y_pos=300

        self.animation_index = 0
        self.speed = 6
        self.image = self.frames[int(self.animation_index)]
        self.rect = self.image.get_rect(bottomright=(randint(900,1300),y_pos))

    def animation(self):
        self.animation_index +=0.1
        if self.animation_index>len(self.frames):
            self.animation_index=0
        self.image = self.frames[int(self.animation_index)]

    def destroy(self):
        if self.rect.x <=-100:
            self.kill()

    def update(self):
        self.animation()
        self.rect.x-=self.speed
        self.destroy()

width=800
height=400

screen = pygame.display.set_mode((width,height))
pygame.display.set_caption("Active")
clock = pygame.time.Clock()

player= pygame.sprite.GroupSingle()
player.add(Player())

obstacle_group = pygame.sprite.Group()


# w1,h1=100,200
# test_surface = pygame.Surface((w1,h1))
# test_surface.fill('Yellow')

sky = pygame.image.load('graphics/Sky.png').convert() #this is not necessary it just makes the game a bit fast
grd = pygame.image.load('graphics/ground.png').convert()

"""creating text(score)"""
f1 = pygame.font.Font('font/Pixeltype.ttf',50) #create font
# #create a surface       (text,Smooth the text,Color)
# score_surf = f1.render("Welcome",True,"DarkBlue")
# score_rect = score_surf.get_rect(center=(400,50))

def display_score():
    ti = int((pygame.time.get_ticks()-start_time)/500)
    score_surf = f1.render(str(ti),False,(64,64,64))
    score_rect = score_surf.get_rect(center=(400,50))
    screen.blit(score_surf,score_rect)
    return ti

"""
Game Over
"""
def Intro():
    screen.fill("yellow", (0, 0, 800, 400))
    player_stand = pygame.image.load("graphics/Player/player_stand.png").convert_alpha()
    player_stand = pygame.transform.rotozoom(player_stand,0,1.5)
    player_stand_rect = player_stand.get_rect(center = (400,200))

    screen.blit(player_stand,player_stand_rect)

    if final_score==0:
        text = "Welcome to Rode Runner"
    else:
        text = f"Your Score : {final_score}"

    name_surface = f1.render(text,False,"black")
    name_rect = name_surface.get_rect(midbottom = player_stand_rect.midtop)
    screen.blit(name_surface,name_rect)

    restart_surf = f1.render("Press space to run",True,"black")
    restart_rect = restart_surf.get_rect(midtop = player_stand_rect.midbottom)
    screen.blit(restart_surf,restart_rect)
"""
Check collision
"""
def collision(player, obstacle):
    global game_active,final_score
    if obstacle:
        for ob in obstacle:
            #check collison
            if player.colliderect(ob):
                print("Collison")
                game_active=False
                final_score = display_score()
                pygame.time.wait(500)

def collision_sprite():
    global game_active,final_score
    """
    True means that anytime player collides with obstacle the obstacle is destroyed
    """
    if pygame.sprite.spritecollide(player.sprite,obstacle_group,False):
        game_active = False
        obstacle_group.empty()
        final_score = display_score()

def obstacle_movement(obstacle_list):
    pass
#     if obstacle_list:
#         for ob in obstacle_list:
#             ob.x -=obstacle_speed
#
#             #display appropriate obstacle
#             if ob.bottom==300:
#                 display_obstacle(snail_surf,ob)
#             else:
#                 display_obstacle(fly_surf,ob)
#
#             # remove obstacle if outside screen
#             if ob.x < -100:
#                 obstacle_rect.remove(ob)
#         return obstacle_list
#
#     return []

def display_obstacle(surf,ob):
    screen.blit(surf, ob)

# def player_animation():
#     global player_index,player_surf
#
#     # jump when in air
#     if player_rect.bottom<300:
#         player_surf = player_jump
#     else:
#         # walk when on floor
#         player_index +=0.1
#         if player_index>len(player_walk):
#             player_index=0
#         player_surf = player_walk[int(player_index)]






#obstacle
# snail_1 = pygame.image.load('graphics/snail/snail1.png').convert_alpha()
# snail_2 = pygame.image.load('graphics/snail/snail2.png').convert_alpha()
# snail_index = 0
# snail = [snail_1,snail_2]
# snail_surf = snail[snail_index]
# fly_1 = pygame.image.load('graphics/Fly/Fly1.png').convert_alpha()
# fly_2 = pygame.image.load('graphics/Fly/Fly2.png').convert_alpha()
# fly_index =0
# fly = [fly_1,fly_2]
# fly_surf = fly[fly_index]
# obstacle_rect =[]

#player

#We use rectangle for positioning and determining collision

player_surf = pygame.image.load('graphics/Player/player_walk_1.png').convert_alpha()
player_rect = player_surf.get_rect(midbottom=(80, 300)) #draws rectangle around the image
player_gravity =0

"""
Timer and obstacle
"""
obstacle_timer = pygame.USEREVENT+1
pygame.time.set_timer(obstacle_timer,1500)
snail_animation_timer =  pygame.USEREVENT+2
pygame.time.set_timer(snail_animation_timer,500)
fly_animation_timer =  pygame.USEREVENT+3
pygame.time.set_timer(fly_animation_timer,200)
obstacle_speed = 5

"""
Intro sound
"""
intro_sound = pygame.mixer.Sound('audio/music.wav')
intro_sound.play(loops=-1, fade_ms=2000)
intro_sound.set_volume(0.1)

flag=True #used to get only one collision at a time
jump=False
game_active=False
start_time =0
final_score =0
while True:
    for event in pygame.event.get():
        # check if x button of window is clicked or not
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if game_active:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if player_rect.collidepoint(event.pos) and player_rect.bottom==300:
                    player_gravity=-20
            if event.type == pygame.KEYDOWN:
                #jump only if on ground
                if event.key==pygame.K_SPACE and player_rect.bottom==300:
                    player_gravity=-20
                    jump=True

            if event.type == obstacle_timer:
                obstacle_group.add(Obstacle(choice(['fly','snail','snail','snail','fly'])))
                # if randint(0,2):
                #     obstacle_rect.append(snail_surf.get_rect(midbottom=(randint(900, 1100),300)))
                # else:
                #     obstacle_rect.append(fly_surf.get_rect(bottomright=(randint(900,1100),200)))

            # if event.type == snail_animation_timer:
            #     snail_index = 0 if snail_index==1 else 1
            #     snail_surf = snail[snail_index]
            #
            # if event.type == fly_animation_timer:
            #     fly_index = 0 if fly_index==1 else 1
            #     fly_surf = fly[fly_index]

        else:
            if event.type==pygame.KEYDOWN:
                #restarting the game
                if event.key==pygame.K_SPACE:
                    start_time = pygame.time.get_ticks()
                    player_rect.bottom=300
                    player_gravity = 0
                    obstacle_rect=[]
                    game_active=True

    if game_active:
        screen.blit(sky,(0,0))
        screen.blit(grd,(0,300))
        display_score()
        #
        # pygame.draw.rect(screen,color="lightblue",rect=score_rect)
        # screen.blit(score_surf,score_rect)


        # """
        # to covert it into moving image update x position and
        # take care snail does not disappear
        # """
        # snail_rect.x-=5
        # if snail_rect.right<0:
        #     snail_rect.left=800
        # """
        # Obstacle Movement
        # """
        # obstacle_rect=obstacle_movement(obstacle_rect)
        """
        Player 
        """
        # screen.blit(player_surf, player_rect)
        player.draw(screen)
        player.update()
        """
        Obstacle
        """
        obstacle_group.draw(screen)
        obstacle_group.update()
        """
        Check for collision 
        """
        # collision(player_rect,obstacle_rect)
        collision_sprite()

        """
        Keyboard Input
        """
        # keys=pygame.key.get_pressed()
        # if keys[pygame.K_SPACE]:
        #     print("Jump")

        # if jump:
        #     player_gravity+=1
        #     player_rect.y +=player_gravity
        #     if player_rect.bottom>=300:
        #         player_rect.bottom=300
        #         jump=False

    else:
        Intro()



    pygame.display.update()
    #While loop does not run faster than 60 times per sec
    #60fps
    clock.tick(60)