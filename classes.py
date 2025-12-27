# Classes used for Kurochan

import pygame, math
from random import randint

pygame.mixer.init()

class BaseClass(pygame.sprite.Sprite): #pygame.sprite.Sprite : Base class for visible game objects

	allsprites = pygame.sprite.Group()   	# Store list of Sprites (Container class to hold & manage multiple Sprite objects)

	def __init__(self, x, y, image_string):


		pygame.sprite.Sprite.__init__(self)
		BaseClass.allsprites.add(self)   	# Add current object to sprite list

		self.image = pygame.image.load(image_string)
		
		self.rect = self.image.get_rect()	# Image Boundary
		self.rect.x = x
		self.rect.y = y

		self.width = self.rect.width
		self.height = self.rect.height

	def destroy(self, ClassName):

		ClassName.List.remove(self)
		BaseClass.allsprites.remove(self)
		del self


	

class Kuro(BaseClass):						# Define Kurochan

	List = pygame.sprite.Group()
	go_right = True

	def __init__(self, x, y, image_string):

		BaseClass.__init__(self, x, y, image_string)
		Kuro.List.add(self)

		self.velx = 0
		self.vely = 0
		self.jump_velocity = -24
		self.gravity = 0.8

		self.health = 1000

		self.jump = False
		self.on_ground = True

	def motion(self, SCREENWIDTH, SCREENHEIGHT):

		predicted_location = self.rect.x + self.velx	# Prevent out of bound Movement

		if predicted_location < 0:
			self.velx = 0
		elif predicted_location + self.width > SCREENWIDTH:
			self.velx = 0

		self.rect.x += self.velx

		self.__jump(SCREENHEIGHT)


	def __jump(self, SCREENHEIGHT):					#Jump Motion with gravity

		ground_level = SCREENHEIGHT - 50

		if self.jump and self.on_ground:
			self.vely = self.jump_velocity
			self.on_ground = False

		if not self.on_ground:
			self.vely += self.gravity
			self.rect.y += self.vely

			if self.rect.y + self.height >= ground_level:
				self.rect.y = ground_level - self.height
				self.vely = 0
				self.on_ground = True
				self.jump = False


class KuroBeam(pygame.sprite.Sprite):

	List = pygame.sprite.Group()
	nor_list = []
	damage = 30
	kurogun = pygame.mixer.Sound("Audio/KuroGun.wav")

	def __init__(self, x, y, image_string, direction):

		pygame.sprite.Sprite.__init__(self)

		pygame.mixer.Sound.set_volume(KuroBeam.kurogun, 0.5)
		
		self.image = pygame.image.load(image_string)
		
		self.rect = self.image.get_rect()	# Image Boundary
		self.velx = None

		if direction:
			self.rect.x = x + 100			#Position Beam Origin Correctly
		else:
			self.rect.x = x

		self.rect.y = y + 75				#Position Beam Origin Correctly

		self.width = self.rect.width
		self.height = self.rect.height

		try:
			last_beam = KuroBeam.nor_list[-1]
			gap = abs(self.rect.x - last_beam.rect.x)

			if(gap < 2*self.width):
				return
		except Exception:
			pass

		KuroBeam.kurogun.play()

		KuroBeam.List.add(self)
		KuroBeam.nor_list.append(self)


	@staticmethod
	def movement(SCREENWIDTH):

		for beam in KuroBeam.List:
			beam.rect.x += beam.velx
			if beam.rect.x > 2*SCREENWIDTH or beam.rect.x < -SCREENWIDTH:
				beam.destroy()


	def destroy(self):
		KuroBeam.List.remove(self)
		KuroBeam.nor_list.remove(self)
		del self


class Fly(BaseClass):

	List = pygame.sprite.Group()
	DeadFly = []
	count = 0
	total = 0

	def __init__(self, x, y, image_string, totalframes=0):

		BaseClass.__init__(self, x, y, image_string)
		Fly.List.add(self)
		Fly.total += 1

		# Progressive speed scaling based on game time
		base_speed = randint(1, 4)
		speed_multiplier = 1 + (totalframes / 10000.0)
		speed_multiplier = min(speed_multiplier, 2.0)

		self.velx = int(base_speed * speed_multiplier)
		self.vely = 3
		self.amplitude = randint(50,150)
		self.period = randint(3,4)/100.0

		self.health = 100

		r = randint(1,2)

		if r == 1:
			self.image = pygame.transform.flip(self.image, True, False)
			self.velx = -self.velx
		

	@staticmethod
	def update_all(SCREENWIDTH, SCREENHEIGHT):

		for fly in Fly.List:

			fly.fly(SCREENWIDTH)

			if fly.health <= 0:

				fly.image = pygame.image.load("Images/deadfly.png")
				if fly.velx < 0:
					fly.image = pygame.transform.flip(fly.image, True, False)
				fly.velx = 0
				fly.fall_velocity = 0
				fly.gravity = 0.5

				Fly.DeadFly.append(fly)					#Keep List Of Dead Flies.
				Fly.List.remove(fly)
				Fly.count += 1
				Fly.total -= 1

		for fly in Fly.DeadFly:							#Drop Dead Flies with gravity.
			fly.fall_velocity += fly.gravity
			fly.rect.y += fly.fall_velocity
			if fly.rect.y > SCREENHEIGHT:
				Fly.DeadFly.remove(fly)
				fly.destroy(Fly)


	def fly(self, SCREENWIDTH):

		if self.rect.x + self.width > SCREENWIDTH or self.rect.x < 0:
			self.image = pygame.transform.flip(self.image, True, False)
			self.velx = -self.velx

		self.rect.x += self.velx
				# Give fly a sine wave motion => a * sin(bx) + y
		self.rect.y = self.amplitude * math.sin(self.period * self.rect.x) + 250



class Boss(BaseClass):

	List = pygame.sprite.Group();
	count = 0

	def __init__(self, x, y, image_string):

		BaseClass.__init__(self, x, y, image_string)
		Boss.List.add(self)

		self.health = 2000

		self.velx = -2
		self.vely = 0
	

	@staticmethod
	def update_all(SCREENWIDTH, SCREENHEIGHT):

		for boss in Boss.List:

			boss.rect.x += boss.velx
			boss.rect.y += boss.vely
			if boss.rect.x <= 800 or boss.rect.x + boss.rect.width > SCREENWIDTH:
				boss.velx = -boss.velx

			if boss.health <= 0:
				boss.velx = 0
				boss.vely = 5
			if boss.rect.y > SCREENHEIGHT:
				boss.destroy(Boss)
				Boss.count += 1



class BossAttack(BaseClass):

	List = pygame.sprite.Group()
	damage = 200
	petrabeam = pygame.mixer.Sound("Audio/petrabeam.wav")
	pygame.mixer.Sound.set_volume(petrabeam, 0.7)

	def __init__(self, x, y, image_string):
		
		BaseClass.__init__(self, x, y, image_string)
		BossAttack.List.add(self)
		self.rect.x -= self.rect.width
		self.endurance = 100
		self.velx = -4
		BossAttack.petrabeam.play()


	@staticmethod
	def movement(SCREENWIDTH):

		for fire in BossAttack.List:

			fire.rect.x += fire.velx

			if fire.rect.x < -SCREENWIDTH:
				fire.destroy(BossAttack)
