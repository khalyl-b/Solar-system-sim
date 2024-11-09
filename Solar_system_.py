#imports
import pygame, time, sys, sqlite3, random
from pygame import mixer
from tkinter import *
#temporary variable which will be used for creating the user
temp = ""
#simple tkinter GUI so that the user can enter their username, this initiates the window
root = Tk()
#this makes sure that the window is in the center of the screen
root.geometry("168x80+580+330")
root.iconbitmap("sun.ico")
root.resizable(False,False)
#simple label which just says 'Enter User'
Label(root, text="Enter User").pack()
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
Button(root, text="Enter", command=sel).pack()
#End of tkinter widgets being able to be applies
root.mainloop()

#Sets the databasename to "" so that it can be modified and edited as this is needed to remove spaces otherwise sql doesnt work
databasename = ""
#loops through every character in temp
for i in temp:
	#if the character is a space
	if i == " ":
		#adds a _ to the end of the databsename
		databasename = databasename + "_"
	else:
		#otherwise it just adds the regular character
		databasename = databasename + i
#secondary database name for the acheivements
databasename2 = databasename + "acheivements"


#background class for deciding whether its in the planets or help or editor menu, no explanation needed
class background:

	def __init__(self, place):
		self.place = place


# initating the background object
back = background("home")

#initiating pygame
pygame.init()
#creating window
win = pygame.display.set_mode((1280, 720))

pygame_icon = pygame.image.load('sun.ico')
pygame.display.set_icon(pygame_icon)

#loading the background image
bg = pygame.image.load("bg.png")

#scale of the planets and orbits and sun
scale = 1
#This is the angle at which the user is looking at the planets at
angle = 1
#speed at which they orbit
#0.001 is 1000 times sped up
a_time = 0.001
#whether the planets are to scale or not, idk if ill use this one coz it could just be a waste of time coz im adding the zoom function in anayway
toscale = False
#sees whether to draw the orbits or not
orbits = True
#variabels
movex = 0
movey = 0

#the first font which will vary depending on the scale
font = pygame.font.SysFont("Arial", 32)
#The second font which will be constant
font2 = pygame.font.SysFont("Arial", 32)

mixer.init()
#For the acheivement of hoverin over all the planets
planetshoveredover = [0, 0, 0, 0, 0, 0, 0, 0]
#To do with hovering over the planets and playing noise
hover_sound = 0
hover_count = 0


