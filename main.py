from __future__ import annotations
import pygame
from pygame.locals import *
import numpy as np
import pickle
from os import path
from copy import deepcopy




pygame.init()

clock = pygame.time.Clock()
fps = 60


screen_w =1000
screen_h=1000

screen=pygame.display.set_mode((screen_w,screen_h))
pygame.display.set_caption('test')


#define font
font_test=pygame.font.SysFont('Bauhaus 93',30)


#game variables
tile_size = 10
main_menu=True
level=1
game_over=0
game_over_ball=0
max_levels=2


#define colours
white=(255,255,255)

#load images here
skybox = pygame.image.load('img/skybox.png')
player_img = pygame.image.load('img/test_player.png')
skybox_img = pygame.transform.scale(skybox, (1000,1000))
r_img = pygame.image.load('img/R.png')
start_img = pygame.transform.scale(pygame.image.load('img/start.png'),(300,100))
quit_img = pygame.transform.scale(pygame.image.load('img/quit.png'),(300,100))



#level reset
def reset_level(level):
    balls.empty()
    goals.empty()
    if path.exists(f'levels/level{level}.plk'):
        pickle_in= open(f'levels/level{level}.plk','rb')
        world_data=pickle.load(pickle_in)
    return world_data
    




#text render
def draw_text(text,font,text_col,x,y):
    img=font.render(text,True,text_col)
    screen.blit(img,(x,y))






class Button():
    def __init__(self,x,y,image):
        self.image = image
        self.rect= self.image.get_rect()
        self.rect.x=x
        self.rect.y=y
        self.clicked=False
        

    def draw(self):
        action=False
        #get mouse pos
        pos=pygame.mouse.get_pos()
        
        #chech mouseover and clicked conditions
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0]==1 and self.clicked==False:
                action=True
                self.clicked=True
        if pygame.mouse.get_pressed()[0]==0:
            self.clicked=False
            

        screen.blit(self.image, self.rect)
        return action        




