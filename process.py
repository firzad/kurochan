#Processing for Kurochan

import pygame, sys, classes, math
from random import randint

# Movement Constants
KURO_SPEED = 8
BEAM_SPEED = 14

# Cache images to avoid repeated loading
kuro_img_right = None
kuro_img_left = None

def init_images():
	global kuro_img_right, kuro_img_left
	if kuro_img_right is None:
		kuro_img_right = pygame.image.load("Images/kuro.png")
		kuro_img_left = pygame.image.load("Images/kuroflp.png")

def process(screen, kuro, FPS, totalframes, SCREENWIDTH, SCREENHEIGHT):
	init_images()

	pause_pressed = False

	# Event Handling
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			sys.exit()
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_p or event.key == pygame.K_ESCAPE:
				pause_pressed = True

	keys = pygame.key.get_pressed()

	# Character Movement
	if keys[pygame.K_RIGHT]:
		kuro.image = kuro_img_right
		kuro.velx = KURO_SPEED
		classes.Kuro.go_right = True
	elif keys[pygame.K_LEFT]:
		kuro.image = kuro_img_left
		kuro.velx = -KURO_SPEED
		classes.Kuro.go_right = False
	else:
		kuro.velx = 0

	# Jump
	if keys[pygame.K_UP]:
		kuro.jump = True

	# Shoot Beam
	if keys[pygame.K_SPACE]:
		b = classes.KuroBeam(kuro.rect.x, kuro.rect.y, "Images/blright.png", kuro.go_right)
		b.velx = BEAM_SPEED if kuro.go_right else -BEAM_SPEED
		if not kuro.go_right:
			b.image = pygame.transform.flip(b.image, True, False)

	# Pause (event-based to prevent toggle spam)
	if pause_pressed:
		return "PAUSE_TOGGLE"

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

	# Progressive difficulty - spawn rate increases over time
	base_interval = FPS * 2.5
	min_interval = FPS * 0.8
	difficulty_factor = 0.0001
	interval = max(min_interval, base_interval * math.exp(-difficulty_factor * totalframes))
	interval = int(interval)

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

	if totalframes % interval == 0 and totalframes > 0:
		classes.Fly(x, y, img, totalframes)
	if totalframes == boss_interval:
		classes.Boss(SCREENWIDTH-245, SCREENHEIGHT-250, boss_img)



def attack(FPS, totalframes):

	# Progressive boss attack frequency
	base_min, base_max = 8, 15
	min_min, min_max = 3, 7

	if totalframes > 600:
		progress = min((totalframes - 600) / 1200.0, 1.0)
		current_min = int(base_min - (base_min - min_min) * progress)
		current_max = int(base_max - (base_max - min_max) * progress)
	else:
		current_min, current_max = base_min, base_max

	r = randint(current_min, current_max)
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