#class for the planets, a is the maximum horizontal displacement from the orgin and b is the maximum y displacement from the origin which correlate to the planets eccentricity, ring is whether to see if it as a ring and tilt is to see how much to rate it on its axis but idk if ill be able to get to it coz its wayy too complicated, rest are self explanatory
class planet:
	def __init__(self, name, a, b, radius, colour, tilt, ring, speed, x, y):
		self.name = name
		self.a = a
		self.b = b
		self.radius = radius
		self.colour = colour
		self.tilt = tilt
		self.ring = ring
		self.speed = speed
		self.x = x
		self.y = y
		if self.name == "Asteroid":
			self.x = random.randint(640-self.a,640+self.a)
		if random.randint(1,2) == 1:
			self.y = 360 + ((self.b * angle) * scale) * ((1 -((self.x - 640) / (self.a * scale))**2)**0.5)

    #the orbit function (and also kinda drawing function)

	def orbit(self):
		global scale
		global speed
		global a_time
		global angle
		global movex
		global movey
		global orbits
		#omd this maths was acc so painful
		#planets more counter-clockwise
		#basically this asses whether the planet is above (technically below) the line y=359 then well use the positive increase in y not negative and also decrese the x as the planets move counter clockwise
		if self.y > 359:
			#the x is decraseing at a rate of which is the orbit speed for the planet multiplied by the orbit time set by the user
			self.x -= self.speed * a_time
			#these next lines of code were so annoying to program because they involved so many rearrangements
			#first the equation of an ellipse is (x-cx)^2/a^2+(y-cy)^2/b^2 = 1 but i was changing the x so i had to change the y to correspond with it so i needed to rearrange it
			#so i got y = +_b*(1-(x-cx)^2/a^2) +cy and the center is (640,340) so it the formula would be y = +_b*(1-(x-640)^2/a^2) + 360 to calculate the y value for the ellipse, however because the y is above the 359 line we take the positive value here
			self.y = (self.b * angle * scale) * ((1 - ((self.x - 640) / (self.a * scale))**2)**0.5) + 360
			#I have absolutely no idea how i got complex numbers here, im assuming that i put a value outside the ellipse because the value of  x was not in the domain of  [640-a,640+] so it created a negative square root, because when doing 1-((x-640)/a)^2, the value of (x-640)/a has to be less than one for the value of it to be positive and if x is outside the domain then it will be negative because (640+_a-640)/a will be +_a/a which is +_1 so its the maximum value that is allowed
			if isinstance(self.y, complex):
				#if it is a complex number then it will just set value to be the horizontal vertex of the ellipse
				self.y = 359
				self.x = 640 - self.a * scale
			#if the value of y is below the line then it will take the negative value of y
		else:
			# same thing happens here except that the x is being increased so it can loop back round
			self.x += self.speed * a_time
			self.y = 360 - ((self.b * angle) * scale) * ((1 - ((self.x - 640) / (self.a * scale))**2)**0.5)
			if isinstance(self.y, complex):
				self.y = 361
				self.x = 640 + self.a * scale

		#waits 0.01 seconds so that the movement is not instantaneous
		#time.sleep(0.01)
		if orbits and self.name != "Asteroid":
			#draws the orbit pattern in grey, the way pygame creates ellipses is by assigning a rectangle to it and its ellipse is there so the (x,y) will be (cx-a,cy-b) and it will be 2a long and 2b wide
			pygame.draw.ellipse(win, (100, 100, 100),((640 - int(self.a * scale) + movex,360 - int(self.b * angle * scale) + movey,2 * int(self.a * scale), 2 * int(self.b * angle * scale))),2)
		#draws a circle with the center and the radius of the planet designated
		pygame.draw.circle(win, self.colour, (self.x + movex, self.y + movey),self.radius * scale)
		#checks to see if the planet has a ring and if ithe ring number is positive it has a horizontal ring otherwise if its negative the ring is vertical like uranus
		if self.ring > 0:
			#draws a ring
			pygame.draw.ellipse(win, (255, 255, 255),(movex + self.x - (self.radius + 15) * scale, self.y -(self.radius + 15) * scale * angle + movey, 2 *(self.radius + 15) * scale, 2 *(self.radius + 15) * scale * angle), int(3))
			pygame.draw.circle(win,self.colour, (self.x + movex, self.y + movey),self.radius * scale,draw_top_right=True,draw_top_left=True)
			#pygame.draw.circle(win,(255,255,255),(int((self.x)),self.y),int((self.radius+15)*scale),int(3*scale))
		elif self.ring < 0:
			#draws a line as it is a plan view of the planets
			pygame.draw.line(win, (255, 255, 255),(movex + self.x, movey + self.y -(self.radius + 5) * scale),(self.x, self.y + (self.radius + 5) * scale),int(3 * scale))

    #This is for when the mouse is hovering over the planets and it displays the information
	def text_popup(self):
		global hover_sound
		global hover_count
		global planetshoveredover
		#icl sometimes i dont even know why i have to make certain things global but it just works smt lmao
		global font
		global win

		#This basically makes sure that the mouse x coord is past the start and before the end and likewise for the y coordinate
		if pygame.mouse.get_pos()[0] >= self.x + movex - self.radius and pygame.mouse.get_pos()[1] >= self.y - self.radius + movey and pygame.mouse.get_pos()[0] <= self.x + movex + self.radius and pygame.mouse.get_pos()[1] <= self.y + movey + self.radius and self.name != "Asteroid":
			#literally the same code repeated so i cba to explain, it just draws the words
			c = font.render(self.name, 0, (255, 255, 255))
			win.blit(c, (self.x - self.radius * scale,self.y - 2 * self.radius * scale))
			c = font2.render(str(self.name) + ":", 0, (255, 255, 255))
			win.blit(c, (0, 0))
			c = font2.render("Furthest distance: " + str(self.a), 0,(255, 255, 255))
			win.blit(c, (0, 30))
			c = font2.render("Shortest distance: " + str(self.b), 0,(255, 255, 255))
			win.blit(c, (0, 60))
			c = font2.render("Radius: " + str(self.radius), 0, (255, 255, 255))
			win.blit(c, (0, 90))
			c = font2.render("Tilt: " + str(self.tilt) + " degrees", 0,(255, 255, 255))
			win.blit(c, (0, 120))
			c = font2.render("Velocity: " + str(self.speed) + "000 mph", 0,(255, 255, 255))
			win.blit(c, (0, 150))

			hover_count += 1
			#Plays the hover sound
			if hover_sound == 0:
				'''
				mixer.music.load("Hover.mp3")
				mixer.music.set_volume(1)
				mixer.music.play()
				hover_sound = 2
				'''

			if acheivements[5] == 0:
				acheivements[5] = 1

			for j in range(0, 8):
				if planets[j].name == self.name:
					if planetshoveredover[j] == 0:
						planetshoveredover[j] = 1

		#Same code but slightly different for the asteroid belt
		if pygame.mouse.get_pos()[0] >= self.x + movex - self.radius and pygame.mouse.get_pos()[1] >= self.y - self.radius + movey and pygame.mouse.get_pos()[0] <= self.x + movex + self.radius and pygame.mouse.get_pos()[1] <= self.y + movey + self.radius and self.name == "Asteroid":
			c = font.render("Asteroid belt", 0, (255, 255, 255))
			win.blit(c, (10,10))
			hover_count += 1

			if hover_sound == 0:
				'''
				mixer.music.load("Hover.mp3")
				mixer.music.set_volume(1)
				mixer.music.play()
				hover_sound = 2
				'''