class Player():
    def __init__(self,world:World):
        self.reset(world)

    
    def update(self):
        dx=0
        dy=0
        
        #key press
        key=pygame.key.get_pressed()
        if key[pygame.K_r]:
            self.reset(self.world)


        if self.alive==True:
            if self.movement==0:
                #key press
                key=pygame.key.get_pressed()
                if key[pygame.K_UP] and self.jumped==False:
                    if self.on_the_ground==True:
                        self.vel_y=-10
                        self.jumped=True
                        self.on_the_ground=False
                if key[pygame.K_UP]==False:
                    self.jumped=False
                    
                if key[pygame.K_LEFT]:
                    if self.on_the_ground==True:
                        if self.l_counter==1:
                            if self.vel_x>-7:
                                self.vel_x-=2
                                self.l_counter=0
                        else: self.l_counter+=1
                        
                if key[pygame.K_RIGHT]: 
                    if self.on_the_ground==True:
                        if self.r_counter==1:
                            if self.vel_x<7:
                                self.vel_x+=2
                                self.r_counter=0
                        else: self.r_counter+=1
                #space+bll collision+not hit the ball yet
                if key[pygame.K_SPACE] and pygame.sprite.spritecollide(self,balls,False) and self.can_hit==True:
                     for ball in balls: 
                        if ball.vel_y==0 and ball.vel_x==0:
                            self.movement=1
                            self.can_hit=False


                #gravity+terminal vel
            
                if self.vel_y < 5:
                    if self.gravcounter==0:    
                        self.vel_y+=1
                        self.gravcounter=1
                    else:
                        self.gravcounter=0
            
                dy+= self.vel_y
                dx+= self.vel_x
                
                #check collision
                for tile in self.world.tile_list:
                    #collisions x 
                    if tile[1].colliderect(self.rect.x+dx,self.rect.y,self.width,self.height):
                        dx=0
                    #collisions y
                    if tile[1].colliderect(self.rect.x,self.rect.y+dy, self.width,self.height):
                        #check below ie jump
                        if self.vel_y<0:
                            dy=tile[1].bottom-self.rect.top
                            self.vel_y=0
                        #check above ie fall
                        elif self.vel_y>=0:
                            dy=tile[1].top-self.rect.bottom
                            self.vel_y=0
                            self.on_the_ground=True


                        #different frictions
                        if tile[2]==1:
                            if abs(self.vel_x) <1:
                                self.vel_x=0
                            elif self.vel_x>0:
                                self.vel_x-=1
                            elif self.vel_x<0:
                                self.vel_x+=1


                


                #update cords
                self.rect.x += dx
                self.rect.y += dy

                if self.rect.bottom > screen_h:
                    self.rect.bottom = screen_h
            


            elif self.movement==1: #ball hiting controlls
                #key press
                key=pygame.key.get_pressed()
                if key[pygame.K_UP]:
                    if self.wait_timer_up==2:
                        if self.power < 100:
                            self.power+=1
                            self.wait_timer_up=0
                    else:
                        self.wait_timer_up+=1
                if key[pygame.K_DOWN]:
                    if self.wait_timer_down==2:
                        if self.power > 0:
                            self.power-=1
                            self.wait_timer_down=0
                    else:
                        self.wait_timer_down+=1
                if key[pygame.K_LEFT]:
                    if self.wait_timer_left==2:
                        if self.angle < 180:
                            self.angle+=1
                            self.wait_timer_left=0
                    else:
                        self.wait_timer_left+=1
                if key[pygame.K_RIGHT]:
                    if self.wait_timer_right==2:
                        if self.angle > 0:
                            self.angle-=1
                            self.wait_timer_right=0
                    else:
                        self.wait_timer_right+=1
                if key[pygame.K_SPACE]==False:
                    self.can_hit=True

                if key[pygame.K_SPACE] and self.can_hit==True:
                    self.movement=0
                    for ball in balls:
                        ball.vel_x=np.cos(self.angle*np.pi/180)*self.power/5
                        ball.vel_y=-np.sin(self.angle*np.pi/180)*self.power/5


            #check collision goal
            if pygame.sprite.spritecollide(self, goals,False):
                globals()['game_over'] = 1
            else:
                globals()['game_over'] = 0
            
            if self.movement==1:
                cords=deepcopy(self.rect)
                if self.power<7:
                    screen.blit(self.power_imgs[0],(cords[0]-15,cords[1]))
                elif self.power<14:
                    screen.blit(self.power_imgs[1],(cords[0]-15,cords[1]))
                elif self.power<21:
                    screen.blit(self.power_imgs[2],(cords[0]-15,cords[1]))
                elif self.power<29:
                    screen.blit(self.power_imgs[3],(cords[0]-15,cords[1]))
                elif self.power<36:
                    screen.blit(self.power_imgs[4],(cords[0]-15,cords[1]))
                elif self.power<43:
                    screen.blit(self.power_imgs[5],(cords[0]-15,cords[1]))
                elif self.power<50:
                    screen.blit(self.power_imgs[6],(cords[0]-15,cords[1]))
                elif self.power<57:
                    screen.blit(self.power_imgs[7],(cords[0]-15,cords[1]))
                elif self.power<54:
                    screen.blit(self.power_imgs[8],(cords[0]-15,cords[1]))
                elif self.power<71:
                    screen.blit(self.power_imgs[9],(cords[0]-15,cords[1]))
                elif self.power<79:
                    screen.blit(self.power_imgs[10],(cords[0]-15,cords[1]))
                elif self.power<86:
                    screen.blit(self.power_imgs[11],(cords[0]-15,cords[1]))
                else:
                    screen.blit(self.power_imgs[12],(cords[0]-15,cords[1]))

        #draws player
        screen.blit(self.image[0],self.rect)


    def reset(self,world:World):
        for ball in balls:
            ball.kill()
            
        img = pygame.image.load('img/test_player.png')
        self.image = [pygame.transform.scale(img, (40,50))]
        self.rect=self.image[0].get_rect()
        self.rect.x = world.player_x
        self.rect.y = world.player_y
        self.width = self.image[0].get_width()
        self.height = self.image[0].get_height()
        self.vel_y=0
        self.vel_x=0
        self.jumped=False
        self.world=world
        self.gravcounter=0
        self.on_the_ground=True
        self.alive=True
        self.movement=0
        self.l_counter=0
        self.r_counter=0

        #power gauge
        self.power_imgs=[]
        for i in range(13):
            imag = pygame.image.load(f'img/power{i}.png')
            imag = pygame.transform.scale(imag,(10,30))
            self.power_imgs.append(imag)

        self.angle=90
        self.power=100
        self.wait_timer_up=0
        self.wait_timer_down=0
        self.wait_timer_left=0
        self.wait_timer_right=0
        self.can_hit=True
        ball=Golf_Ball(self.world.ball_x, self.world.ball_y)
        balls.add(ball)











class World():
    def __init__(self, data):

        self.tile_list=[]

        #load tile images
        tile_dirt=pygame.image.load('img/dirt.png')

        row_count=0
        for row in data:
            col_count=0
            for tile in row:
                if tile ==1:
                    img = pygame.transform.scale(tile_dirt, (tile_size, tile_size))
                    img_rect = img.get_rect()
                    img_rect.x=col_count * tile_size
                    img_rect.y=row_count * tile_size
                    tile=(img,img_rect,1)
                    self.tile_list.append(tile)
                elif tile == 'p':
                    self.player_x=col_count * tile_size
                    self.player_y=row_count * tile_size
                elif tile=='b':
                    self.ball_x=col_count * tile_size
                    self.ball_y=row_count * tile_size
                elif tile=='g':
                    goal=Goal(col_count*tile_size,row_count * tile_size)
                    goals.add(goal)
                
                col_count+=1
            row_count+=1

    def draw(self):
        for tile in self.tile_list:
            screen.blit(tile[0],tile[1])
        





