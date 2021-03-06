import pygame
import math
import random
import time
import threading
from settings import *

INF = 9999999
vec = pygame.math.Vector2

class Ghost_Template:
	def __init__(self, app, pos, spriteSheet, color = "red"):
		self.app = app
		self.posGrid = pos
		self.posPx = self.get_posPx()
		self.color = color
		self.speed = 1.25
		self.direction = vec(self.speed,0)
		self.nextDirection = None
		self.spriteSheet = spriteSheet
		self.smartMoveCount = 0
		self.dumbMoveCount = 0
		self.atBase = True
		self.eaten = False
		self.imgIndex = 0
		self.ghostColours = []
		self.imgArr = []
		self.getSprite()
		self.img = self.imgArr[0]
		self.rect=pygame.Rect(self.posGrid[0],self.posGrid[1],self.app.cellWidth,self.app.cellHeight)

		white = pygame.transform.smoothscale((self.spriteSheet.grabImage(10, 4, 16, 16)), (self.app.cellWidth-1, self.app.cellHeight-1))
		blue = pygame.transform.smoothscale((self.spriteSheet.grabImage(8, 4, 16, 16)), (self.app.cellWidth-1, self.app.cellHeight-1))
		
		for i in range(16):
			self.ghostColours.append(white)
		
		for i in range(16):
			self.ghostColours.append(blue)
	
	def update_essential(self):
		
		if self.app.player.poweredUp == True:	
			if self.imgIndex != 30:
				self.img = self.ghostColours[self.imgIndex]
				self.imgIndex+=1
			else:
				self.imgIndex = 0
		else:
			if self.direction == (0,self.speed):	#down
				self.img = self.imgArr[3]
			elif self.direction == (0,-self.speed):	#up
				self.img = self.imgArr[2]
			elif self.direction == (-self.speed,0):	#left
				self.img = self.imgArr[1]
			elif self.direction == (self.speed,0):	#right
				self.img = self.imgArr[0]

		if self.atBase:
			self.direction = vec(0,0)
		else:
			self.posPx += self.direction
			self.pacmanCollision()
			self.teleportGhost()
		
			#grid position
			self.posGrid[0] = (self.posPx[0]-BORDER_BUFFER +self.app.cellWidth//2)//self.app.cellWidth+1
			self.posGrid[1] = (self.posPx[1]-BORDER_BUFFER +self.app.cellHeight//2)//self.app.cellHeight+1
			self.rect.x = self.posPx.x
			self.rect.y = self.posPx.y
			
			self.teleportGhost()


	def draw(self):
		self.app.screen.blit(self.img, (int(self.posPx.x),int(self.posPx.y)))

	######################################################

	def get_posPx(self):
		return vec(self.posGrid.x * self.app.cellWidth + BORDER_BUFFER//2, self.posGrid.y * self.app.cellHeight + BORDER_BUFFER//2)


	def getSprite(self):
		#used to offset sprite sheet selection -> depending on direction
		if self.color == "yellow":
			self.imgArr.append(self.spriteSheet.grabImage(0, 7, 16, 16))
			self.imgArr[0] = pygame.transform.smoothscale(self.imgArr[0], (self.app.cellWidth-1, self.app.cellHeight-1))
			self.imgArr.append(self.spriteSheet.grabImage(2, 7, 16, 16))
			self.imgArr[1] = pygame.transform.smoothscale(self.imgArr[1], (self.app.cellWidth-1, self.app.cellHeight-1))
			self.imgArr.append(self.spriteSheet.grabImage(4, 7, 16, 16))
			self.imgArr[2] = pygame.transform.smoothscale(self.imgArr[2], (self.app.cellWidth-1, self.app.cellHeight-1))
			self.imgArr.append(self.spriteSheet.grabImage(6, 7, 16, 16))
			self.imgArr[3] = pygame.transform.smoothscale(self.imgArr[3], (self.app.cellWidth-1, self.app.cellHeight-1))
			self.imgArr.append(self.spriteSheet.grabImage(8, 4, 16, 16))
			self.imgArr[4] = pygame.transform.smoothscale(self.imgArr[4], (self.app.cellWidth-1, self.app.cellHeight-1)) #using 4th and 5th index in array to hold transformation				
			self.imgArr.append(self.spriteSheet.grabImage(10, 4, 16, 16))
			self.imgArr[5] = pygame.transform.smoothscale(self.imgArr[5], (self.app.cellWidth-1, self.app.cellHeight-1)) 
		elif self.color == "pink":
			self.imgArr.append(self.spriteSheet.grabImage(0, 5, 16, 16))
			self.imgArr[0] = pygame.transform.smoothscale(self.imgArr[0], (self.app.cellWidth-1, self.app.cellHeight-1))
			self.imgArr.append(self.spriteSheet.grabImage(2, 5, 16, 16))
			self.imgArr[1] = pygame.transform.smoothscale(self.imgArr[1], (self.app.cellWidth-1, self.app.cellHeight-1))
			self.imgArr.append(self.spriteSheet.grabImage(4, 5, 16, 16))
			self.imgArr[2] = pygame.transform.smoothscale(self.imgArr[2], (self.app.cellWidth-1, self.app.cellHeight-1))
			self.imgArr.append(self.spriteSheet.grabImage(6, 5, 16, 16))
			self.imgArr[3] = pygame.transform.smoothscale(self.imgArr[3], (self.app.cellWidth-1, self.app.cellHeight-1))
			self.imgArr.append(self.spriteSheet.grabImage(8, 4, 16, 16))
			self.imgArr[4] = pygame.transform.smoothscale(self.imgArr[4], (self.app.cellWidth-1, self.app.cellHeight-1))
			self.imgArr.append(self.spriteSheet.grabImage(10, 4, 16, 16))
			self.imgArr[5] = pygame.transform.smoothscale(self.imgArr[5], (self.app.cellWidth-1, self.app.cellHeight-1))
		elif self.color == "blue":
			self.imgArr.append(self.spriteSheet.grabImage(0, 6, 16, 16))
			self.imgArr[0] = pygame.transform.smoothscale(self.imgArr[0], (self.app.cellWidth-1, self.app.cellHeight-1))
			self.imgArr.append(self.spriteSheet.grabImage(2, 6, 16, 16))
			self.imgArr[1] = pygame.transform.smoothscale(self.imgArr[1], (self.app.cellWidth-1, self.app.cellHeight-1))
			self.imgArr.append(self.spriteSheet.grabImage(4, 6, 16, 16))
			self.imgArr[2] = pygame.transform.smoothscale(self.imgArr[2], (self.app.cellWidth-1, self.app.cellHeight-1))
			self.imgArr.append(self.spriteSheet.grabImage(6, 6, 16, 16))
			self.imgArr[3] = pygame.transform.smoothscale(self.imgArr[3], (self.app.cellWidth-1, self.app.cellHeight-1))
			self.imgArr.append(self.spriteSheet.grabImage(8, 4, 16, 16))
			self.imgArr[4] = pygame.transform.smoothscale(self.imgArr[4], (self.app.cellWidth-1, self.app.cellHeight-1))
			self.imgArr.append(self.spriteSheet.grabImage(10, 4, 16, 16))
			self.imgArr[5] = pygame.transform.smoothscale(self.imgArr[5], (self.app.cellWidth-1, self.app.cellHeight-1))
		else: #red
			self.imgArr.append(self.spriteSheet.grabImage(0, 4, 16, 16))
			self.imgArr[0] = pygame.transform.smoothscale(self.imgArr[0], (self.app.cellWidth-1, self.app.cellHeight-1))
			self.imgArr.append(self.spriteSheet.grabImage(2, 4, 16, 16))
			self.imgArr[1] = pygame.transform.smoothscale(self.imgArr[1], (self.app.cellWidth-1, self.app.cellHeight-1))
			self.imgArr.append(self.spriteSheet.grabImage(4, 4, 16, 16))
			self.imgArr[2] = pygame.transform.smoothscale(self.imgArr[2], (self.app.cellWidth-1, self.app.cellHeight-1))
			self.imgArr.append(self.spriteSheet.grabImage(6, 4, 16, 16))
			self.imgArr[3] = pygame.transform.smoothscale(self.imgArr[3], (self.app.cellWidth-1, self.app.cellHeight-1))
			self.imgArr.append(self.spriteSheet.grabImage(8, 4, 16, 16))
			self.imgArr[4] = pygame.transform.smoothscale(self.imgArr[4], (self.app.cellWidth-1, self.app.cellHeight-1))	
			self.imgArr.append(self.spriteSheet.grabImage(10, 4, 16, 16))
			self.imgArr[5] = pygame.transform.smoothscale(self.imgArr[5], (self.app.cellWidth-1, self.app.cellHeight-1))	
	
	def checkCollide(self,x,y):
		rec = pygame.Rect(x,y,self.app.cellWidth,self.app.cellHeight)
		for w in self.app.walls:
			if rec.colliderect(w.rect):
				return True
		return False

	def getAvailDirs(self, curDir):
		dirs = []

		#Current direction is up or down
		if curDir == vec(0,-self.speed) or curDir == vec(0,self.speed):
			#if curDir is up and no collision ahead -> append curdir
			if curDir == vec(0,-self.speed) and not self.checkCollide(self.posPx.x,self.posPx.y - self.app.cellHeight):
				dirs.append(curDir)
			#if curDir is down and no collision ahead -> append curdir
			elif curDir == vec(0,self.speed) and not self.checkCollide(self.posPx.x,self.posPx.y + self.app.cellHeight):
				dirs.append(curDir)
			if not self.checkCollide(self.posPx.x - self.app.cellWidth,self.posPx.y):
				dirs.append(vec(-self.speed,0))
			if not self.checkCollide(self.posPx.x + self.app.cellWidth,self.posPx.y):
				dirs.append(vec(self.speed,0))
		#left
		elif curDir == vec(-self.speed,0) or curDir == vec(self.speed,0):
			#if curDir is left and no collision ahead -> append curdir
			if curDir == vec(-self.speed,0) and not self.checkCollide(self.posPx.x - self.app.cellWidth,self.posPx.y):
				dirs.append(curDir)
			#if curDir is right and no collision ahead -> append curdir
			elif curDir == vec(self.speed,0) and not self.checkCollide(self.posPx.x + self.app.cellWidth, self.posPx.y):
				dirs.append(curDir)

			if not self.checkCollide(self.posPx.x,self.posPx.y - self.app.cellHeight):
				dirs.append(vec(0,-self.speed))
			if not self.checkCollide(self.posPx.x,self.posPx.y + self.app.cellHeight):
				dirs.append(vec(0,self.speed))
		return dirs

	def pacmanCollision(self):
		if self.rect.colliderect(self.app.player.rect) and not self.app.player.deadAnimation:
			if self.app.player.poweredUp != True:
				self.app.player.die()
				self.app.resetGhosts()
			else:
				#would implement resetting the eaten ghosts here
				#self.app.resetGhosts()
				if self.color == "red":
					self.posGrid = vec(14,14)
				elif self.color == "blue":
					self.posGrid = vec(13,14)
				elif self.color == "pink":
					self.posGrid = vec(15,14)
				else:
					self.posGrid = vec(12,14)
				
				self.posPx = self.get_posPx()
				self.app.start_ticks=pygame.time.get_ticks() #starter tick
				self.app.seconds=0
				self.atBase = True
	
	def teleportGhost(self):
		if self.posGrid[0] < 1:
			self.posGrid[0] = 26
			self.posPx = self.get_posPx()

		elif self.posGrid[0] >26: #right side teleporter
			self.posGrid[0] = 1
			self.posPx = self.get_posPx()


	def releaseFromBase(self):
		self.posGrid = vec(14,11)
		self.posPx = self.get_posPx()
		self.direction = vec(self.speed,0)
		self.atBase = False

