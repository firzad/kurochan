# PROJECT  F.I.R.E  -  Kurochan Beta v2.0

import pygame, sys, Functions
from classes import *
from process import process

pygame.init()
pygame.mixer.init()

# Game Constants
SCREENWIDTH, SCREENHEIGHT = 1280, 720
FPS = 30

# Initialize Display
screen = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT), 0, 32)
pygame.display.set_caption("Kurochan Beta v2.0")
clock = pygame.time.Clock()

# Game Variables
totalframes = 0
kuro = Kuro(0, SCREENHEIGHT - 185, "Images/kuro.png")

# Load Assets Once
background = pygame.image.load("Images/forest2.jpg")
gameover_image = pygame.image.load("Images/GameOver.jpg")
kuro_image_right = pygame.image.load("Images/kuro.png")
kuro_image_left = pygame.image.load("Images/kuroflp.png")

# Initialize Music
pygame.mixer.music.load("Audio/spgr.wav")
pygame.mixer.music.play(-1)
pygame.mixer.music.set_volume(0.7)

# Game State Variables
GAME_STATE = "INTRO"
game_over_start_time = 0
show_game_over_menu = False
game_over_reason = ""

while True:

	# STATE: INTRO
	if GAME_STATE == "INTRO":
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()
			if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
				GAME_STATE = "PLAYING"

		screen.fill([0,0,0])
		Functions.displayTextCentered(screen, "KURO QUEST", 120, 100, [255, 255, 255])

		Functions.displayTextCentered(screen, "CONTROLS", 250, 50, [200, 200, 255])
		Functions.displayTextCentered(screen, "Arrow Keys - Move Character", 330, 40, [255, 255, 255], "monospace")
		Functions.displayTextCentered(screen, "Up Arrow - Jump", 380, 40, [255, 255, 255], "monospace")
		Functions.displayTextCentered(screen, "Space - Shoot Beam", 430, 40, [255, 255, 255], "monospace")
		Functions.displayTextCentered(screen, "ESC / P - Pause", 480, 40, [255, 255, 255], "monospace")

		Functions.displayTextCentered(screen, "OBJECTIVE", 560, 50, [255, 200, 0])
		Functions.displayTextCentered(screen, "Keep fly count below 20 and defeat the Boss!", 625, 40, [255, 255, 255])

		Functions.displayTextCentered(screen, "Press any key to start", 685, 38, [100, 255, 100])
		pygame.display.update()
		clock.tick(60)
		continue

	# STATE: PAUSED
	if GAME_STATE == "PAUSED":
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				sys.exit()
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_p or event.key == pygame.K_ESCAPE:
					GAME_STATE = "PLAYING"
				elif event.key == pygame.K_q:
					pygame.quit()
					sys.exit()

		# Create dark overlay for better text visibility
		overlay = pygame.Surface((SCREENWIDTH, SCREENHEIGHT))
		overlay.set_alpha(180)
		overlay.fill((0, 0, 0))
		screen.blit(overlay, (0, 0))

		Functions.displayTextCentered(screen, "PAUSED", 280, 80, [255, 255, 0])
		Functions.displayTextCentered(screen, "Press ESC or P to Resume", 400, 45, [255, 255, 255])
		Functions.displayTextCentered(screen, "Press Q to Quit", 470, 45, [255, 100, 100])
		pygame.display.update()
		clock.tick(30)
		continue

	# STATE: GAME_OVER
	if GAME_STATE == "GAME_OVER":
		if game_over_start_time == 0:
			pygame.mixer.music.stop()
			game_over_start_time = pygame.time.get_ticks()
			show_game_over_menu = False

		final_score = Fly.count * 5 + Boss.count * 100
		elapsed_time = pygame.time.get_ticks() - game_over_start_time

		if elapsed_time < 2000:
			# Phase 1: Show only the GameOver PNG image (0-2 seconds)
			screen.blit(gameover_image, (0, 0))
		else:
			# Phase 2: Show black screen with game over menu (after 2 seconds)
			show_game_over_menu = True
			screen.fill([0, 0, 0])

			Functions.displayTextCentered(screen, "GAME OVER", 100, 100, [255, 0, 0])
			Functions.displayTextCentered(screen, "Reason: {0}".format(game_over_reason), 220, 42, [255, 200, 0])

			Functions.displayTextCentered(screen, "STATS", 300, 50, [100, 200, 255])
			Functions.displayTextCentered(screen, "Final Score: {0}".format(final_score), 380, 48, [255, 255, 255])
			Functions.displayTextCentered(screen, "Flies Defeated: {0}".format(Fly.count), 450, 42, [200, 200, 200])
			Functions.displayTextCentered(screen, "Bosses Defeated: {0}".format(Boss.count), 510, 42, [200, 200, 200])

			Functions.displayTextCentered(screen, "Press R to Restart", 590, 45, [0, 255, 0])
			Functions.displayTextCentered(screen, "Press Q to Quit", 650, 45, [255, 100, 100])

		pygame.display.update()

		if show_game_over_menu:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.quit()
					sys.exit()
				if event.type == pygame.KEYDOWN:
					if event.key == pygame.K_r:
						GAME_STATE = "PLAYING"
						totalframes = 0
						game_over_start_time = 0
						show_game_over_menu = False
						game_over_reason = ""

						BaseClass.allsprites.empty()
						Fly.List.empty()
						Fly.DeadFly.clear()
						Boss.List.empty()
						KuroBeam.List.empty()
						KuroBeam.nor_list.clear()
						BossAttack.List.empty()

						Fly.count = 0
						Fly.total = 0
						Boss.count = 0

						kuro = Kuro(0, SCREENHEIGHT - 185, "Images/kuro.png")

						pygame.mixer.music.play(-1)

					elif event.key == pygame.K_q:
						pygame.quit()
						sys.exit()
		else:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					pygame.quit()
					sys.exit()

		clock.tick(30)
		continue

	# STATE: PLAYING
	if GAME_STATE == "PLAYING":
		pause_signal = process(screen, kuro, FPS, totalframes, SCREENWIDTH, SCREENHEIGHT)

		if pause_signal == "PAUSE_TOGGLE":
			GAME_STATE = "PAUSED"
			continue

		kuro.motion(SCREENWIDTH, SCREENHEIGHT)
		Fly.update_all(SCREENWIDTH, SCREENHEIGHT)
		Boss.update_all(SCREENWIDTH, SCREENHEIGHT)
		KuroBeam.movement(SCREENWIDTH)
		BossAttack.movement(SCREENWIDTH)
		totalframes +=1

		if kuro.health <= 0:
			GAME_STATE = "GAME_OVER"
			game_over_reason = "Health Depleted"
			continue
		elif Fly.total >= 20:
			GAME_STATE = "GAME_OVER"
			game_over_reason = "Too Many Flies (20+)"
			continue

		screen.blit(background, (0,0))
		BaseClass.allsprites.draw(screen)
		KuroBeam.List.draw(screen)

		Functions.displayText(screen, "HEALTH: {0}".format(kuro.health), 10, 10, 35, [255, 0, 0])
		total_score = Fly.count * 5 + Boss.count * 100
		Functions.displayText(screen, "SCORE: {0}".format(total_score), 500, 10, 35, [255, 255, 0])
		Functions.displayText(screen, "COUNT: {0}".format(Fly.total), 1000, 10, 35, [255, 255, 255])

		pygame.display.flip()
		clock.tick(FPS)
