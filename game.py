"""SideScroll game"""

import math
import random

import pyglet
from pyglet import app, clock, image
from pyglet.graphics import Batch
from pyglet.sprite import Sprite
from pyglet.window import Window, key, mouse

# The images used for sprites
images = {
    'arch':   image.load('sprites/arch-rotated.png'),
    'bullet': image.load('sprites/tilde.png'),
    'star':   image.load('sprites/star.png'),
    'windows': image.load('sprites/big_windows.png'),
}

class Player(Sprite):
    def __init__(self, game, keyboard, *args, **kwargs):
        super(Player, self).__init__(*args, **kwargs)

        # Reference the keyboard object so that we can watch it
        self.keyboard = keyboard

	self.game = game	

	self.paused = False;

	self.health = 5
	self.points = 0

        # Call move_player() 60 times a second
        clock.schedule_interval(self.move, 1/60.0)

	clock.schedule_interval(self.check_if_paused, 1/10.0)

    def is_sprite_in_bounds(self, sprite, border=0):
    	"""Returns true if a sprite is in the window"""
        x = sprite.x + sprite.width / 2
        y = sprite.y + sprite.height / 2
        return (border < x < self.width - border
        	and border < y < self.height - border)

    def move(self, dt):
        """This is called on every update

        It uses the keyboard input to move the player
        at around 200 pixels per second"""

        distance = dt * 400
    
	#Edges dont seem to be at the same size of window.....
	#locks ships x axis, can not go off screen in x direction
       	if (self.keyboard[key.RIGHT] or self.keyboard[key.D]) and (self.x < self.game.width-self.width):
       	    	self.x += distance
        
       	if (self.keyboard[key.LEFT] or self.keyboard[key.A]) and (self.x > 0):
      		self.x -= distance

       	if (self.keyboard[key.UP] or self.keyboard[key.W]) and (self.y < self.game.height-(self.height/3)*2):
       		self.y += distance

       	if (self.keyboard[key.DOWN] or self.keyboard[key.S]) and (self.y > 0-self.height/3):
      		self.y -= distance


########################## Pause button #######################
    def check_if_paused(self, dt):
	if (self.keyboard[key.P]):
		self.check_pause()	

    def check_pause(self):
	if(self.paused):
		print "True"
		self.paused = False
		self.game.resume()
	else:
		print "False"
		self.paused = True
		self.game.clear_schedules()

	

class Game(Window):
    def __init__(self):
        """This is run when the game is created"""
        super(Game, self).__init__()

        # A handler that watches the keyboard state
        self.keyboard = key.KeyStateHandler()
        self.set_handlers(self.keyboard)

	#label for the pause menu
#	self.label = pyglet.text.Label

        # Create the sprites
        self.player = Player(self, self.keyboard, images['arch'], x=100, y=50)

        self.bullet_batch = Batch()
        self.bullets = []

	#background stars
	self.star_batch = Batch()
	self.stars = []
	
	self.fast_star_batch = Batch()
	self.fast_stars = []

	#windows enemies
	self.enemy_batch = Batch()
	self.win_enemy = [] 

        # Display the current FPS on screen
        self.fps_display = clock.ClockDisplay()

        clock.schedule_interval(self.update_bullets, 1/30.0)
        clock.schedule_interval(self.fire_bullets, 1/15.0)

	#update background 
	clock.schedule_interval(self.update_stars, 1/15.0)
	clock.schedule_interval(self.background_1, 1/10.0)
	clock.schedule_interval(self.update_back_stars, 1/30.0)
	clock.schedule_interval(self.background_2, 1/20.0 )

	time = random.uniform(2.0, 5.0)
	
	#update enemies
	clock.schedule_interval(self.update_enemy, 1/60.0)
	clock.schedule_interval(self.enemy, 1/time)

	#update enemy hit
	clock.schedule_interval(self.on_hit, 1/60.0)
	
	#check players health
	clock.schedule_interval(self.checkHealth, 1/60.0)

	#refreshes player info
	clock.schedule_interval(self.gui_update, 1/60.0)

	#update player hit
	clock.schedule_interval(self.on_hit_player, 1/59.0)

    def gui_update(self, dt):
	self.player_points = pyglet.text.Label('Player Points: %d' % self.player.points,
						font_size=14,
                                                x= 100,
                                                y= 25,
                                                anchor_x='center',
                                                )

	self.player_health = pyglet.text.Label('Player Health: %d' % self.player.health, 
                                                font_size=14,
                                                x= 275,
                                                y= 25,
                                                anchor_x='center',
                                                )

	


    #change border to allow sprites off screen
    def is_sprite_in_bounds(self, sprite, border=-50):
        """Returns true if a sprite is in the window"""
        x = sprite.x + sprite.width / 2
        y = sprite.y + sprite.height / 2
        return (border < x < self.width - border
            and border < y < self.height - border)

#-------------------------------------Enemies section --------------------------#
    def update_enemy(self, dt):
	for enemy in self.win_enemy:
		enemy.x = enemy.x - dt * 200
		enemy.y = enemy.startY + math.sin((enemy.x + enemy.startY) / 50)*50
		if not self.is_sprite_in_bounds(enemy):
		    self.win_enemy.remove(enemy)

    def enemy(self, dt):
	"""creates enemies """
        enemy = Sprite(images['windows'], batch=self.enemy_batch)

	enemy.y = random.uniform(0, self.width)
	enemy.x = self.width
	enemy.startX = enemy.x
	enemy.startY = enemy.y

	self.win_enemy.append(enemy)	


