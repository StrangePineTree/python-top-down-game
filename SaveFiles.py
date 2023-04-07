import pygame
import random

#set up pygame stuff
pygame.init()  
pygame.display.set_caption("top down game")  # sets the window title
screen = pygame.display.set_mode((800, 800))  # creates game screen
screen.fill((0,0,0))
clock = pygame.time.Clock() #set up clock

#game variables
timer = 0 #used for sheep movement
score = 0
running = True
sheepNumber = 0

#images and fonts
SheepPic = pygame.image.load("sheep.jpg")
font = pygame.font.Font('freesansbold.ttf', 32)
text = font.render('timer:', True, (200, 200, 0))
text2 = font.render(str(score), True, (200, 200, 0))
text3 = font.render('your score was', True, (200, 200, 0))
text5 = font.render('YOU LOSE', True, (200, 200, 0))

loser = False
#CONSTANTS (not required, just makes code easier to read)
LEFT = 0
RIGHT = 1
UP = 2
DOWN = 3

#function defintions------------------------------------
#can you tell me what the parameters are for these functions, and what they return (if anything)?

class Sheep:
    def __init__(self,posx,posy):
        self.pos = pygame.math.Vector2(posx,posy)
        self.direction = RIGHT
        self.caught = False
    def collide(self, PlayerX, PlayerY):
        if PlayerX+40 > self.pos.x:
            if PlayerX < self.pos.x+40:
                if PlayerY+40 >self.pos.y:
                    if PlayerY < self.pos.y+40:
                        if self.caught == False: #only catch uncaught sheeps!
                            self.caught = True #catch da sheepies!
                            global sheepNumber
                            sheepNumber -=1
        if self.pos.x < 50:
            self.direction = RIGHT
        if self.pos.x > 750:
            self.direction = LEFT
        if self.pos.y < 50:
            self.direction = DOWN
        if self.pos.y > 750:
            self.direction = UP
    def move(self):
        if timer % 50 == 0: #only change direction every 50 game loops
            self.direction = random.randrange(0, 4) #set random direction
        if self.direction == LEFT:
            self.pos.x -= 2
        elif self.direction == RIGHT:
            self.pos.x+=2
        elif self.direction == UP: 
            self.pos.y -=2
        else:
            self.pos.y += 2

#create sheep!
#numbers in list represent xpos, ypos, direction moving, and whether it's been caught or not!
sheeplist: list[Sheep] = []
#make more sheeps here!
for x in range (24):
    sheeplist.append(Sheep(random.randrange(100,700),random.randrange(100,700)))
    sheepNumber+=1

#player variables
xpos = 500 #xpos of player
ypos = 200 #ypos of player
vx = 0 #x velocity (left/right speed) of player
vy = 0 #y velocity (up/down speed) of player
keys = [False, False, False, False] #this list holds whether each key has been pressed

while running: #GAME LOOP############################################################
    clock.tick(60) #FPS
    timer+=1
    
    
    #Input Section------------------------------------------------------------
    for event in pygame.event.get(): #quit game if x is pressed in top corner
        if event.type == pygame.QUIT:
            running = False
            loser = True
      
        #check if a key has been PRESSED
        if event.type == pygame.KEYDOWN: 
            if event.key == pygame.K_a:
                keys[LEFT] = True
            elif event.key == pygame.K_d:
                keys[RIGHT] = True
            elif event.key == pygame.K_s:
                keys[DOWN] = True
            elif event.key == pygame.K_w:
                keys[UP] = True

        #check if a key has been LET GO
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                keys[LEFT] = False
            elif event.key == pygame.K_d:
                keys[RIGHT] = False
            elif event.key == pygame.K_s:
                keys[DOWN] = False
            elif event.key == pygame.K_w:
                keys[UP] = False
          
    #physics
    #section--------------------------------------------------------------------
    if timer % 60 == 0:
        score += 1
    #player movement!--------
    if keys[LEFT] == True:
        vx = -3
    elif keys[RIGHT] == True:
        vx = 3
    else:
        vx = 0
    if keys[UP] == True:
        vy = -3
    elif keys[DOWN] == True:
        vy = 3
    else:
        vy = 0


    #player/sheep collision!
    for sheep in sheeplist:
        sheep.move()
        sheep.collide(xpos,ypos)
    if sheepNumber == 0:
        running = False

    #update player position
    xpos+=vx 
    ypos+=vy
    
      
    # RENDER
    # Section--------------------------------------------------------------------------------
            
    screen.fill((0,0,0)) #wipe screen so it doesn't smear
  
    #draw player
    pygame.draw.rect(screen, (100, 200, 100), (xpos, ypos, 40, 40))

    for sheep in sheeplist:
        if sheep.caught == False:
            screen.blit(SheepPic, (sheep.pos))
    
    #display score
    screen.blit(text, (20, 20))
    text2 = font.render(str(score), True, (200, 200, 0))#update score number
    screen.blit(text2, (140, 20))

    pygame.display.flip()#this actually puts the pixel on the screen
    
#end game loop------------------------------------------------------------------------------

#end screen
screen.fill((0,0,0)) 
text4 = font.render(str(score), True, (200, 200, 0))
if loser:
    screen.blit(text5, (400, 400))
else:
    screen.blit(text3, (400,400))
    screen.blit(text4, (640,400))
pygame.display.flip()
pygame.time.wait(750)#pause for a bit before ending

pygame.quit()