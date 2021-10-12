import pygame
import os

pygame.init()



SCREEN_WIDTH = 800
SCREEN_HEIGHT = 768 #int(SCREEN_WIDTH * 0.8)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Shadowy_Ninja")

#set frame rate
clock = pygame.time.Clock()
FPS = 60

#define game variables
GRAVITY = 0.75

#define player action variables
moving_left = False
moving_right = False

#define colors
background = pygame.image.load("C:/Users/Cybineer/Desktop/MyCode/Shadowy_Ninja/png/Background.png").convert_alpha()


#BG = (0, 0,0)
RED = (255, 0, 0)


def draw_bg():
    screen.blit(background, (0, 0))
    ##pygame.draw.line(screen, RED, (0,725), (SCREEN_WIDTH, 725))



#creating Class
class Ninja(pygame.sprite.Sprite):
    def __init__(self,char_type, x, y, scale, speed):
        pygame.sprite.Sprite.__init__(self)
        self.alive = True
        self.char_type = char_type
        self.speed = speed
        self.direction = 1
        self.velocity_y = 0
        self.jump = False
        self.in_air = True
        self.flip = False
        self.animation_list = []
        self.frame_index = 0
        self.action = 0
        self.update_time = pygame.time.get_ticks()

        #load all images for the players
        animation_types = ["Idle", "Run", "Jump" ]
        for animation in animation_types:
            #reset temporary list of images
            temp_list = []
            #count number of files in the folder
            num_of_frames = len(os.listdir(f"C:/Users/Cybineer/Desktop/MyCode/Shadowy_Ninja/png/{self.char_type}/{animation}"))

            for i in range(num_of_frames):
                ninja = pygame.image.load(f"C:/Users/Cybineer/Desktop/MyCode/Shadowy_Ninja/png/{self.char_type}/{animation}/{i}.png").convert_alpha()
                #ninja = pygame.transform.scale(ninja, (ninja.get_width() - 200, (ninja.get_height() - 300 )))
                ninja = pygame.transform.scale(ninja, (ninja.get_width() % scale, (ninja.get_height() % scale)))
                temp_list.append(ninja)
            self.animation_list.append(temp_list)
        self.ninja = self.animation_list[self.action][self.frame_index]
        self.rect = self.ninja.get_rect()
        self.rect.center = (x,y)


    def move(self, moving_left, moving_right):
        #reset movement variables (dealta stands for change in x and change in y)
        dealta_x = 0
        dealta_y = 0


        #assign movement variables if moving left or right
        if moving_left:
            dealta_x = -self.speed
            self.flip = True
            self.direction = -1
        if moving_right:
            dealta_x = self.speed
            self.flip = False
            self.direction = 1
        #jump
        if self.jump == True and self.in_air == False:
            self.velocity_y = -11
            self.jump = False
            self.in_air = True

        #apply gravity
        self.velocity_y += GRAVITY
        if self.velocity_y > 10:
            self.velocity_y
        dealta_y += self.velocity_y

        #check collision with floor
        if self.rect.bottom + dealta_y > 725:
            dealta_y = 725 - self.rect.bottom
            self.in_air = False
            
        

        # update rectangle position
        self.rect.x += dealta_x
        self.rect.y += dealta_y        


    def update_animation(self):
            #update animation
            ANIMATION_COOLDOWN = 100
            
            #update image depending on current frame
            self.ninja = self.animation_list[self.action][self.frame_index]

            #check if enough time has passed since last update
            if pygame.time.get_ticks() - self.update_time > ANIMATION_COOLDOWN:
                self.update_time = pygame.time.get_ticks()
                self.frame_index += 1
            # if animation has run out reset back to start
            if self.frame_index >= len(self.animation_list[self.action]):
                self.frame_index = 0
                

    def update_action(self, new_action):
        #check if new action is different to the previous one
        if new_action != self.action:
            self.action = new_action
            #update the animation setting
            self.frame_index = 0
            self.update_time = pygame.time.get_ticks()


    def draw(self):
        screen.blit(pygame.transform.flip(self.ninja, self.flip, False), self.rect)






#creating player
player = Ninja("player", 50,768, 200, 5)
# enemy = Ninja("enemy",200, 200, 200, 5)




run = True
while run:

    clock.tick(FPS) 


    draw_bg()
    player.update_animation()
    player.draw()
    #enemy.draw()


    #update player action
    if player.alive:
        if player.in_air:
            player.update_action(2)  # 2 means jump            
        elif moving_left or moving_right:
            player.update_action(1)  # 1 means run
        else:
            player.update_action(0)  # 0 means idle
        player.move(moving_left, moving_right)


    for event in pygame.event.get():
        #quit game
        if event.type == pygame.QUIT:
            run = False
        # keyboard presses
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                moving_left = True
            if event.key == pygame.K_RIGHT:
                moving_right = True
            if event.key == pygame.K_UP and player.alive:
                player.jump = True
            if event.key == pygame.K_ESCAPE:
                run = False

        # keyboard button release
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                moving_left = False
            if event.key == pygame.K_RIGHT:
                moving_right = False      
    
    pygame.display.update()

pygame.quit()