#--------------------------------------Background stuff -------------------------#
    def update_back_stars(self, dt):
	for fast_star in self.fast_stars:
	    fast_star.x = fast_star.x + (fast_star.scale-10)*1.0 
	    if not self.is_sprite_in_bounds(fast_star):
		self.fast_stars.remove(fast_star)

    def background_2(self, dt):
	"""Random stars created in back moving faster"""
	fast_star = Sprite(images['star'], batch=self.fast_star_batch)

	fast_star.y = random.uniform(0, self.height)
	fast_star.x = self.width
	
	fast_star.scale = random.uniform(0.2, 2)

	self.fast_stars.append(fast_star)

    #creates a load of left moving stars for background
    def update_stars(self, dt):
	for star in self.stars:
	    star.x = star.x + (star.scale-10)*1.0
	    if not self.is_sprite_in_bounds(star):
		self.stars.remove(star)

    def background_1(self, dt):
	"""create random number of stars at random y co ordinates"""
	#for star in self.star:
	star = Sprite(images['star'], batch=self.star_batch)
	
	star.y = random.uniform(0,self.width-2)
	star.x = self.width 

	star.scale = random.uniform(0.2, 2)
	
	self.stars.append(star) 


#-----------------------------------bullet update and collision------------------#
    def update_bullets(self, dt):
        for bullet in self.bullets:
            bullet.x = bullet.x + dt * 800
            if not self.is_sprite_in_bounds(bullet):
                self.bullets.remove(bullet)

    def fire_bullets(self, dt):
        if self.keyboard[key.SPACE]:
            self.fire()

    def on_hit(self, dt):
	for bullet in self.bullets:
	    for enemy in self.win_enemy:
	#	print bullet.x
		if bullet.x > enemy.x and bullet.x < (enemy.x + enemy.width) and bullet.y < enemy.y+enemy.height and bullet.y > enemy.y-enemy.height:
		    self.bullets.remove(bullet)
		    self.win_enemy.remove(enemy)
		    self.player.points += 1
		    print "Points: %d" %  (self.player.points)

################################################################# Check player health if <= 0 clear screen display game over
    def checkHealth(self, dt):
        if self.player.health <= 0:
	   self.clear_schedules()
	   self.player.health = 5
	   	   
    def clear_schedules(self):
	clock.unschedule(self.update_bullets)
	clock.unschedule(self.fire_bullets)
	clock.unschedule(self.update_stars)
	clock.unschedule(self.background_1)
	clock.unschedule(self.update_back_stars)
	clock.unschedule(self.background_2)
	clock.unschedule(self.update_enemy)
	clock.unschedule(self.enemy)
	clock.unschedule(self.on_hit)
	clock.unschedule(self.checkHealth)
	clock.unschedule(self.gui_update)
	clock.unschedule(self.on_hit_player)
	clock.unschedule(self.player.move)
	#self.clear();

    def resume(self):
	clock.schedule_interval(self.update_bullets, 1/30.0)
        clock.schedule_interval(self.fire_bullets, 1/15.0)
        clock.schedule_interval(self.update_stars, 1/15.0)
        clock.schedule_interval(self.background_1, 1/10.0)
        clock.schedule_interval(self.update_back_stars, 1/30.0)
        clock.schedule_interval(self.background_2, 1/20.0 )
        clock.schedule_interval(self.update_enemy, 1/60.0)
	time = random.uniform(2.0, 5.0)
        clock.schedule_interval(self.enemy, 1/time)
        clock.schedule_interval(self.on_hit, 1/60.0)
        clock.schedule_interval(self.checkHealth, 1/60.0)
        clock.schedule_interval(self.gui_update, 1/60.0)
        clock.schedule_interval(self.on_hit_player, 1/59.0)
	clock.schedule_interval(self.player.move, 1/60.0)


	
###################################################################

    def on_hit_player(self, dt):
	for enemy in self.win_enemy:
	   if enemy.x < self.player.x and enemy.x > self.player.x-self.player.width and enemy.y < self.player.y+self.player.height and enemy.y > self.player.y-self.player.height:
		self.win_enemy.remove(enemy)
		self.player.health = self.player.health -1
		print "Health: %d" % self.player.health

    def on_draw(self):
        """Clear the window, display the framerate and draw the sprites"""
        self.clear()
        self.fps_display.draw()

        # Draw the sprites
        self.star_batch.draw()
	self.fast_star_batch.draw()
	self.enemy_batch.draw()
	self.player.draw()
        self.bullet_batch.draw()
	
	self.player_points.draw()
	self.player_health.draw()

    def fire(self):
        """Create a new bullet"""
        bullet = Sprite(images['bullet'], batch=self.bullet_batch)
        
        bullet.x = self.player.x + self.player.width  
        bullet.y = self.player.y + self.player.height / 2 - bullet.height / 2

        self.bullets.append(bullet)


    def on_mouse_press(self, x, y, button, modifiers):
        """This is run when a mouse button is pressed"""
        if button == mouse.LEFT:
            print "The left mouse button was pressed."
        elif button == mouse.RIGHT:
           print "The right mouse button was pressed."

window = Game()
app.run()
