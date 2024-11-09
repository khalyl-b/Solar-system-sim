import pygame, math, sqlite3, random,io
from urllib.request import urlopen
from pygame import mixer
from tkinter import *

temp = ""
#simple tkinter GUI so that the user can enter their username, this initiates the window
root = Tk()
#this makes sure that the window is in the center of the screen
root.geometry("+580+330")
#simple label which just says 'Enter User'
Label(root,text="Enter User").pack()
#Entry widget which allows the user to enter their user
e = Entry(root)
#The reason i had to pack this on a separate line is because to get the information from the widget it is not possible as it sees the 1 line creation and pack as a None type variable
e.pack()
#command for the button
def sel():
	#idk why i had to global it
	global temp
	#temp is set to whatever is in the entry widget
	temp = str(e.get())
	#The tkinter window is destroyed
	root.destroy()
#Creates a button which undergos the command 'sel' when pressed
Button(root,text="Enter",command=sel).pack()
#End of tkinter widgets being able to be applies
root.mainloop()

run = True

ldm = False
autoldm = True

#Sets the databasename to "" so that it can be modified and edited as this is needed to remove spaces otherwise sql doesnt work
databasename = ""
#loops through every character in temp
for i in temp:
	#if the character is a space
	if i == " ":
		#adds a _ to the end of the databsename
		databasename = databasename+"_"
	else:
		#otherwise it just adds the regular character
		databasename = databasename+i
#secondary database name for the acheivements
databasename2 = databasename + "acheivements"

image_url = "https://www.startwithaskateboard.com/MusixTube/assets/images/star.png"
#image_str = urlopen(image_url).read()
image_file = "bg.png"


bg = pygame.image.load(image_file)


pygame.init()


setting = "home"

win = pygame.display.set_mode((1280,720))

scale = 1
speed = 1
movex = 0
movey = 0
orbits = True
planetshoveredover = [0,0,0,0,0,0,0,0]
planetshoveredover = [1,1,1,1,1,1,1,1]

hover_sound = 0
hover_count = 0

font1 = pygame.font.SysFont("Arial",32)
font2 = pygame.font.SysFont("Arial",50)
font3 = pygame.font.SysFont("Arial",15)
font4 = pygame.font.SysFont("Arial",20)


class Planets:
	def __init__(self,name,a,b,r,c,t,z,s):
		self.name = name
		self.a = a
		self.b = b
		self.r = r
		self.c = c
		self.s = s
		self.t = t
		self.z = z
		self.x = 0
		self.y = 0
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
		self.checked = False
		self.turn = 1
		self.current = self.tempy
		if self.name == "asteroid":
			self.x = random.randint(0,2*self.a)
		if random.randint(1,2) == 1:
			self.y = (self.b*self.angley)*((1-((self.x-(self.a-self.anglez))/(self.a-self.anglez))**2)**0.5) + self.b

	def draw(self):
		'''
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
		'''

		self.surf = pygame.Surface(self.rect.size,pygame.SRCALPHA)
		if orbits and not self.name == "asteroid":
			pygame.draw.ellipse(self.surf,(100,100,100),(0+self.anglez,self.b-self.angley*self.b,self.rect.size[0]-2*self.anglez,self.angley*self.rect.size[1]),2)
		pygame.draw.circle(self.surf,self.c,((self.x+self.anglez),(self.y)),self.r)
		if self.z > 0:

			pygame.draw.ellipse(self.surf,(255,255,255),(movex+self.x-(self.r+15*scale),self.y-(self.r+15*scale)*self.angley+movey,2*(self.r+15*scale),2*(self.r+15*scale)*self.angley),3)
			if self.tempy > 0:
				pygame.draw.circle(self.surf,self.c,((self.x+self.anglez),(self.y)),self.r,draw_top_right=True,draw_top_left=True)
			else:
				pygame.draw.circle(self.surf,self.c,((self.x+self.anglez),(self.y)),self.r,draw_bottom_right=True,draw_bottom_left=True)

		if pygame.mouse.get_pos()[0] >= (self.x+640-self.a)+movex-self.r and pygame.mouse.get_pos()[1] >= (360+self.y-self.b)-self.r+movey and pygame.mouse.get_pos()[0] <= (self.x+640-self.a)+movex+self.r and pygame.mouse.get_pos()[1] <= (360+self.y-self.b)+movey+self.r:
			c = font1.render(self.name, 0, (255,255,255))
			self.surf.blit(c, (self.x-self.r*scale,self.y-2*self.r*scale))

		self.surf = pygame.transform.scale(self.surf,(self.rect.size[0]*scale,self.rect.size[1]*scale))
		self.surf = pygame.transform.rotate(self.surf,self.anglex)
		win.blit(self.surf,self.surf.get_rect(center=self.rect.center))


	def orbit(self):

		if self.turn == 1:
			if self.y > self.b-1:
				self.x -= self.s*speed/100
				self.y = (self.b*self.angley)*((1-((self.x-(self.a-self.anglez))/(self.a-self.anglez))**2)**0.5) + self.b
				if isinstance(self.y,complex):
					self.y = self.b-1
					self.x = 0
			else:
				self.x += self.s*speed/100
				self.y = self.b-((self.b*self.angley))*((1-((self.x-(self.a-self.anglez))/(self.a-self.anglez))**2)**0.5)
				if isinstance(self.y,complex): 
					self.y = self.b+1
					self.x = 2*(self.a-self.anglez)
		else:
			if self.y > self.b+1:
				self.x += self.s*speed/100
				self.y = self.b+(self.b*self.angley)*((1-((self.x-(self.a-self.anglez))/(self.a-self.anglez))**2)**0.5)
				if isinstance(self.y,complex):
					self.y = self.b-1
					self.x = 2*(self.a-self.anglez)
			else:
				self.x -= self.s*speed/100
				self.y = self.b-((self.b*self.angley))*((1-((self.x-(self.a-self.anglez))/(self.a-self.anglez))**2)**0.5)
				if isinstance(self.y,complex): 
					self.y = self.b+2
					self.x = 0

		
		if self.tempy != self.current and not self.checked:
			self.checked = True
			self.y = self.rect.size[1]-self.y

		self.current = self.tempy

	def asteroid_orbit(self):
		return

	def text_popup(self):
		global hover_count
		global planetshoveredover

		#print(pygame.mouse.get_pos())
		if pygame.mouse.get_pos()[0] >= (self.x+640-self.a)+movex-self.r and pygame.mouse.get_pos()[1] >= (360+self.y-self.b)-self.r+movey and pygame.mouse.get_pos()[0] <= (self.x+640-self.a)+movex+self.r and pygame.mouse.get_pos()[1] <= (360+self.y-self.b)+movey+self.r:
			#literally the same code repeated so i cba to explain, it just draws the words
			c = font1.render(self.name, 0, (255,255,255))
			self.surf.blit(c, (self.x-self.r*scale,self.y-2*self.r*scale))
			c = font1.render(str(self.name)+":", 0, (255,255,255))
			win.blit(c, (0,0))
			c = font1.render("Furthest distance: "+str(self.a), 0, (255,255,255))
			win.blit(c, (0,30))
			c = font1.render("Shortest distance: "+str(self.b), 0, (255,255,255))
			win.blit(c, (0,60))
			c = font1.render("Radius: "+str(self.r), 0, (255,255,255))
			win.blit(c, (0,90))
			c = font1.render("Tilt: "+str(self.t)+" degrees", 0, (255,255,255))
			win.blit(c, (0,120))
			c = font1.render("Velocity: "+str(self.s)+"000 mph", 0, (255,255,255))
			win.blit(c, (0,150))
			
			hover_count+=1
			'''
			if hover_sound == 0:
				mixer.music.load("Hover.mp3") 
				mixer.music.set_volume(1) 
				mixer.music.play()
				hover_sound = 2
			'''
	
			if acheivements[5] == 0:
				acheivements[5] = 1
	
			for j in range(0,len(planets)):
				if planets[j].name == self.name:
					if planetshoveredover[j] == 0:
						planetshoveredover[j] = 1
		




