#Processing for Kurochan 

import pygame, sys, classes,easygui
from random import randint


def process(screen, kuro, FPS, totalframes, SCREENWIDTH, SCREENHEIGHT):

	#PROCESSING

	for event in pygame.event.get():        #Functionality To Close Window
		if event.type == pygame.QUIT:
			# easygui.msgbox('Flies Fried: ' + str(classes.Fly.count),'COUNT')
			# easygui.msgbox('The Score Is: ' + str(classes.Fly.count*5 + classes.Boss.count*100) + '!!!','SCOREBOARD')
			pygame.quit()
			sys.exit()


	# if classes.Fly.total >= 20:
	# 	pygame.quit()
	# 	sys.exit()

	keys = pygame.key.get_pressed()

	if keys[pygame.K_RIGHT]:									#Key Mappings
		kuro.image = pygame.image.load("Images/kuro.png")
		kuro.velx = 5
		classes.Kuro.go_right = True		
	elif keys[pygame.K_LEFT]:
		kuro.image = pygame.image.load("Images/kuroflp.png")
		kuro.velx = -5
		classes.Kuro.go_right = False
	else:
		kuro.velx = 0

	if keys[pygame.K_UP]:
		kuro.jump = True

	if keys[pygame.K_SPACE]:
		b = classes.KuroBeam(kuro.rect.x, kuro.rect.y, "Images/blright.png", kuro.go_right)
		
		if kuro.go_right:					#Direction of Kuro Beam
			b.velx = 8
		else:
			b.image = pygame.transform.flip(b.image, True, False)
			b.velx =  -8

	# if keys[pygame.K_RETURN] and classes.KuroShuriken.count>0:
	# 	c = classes.KuroShuriken(kuro.rect.x, kuro.rect.y, "Images/shkn.png", kuro.go_right)

	# 	if kuro.go_right:					#Direction of Kuro Beam
	# 		c.velx = 8
	# 	else:
	# 		c.image = pygame.transform.flip(c.image, True, False)
	# 		c.velx =  -8



	spawn(FPS, totalframes, SCREENWIDTH, SCREENHEIGHT)
	attack(FPS, totalframes)
	collisions()


	#PROCESSING


def spawn(FPS, totalframes, SCREENWIDTH, SCREENHEIGHT):				#AutoSpawn Flies

	interval = FPS * 2

	boss_interval = FPS * 25

	r = randint(1,3)		#Random X coordinate
	t = randint(1,3)		#Random Fly Image
	s = randint(1,3)		#Random Y coordinate
	x, y = 10, 350


	if t == 1:
		img = "Images/fly1.png"
	elif t == 2:
		img = "Images/fly2.png"
	else:
		img = "Images/fly3.png"

	boss_img = "Images/boss.png"

	if r == 2:
		x = 1205
	elif r == 3:
		x = 590

	if s == 2:
		y = 450
	elif s == 3:
		y = 250

	if totalframes % interval == 0:
		classes.Fly(x, y, img)
	if totalframes == boss_interval:
		classes.Boss(SCREENWIDTH-245, SCREENHEIGHT-250, boss_img)



def attack(FPS, totalframes):

	r = randint(5,15)
	interval = FPS * r

	for boss in classes.Boss.List:
		if totalframes % interval == 0:
			b = classes.BossAttack(boss.rect.x, boss.rect.y+boss.rect.width/2, "Images/petrabeam.png")


def collisions():

	for kuro in classes.Kuro.List:
		if pygame.sprite.spritecollide(kuro, classes.Boss.List, False):
			kuro.velx = 0
			kuro.rect.x -= 2

	for fly in classes.Fly.List:
		if pygame.sprite.spritecollide(fly, classes.KuroBeam.List, False):  #Detect collision bwn Beam and Flies
			fly.health -= classes.KuroBeam.damage

	for beam in classes.KuroBeam.List:
		if pygame.sprite.spritecollide(beam, classes.Fly.List, False):
			beam.rect.x = 2 * -beam.rect.width
			beam.destroy()
			
	for boss in classes.Boss.List:

		if pygame.sprite.spritecollide(boss, classes.KuroBeam.List, False): #Detect collision bwn Beam and Boss
			boss.health -= 25

	for boss in classes.Boss.List:
		if pygame.sprite.spritecollide(boss, classes.Kuro.List, False):
 			boss.velx = -boss.velx

	for beam in classes.KuroBeam.List:
		if pygame.sprite.spritecollide(beam, classes.Boss.List, False) or pygame.sprite.spritecollide(beam, classes.BossAttack.List, False):
			beam.rect.x = 2 * -beam.rect.width
			beam.destroy()

	for kuro in classes.Kuro.List:
		if pygame.sprite.spritecollide(kuro, classes.BossAttack.List, False):
			kuro.health -= classes.BossAttack.damage

	for fire in classes.BossAttack.List:
		if pygame.sprite.spritecollide(fire, classes.Kuro.List, False):
			fire.destroy(classes.BossAttack)
		if pygame.sprite.spritecollide(fire, classes.KuroBeam.List, False):
			fire.endurance -= 2*classes.KuroBeam.damage



