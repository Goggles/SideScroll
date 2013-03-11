"""SideScroll game"""
import math

from pyglet import app, clock, image
from pyglet.sprite import Sprite
from pyglet.window import Window, key, mouse

# The images used for sprites
images = {
    'arch':   image.load('sprites/arch-rotated.png'),
    'bullet': image.load('sprites/tilde.png'),
    'star':   image.load('sprites/star.png'),
}

#global ship x and y co ordinates
global ship_x 
global ship_y 

class Player(Sprite):
    def __init__(self, keyboard, *args, **kwargs):
        super(Player, self).__init__(*args, **kwargs)

        # Reference the keyboard object so that we can watch it
        self.keyboard = keyboard

	#add speed of bullet
	self.bullet_speed = 700.0

        # Call move_player() 60 times a second
        clock.schedule_interval(self.move, 1/60.0)

    
    def move(self, dt):
        """This is called on every update

        It uses the keyboard input to move the player
        at around 200 pixels per second"""
	global ship_x
	global ship_y

        distance = dt * 200
	
	#update ship img pos and global co ordinates
        if self.keyboard[key.RIGHT]:
            self.x += distance
	    ship_x = self.x
        
	if self.keyboard[key.LEFT]:
            self.x -= distance
	    ship_x = self.x

        if self.keyboard[key.UP]:
            self.y += distance
	    ship_y = self.y

        if self.keyboard[key.DOWN]:
            self.y -= distance
	    ship_y = self.y


class Game(Window):
    def __init__(self):
        """This is run when the game is created"""
        super(Game, self).__init__()

        # A handler that watches the keyboard state
        self.keyboard = key.KeyStateHandler()
        self.set_handlers(self.keyboard)

        # Create the sprites
        self.player = Player(self.keyboard, images['arch'], x=50, y=50)
        #self.bullet = Sprite(images['bullet'], x=50, y=50)

        # Display the current FPS on screen
        self.fps_display = clock.ClockDisplay()

    def on_draw(self):
        """Clear the window, display the framerate and draw the sprites"""
        self.clear()
        self.fps_display.draw()

        # Draw the sprites
        self.player.draw()

	if self.keyboard[key.SPACE]:
		self.fire()

#-------------------- Trying to update bullet so moves off screen -------------
    def fire(self):
	if self.keyboard[key.SPACE]:
		print 'Spaceeee'
		global ship_x
		global ship_y
	 	temp_ship_x = ship_x + 55	
		temp_ship_y = ship_y + 18		
	#	print ship_x
	#	self.bullet_sprite = pyglet.sprite.Sprite(bullet)
	#	self.bullet_sprite.dx = 10.0
		
		#self.bullet.dx = 10.0		
                
		self.bullet = Sprite(images['bullet'], x = temp_ship_x, y = temp_ship_y)
		self.bullet.draw()
		temp_ship_x = 0
		temp_ship_y = 0

 #   def bullet_update(dt):
#	bullet.x += bullet_sprite_dx  * dt
 #   clock.schedule_interval(bullet_update, 1/60.0)		
	
    def on_mouse_press(self, x, y, button, modifiers):
        """This is run when a mouse button is pressed"""
        if button == mouse.LEFT:
            print "The left mouse button was pressed."
        elif button == mouse.RIGHT:
           print "The right mouse button was pressed."

window = Game()
app.run()