#a,b,r,rr,gg,bb,t,z,s


baseplanets = [
	["Mercury",119,114,1.6,180,180,180,0,0,107],
	["Venus",158,157,3.8,222,171,2,3,0,78],
	["Earth",184,181,4.0,1,81,130,23,0,66],
	["Mars",244,217,2.1,117,51,0,25,0,54],
	["Jupiter",598,550,43.4,164,191,191,3,0,29],
	["Saturn",1024,929,36.2,186,149,101,27,25,21],
	["Uranus",1980,1790,15.8,4,93,140,82,-5,15],
	["Neptune",2909,2861,15.3,55,102,163,57,0,12]
]


asteroid_belt = []

for i in range(0,200):
	asteroid_belt.append(Planets("asteroid",random.randint(297,390),random.randint(297,390),2,(255,255,255),0,0,5))


'''

baseplanets = [
	["Mercury",119,114,1.6,180,180,180,0,0,107],
	["Venus",158,157,3.8,222,171,2,3,0,78],
	["Earth",184,181,4.0,1,81,130,23,0,66],
	["Mars",244,217,2.1,117,51,0,25,0,54]
]

'''

#connects to a database called users_planets
conn = sqlite3.connect('User_information.db')
#creates a cursor to the database
curs = conn.cursor()
#This will attempt to create a new table with the user's username and fill it with the base planets but will fail if there already is one
try:
	#creates a table in the database with the users username
	curs.execute(f"""CREATE TABLE {databasename} (
				name text,
				a int,
				b int,
				r real,
				rr int,
				gg int,
				bb int,
				t int,
				z int,
				s int
				)""")
	#will loop through all the base planets and will fill in their attributs in the table
	for i in baseplanets:
		curs.execute(f"INSERT INTO {databasename} VALUES (:name,:a,:b,:r,:rr,:gg,:bb,:t,:z,:s)",
		{
			'name':i[0],
			'a':i[1],
			'b':i[2],
			'r':i[3],
			'rr':i[4],
			'gg':i[5],
			'bb':i[6],
			't':i[7],
			'z':i[8],
			's':i[9]
		})
	#this will create a datebase for the acheivements
	curs.execute(f"""CREATE TABLE {databasename2} (
				zoomin int,
				zoomout int,
				speedup int,
				slowdown int,
				constellation int,
				hoveronsingle int,
				hoveronall int,
				createnew int,
				editold int,
				rotate int
				)""")
	#This will just fill all the values as 0 as it is being created so the value is null
	curs.execute(f"INSERT INTO {databasename2} VALUES (:zoomin,:zoomout,:speedup,:slowdown,:constellation,:hoveronsingle,:hoveronall,:createnew,:editold,:rotate)",
	{
		'zoomin':0,
		'zoomout':0,
		'speedup':0,
		'slowdown':0,
		'constellation':0,
		'hoveronsingle':0,
		'hoveronall':0,
		'createnew':0,
		'editold':0,
		'rotate':0
		})

