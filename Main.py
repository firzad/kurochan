# PROJECT  F.I.R.E  -  Kurochan Beta v2.0

import pygame, sys, Functions
from classes import *
from process import process
from random import randint
from time import sleep

pygame.init()
pygame.mixer.init()

SCREENWIDTH,SCREENHEIGHT = 1280,720
screen = pygame.display.set_mode((SCREENWIDTH,SCREENHEIGHT),0,32)   #To initialize a window for display 
                                                                    #set_mode((height,width),flag,depth)

clock = pygame.time.Clock()             #To Keep constant Frame/Loop Speed (creates an object to help track time)
FPS = 24
totalframes = 0

kuro = Kuro(0, SCREENHEIGHT - 185, "Images/kuro.png")

background = pygame.image.load("Images/forest2.jpg") #Load new image from a file
pygame.mixer.music.load("Audio/spgr.wav")
pygame.mixer.music.play(-1)
pygame.mixer.music.set_volume(0.7)	     #Volume Values 0.1-1	

FLAG = True	

while True:          #Infinite Loop To keep Game Up
	
	while FLAG:
		screen.fill([0,0,0])
		Functions.displayText(screen, "KURO QUEST", 350, 200, 100, [255,255,255])
		Functions.displayText(screen, "Arrow Keys To Move Character", 300, 400, 40, [255,255,255],"monospace")
		Functions.displayText(screen, "Space To shoot", 450, 500, 40, [255,255,255], "monospace")
		Functions.displayText(screen, "Fly count shouldn't exceed 20. Beat The Boss.", 100, 600, 40, [255,255,255],"monospace")
		pygame.display.update()
		sleep(5)
		FLAG = False


	process(screen, kuro, FPS, totalframes, SCREENWIDTH, SCREENHEIGHT)

	#GAME LOGIC
      
	kuro.motion(SCREENWIDTH, SCREENHEIGHT)
	Fly.update_all(SCREENWIDTH, SCREENHEIGHT          )
	Boss.update_all(SCREENWIDTH, SCREENHEIGHT)            
	KuroBeam.movement(SCREENWIDTH)
	BossAttack.movement(SCREENWIDTH)
	totalframes +=1

	if kuro.health <= 0 or Fly.total >= 20:
		pygame.mixer.music.stop()
		sleep(1)
		screen.blit(pygame.image.load("Images/GameOver.jpg"), (0, 0))
		pygame.display.update()
		sleep(5)
		pygame.quit()
		sys.exit()


	#GAME LOGIC
	#-----------------#  
	#DRAW

	screen.blit(background, (0,0))			#Set Game BackGround
	BaseClass.allsprites.draw(screen)		#Draw All Elements
	KuroBeam.List.draw(screen)
	# Functions.displayText(screen, "H E A L T H :- {0}".format(kuro.health), 10, 0)
	Functions.displayText(screen, "C O U N T :- {0}".format(Fly.total), 1000, 0)
	# Functions.displayText(screen, "S C O R E :- {0}".format(Fly.count*5), 500, 0)
	pygame.display.flip() 					#Update Screen


	#DRAW 
	#-----------------#