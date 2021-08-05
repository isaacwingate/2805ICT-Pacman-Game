import pygame
import sys
from settings import *

pygame.init()
vec = pygame.math.Vector2


class App:
	def __init__(self):
		self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
		self.clock = pygame.time.Clock()
		self.running = True
		self.state = 'mMenu'
		self.sel = 'play'
		self.cellWidth = WIDTH//28
		self.cellHeight = HEIGHT//30

		self.load()

	def run(self):
		while self.running:
			if self.state == 'mMenu':
				self.mMenu_events()
				self.mMenu_update()
				self.mMenu_draw()
			elif self.state == 'playing':
				self.game_events()
				self.game_update()
				self.game_draw()
			else:
				self.running = False
			self.clock.tick(FPS)
		pygame.quit()
		sys.exit()

#########################	Helper Functions 	#########################
	# Text Renderer
	def drawText (self, text, screen, pos, font, size, color, center = False):
		nFont=pygame.font.Font(font, size)
		nText=nFont.render(text, 0, color)
		textSize = nText.get_size()
		if center:
			pos[0] = pos[0]-textSize[0]//2
			pos[1] = pos[1]-textSize[1]//2
		screen.blit(nText, pos)

	def load(self):
		self.mazeBG = pygame.image.load('assets/img/maze.png')
		self.mazeBG = pygame.transform.scale(self.mazeBG, (WIDTH, HEIGHT))

	def drawGrid(self):
		for i in range(WIDTH//self.cellWidth):
			pygame.draw.line(self.screen, gray, (i*self.cellWidth,0),(i*self.cellWidth,HEIGHT))
		for i in range(HEIGHT//self.cellHeight):
			pygame.draw.line(self.screen, gray, (0, i*self.cellHeight),(WIDTH, i*self.cellHeight))

	#########################	Main Menu State 	#########################

	def mMenu_events(self):
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				self.running = False
			if event.type==pygame.KEYDOWN:
				if event.key==pygame.K_UP:
					if self.sel == "config":
						self.sel = "play"
					elif self.sel == "exit":
						self.sel = "config"
				if event.key==pygame.K_DOWN:
					if self.sel == "play":
						self.sel = "config"
					elif self.sel == "config":
						self.sel = "exit"
				if event.key==pygame.K_RETURN:
					if self.sel =="play":
						self.state = 'playing'
					elif self.sel == "config":
						print("config")
					elif self.sel =="exit":
						self.running = False


	def mMenu_update(self):
		pass

	def mMenu_draw(self):
		self.screen.fill(black)

		if self.sel == 'play':
			self.drawText('Play',self.screen, [WIDTH//2, HEIGHT//2], MENU_FONT, MENU_FONT_LARGE, yellow, True)
		else:
			self.drawText('Play',self.screen, [WIDTH//2, HEIGHT//2], MENU_FONT, MENU_FONT_LARGE, white, True)
		if self.sel == 'config':
			self.drawText('Configure',self.screen, [WIDTH//2, HEIGHT//2+65], MENU_FONT, MENU_FONT_LARGE, yellow, True)
		else:
			self.drawText('Configure',self.screen, [WIDTH//2, HEIGHT//2+65], MENU_FONT, MENU_FONT_LARGE, white, True)
		if self.sel == 'exit':
			self.drawText('Exit',self.screen, [WIDTH//2, HEIGHT//2+130], MENU_FONT, MENU_FONT_LARGE, yellow, True)
		else:
			self.drawText('Exit',self.screen, [WIDTH//2, HEIGHT//2+130], MENU_FONT, MENU_FONT_LARGE, white, True)


		#Course and students
		self.drawText("2805ICT - 2021", self.screen, [0,750], MENU_FONT, MENU_FONT_SMALL, blue)
		self.drawText("Harry Rowe", self.screen, [0,780], MENU_FONT, MENU_FONT_SMALL, blue)
		self.drawText("Isaac Wilson",self.screen, [0,810], MENU_FONT, MENU_FONT_SMALL, blue)
		self.drawText("Isaac Wingate", self.screen, [0,840], MENU_FONT, MENU_FONT_SMALL, blue)
		self.drawText("Krittawat Auskulsuthi", self.screen, [0,870], MENU_FONT, MENU_FONT_SMALL, blue)

		#high score
		self.drawText('HIGH SCORE:', self.screen, [4,0], MENU_FONT, 14, white)

		pygame.display.update()

	#########################	Playing State 	#########################

	def game_events(self):
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				self.running = False

	def game_update(self):
		pass

	def game_draw(self):
		self.screen.blit(self.mazeBG, (0,0))
		self.drawGrid()

		pygame.display.update()