except Exception as e:
	#for debugging
	print(e)
#Just for debugging
run = False
acheivements = []

#Had to put try here in case someone entered nothing
try:
	#Then it selects everything from the table and not the base planets so that any new planets created or edited planets will be loaded
	curs.execute(f"SELECT * FROM {databasename}")
	#empty array called planets which will store all the planet objects information because then its easier to loop through them then to call each individual object
	planets = []
	#Everything that was in the table will be cycled through and it will create an object with that information and add it to the array called planets
	for i in curs.fetchall():
		planets.append(Planets(i[0],i[1],i[2],i[3],(i[4],i[5],i[6]),i[7],i[8],i[9]))
	
	#Same thing with the planets but for the acheivements
	acheivements = []
	#It will fetch everything from theacheivemetns and put them in an array called acheivemetns

	curs.execute(f"SELECT * FROM {databasename2}")
	for i in curs.fetchall()[0]:
		acheivements.append(i)

	run = True

except Exception as e:
	#for debugging
	print(e)

#commits all changes
conn.commit()
#closes the connection
conn.close()



'''
mercury = Planets("Mercury",0,200,120,115,2,(180,180,180),107/100,0,0)
venus = Planets("Venus",0,200,158,157,4,(222,171,2),78/100,3,0)
earth = Planets("Earth",0,200,184,181,4,(1,81,130),66/100,23,0)
mars = Planets("Mars",0,200,244,217,2,(117,51,0),54/100,25,0)
jupiter = Planets("Jupiter",0,200,598,550,43,(164,191,191),29/100,3,0)
saturn = Planets("Saturn",0,200,1024,929,36,(186,149,101),21/100,27,25)
uranus = Planets("Uranus",0,200,1980,1790,16,(4,93,140),15/100,82,-5)
neptune = Planets("Neptune",0,200,2909,2861,15,(55,102,163),12/100,57,0)
'''

#planets = [mercury,venus,earth,mars,jupiter,saturn,uranus,neptune]

mercury = Planets("Mercury",120,115,2,(180,180,180),0,0,107)
venus = Planets("Venus",158,157,4,(222,171,2),3,0,78)
earth = Planets("Earth",184,181,4,(1,81,130),23,0,88)
mars = Planets("Mars",244,217,2,(117,51,0),25,0,54)

#planets = [mercury,venus,earth,mars]#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!DELETE THIS WHEN YOUVE FINISHED EVERYTHING
#planets = [neptune]

down = False
down2 = 0

help_menu = ["Help menu","if i remember ill actually add a help menu but for now i cba","controls","menus","login","planet creator","infor or smt idk","(T) to toggle orbits on and off","Press E to edit the planets","L for acheiments","Press F to display FPS","Low detail mode in the corner (helps with lag)"]

current = 0
z = 0
alphabet = "abcdefghijklmnopqrstuvwxyz0123456789(),-ABCDEFGHIJKLMNOPQRSTUVWXYZ'"
pos = 0
acheivementscheck = []
for i in acheivements:
	acheivementscheck.append(i)

acheivementslist = ["zoom in","zoom out","speed up","slow down","find the constellation","hover over a planet","hover over all the planets","create a new planet","edit a new planet","rotate along the horizontal"]

hover_sound2 = 0
clock = pygame.time.Clock()

display_fps = False

rect = pygame.Rect((0,0,1280,720))
surf = pygame.Surface(rect.size,pygame.SRCALPHA)


def home_btn(previous):
	win.blit(font1.render("Home", 0, (255,255,255)),(15,670))
	pygame.draw.rect(win,(255,255,255),(10,670,80,40),2)
	if pygame.mouse.get_pos()[0] >= 10 and pygame.mouse.get_pos()[0] <= 90:
		if pygame.mouse.get_pos()[1] >= 670 and pygame.mouse.get_pos()[1] <= 710:
			win.blit(font1.render("Home", 0, (100,100,100)),(15,670))
			if pygame.mouse.get_pressed()[0]:
				return "home"

	return previous

starmovex = 0
starmovey = 0

star_surf = pygame.Surface((1280,720),pygame.SRCALPHA)

def twinkle(x,y):
  pygame.draw.circle(star_surf,(255,255,255),((x+starmovex)*(1/scale),(y+starmovey)),random.randint(0,5)*scale)

stars = []
for i in range(0,50):
  stars.append((random.randint(50,380),random.randint(150,480)))

stardisplay = False

