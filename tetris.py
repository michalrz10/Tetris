import pygame
import numpy as np
import random
import copy
import sys

class Node:
	def __init__(self,x,y):
		self.x=x
		self.y=y

class Block:
	def __init__(self,x,y):
		self.random=False
		self.center=Node(x,y)
		self.nodes=[]
	def addNode(self,x,y):
		self.nodes.append(Node(x,y))
	def rotate(self):
		for i in self.nodes:
			p=-i.y
			i.y=i.x
			i.x=p
	def reverseRotate(self):
		for i in self.nodes:
			p=i.y
			i.y=-i.x
			i.x=p
		

class Game:
	def __init__(self):
		self.map=np.zeros((20,10),np.int)
		self.points=0
		
		self.possibleBlocks=[]
		#creating I
		p=Block(4,0)
		p.random=False
		p.addNode(0,0)
		p.addNode(-1,0)
		p.addNode(1,0)
		p.addNode(2,0)
		self.possibleBlocks.append(p)
		#creating T
		p=Block(4,0)
		p.random=True
		p.addNode(0,0)
		p.addNode(-1,0)
		p.addNode(1,0)
		p.addNode(0,1)
		self.possibleBlocks.append(p)
		#creating O
		p=Block(4.5,0.5)
		p.random=False
		p.addNode(0.5,0.5)
		p.addNode(-0.5,0.5)
		p.addNode(0.5,-0.5)
		p.addNode(-0.5,-0.5)
		self.possibleBlocks.append(p)
		#creating L
		p=Block(4,0)
		p.random=True
		p.addNode(0,0)
		p.addNode(1,0)
		p.addNode(-1,0)
		p.addNode(-1,1)
		self.possibleBlocks.append(p)
		#creating J
		p=Block(4,0)
		p.random=True
		p.addNode(0,0)
		p.addNode(1,0)
		p.addNode(-1,0)
		p.addNode(1,1)
		self.possibleBlocks.append(p)
		#creating S
		p=Block(4,1)
		p.random=True
		p.addNode(0,0)
		p.addNode(-1,0)
		p.addNode(0,-1)
		p.addNode(1,-1)
		self.possibleBlocks.append(p)
		#creating Z
		p=Block(4,1)
		p.random=True
		p.addNode(0,0)
		p.addNode(1,0)
		p.addNode(0,-1)
		p.addNode(-1,-1)
		self.possibleBlocks.append(p)
		
		self.nextBlock=False
		self.newBlock()
	
	def newBlock(self):
		self.block=copy.deepcopy(self.possibleBlocks[random.randint(0,6)])
		if self.block.random: self.block.center.x+=random.randint(0,1)
		if self.colission(): self.reset()
	
	def colission(self):
		for i in self.block.nodes:
			if self.block.center.x+i.x>=10 or self.block.center.x+i.x<0 or self.block.center.y+i.y<0 or self.block.center.y+i.y>=20: return True
			if self.map[int(self.block.center.y+i.y)][int(self.block.center.x+i.x)]==1: return True
		return False
		
	def reset(self):
		self.map=np.zeros((20,10),np.int)
		print(self.points)
		self.points=0
		self.nextBlock=True
		
	def gravity(self):
		if self.nextBlock:
			self.newBlock()
			self.nextBlock=False
		else:
			self.block.center.y+=1
			if self.colission():
				point=0
				self.block.center.y-=1
				self.nextBlock=True
				
				for i in self.block.nodes:
					self.map[int(self.block.center.y+i.y)][int(self.block.center.x+i.x)]=1
				
				i=19
				while i>-1:
					temp=True
					for j in range(10):
						if self.map[i][j]==0:
							temp=False
							break
					if temp:
						point+=1
						for j in range(i,0,-1):
							for k in range(10):
								self.map[j][k]=self.map[j-1][k]
					else: i-=1
				if point>0: self.points+=2**(point-1)				
		
	def rotate(self):
		self.block.rotate()
		if self.colission(): self.block.reverseRotate()
	
	def move(self,direction): #true right, false left
		if direction:
			self.block.center.x+=1
			if self.colission(): self.block.center.x-=1
		else:
			self.block.center.x-=1
			if self.colission(): self.block.center.x+=1

class Display:
	def __init__(self):
		pygame.init()
		self.window = pygame.display.set_mode((200, 400))
		pygame.display.set_caption(('Tetris'))
		self.clock = pygame.time.Clock()
		self.game=Game()
		pygame.time.set_timer(25,500)

	def show(self):
		self.window.fill((255,255,255))
		#draw
		for y in range(20):
			for x in range(10):
				if self.game.map[y][x]==1: pygame.draw.rect(self.window,(0,0,0),pygame.Rect(20*x,20*y,20,20))
		pos=Node(self.game.block.center.x,self.game.block.center.y)
		for i in self.game.block.nodes:
			pygame.draw.rect(self.window,(255,0,0),pygame.Rect(20*int(pos.x+i.x),20*int(pos.y+i.y),20,20))
		
		for i in range(9):
			pygame.draw.line(self.window,(0,0,0),(i*20+20,0),(i*20+20,400),1)
		for i in range(19):
			pygame.draw.line(self.window,(0,0,0),(0,i*20+20),(200,i*20+20),1)
		
		pygame.display.flip()
		self.clock.tick(60)
	
	def loop(self):
		while True:
			for event in pygame.event.get():
				if event.type==pygame.QUIT:
					sys.exit(0)
				if event.type == pygame.KEYDOWN:
					if event.key == pygame.K_RIGHT:
						self.game.move(True)
					if event.key == pygame.K_LEFT:
						self.game.move(False)
					if event.key == pygame.K_UP:
						self.game.rotate()
					if event.key == pygame.K_DOWN:
						self.game.gravity()
				if event.type==25:
					self.game.gravity()
			
			self.show()

Display().loop()
