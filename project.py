import pygame,math

pygame.init()
run = True

win = pygame.display.set_mode((1280,720))

class Planets:
	def __init__(self,x,y,a,b,r,c,s):
		self.x = x
		self.y = y
		self.a = a
		self.b = b
		self.r = r
		self.c = c
		self.s = s
		self.p = math.pi*(self.a+self.b)*((3*(((self.a-self.b)**2)/(((self.a+self.b)**2)*((((-3*(((self.a-self.b)**2)/((self.a+self.b)**2)))+4)**0.5)+10))))+1)
		self.rect = pygame.Rect((640-self.a,360-self.b,self.a*2,self.b*2))
		self.surf = pygame.Surface(self.rect.size,pygame.SRCALPHA)
		self.anglex = 0
		self.angley = 1
		self.anglez = 0
		self.oldx,self.oldy = pygame.mouse.get_pos()
		self.movex,self.movey = pygame.mouse.get_pos()
		self.tempx = self.anglex
		self.tempy = self.angley
		self.tempz = self.anglez

	def draw(self):
		keys = pygame.key.get_pressed()
		if keys[pygame.K_LEFT]:
			self.surf = pygame.transform.rotate(self.surf,1)
			self.anglex+=1
		if keys[pygame.K_RIGHT]:	
			self.surf = pygame.transform.rotate(self.surf,-1)
			self.anglex-=1
		if keys[pygame.K_UP]:
			if self.angley <= self.a-20:
				self.angley+=1
		if keys[pygame.K_DOWN]:
			if self.angley > 0:
				self.angley-=1	

		self.surf = pygame.Surface(self.rect.size,pygame.SRCALPHA)
		pygame.draw.ellipse(self.surf,(100,100,100),(0+self.anglez,self.b-self.angley*self.b,self.rect.size[0]-2*self.anglez,self.angley*self.rect.size[1]),2)
		pygame.draw.circle(self.surf,self.c,((self.x+self.anglez),(self.y)),self.r)
		self.surf = pygame.transform.rotate(self.surf,self.anglex)
		win.blit(self.surf,self.surf.get_rect(center=self.rect.center))


	def orbit(self):
		if self.y > self.b-1:
			self.x-= self.s	
			self.y = (self.b*self.angley)*((1-((self.x-(self.a-self.anglez))/(self.a-self.anglez))**2)**0.5) + self.b
			if isinstance(self.y,complex):
				self.y = self.b-1
				self.x = 0
		else:
			self.x += self.s
			self.y = self.b-((self.b*self.angley))*((1-((self.x-(self.a-self.anglez))/(self.a-self.anglez))**2)**0.5)
			if isinstance(self.y,complex): 
				self.y = self.b+1
				self.x = 2*(self.a-self.anglez)

mercury = Planets(0,200,120,115,5,(255,0,0),2)
venus = Planets(0,200,158,157,5,(255,0,0),2)
'''
Mercury",,114,1.6,180,180,180,0,0,107,734,360],
Venus",158,157,3.8,222,171,2,3,0,78,798,360],
Earth",184,181,4.0,1,81,130,23,0,66,824,360],
Mars",244,217,2.1,117,51,0,25,0,54,884,360],
Jupiter",598,550,43.4,164,191,191,3,0,29,1238,360],
Saturn",1024,929,36.2,186,149,101,27,25,21,1664,360],
Uranus",1980,1790,15.8,4,93,140,82,-5,15,2620,360],
Neptune",2909,2861,15.3,55,102,163,57,0,12,3549,360]
'''
planets = [mercury,venus]

down = False
down2 = 0

clock = pygame.time.Clock()

rect = pygame.Rect((0,0,1280,720))
surf = pygame.Surface(rect.size,pygame.SRCALPHA)

while run:
	clock.tick(60)
	win.fill((0,0,0))
	pygame.draw.circle(win,(255,205,0),(640,360),100)

	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			run = False

		if event.type == 1025:
			down = True
			down2 = 1
			
		if event.type == 1026:
			down = False

	if down2 == 1:
		for i in planets:
		 i.oldx,i.oldy = pygame.mouse.get_pos()

	if down:
		for i in planets:
			i.mousex,i.mousey = pygame.mouse.get_pos()
			if i.mousey > 360:
				i.anglex+=(i.mousex-i.oldx)*0.1
			else:
				i.anglex-=(i.mousex-i.oldx)*0.1
			

			if i.tempy > 0:
				i.angley+=(i.mousey-i.oldy)/100
				i.tempy+=(i.mousey-i.oldy)/100
				if i.tempy < 0.05:
					i.tempy = -0.05
					i.angley = 0.05
			else:
				i.angley-=(i.mousey-i.oldy)/100
				i.tempy+=(i.mousey-i.oldy)/100
				if i.tempy > -0.05:
					i.tempy = 0.05
					i.angley = 0.05



			

			if i.tempy > 1:
				i.tempy = -0.9
			if i.tempy < -1:
				i.tempy = 0.9

			if i.anglex <= -90 or i.anglex >= 90:
				i.anglex = i.tempx

			i.oldx,i.oldy = i.mousex,i.mousey
			print(i.angley)

	for i in planets:
		i.draw()
		i.orbit()

	if down2 == 1:
		down2 = 2

	surf = pygame.Surface(rect.size,pygame.SRCALPHA)
	if mercury.tempy > 0:
		pygame.draw.circle(surf,(255,205,0),(640,360),100,draw_top_right=True,draw_top_left=True)
	else:
		pygame.draw.circle(surf,(255,205,0),(640,360),100,draw_bottom_right=True,draw_bottom_left=True)
	surf = pygame.transform.rotate(surf,mercury.anglex)
	win.blit(surf,surf.get_rect(center=rect.center))
	
	pygame.display.update()