while run:
	clock.tick(60)
	hover_count = 0
	win.fill((0,0,0))


	if planetshoveredover == [1,1,1,1,1,1,1,1]:
		acheivements[6] = 1

	if setting == "home":
		for event in pygame.event.get():
			if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
				run = False

			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_f:
					if display_fps == True:
						display_fps = False
					else:
						display_fps = True

		if hover_count == 0:
			hover_sound = 0

		pygame.draw.rect(win,(255,255,255),(500,50,280,100),2)
		win.blit(font2.render("Solar System", 0, (255,255,255)),(520,70))
		pygame.draw.rect(win,(255,255,255),(500,180,280,100),2)
		win.blit(font2.render("Help", 0, (255,255,255)),(595,200))
		pygame.draw.rect(win,(255,255,255),(500,310,280,100),2)
		win.blit(font2.render("Editor", 0, (255,255,255)),(585,330))
		pygame.draw.rect(win,(255,255,255),(500,440,280,100),2)
		win.blit(font2.render("Creator", 0, (255,255,255)),(575,460))
		pygame.draw.rect(win,(255,255,255),(500,570,280,100),2)
		win.blit(font2.render("Acheivements", 0, (255,255,255)),(510,590))

		if pygame.mouse.get_pos()[0] >= 500 and pygame.mouse.get_pos()[0] <= 780:
			if pygame.mouse.get_pos()[1] >= 50 and pygame.mouse.get_pos()[1] <= 150:
				win.blit(font2.render("Solar System", 0, (100,100,100)),(520,70))
				if pygame.mouse.get_pressed()[0]:
					setting = "system"
			if pygame.mouse.get_pos()[1] >= 180 and pygame.mouse.get_pos()[1] <= 280:
				win.blit(font2.render("Help", 0, (100,100,100)),(595,200))
				if pygame.mouse.get_pressed()[0]:
					setting = "help"
			if pygame.mouse.get_pos()[1] >= 310 and pygame.mouse.get_pos()[1] <= 410:
				win.blit(font2.render("Editor", 0, (100,100,100)),(585,330))
				if not (ldm or (autoldm and clock.get_fps() < 30)):
					if pygame.mouse.get_pressed()[0]:
						setting = "edit"
			if pygame.mouse.get_pos()[1] >= 440 and pygame.mouse.get_pos()[1] <= 540:
				win.blit(font2.render("Creator", 0, (100,100,100)),(575,460))
				if not (ldm or (autoldm and clock.get_fps() < 30)):
					if pygame.mouse.get_pressed()[0]:
						setting = "create"
			if pygame.mouse.get_pos()[1] >= 570 and pygame.mouse.get_pos()[1] <= 670:
				win.blit(font2.render("Acheivements", 0, (100,100,100)),(510,590))
				if not (ldm or (autoldm and clock.get_fps() < 30)):
					if pygame.mouse.get_pressed()[0]:
						setting = "acheivements"

		if (ldm or (autoldm and clock.get_fps() < 30)):
			pygame.draw.rect(win,(100,100,100),(500,310,280,100),2)
			win.blit(font2.render("Editor", 0, (100,100,100)),(585,330))
			pygame.draw.rect(win,(100,100,100),(500,440,280,100),2)
			win.blit(font2.render("Creator", 0, (100,100,100)),(575,460))
			pygame.draw.rect(win,(100,100,100),(500,570,280,100),2)
			win.blit(font2.render("Acheivements", 0, (100,100,100)),(510,590))

	elif setting == "system":
		star_surf = pygame.Surface((1280,1080),pygame.SRCALPHA)
		
		
		for event in pygame.event.get():
			if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
					run = False

			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_f:
					if display_fps == True:
						display_fps = False
					else:
						display_fps = True

			if event.type == 1025:
				down = True
				down2 = 1

			if event.type == 1026:
				down = False

			if event.type == pygame.KEYDOWN:

				if event.key == pygame.K_UP:
					if scale < 2:
						scale += 0.1
					if acheivements[0] == 0:
						acheivements[0] = 1
				#same for minus
				if event.key == pygame.K_DOWN:
					if scale > 0.2:
						scale -= 0.1
					if acheivements[1] == 0:
						acheivements[1] = 1
				#same principle as above except it changes the orbit speed
				if event.key == pygame.K_RIGHT:
					if speed < 50:
						speed += 1
					if acheivements[2] == 0:
						acheivements[2] = 1
				#^^
				if event.key == pygame.K_LEFT:
					if speed > 0:
						speed -= 1
					if acheivements[3] == 0:
						acheivements[3] = 1
				if event.key == pygame.K_w:
					movey -= 10
				if event.key == pygame.K_a:
					movex -= 10
				if event.key == pygame.K_s:
					movey += 10
				if event.key == pygame.K_d:
					movex += 10
				if event.key == pygame.K_t:
					if orbits:
						orbits = False
					else:
						orbits = True

		if down2 == 1:
			for i in planets:
				i.oldx,i.oldy = pygame.mouse.get_pos()

		if down:
			for i in planets+asteroid_belt:
				i.mousex,i.mousey = pygame.mouse.get_pos()
				deltax = i.mousex-i.oldx
				deltay = i.mousey-i.oldy
				qzzz = deltax
				modulus = (deltax**2+deltay**2)**0.5

				if i.mousey > 360:
					i.anglex+=deltax*0.1
				else:
					i.anglex-=deltax*0.1

				q = deltay/100

				if q > 0.1:
					q = 0.1

				if i.tempy > 0:
					i.angley+=q
					i.tempy+=q
					if i.tempy < 0.07:
						i.turn *=-1
						i.checked = False
						i.tempy = -0.07
						i.angley = 0.07
				else:
					i.angley-=q
					i.tempy+=q
					if i.tempy > -0.07:
						i.turn *=-1
						i.checked = False
						i.tempy = 0.07
						i.angley = 0.07

				if i.angley > 1:
					if i.tempy > 0:
						
						i.angley = 1
						i.tempy = -1
					else:
						i.angley = 1
						i.tempy = 1

				if i.anglex <= -90.01 or i.anglex >= 90.01:
					i.anglex = i.tempx
				else:
					i.tempx = i.anglex

				i.oldx,i.oldy = i.mousex,i.mousey

		star_surf.blit(bg,bg.get_rect(center=(640,540)))
		starmovey = -planets[0].tempy*100
		#50,200),random.randint(150,300)))
		if planets[0].tempx > -150 and planets[0].tempx < 60 and planets[0].tempy > 0.1 and planets[0].tempy < 0.4:
			if pygame.mouse.get_pos()[0] > 20 and pygame.mouse.get_pos()[0] < 200 and pygame.mouse.get_pos()[1] > 150 and pygame.mouse.get_pos()[1] < 300:
				stardisplay = True


				for i in stars:
					twinkle(i[0],i[1])



				if acheivements[4] == 0:
					acheivements[4] = 1
			else:
				stardisplay = False
		else:
			stardisplay = False

		star_surf = pygame.transform.rotate(star_surf,planets[0].tempx)




		win.blit(star_surf,star_surf.get_rect(center=(640+starmovex,360+starmovey)))
		win.blit(star_surf,star_surf.get_rect(center=(640+starmovex,360+starmovey)))

		if stardisplay:
			c = font1.render("Star constellation", 0, (255,255,255))
			win.blit(c, (1000,640))
			c = font1.render("Information about it", 0, (255,255,255))
			win.blit(c, (1000,670))



		if planets[0].turn == 1:
			win.blit(font1.render("UP", 0, (255,255,255)),(1220,0))
		else:
			win.blit(font1.render("DOWN", 0, (255,255,255)),(1190,0))
			if acheivements[9] == 0:
				acheivements[9] = 1
			if acheivements[9] == 0:
				acheivements[9] = 1

		pygame.draw.circle(win,(255,205,0),(640,360),100*scale)

		for i in planets:
			i.draw()
			i.orbit()
			i.text_popup()

		if not (ldm or (autoldm and clock.get_fps() < 30)):
			for i in asteroid_belt:
				i.draw()
				i.orbit()

		if down2 == 1:
			down2 = 2

		surf = pygame.Surface(rect.size,pygame.SRCALPHA)

		if planets[0].tempy > 0:
			pygame.draw.circle(surf,(255,205,0),(640,360),100*scale,draw_top_right=True,draw_top_left=True)
		else:
			pygame.draw.circle(surf,(255,205,0),(640,360),100*scale,draw_bottom_right=True,draw_bottom_left=True)

		surf = pygame.transform.rotate(surf,planets[0].anglex)
		win.blit(surf,surf.get_rect(center=rect.center))

		setting = home_btn("system")

	elif setting == "help":

		pygame.draw.rect(win,(255,255,255),(1210,610,30,30),2)
		win.blit(font1.render("LDM", 0, (255,255,255)),(1150,605))
		if ldm:
			if pygame.mouse.get_pos()[0] >= 1210 and pygame.mouse.get_pos()[0] <= 1240 and pygame.mouse.get_pos()[1] >= 610 and pygame.mouse.get_pos()[1] <= 640:
				pygame.draw.polygon(win,(100,100,100),((1215,620),(1225,630),(1255,590),(1225,625)))
			else:
				pygame.draw.polygon(win,(255,255,255),((1215,620),(1225,630),(1255,590),(1225,625)))
		pygame.draw.rect(win,(255,255,255),(1210,650,30,30),2)
		win.blit(font1.render("Auto LDM", 0, (255,255,255)),(1090,645))
		if autoldm:
			if pygame.mouse.get_pos()[0] >= 1210 and pygame.mouse.get_pos()[0] <= 1240 and pygame.mouse.get_pos()[1] >= 650 and pygame.mouse.get_pos()[1] <= 690:
				pygame.draw.polygon(win,(100,100,100),((1215,660),(1225,670),(1255,630),(1225,665)))
			else:
				pygame.draw.polygon(win,(255,255,255),((1215,660),(1225,670),(1255,630),(1225,665)))

		for event in pygame.event.get():
			if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
				run = False

			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_f:
					if display_fps == True:
						display_fps = False
					else:
						display_fps = True

			if event.type == pygame.MOUSEBUTTONDOWN:
				if pygame.mouse.get_pos()[0] >= 1210 and pygame.mouse.get_pos()[0] <= 1240:
					if pygame.mouse.get_pos()[1] >= 610 and pygame.mouse.get_pos()[1] <= 640:
						if ldm:
							ldm = False
						else:
							ldm = True
					if pygame.mouse.get_pos()[1] >= 650 and pygame.mouse.get_pos()[1] <= 690:
						if autoldm:
							autoldm = False
						else:
							autoldm = True


		for i in range(0,len(help_menu)):
			win.blit(font1.render(help_menu[i], 0, (255,255,255)),(5,i*32))


		setting = home_btn("help")

	elif setting == "edit":
		setting = home_btn("edit")
		if z == 0:
			z+=1
			strings = [
				planets[current].name,
				str(planets[current].a),
				str(planets[current].b),
				str(planets[current].r),
				str(planets[current].c),
				str(planets[current].t),
				str(planets[current].z),
				str(planets[current].s)
			]
			pos = 0
			r = ""
			g = ""
			b = ""

		win.blit(font4.render("Name",0,(255,255,255)),(610,10))
		pygame.draw.rect(win,(255,255,255),(560,40,160,40),2)
		win.blit(font4.render("Furthest horizontal distance from the sun",0,(255,255,255)),(460,80))
		pygame.draw.rect(win,(255,255,255),(560,110,160,40),2)
		win.blit(font4.render("Furthest vertical distance from the sun",0,(255,255,255)),(470,150))
		pygame.draw.rect(win,(255,255,255),(560,180,160,40),2)
		win.blit(font4.render("Radius",0,(255,255,255)),(610,220))
		pygame.draw.rect(win,(255,255,255),(560,250,160,40),2)
		win.blit(font4.render("Colour",0,(255,255,255)),(610,290))
		pygame.draw.rect(win,(255,255,255),(560,320,160,40),2)
		win.blit(font4.render("Tilt",0,(255,255,255)),(630,360))
		pygame.draw.rect(win,(255,255,255),(560,390,160,40),2)
		win.blit(font4.render("Ring",0,(255,255,255)),(620,430))
		pygame.draw.rect(win,(255,255,255),(560,460,160,40),2)
		win.blit(font4.render("Speed",0,(255,255,255)),(610,500))
		pygame.draw.rect(win,(255,255,255),(560,530,160,40),2)
		pygame.draw.polygon(win,(255,255,255),((760,60),(730,75),(730,45)))
		pygame.draw.polygon(win,(255,255,255),((520,60),(550,75),(550,45)))


		win.blit(font4.render(strings[0],0,(255,255,255)),(560,40))
		win.blit(font4.render(strings[1],0,(255,255,255)),(560,110))
		win.blit(font4.render(strings[2],0,(255,255,255)),(560,180))
		win.blit(font4.render(strings[3],0,(255,255,255)),(560,250))
		win.blit(font4.render(strings[4],0,(255,255,255)),(560,320))
		win.blit(font4.render(strings[5],0,(255,255,255)),(560,390))
		win.blit(font4.render(strings[6],0,(255,255,255)),(560,460))
		win.blit(font4.render(strings[7],0,(255,255,255)),(560,530))

		pygame.draw.rect(win,(255,255,255),(1190,670,80,40),2)
		win.blit(font1.render("Reset",0,(255,255,255)),(1195,670))

		if pygame.mouse.get_pos()[0] >= 1190 and pygame.mouse.get_pos()[0] <= 1270:
			if pygame.mouse.get_pos()[1] >= 670 and pygame.mouse.get_pos()[1] <= 710:
				win.blit(font1.render("Reset",0,(100,100,100)),(1195,670))


		for event in pygame.event.get():
			if event.type == pygame.KEYDOWN:
				for i in alphabet:
					if event.unicode == i:
						strings[pos] = strings[pos] + event.unicode

				if event.key == 13 or event.key == 1073741905:
					pos+=1
					'''
					mixer.music.load("Hover.mp3") 
					mixer.music.set_volume(1) 
					mixer.music.play()
					'''
				if event.key == 1073741906:
					pos-=1
					'''
					mixer.music.load("Hover.mp3") 
					mixer.music.set_volume(1) 
					mixer.music.play()
					'''
					if pos == -1:
						pos = 0
				if event.key == 8:
					strings[pos] = strings[pos][:len(strings[pos])-1]
				if event.key == pygame.K_KP_PLUS or pos >= 8:
					setting = "home"
					if acheivements[8] == 0:
						acheivements[8] = 1
					try:
						nameinput = strings[0]
						ainput = int(strings[1])
						binput = int(strings[2])
						radiusinput = float(strings[3])
						tally = 1
						for i in strings[4]:
							if i == ",":
								tally += 1
							elif tally == 1 and i != "(":
								r = r+i
							elif tally == 2:
								g = g+i
							elif tally == 3 and i != ")":
								b = b + i


						colourinput = (int(r),int(g),int(b))
						tiltinput = int(strings[5])
						ringinput = int(strings[6])
						speedinput = int(strings[7])

						if ainput <90+radiusinput:
							ainput = 90+radiusinput+5
						if binput <90+radiusinput:
							binput = 90+radiusinput+5

						#connects to a database called users_planets
						conn = sqlite3.connect('User_information.db')
						#creates a cursor to the database
						curs = conn.cursor()
						curs.execute(f"""UPDATE {databasename} SET
							name = :name,
							a = :a,
							b = :b,
							r = :r,
							rr = :rr,
							gg = :gg,
							bb = :bb,
							t = :t,
							z = :z,
							s = :s

							WHERE oid = :oid""",
							{
							'name': nameinput,
							'a': ainput,
							'b': binput,
							'r': radiusinput,
							'rr': colourinput[0],
							'gg': colourinput[1],
							'bb': colourinput[2],
							't': tiltinput,
							'z': ringinput,
							's': speedinput,

							'oid' : current+1
						})

						#commits all changes
						conn.commit()
						conn.close()
						conn = sqlite3.connect('User_information.db')
						curs = conn.cursor()

						curs.execute(f"SELECT * FROM {databasename}")
						#empty array called planets which will store all the planet objects information because then its easier to loop through them then to call each individual object
						planets = []
						#Everything that was in the table will be cycled through and it will create an object with that information and add it to the array called planets
						for i in curs.fetchall():
							planets.append(Planets(i[0],i[1],i[2],i[3],(i[4],i[5],i[6]),i[7],i[8],i[9]))

						curs.execute(f"SELECT * FROM {databasename}")
						conn.commit()
						conn.close()
					except Exception as e:
						print(e)
						print("incorrect values")#do popup ltr

			if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
				run = False
			if event.type == pygame.MOUSEBUTTONDOWN:
				if event.pos[1] >= 45 and event.pos[1] <= 75:
					if event.pos[0] >= 730 and event.pos[0] <= 760:
						current+=1
						z = 0
						'''
						mixer.music.load("Select.mp3") 
						mixer.music.set_volume(1) 
						mixer.music.play()
						'''
					if event.pos[0] >= 520 and event.pos[0] <= 550:
						current-=1
						z = 0
						'''
						mixer.music.load("Select.mp3") 
						mixer.music.set_volume(1) 
						mixer.music.play()
						'''
				if event.pos[0] >= 1200 and event.pos[0] <= 1270:
					if event.pos[1] >= 670 and event.pos[1] <= 710:
						'''
						mixer.music.load("Select.mp3") 
						mixer.music.set_volume(1) 
						mixer.music.play()
						'''


						conn = sqlite3.connect('User_information.db')
						curs = conn.cursor()
						for i in range(1,len(planets)+1):
							curs.execute(f"DELETE FROM {databasename} WHERE oid= {i}")
						curs.execute(f"SELECT * FROM {databasename}")
						conn.commit()
						conn.close()
						conn = sqlite3.connect('User_information.db')
						curs = conn.cursor()
						for i in baseplanets:
							curs.execute(f"INSERT INTO {databasename} VALUES (:name,:a,:b,:r,:rr,:gg,:bb,:t,:z,:s)",
							{
								'name':i[0],
								'a':i[1],
								'b':i[2],
								'r':i[3],
								'rr':i[4],
								'gg':i[5],
								'bb':i[6],
								't':i[7],
								'z':i[8],
								's':i[9]
							})
						curs.execute(f"SELECT * FROM {databasename}")
						planets = []
						for i in curs.fetchall():
							planets.append(Planets(i[0],i[1],i[2],i[3],(i[4],i[5],i[6]),i[7],i[8],i[9]))
						conn.commit()
						conn.close()

						setting = "home"



		if pos != 8:
			pygame.draw.rect(win,(100,100,100),(560,40+70*pos,160,40),2)

		if pygame.mouse.get_pos()[1] >= 45 and pygame.mouse.get_pos()[1] <= 75:
			if pygame.mouse.get_pos()[0] >= 730 and pygame.mouse.get_pos()[0] <= 760:
				pygame.draw.polygon(win,(100,100,100),((760,60),(730,75),(730,45)))
				if hover_sound2 == 0:
					'''
					mixer.music.load("Hover.mp3") 
					mixer.music.set_volume(1) 
					mixer.music.play()
					hover_sound2 = 1
					'''

			if pygame.mouse.get_pos()[0] >= 520 and pygame.mouse.get_pos()[0] <= 550:
				pygame.draw.polygon(win,(100,100,100),((520,60),(550,75),(550,45)))
				if hover_sound2 == 0:
					'''
					mixer.music.load("Hover.mp3") 
					mixer.music.set_volume(1) 
					mixer.music.play()
					hover_sound2 = 1
					'''
		else:
			hover_sound2 = 0




	elif setting == "create":
		
		setting = home_btn("create")

		if z == 0:
			z+=1
			strings = ["","","","","","","",""]
			pos = 0
			r = ""
			g = ""
			b = ""

		win.blit(font4.render("Name",0,(255,255,255)),(610,10))
		pygame.draw.rect(win,(255,255,255),(560,40,160,40),2)
		win.blit(font4.render("Furthest horizontal distance from the sun",0,(255,255,255)),(460,80))
		pygame.draw.rect(win,(255,255,255),(560,110,160,40),2)
		win.blit(font4.render("Furthest vertical distance from the sun",0,(255,255,255)),(470,150))
		pygame.draw.rect(win,(255,255,255),(560,180,160,40),2)
		win.blit(font4.render("Radius",0,(255,255,255)),(610,220))
		pygame.draw.rect(win,(255,255,255),(560,250,160,40),2)
		win.blit(font4.render("Colour",0,(255,255,255)),(610,290))
		pygame.draw.rect(win,(255,255,255),(560,320,160,40),2)
		win.blit(font4.render("Tilt",0,(255,255,255)),(630,360))
		pygame.draw.rect(win,(255,255,255),(560,390,160,40),2)
		win.blit(font4.render("Ring",0,(255,255,255)),(620,430))
		pygame.draw.rect(win,(255,255,255),(560,460,160,40),2)
		win.blit(font4.render("Speed",0,(255,255,255)),(610,500))
		pygame.draw.rect(win,(255,255,255),(560,530,160,40),2)

		win.blit(font4.render(strings[0],0,(255,255,255)),(560,40))
		win.blit(font4.render(strings[1],0,(255,255,255)),(560,110))
		win.blit(font4.render(strings[2],0,(255,255,255)),(560,180))
		win.blit(font4.render(strings[3],0,(255,255,255)),(560,250))
		win.blit(font4.render(strings[4],0,(255,255,255)),(560,320))
		win.blit(font4.render(strings[5],0,(255,255,255)),(560,390))
		win.blit(font4.render(strings[6],0,(255,255,255)),(560,460))
		win.blit(font4.render(strings[7],0,(255,255,255)),(560,530))



		for event in pygame.event.get():
			if event.type == pygame.KEYDOWN:
				for i in alphabet:
					if event.unicode == i:
						strings[pos] = strings[pos] + event.unicode
				if event.key == 8:
					strings[pos] = strings[pos][:len(strings[pos])-1]

				if event.key == pygame.K_KP_PLUS or pos == 8:
					setting = "home"
					if acheivements[7] == 0:
							acheivements[7] = 1
					try:
						nameinput = strings[0]
						ainput = int(strings[1])
						binput = int(strings[2])
						radiusinput = float(strings[3])
						tally = 1
						for i in strings[4]:
							if i == ",":
								tally += 1
							elif tally == 1 and i != "(":
								r = r+i
							elif tally == 2:
								g = g+i
							elif tally == 3 and i != ")":
								b = b + i
						colourinput = (int(r),int(g),int(b))
						tiltinput = int(strings[5])
						ringinput = int(strings[6])
						speedinput = int(strings[7])

						if ainput <90+radiusinput:
							ainput = 90+radiusinput+5
						if binput <90+radiusinput:
							binput = 90+radiusinput+5

						conn = sqlite3.connect('User_information.db')
						curs = conn.cursor()

						curs.execute(f"INSERT INTO {databasename} VALUES (:name,:a,:b,:r,:rr,:gg,:bb,:t,:z,:s)",
						{
						'name': nameinput,
						'a': ainput,
						'b': binput,
						'r': radiusinput,
						'rr': colourinput[0],
						'gg': colourinput[1],
						'bb': colourinput[2],
						't': tiltinput,
						'z': ringinput,
						's': speedinput
						})
						curs.execute(f"SELECT * FROM {databasename}")
						planets = []
						for i in curs.fetchall():
							planets.append(Planets(i[0],i[1],i[2],i[3],(i[4],i[5],i[6]),i[7],i[8],i[9]))
						conn.commit()
						conn.close()
					except Exception as e:
						print(e)#change when you can
				if event.key == 13 or event.key == 1073741905:
					pos+=1
					'''
					mixer.music.load("Hover.mp3") 
					mixer.music.set_volume(1) 
					mixer.music.play()
					'''
				if event.key == 1073741906:
					pos-=1
					'''
					mixer.music.load("Hover.mp3") 
					mixer.music.set_volume(1) 
					mixer.music.play()
					'''
					if pos == -1:
						pos = 0
			if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
				run = False






		if pos != 8:
			pygame.draw.rect(win,(100,100,100),(560,40+70*pos,160,40),2)
		for event in pygame.event.get():
			if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
				run = False

		

	elif setting == "acheivements":

		for event in pygame.event.get():
			if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
				run = False
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_f:
					if display_fps == True:
						display_fps = False
					else:
						display_fps = True

		for i in range(0,10):
			if acheivements[i] == 1:
				win.blit(font4.render(acheivementslist[i],0,(255,255,255)),(560,10+40*i))

		if acheivements == [1,1,1,1,1,1,1,1,1,1]:
			win.blit(font2.render("All acheivements completed",0,(255,255,255)),(560,10+40*11))

		setting = home_btn("acheivements")

	if setting != "edit" and setting != "create":
		current = 0
		z = 0

	if current == len(planets):
		current = 0
	elif current == -1:
		current = len(planets)-1

	#print(acheivements)
	if acheivementscheck != acheivements:
		conn = sqlite3.connect('User_information.db')
		#creates a cursor to the database
		curs = conn.cursor()

		curs.execute(f"""UPDATE {databasename2} SET
							zoomin = :zoomin,
							zoomout = :zoomout,
							speedup = :speedup,
							slowdown = :slowdown,
							constellation = :constellation,
							hoveronsingle = :hoveronsingle,
							hoveronall = :hoveronall,
							createnew = :createnew,
							editold = :editold,
							rotate = :rotate

							WHERE oid = :oid""",
							{
							'zoomin': acheivements[0],
							'zoomout': acheivements[1],
							'speedup': acheivements[2],
							'slowdown': acheivements[3],
							'constellation': acheivements[4],
							'hoveronsingle': acheivements[5],
							'hoveronall': acheivements[6],
							'createnew': acheivements[7],
							'editold': acheivements[8],
							'rotate': acheivements[9],

							'oid' : 1
						})
		
		curs.execute(f"SELECT * FROM {databasename2}")
		conn.commit()
		#closes the connection
		conn.close()
		acheivementscheck = []
		for i in acheivements:
			acheivementscheck.append(i)

	if display_fps:

		win.blit(font1.render(str(int(clock.get_fps()))+" fps",0,(255,255,255)),(0,0))
	
	pygame.display.update()