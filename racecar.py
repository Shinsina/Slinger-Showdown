import pygame
from pygame.sprite import Sprite
from pygame.math import Vector2
import math

class Racecar(Sprite):
    #A class to manage to racecar

    def __init__(self,sd_game):
        #Initialize the car and set its starting position
        super().__init__()

        #Base reference to the game screen
        self.screen = sd_game.screen
        self.screen_rect = sd_game.screen.get_rect()
        self.sd_game = sd_game

        #Audio channel setups for checkpoint and engine sound
        self.chan1 = pygame.mixer.Channel(1)
        self.chan2 = pygame.mixer.Channel(2)
        self.cpsound = pygame.mixer.Sound('Checkpoint.mp3')
        self.enginenoise = pygame.mixer.Sound('EngineNoise.wav')
        

        #Load the car image and get its rect
        self.original_image = pygame.image.load('racecar.png')
        self.original_image = pygame.transform.scale(self.original_image, (50,50))
        self.image = self.original_image
        self.rect = self.image.get_rect()
        self.angle = 0
        
        #Path that the car will follow onscreen
        self.carpoints = [(550,530), (850,515), (1055,282), (850,49), (550,34), (250,49), (45,282), (250,515)]
        self.ptp = [(300, -15), (205, -233), (-205, -233), (-300, -15), (-300, 15), (-205, 233), (205, 233), (300,15)]
        

        #Start the car at the start of the path
        self.rect.centerx = self.carpoints[0][0]
        self.rect.centery = self.carpoints[0][1]
        self.index = 0
        self.movement = self.ptp[self.index]
        self.movement = Vector2(self.movement[0],self.movement[1])
        self.distance = self.movement.length()
        self.movement.normalize_ip()

        #Store a decimal value for the car's horizontal and vertical positions
        self.x = float(self.rect.centerx)
        self.y = float(self.rect.centery)

        #Starting point offset
        self.x += self.movement[0]
        self.y += self.movement[1]

        #Store if moving is occuring
        self.is_moving = False

        #Total distance covered
        self.distancetotal = 0

        #Time Boosts
        self.timeboosts = 0

        #Lap counter
        self.lapcount = 0


    def update(self):
        if self.is_moving:
            #Keep the car on its track 
            self.x += 1.0*self.movement[0]
            self.y += 1.0*self.movement[1]
            self.rect.centerx = self.x
            self.rect.centery = self.y
        
        #If you reach a checkpoint do something
        if abs(self.carpoints[self.index][0]-abs(self.rect.centerx)) - abs(self.ptp[self.index][0]) == 0 or abs(self.carpoints[self.index][1]-abs(self.rect.centery)) - abs(self.ptp[self.index][1]) == 0:
            if(abs(self.carpoints[self.index][0]-abs(self.rect.centerx)) - abs(self.ptp[self.index][0])!=0): #If the x-value when checkpoint is hit is not what it's supposed to be
                self.x = self.carpoints[self.index+1][0] #Set the position to the proper value
            elif((abs(self.carpoints[self.index][1]-abs(self.rect.centery)) - abs(self.ptp[self.index][1]))!=0): #If the y-value when checkpoint is hit is not what it's supposed to be
                self.y = self.carpoints[self.index+1][1] #Set the position to the proper value
            if(self.index==7): #This is for the last checkpoint
                self.index = 0 #Reset counter
                self.movement = self.ptp[self.index]
                self.movement = Vector2(self.movement[0],self.movement[1]) #Make a vector to use for vector calculation later
                self.distance = self.movement.length() #Set distance to how far you moved
                #print(self.distance)
                self.distancetotal += int(self.distance) #Round distance to an int and add it to total distance
                #print(self.distancetotal)
                self.movement.normalize_ip() #Create a normal vector for the movement
                self.sd_game.timer += 10 #Increase timer by 10
                self.timeboosts += 1 #Increase number of boosts
                self.chan1.play(self.enginenoise) #Play engine sound
                self.chan2.play(self.cpsound) #Play checkpoint sound
                self.lapcount += 1 #Increment laps by 1
            else:
                self.index += 1 #Increment counter
                #print(self.index)
                self.movement = self.ptp[self.index]
                self.movement = Vector2(self.movement[0],self.movement[1]) #Make a vector to use for vector calculation later
                self.distance = self.movement.length() #Set distance to how far you moved
                self.distancetotal += int(self.distance) #Round distance to an int and add it to total distance
                #print(self.distancetotal)
                #print(self.distance)
                self.movement.normalize_ip() #Create a normal vector for the movement
                #print(self.movement)
                #print(self.angle)
                self.angle = -math.degrees(math.atan2(self.movement[1],self.movement[0])) #Calculate the angle to the next checkpoint in order to travel to it
                self.timeboosts += 1 #Increase number of boosts
                self.chan1.play(self.enginenoise) #Play engine sound
                self.chan2.play(self.cpsound) #play checkpoint sound 
                #if(self.index != 4):
                self.image = pygame.transform.rotate(self.original_image, self.angle) #For debugging move this inside the previous if, in terms of actual note, this rotates the car image appropriately based on previous calculation
                    #print(self.angle)
                    #self.rect = self.image.get_rect()
                            
    def blitme(self):
        self.screen.blit(self.image, self.rect) #Draw car to screen
        #pygame.gfxdraw.ellipse(self.screen, 550, 282, 515, 250, (0,0,0)) #DEBUG LINE
        #pygame.gfxdraw.filled_circle(self.screen, 550, 530, 5,(0,0,0,255)) #DEBUG LINE STARTING POINT
        #pygame.gfxdraw.filled_circle(self.screen, 850, 515, 5,(0,0,0,255)) #DEBUG LINE ENTRY T1
        #pygame.gfxdraw.filled_circle(self.screen, 1055, 282, 5,(0,0,0,255)) #DEBUG LINE CENTER T1 AND T2
        #pygame.gfxdraw.filled_circle(self.screen, 850, 49, 5,(0,0,0,255)) #DEBUG LINE EXIT T2
        #pygame.gfxdraw.filled_circle(self.screen, 550, 34, 5,(0,0,0,255)) #DEBUG LINE BACKSTRETCH
        #pygame.gfxdraw.filled_circle(self.screen, 250, 49, 5,(0,0,0,255)) #DEBUG LINE ENTRY T3
        #pygame.gfxdraw.filled_circle(self.screen, 45, 282, 5,(0,0,0,255)) #DEBUG LINE CENTER T3 AND T4
        #pygame.gfxdraw.filled_circle(self.screen, 250, 515, 5,(0,0,0,255)) #DEBUG LINE EXIT T4
 