class Goal(pygame.sprite.Sprite):
    def __init__(self,x,y, *groups):
        super().__init__(*groups)
        img=pygame.image.load('img/goal.png')
        self.image=pygame.transform.scale(img,(20,70))
        self.rect=self.image.get_rect()
        self.rect.x=x
        self.rect.y=y-50









class Golf_Ball(pygame.sprite.Sprite):
    def __init__(self,x,y):
        pygame.sprite.Sprite.__init__(self)
        img = pygame.image.load('img/ender_pearl.png')
        self.ball_R = 10
        self.image = pygame.transform.scale(img, (self.ball_R,self.ball_R))
        self.rect=self.image.get_rect()

        arrowimg = pygame.image.load('img/arrow.png')
        self.arrow_h=60
        self.arrow_w=20
        self.arrow_img = pygame.transform.scale(arrowimg, (self.arrow_w,self.arrow_h))



        self.rect.x=x
        self.rect.y=y

        self.width = self.image.get_width()
        self.height = self.image.get_height()

        self.vel_y=0
        self.vel_x=0

        self.jumped=False
        self.gravcounter=0
        self.on_the_ground=True




    def update(self):
        dx=0
        dy=0

        #gravity+terminal vel
        
        if self.vel_y < 5:
            if self.gravcounter==0:
                self.vel_y+=1
                self.gravcounter=1
            else:
                self.gravcounter=0

        

        #check collision
        for tile in world.tile_list:
            #collisions x 
                if tile[1].colliderect(self.rect.x+self.vel_x,self.rect.y,self.width,self.height):
                    self.vel_x = -self.vel_x


                #collisions y
                if tile[1].colliderect(self.rect.x,self.rect.y+self.vel_y, self.width,self.height):
                    #check below ie jump
                    if self.vel_y<0:
                        self.vel_y= -self.vel_y
                        
                    #check above ie fall
                    elif self.vel_y>=0:
                        if self.vel_y<5:
                            self.vel_y=0
                        else:    self.vel_y= -self.vel_y/2
                        self.on_the_ground=True
                        
                        #different frictions
                        if tile[2]==1:
                            if abs(self.vel_x) <5:
                                self.vel_x=0
                            elif self.vel_x>0:
                                self.vel_x-=5
                            elif self.vel_x<0:
                                self.vel_x+=5
                        
        dy+= self.vel_y
        dx+= self.vel_x
        

        if pygame.sprite.spritecollide(player,balls,False) and player.movement==0 and self.vel_x==0 and self.vel_y==0:
            player.can_hit==True

        if pygame.sprite.spritecollide(self,goals,False):
            globals()['game_over_ball']=1
        else:
            globals()['game_over_ball']=0

        #update cords
        self.rect.x += dx
        self.rect.y += dy
        if self.rect.bottom > screen_h:
            self.rect.bottom = screen_h
        


        #targetting arrow
        if player.movement==1:
            cords=deepcopy(self.rect.center)
            if player.angle<=90:
                screen.blit(pygame.transform.rotate(self.arrow_img, player.angle-90), (cords[0]-self.ball_R/2+self.arrow_w*np.cos(player.angle*np.pi/180)/2.5,cords[1]-self.arrow_h*np.sin(player.angle*np.pi/180)-self.arrow_w/3*np.cos(player.angle*np.pi/180)))
            else:
                screen.blit(pygame.transform.rotate(self.arrow_img, player.angle-90), (cords[0]+self.arrow_h*np.cos(player.angle*np.pi/180),cords[1]-self.arrow_h*np.sin(player.angle*np.pi/180)+self.arrow_w/1.5*np.cos(player.angle*np.pi/180)))

        #draws ball
        screen.blit(self.image,self.rect)
    








#define sprite groups
balls=pygame.sprite.Group()
goals=pygame.sprite.Group()


#load level data and crate world
if path.exists(f'levels/level{level}.plk'):
    pickle_in= open(f'levels/level{level}.plk','rb')
    world_data=pickle.load(pickle_in)
world=World(world_data)

player=Player(world)

#buttons
restart_button = Button(screen_w/40, screen_h/40, r_img)
start_button = Button(screen_w/2-325, screen_h/2,start_img)
quit_button = Button(screen_w/2+25, screen_h/2,quit_img)

run = True
while run==True:

    clock.tick(fps)

    screen.blit(skybox_img,(0,0))
    if main_menu==True:
        if quit_button.draw():
            run=False
        if start_button.draw():
            main_menu=False
    else:
        world.draw()
        player.update()
        balls.update()
        goals.draw(screen)
        
        if restart_button.draw():
            player.reset(world)

        #player won
        if game_over==1 and game_over_ball==1:
            level += 1
            if level <= max_levels:
                world_data=[]
                world=World(reset_level(level))
                game_over=0
                game_over_ball=0
                player.reset(world)
    

        #test
        #draw_text(f'A={player.angle}',font_test,white,900,10)
        #draw_text(f'p={player.power}',font_test,white,900,60)
        #draw_text(f'g={game_over}',font_test,white,900,110)


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run=False

    pygame.display.update()

pygame.quit()