#These are the base planets which are the normal ones that exist in our solar system with their respective attributes
baseplanets = [
["Mercury", 119, 114, 1.6, 180, 180, 180, 0, 0, 107, 734,360],
["Venus", 158, 157, 3.8, 222, 171, 2, 3, 0, 78, 798, 360],
["Earth", 184, 181, 4.0, 1, 81, 130, 23, 0, 66, 824, 360],
["Mars", 244, 217, 2.1, 117, 51, 0, 25, 0, 54, 884, 360],
["Jupiter", 598, 550, 43.4, 164, 191, 191, 3, 0, 29, 1238, 360],
["Saturn", 1024, 929, 36.2, 186, 149, 101, 27, 25, 21, 1664, 360],
["Uranus", 1980, 1790, 15.8, 4, 93, 140, 82, -5, 15, 2620, 360],
["Neptune", 2909, 2861, 15.3, 55, 102, 163, 57, 0, 12, 3549, 360]
]



#name, a, b, radius, colour, tilt, ring, speed
#12 values in the database

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
				radius real,
				rr int,
				gg int,
				bb int,
				tilt int,
				ring int,
				speed int,
				x int,
				y int
				)""")
	#will loop through all the base planets and will fill in their attributs in the table
	for i in baseplanets:
		curs.execute(
			f"INSERT INTO {databasename} VALUES (:name,:a,:b,:radius,:rr,:gg,:bb,:tilt,:ring,:speed,:x,:y)",
			{
				'name': i[0],
				'a': i[1],
				'b': i[2],
				'radius': i[3],
				'rr': i[4],
				'gg': i[5],
				'bb': i[6],
				'tilt': i[7],
				'ring': i[8],
				'speed': i[9],
				'x': i[10],
				'y': i[11]
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
	curs.execute(
		f"INSERT INTO {databasename2} VALUES (:zoomin,:zoomout,:speedup,:slowdown,:constellation,:hoveronsingle,:hoveronall,:createnew,:editold,:rotate)",
		{
			'zoomin': 0,
			'zoomout': 0,
			'speedup': 0,
			'slowdown': 0,
			'constellation': 0,
			'hoveronsingle': 0,
			'hoveronall': 0,
			'createnew': 0,
			'editold': 0,
			'rotate': 0
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
		planets.append(planet(i[0], i[1], i[2], i[3], (i[4], i[5], i[6]), i[7], i[8],i[9], i[10], i[11]))

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

asteroid_belt = []
#Same as the planets but for the asteroids
for i in range(0,1000):
	asteroid_belt.append(planet("Asteroid",random.randint(297,390),random.randint(297,390),random.randint(1,3),(150,150,150),0,0,20,0,0))

#just info on the planets
'''
mercury = 29,43
venus = 67,68
earth = 91,94
mars = 128,154lol
jupiter = 460, 508
saturn = 839, 934
uranus = 1700,1890
neptune = 2771, 2819
million miles ^^
everything is in miles
'''
#sun  = 432685.616miles radius ~ 450 -> 90 pixles

#5 miles = 1 pixles

#dead code
'''

#just all the planets and their corresponding values, theyre in an ratio relative to their actual distances and sizes, everythings in miles or miles per hour
mercury = planet("Mercury",29+90*scale,24+90*scale,1.6,(180,180,180),0,0,107,640+(4+90*scale)*scale,360)
venus = planet("Venus",68+90*scale,67+90*scale,3.8,(222, 171, 2),3,0,78,640+(68+90*scale)*scale,360)
earth = planet("Earth",94+90*scale,91+90*scale,4.0,(1, 81, 130),23,0,66,640+(94+90*scale)*scale,360)
mars = planet("Mars",154+90*scale,127+90*scale,2.1,(117, 51, 0),25,0,54,640+90+154*scale,360)
#asteroid belt - idk if ill get to it but mabye
jupiter = planet("Jupiter",508+90,460+90,43.4,(164, 191, 191),3,0,29,640+(508+90*scale)*scale,360)
saturn = planet("Saturn",934+90*scale,839+90*scale,36.2,(186, 149, 101),27,25,21,640+(934+90*scale)*scale,360)
uranus = planet("Uranus",1890+90*scale,1700+90*scale,15.8,(4, 93, 140),82,-5,15,640+(1890+90*scale)*scale,360)
neptune = planet("Neptune",2819+90*scale,2771+90*scale,15.3,(55, 102, 163),57,0,12,640+(2819+90*scale)*scale,360)

#putting all the object in a class so that its easier to edit all of them
planets = [mercury,venus,earth,mars,jupiter,saturn,uranus,neptune]

'''
#probs just dead code coz i dont think ill use this anymore but it was basically making them not to scale because eveything was so far away
'''
if not toscale:
	for i in range(0,len(planets)):
		if i < 4:
			planets[i].radius *= 4
			planets[i].a -= (4-i)*5
			planets[i].b -= (4-i)*5
		
		else:
			planets[i].a /= (i/2)
			planets[i].b /= (i/2)
		if i > 5:
			planets[i].a /= (i/4.5)
			planets[i].b /= (i/4.5)
		if  i == 2:
			planets[i].a += 25
			planets[i].b += 25
'''

#more dead code that idk if ill use but it would draw the planets but i think ive found a better way of doing it
'''
for i in planets:
	pygame.draw.ellipse(win, (255,255,255), ((640-90-i.a*scale),(360-90-i.b*scale),(2*i.a*scale+180),(2*i.b*scale+180)),2)
	pygame.draw.circle(win, i.colour[0], ((i.x),i.y),i.radius*scale)

	if i.ring[0] > 0:

		pygame.draw.circle(win,i.ring[1],(int((i.x)),i.y),int((i.radius+15)*scale),int(3*scale))
	elif i.ring[0] < 0:
		pygame.draw.line(win,i.ring[1],(int((640+90+i.a)*scale),int((360+20)*scale)),(int((640+90+i.a)*scale),int((360-20)*scale)),int(3*scale))
'''


#The asteroid belt needs to be reset every time its zoomed in otherwise it will break
def reset_asteroid_belt():
	for i in asteroid_belt:
		i.x = random.randint(int(640-i.a*scale),int(640+i.a*scale))
		if random.randint(1,2) == 1:
			i.y = 360 + ((i.b * angle) * scale) * ((1 -((i.x - 640) / (i.a * scale))**2)**0.5)
			if isinstance(i.y, complex):
				i.y = 359
				i.x = 640 + i.a * scale
		else:
			i.y =  360 - ((i.b * angle) * scale) * ((1 -((i.x - 640) / (i.a * scale))**2)**0.5)
			if isinstance(i.y, complex):
				i.y = 359
				i.x = 640 - i.a * scale

#what changes the scale of all thye planets and orbits and the sun
#code is so basic i cba to explain, its 1 in the morning
def scale_change(num):
	global scale
	if num > 0 and scale < 1.2:
		scale += num
		reset_asteroid_belt()
		if acheivements[0] == 0:
			acheivements[0] = 1
	elif num < 0 and scale > 0.3:
		scale += num
		reset_asteroid_belt()
		if acheivements[1] == 0:
			acheivements[1] = 1
	else:
		print("Scaled in too much")


#will do one for the orbit time as well
#nvm already have done
def a_time_changer(num):
	global a_time
	if num > 0 and a_time < 0.1:
		a_time += num
		if acheivements[2] == 0:
			acheivements[2] = 1
	elif num < 0 and a_time >= 0:
		a_time += num
		if acheivements[3] == 0:
			acheivements[3] = 1
	if a_time < 0:
		a_time = 0
	else:
		print("Max")


#Same thing for changing tha angle against the horizontal
def angle_changer(num):
	global angle
	if num > 0 and round(angle, 1) < 1:
		angle += num

		if acheivements[9] == 0:
			acheivements[9] = 1

	elif num < 0 and round(angle, 1) > 0.1:
		angle += num

		if acheivements[9] == 0:
			acheivements[9] = 1

	if angle <= 0:
		angle = 0.1
	else:
		print("Max")


'''
#playes music
mixer.init() 
#find a more appropriate song tho mate
mixer.music.load("MDK_Space_invaders.mp3") 
mixer.music.set_volume(0.01) 
mixer.music.play()
'''


stars = []

for i in range(0,20):
	stars.append((random.randint(10,100),random.randint(0,100)))


#Draws the star constellation
def star_constellation():
	global acheivements
	if pygame.mouse.get_pos()[0] >= 10 and pygame.mouse.get_pos()[1] >= 10 and pygame.mouse.get_pos()[0] <= 100 and pygame.mouse.get_pos()[1] <= 100:
		for i in stars:
			pygame.draw.circle(win, (255, 255, 255), (i[0], i[1]), random.randint(1,3))


		c = font2.render("Star constellation", 0, (255, 255, 255))
		win.blit(c, (1000, 0))
		c = font2.render("Information about it", 0, (255, 255, 255))
		win.blit(c, (1000, 30))
		if acheivements[4] == 0:
			acheivements[4] = 1


#This is what will be draw when the help menu is initaited
help_menu = [
	"Help menu",
	"Use → and ← to change the speed of the planets", "Use ↑ and ↓ to change the angle with the horizontal",
	"Press H to go home", "Use WASD to move the center of the system", "Press (E) to edit/create planets", "Press (L) to go to acheivements",
	"(T) to toggle orbits on and off","Any changes you make to the program will be saved under your username","Your acheivements will also be saved"
]
#new font which is much smaller than the other 2 so that it can be at the bottom but not be obscuring
font3 = pygame.font.SysFont("Arial", 15)

font4 = pygame.font.SysFont("Arial", 20)
#variables useful in the code
current = 0
z = 0
alphabet = "abcdefghijklmnopqrstuvwxyz0123456789(),"
pos = 0
acheivementscheck = []
for i in acheivements:
	acheivementscheck.append(i)

acheivementslist = [
	"zoom in", "zoom out", "speed up", "slow down", "find the constellation",
	"hover over a planet", "hover over all the planets", "create a new planet",
	"edit a new planet", "rotate along the horizontal"
]

hover_sound2 = 0
clock = pygame.time.Clock()
while run:
	#runs the game at 60fps
	clock.tick(60)
	hover_count = 0
	#creates the font
	font = pygame.font.SysFont("Arial", int(32 * (scale**0.5)))
	pygame.draw.rect(win, (0, 0, 0), (0, 0, 1280, 10))
	#draws the background image

	win.blit(bg, (0, 10))
	if planetshoveredover == [1, 1, 1, 1, 1, 1, 1, 1]:
		acheivements[6] = 1

	#if the place is the planets not any menu then itll draw the planets
	if back.place == "home":
		#draws the sun in the center
		pygame.draw.circle(win, (255, 205, 5), (640 + movex, 360 + movey),(90 * (scale**2)))
	#loops through all the planets and passes them through the orbit function which draws them and the text popup function checks whether the mouse is over the planets

		for i in planets+asteroid_belt:
			i.orbit()
			i.text_popup()
		star_constellation()
		if hover_count == 0:
			hover_sound = 0
		pygame.draw.circle(win, (255, 205, 5), (640 + movex, movey + 360),(90 * (scale**2)),draw_top_right=True,draw_top_left=True)
		#draws a little notice at the bottom of the screen if anyone wants help
		win.blit(font3.render("Press (H) for help", 0, (255, 255, 255)),(587, 700))
		#for anything happening in pygame  it will loop through these conditions
		for event in pygame.event.get():
			#If the user has perssed a key then it will see what key is pressed
			if event.type == pygame.KEYDOWN:
				#if its H then it will change place to the help menu
				if event.key == pygame.K_h:
					back.place = "help"
				#If its e then it will change place to the editor selection menu
				if event.key == pygame.K_e:
					back.place = "editor_sel"

				if event.key == pygame.K_l:
					back.place = "acheivements"
				#if the plus arrow is pressed it will call the scale change function which zooms in
				if event.key == pygame.K_KP_PLUS or event.key == pygame.K_z:
					scale_change(0.1)
				#same for minus
				if event.key == pygame.K_KP_MINUS or event.key == pygame.K_x:
					scale_change(-0.1)
				if event.key == pygame.K_RIGHT:
					a_time_changer(0.001)
				#^^
				if event.key == pygame.K_LEFT:
					a_time_changer(-0.001)
				if event.key == pygame.K_UP:
					angle_changer(-0.1)
				if event.key == pygame.K_DOWN:
					angle_changer(0.1)
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
			#If the X button at the top is pressed then it will exit the program
			if event.type == pygame.QUIT:
				run = False

    #If the place is help then it will just draw the help menu and check whether the H key has been pressed again which would then direct you home to the planets
	elif back.place == "help":
		for event in pygame.event.get():
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_h:
					back.place = "home"
			if event.type == pygame.QUIT:
				run = False
		win.blit(font3.render("Press (H) to return", 0, (255, 255, 255)),(585, 700))
		for i in range(0, len(help_menu)):
			win.blit(font2.render(help_menu[i], 0, (255, 255, 255)),(5, i * 32))
	#changes to the editor selction menu
	elif back.place == "editor_sel":
		for event in pygame.event.get():
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_h:
					back.place = "home"
			if event.type == pygame.QUIT:
				run = False
			#if the user clicks and its on one of the buttons it will go to that menu
			if event.type == pygame.MOUSEBUTTONDOWN:
				if event.pos[0] >= 500 and event.pos[0] <= 500 + 280:
					if event.pos[1] >= 220 and event.pos[1] <= 220 + 135:
						back.place = "editor_edit"
						'''
						mixer.music.load("Select.mp3")
						mixer.music.set_volume(1)
						mixer.music.play()
						'''
					if event.pos[1] >= 365 and event.pos[1] <= 365 + 135:

						back.place = "editor_create"
						'''
						mixer.music.load("Select.mp3")
						mixer.music.set_volume(1)
						mixer.music.play()
						'''

		#just drawing the buttons

		#base
		pygame.draw.rect(win, (255, 255, 255), (490, 210, 300, 300), 2)
		#edit
		pygame.draw.rect(win, (255, 255, 255), (500, 220, 280, 135), 2)
		#create
		pygame.draw.rect(win, (255, 255, 255), (500, 365, 280, 135), 2)

		#blitting them onto the screen

		win.blit(font2.render("Edit Planet", 0, (255, 255, 255)), (560, 265))
		win.blit(font2.render("Create New Planet", 0, (255, 255, 255)),(505, 410))
		win.blit(font3.render("Press (H) to return", 0, (255, 255, 255)),(585, 700))

	elif back.place == "editor_edit":
		if z == 0:
			z += 1
			#These temporatily get the names so that when they get edited if theres any problem it jsut reverts to the orignal
			strings = [
				planets[current].name,
				str(planets[current].a),
				str(planets[current].b),
				str(planets[current].radius),
				str(planets[current].colour),
				str(planets[current].tilt),
				str(planets[current].ring),
				str(planets[current].speed)
			]
			pos = 0
			r = ""
			g = ""
			b = ""

		win.blit(font3.render("Press (/) to cancel", 0, (255, 255, 255)),(585, 700))

		win.blit(font4.render("Name", 0, (255, 255, 255)), (610, 10))
		pygame.draw.rect(win, (255, 255, 255), (560, 40, 160, 40), 2)
		win.blit(font4.render("Furthest horizontal distance from the sun", 0,(255, 255, 255)), (460, 80))
		pygame.draw.rect(win, (255, 255, 255), (560, 110, 160, 40), 2)
		win.blit(font4.render("Furthest vertical distance from the sun", 0,(255, 255, 255)), (470, 150))
		pygame.draw.rect(win, (255, 255, 255), (560, 180, 160, 40), 2)
		win.blit(font4.render("Radius", 0, (255, 255, 255)), (610, 220))
		pygame.draw.rect(win, (255, 255, 255), (560, 250, 160, 40), 2)
		win.blit(font4.render("Colour", 0, (255, 255, 255)), (610, 290))
		pygame.draw.rect(win, (255, 255, 255), (560, 320, 160, 40), 2)
		win.blit(font4.render("Tilt", 0, (255, 255, 255)), (630, 360))
		pygame.draw.rect(win, (255, 255, 255), (560, 390, 160, 40), 2)
		win.blit(font4.render("Ring", 0, (255, 255, 255)), (620, 430))
		pygame.draw.rect(win, (255, 255, 255), (560, 460, 160, 40), 2)
		win.blit(font4.render("Speed", 0, (255, 255, 255)), (610, 500))
		pygame.draw.rect(win, (255, 255, 255), (560, 530, 160, 40), 2)
		pygame.draw.polygon(win, (255, 255, 255),((760, 60), (730, 75), (730, 45)))
		pygame.draw.polygon(win, (255, 255, 255),((520, 60), (550, 75), (550, 45)))

		win.blit(font4.render(strings[0], 0, (255, 255, 255)), (560, 40))
		win.blit(font4.render(strings[1], 0, (255, 255, 255)), (560, 110))
		win.blit(font4.render(strings[2], 0, (255, 255, 255)), (560, 180))
		win.blit(font4.render(strings[3], 0, (255, 255, 255)), (560, 250))
		win.blit(font4.render(strings[4], 0, (255, 255, 255)), (560, 320))
		win.blit(font4.render(strings[5], 0, (255, 255, 255)), (560, 390))
		win.blit(font4.render(strings[6], 0, (255, 255, 255)), (560, 460))
		win.blit(font4.render(strings[7], 0, (255, 255, 255)), (560, 530))

		pygame.draw.rect(win, (255, 255, 255), (1200, 670, 70, 40), 2)
		win.blit(font4.render("Reset", 0, (255, 255, 255)), (1210, 680))

		for event in pygame.event.get():
			if event.type == pygame.KEYDOWN:
				for i in alphabet:
					if event.unicode == i:
						strings[pos] = strings[pos] + event.unicode
				if event.key == 13 or event.key == 1073741905:
					pos += 1
					'''
					mixer.music.load("Hover.mp3")
					mixer.music.set_volume(1)
					mixer.music.play()
					'''
				if event.key == 1073741906:
					pos -= 1
					'''
					mixer.music.load("Hover.mp3")
					mixer.music.set_volume(1)
					mixer.music.play()
					'''
					if pos == -1:
						pos = 0
				if event.key == 8:
					strings[pos] = strings[pos][:len(strings[pos]) - 1]
				if event.key == 47:
					back.place = "home"
				if event.key == pygame.K_KP_PLUS or pos == 8:
					back.place = "home"
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
								r = r + i
							elif tally == 2:
								g = g + i
							elif tally == 3 and i != ")":
								b = b + i
						colourinput = (int(r), int(g), int(b))
						tiltinput = int(strings[5])
						ringinput = int(strings[6])
						speedinput = int(strings[7])

						if ainput < 90 + radiusinput:
							ainput = 90 + radiusinput + 5
						if binput < 90 + radiusinput:
							binput = 90 + radiusinput + 5

						#connects to a database called users_planets
						conn = sqlite3.connect('User_information.db')
						#creates a cursor to the database
						curs = conn.cursor()
						curs.execute(
							f"""UPDATE {databasename} SET
							name = :name,
							a = :a,
							b = :b,
							radius = :radius,
							rr = :rr,
							gg = :gg,
							bb = :bb,
							tilt = :tilt,
							ring = :ring,
							speed = :speed

							WHERE oid = :oid""", {
								'name': nameinput,
								'a': ainput,
								'b': binput,
								'radius': radiusinput,
								'rr': colourinput[0],
								'gg': colourinput[1],
								'bb': colourinput[2],
								'tilt': tiltinput,
								'ring': ringinput,
								'speed': speedinput,
								'oid': current + 1
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
							planets.append(planet(i[0], i[1], i[2], i[3],(i[4], i[5], i[6]), i[7], i[8], i[9],i[10], i[11]))

						curs.execute(f"SELECT oid FROM {databasename}")
						conn.commit()
						conn.close()
					except Exception as e:
						print(e)
						print("incorrect values")  #do popup ltr

			if event.type == pygame.QUIT:
				run = False
			if event.type == pygame.MOUSEBUTTONDOWN:
				if event.pos[1] >= 45 and event.pos[1] <= 75:
					if event.pos[0] >= 730 and event.pos[0] <= 760:
						current += 1
						z = 0
						'''
						mixer.music.load("Select.mp3")
						mixer.music.set_volume(1)
						mixer.music.play()

						'''
					if event.pos[0] >= 520 and event.pos[0] <= 550:
						current -= 1
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
						for i in range(1, len(planets) + 1):
							curs.execute(f"DELETE FROM {databasename} WHERE oid= {i}")
						curs.execute(f"SELECT * FROM {databasename}")
						conn.commit()
						conn.close()
						conn = sqlite3.connect('User_information.db')
						curs = conn.cursor()
						for i in baseplanets:
							curs.execute(f"INSERT INTO {databasename} VALUES (:name,:a,:b,:radius,:rr,:gg,:bb,:tilt,:ring,:speed,:x,:y)",
							{
									'name': i[0],
									'a': i[1],
									'b': i[2],
									'radius': i[3],
									'rr': i[4],
									'gg': i[5],
									'bb': i[6],
									'tilt': i[7],
									'ring': i[8],
									'speed': i[9],
									'x': i[10],
									'y': i[11]
								})
						curs.execute(f"SELECT * FROM {databasename}")
						planets = []
						for i in curs.fetchall():
							planets.append(planet(i[0], i[1], i[2], i[3],(i[4], i[5], i[6]), i[7], i[8], i[9],i[10], i[11]))
						conn.commit()
						conn.close()

						back.place = "home"

		if pos != 8:
			pygame.draw.rect(win, (100, 100, 100),(560, 40 + 70 * pos, 160, 40), 2)

		if pygame.mouse.get_pos()[1] >= 45 and pygame.mouse.get_pos()[1] <= 75:
			if pygame.mouse.get_pos()[0] >= 730 and pygame.mouse.get_pos()[0] <= 760:
				pygame.draw.polygon(win, (100, 100, 100),((760, 60), (730, 75), (730, 45)))
				if hover_sound2 == 0:
					'''
					mixer.music.load("Hover.mp3")
					mixer.music.set_volume(1)
					mixer.music.play()
					hover_sound2 = 1
					'''

			if pygame.mouse.get_pos()[0] >= 520 and pygame.mouse.get_pos()[0] <= 550:
				pygame.draw.polygon(win, (100, 100, 100),((520, 60), (550, 75), (550, 45)))
				if hover_sound2 == 0:
					'''
					mixer.music.load("Hover.mp3")
					mixer.music.set_volume(1)
					mixer.music.play()
					hover_sound2 = 1
					'''
		else:
			hover_sound2 = 0

	elif back.place == "editor_create":
		if z == 0:
			z += 1
			strings = ["", "", "", "", "", "", "", ""]
			pos = 0
			r = ""
			g = ""
			b = ""
		win.blit(font3.render("Press (/) to cancel", 0, (255, 255, 255)),(585, 700))

		win.blit(font4.render("Name", 0, (255, 255, 255)), (610, 10))
		pygame.draw.rect(win, (255, 255, 255), (560, 40, 160, 40), 2)
		win.blit(font4.render("Furthest horizontal distance from the sun", 0,(255, 255, 255)), (460, 80))
		pygame.draw.rect(win, (255, 255, 255), (560, 110, 160, 40), 2)
		win.blit(font4.render("Furthest vertical distance from the sun", 0,(255, 255, 255)), (470, 150))
		pygame.draw.rect(win, (255, 255, 255), (560, 180, 160, 40), 2)
		win.blit(font4.render("Radius", 0, (255, 255, 255)), (610, 220))
		pygame.draw.rect(win, (255, 255, 255), (560, 250, 160, 40), 2)
		win.blit(font4.render("Colour", 0, (255, 255, 255)), (610, 290))
		pygame.draw.rect(win, (255, 255, 255), (560, 320, 160, 40), 2)
		win.blit(font4.render("Tilt", 0, (255, 255, 255)), (630, 360))
		pygame.draw.rect(win, (255, 255, 255), (560, 390, 160, 40), 2)
		win.blit(font4.render("Ring", 0, (255, 255, 255)), (620, 430))
		pygame.draw.rect(win, (255, 255, 255), (560, 460, 160, 40), 2)
		win.blit(font4.render("Speed", 0, (255, 255, 255)), (610, 500))
		pygame.draw.rect(win, (255, 255, 255), (560, 530, 160, 40), 2)

		win.blit(font4.render(strings[0], 0, (255, 255, 255)), (560, 40))
		win.blit(font4.render(strings[1], 0, (255, 255, 255)), (560, 110))
		win.blit(font4.render(strings[2], 0, (255, 255, 255)), (560, 180))
		win.blit(font4.render(strings[3], 0, (255, 255, 255)), (560, 250))
		win.blit(font4.render(strings[4], 0, (255, 255, 255)), (560, 320))
		win.blit(font4.render(strings[5], 0, (255, 255, 255)), (560, 390))
		win.blit(font4.render(strings[6], 0, (255, 255, 255)), (560, 460))
		win.blit(font4.render(strings[7], 0, (255, 255, 255)), (560, 530))

		for event in pygame.event.get():
			if event.type == pygame.KEYDOWN:
				for i in alphabet:
					if event.unicode == i:
						strings[pos] = strings[pos] + event.unicode
				if event.key == 8:
					strings[pos] = strings[pos][:len(strings[pos]) - 1]
				if event.key == 47:
					back.place = "home"
				if event.key == pygame.K_KP_PLUS or pos == 8:
					back.place = "home"
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
								r = r + i
							elif tally == 2:
								g = g + i
							elif tally == 3 and i != ")":
								b = b + i
						colourinput = (int(r), int(g), int(b))
						tiltinput = int(strings[5])
						ringinput = int(strings[6])
						speedinput = int(strings[7])

						if ainput < 90 + radiusinput:
							ainput = 90 + radiusinput + 5
						if binput < 90 + radiusinput:
							binput = 90 + radiusinput + 5

						conn = sqlite3.connect('User_information.db')
						curs = conn.cursor()

						curs.execute(f"INSERT INTO {databasename} VALUES (:name,:a,:b,:radius,:rr,:gg,:bb,:tilt,:ring,:speed,:x,:y)",
							{
								'name': nameinput,
								'a': ainput,
								'b': binput,
								'radius': radiusinput,
								'rr': colourinput[0],
								'gg': colourinput[1],
								'bb': colourinput[2],
								'tilt': tiltinput,
								'ring': ringinput,
								'speed': speedinput,
								'x': 640 + ainput,
								'y': 360
							})
						curs.execute(f"SELECT * FROM {databasename}")
						planets = []
						for i in curs.fetchall():
							planets.append(planet(i[0], i[1], i[2], i[3],(i[4], i[5], i[6]), i[7], i[8], i[9],i[10], i[11]))
						conn.commit()
						conn.close()
					except Exception as e:
						print(e)  #change when you can
				if event.key == 13 or event.key == 1073741905:
					pos += 1
					'''
					mixer.music.load("Hover.mp3")
					mixer.music.set_volume(1)
					mixer.music.play()
					'''
				if event.key == 1073741906:
					pos -= 1
					'''
					mixer.music.load("Hover.mp3")
					mixer.music.set_volume(1)
					mixer.music.play()
					'''
					if pos == -1:
						pos = 0
			if event.type == pygame.QUIT:
				run = False

		if pos != 8:
			pygame.draw.rect(win, (100, 100, 100),(560, 40 + 70 * pos, 160, 40), 2)

	elif back.place == "acheivements":
		for i in range(0, 10):
			win.blit(font4.render(acheivementslist[i], 0, (100, 100, 100)),(560, 10 + 40 * i))
			if acheivements[i] == 1:
				win.blit(font4.render(acheivementslist[i], 0, (255, 255, 255)),(560, 10 + 40 * i))
		

		if acheivements == [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]:
			win.blit(font2.render("All acheivements completed", 0, (255, 255, 255)),(560, 10 + 40 * 11))

		for event in pygame.event.get():
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_h:
					back.place = "home"
			if event.type == pygame.QUIT:
				run = False

		win.blit(font3.render("Press (H) to return", 0, (255, 255, 255)),(585, 700))

	if back.place != "editor_edit" and back.place != "editor_create":
		current = 0
		z = 0
	if back.place != "home":
		scale = 1
		angle = 1
		a_time = 0.01

	#updates any changes made to the graphics
	pygame.display.update()
	if current == len(planets):
		current = 0
	elif current == -1:
		current = len(planets) - 1
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

							WHERE oid = :oid""", {
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
				'oid': 1
			})

		curs.execute(f"SELECT * FROM {databasename2}")
		conn.commit()
		#closes the connection
		conn.close()
		acheivementscheck = []
		for i in acheivements:
			acheivementscheck.append(i)
