#Utility Functions Used

import pygame


#Function to Display Text in Game Window
def displayText(screen, text, x, y, size = 30, color = [200,25,20], font_type = 'capture it'):

	try:
		text = str(text)
		font = pygame.font.SysFont(font_type, size)
		text = font.render(text, True, color)
		screen.blit(text, (x, y))

	except Exception as e:
		print("Font Error!")
		raise e


#Function to Display Centered Text in Game Window
def displayTextCentered(screen, text, y, size = 30, color = [200,25,20], font_type = 'capture it', screen_width = 1280):

	try:
		text = str(text)
		font = pygame.font.SysFont(font_type, size)
		rendered_text = font.render(text, True, color)
		text_width = rendered_text.get_width()
		x = (screen_width - text_width) // 2
		screen.blit(rendered_text, (x, y))

	except Exception as e:
		print("Font Error!")
		raise e