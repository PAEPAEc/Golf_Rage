from __future__ import annotations
import pygame
from pygame.locals import *





pygame.init()

clock = pygame.time.Clock()
fps = 60


screen_w =1000
screen_h=1000

screen=pygame.display.set_mode((screen_w,screen_h))
pygame.display.set_caption('test')

#game variables
tile_size = 50


#load images here
skybox = pygame.image.load('img/skybox.png')
player_img = pygame.image.load('img/test_player.png')
skybox_img = pygame.transform.scale(skybox, (1000,1000))

class Player():
    def __init__(self,x,y,world:World):
        img = pygame.image.load('img/test_player.png')
        self.image = pygame.transform.scale(img, (40,50))
        self.rect=self.image.get_rect()
        self.rect.x=x
        self.rect.y=y
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.vel_y=0
        self.jumped=False
        self.world=world
        self.gravcounter=0
        self.on_the_ground=True
    
    def update(self):
        dx=0
        dy=0
        
        #key press
        key=pygame.key.get_pressed()
        if key[pygame.K_SPACE] and self.jumped==False:
            if self.on_the_ground==True:
                self.vel_y=-10
                self.jumped=True
                self.on_the_ground=False
        if key[pygame.K_SPACE]==False:
            self.jumped=False
        if key[pygame.K_LEFT]:
            dx-=5
        if key[pygame.K_RIGHT]: 
            dx+=5

        #gravity+terminal vel
        
        if self.vel_y < 10:
            if self.gravcounter==0:    
                self.vel_y+=1
                self.gravcounter=1
            else:
                self.gravcounter=0
        


        dy+= self.vel_y
        

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
                
                
                






        #update cords
        self.rect.x += dx
        self.rect.y += dy

        if self.rect.bottom > screen_h:
            self.rect.bottom = screen_h


        #draws player
        screen.blit(self.image,self.rect)



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
                    tile=(img,img_rect)
                    self.tile_list.append(tile)
                col_count+=1
            row_count+=1

    def draw(self):
        for tile in self.tile_list:
            screen.blit(tile[0],tile[1])
















class Golf_Ball():
    def __init__(self,x,y,world):
        img = pygame.image.load('img/ender_pearl.png')
        self.image = pygame.transform.scale(img, (10,10))
        self.rect=self.image.get_rect()

        self.rect.x=x
        self.rect.y=y

        self.width = self.image.get_width()
        self.height = self.image.get_height()

        self.vel_y=0
        self.vel_x=0

        self.jumped=False
        self.world=world
        self.gravcounter=0
        self.on_the_ground=True





























world_data=[
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
]



world=World(world_data)
player = Player(100,screen_h-130,world)


run = True
while run==True:

    clock.tick(fps)

    screen.blit(skybox_img,(0,0))
    world.draw()
    player.update()

    
    
    if player.on_the_ground==True:
        tile_dirt=pygame.image.load('img/dirt.png')
        img = pygame.transform.scale(tile_dirt, (tile_size, tile_size))
        img_rect = img.get_rect()
        img_rect.x=0
        img_rect.y=0
        tile=(img,img_rect)
        screen.blit(tile[0],tile[1])
    else: 
        tile_dirt=pygame.image.load('img/end_stone.png')
        img = pygame.transform.scale(tile_dirt, (tile_size, tile_size))
        img_rect = img.get_rect()
        img_rect.x=0
        img_rect.y=0
        tile=(img,img_rect)
        screen.blit(tile[0],tile[1])


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run=False

    pygame.display.update()

pygame.quit()