"""SideScroll game"""
import math

from pyglet import app, clock, image
from pyglet.graphics import Batch
from pyglet.sprite import Sprite
from pyglet.window import Window, key, mouse

# The images used for sprites
images = {
    'arch':   image.load('sprites/arch-rotated.png'),
    'bullet': image.load('sprites/tilde.png'),
    'star':   image.load('sprites/star.png'),
}

class Player(Sprite):
    def __init__(self, game, keyboard, *args, **kwargs):
        super(Player, self).__init__(*args, **kwargs)

        # Reference the keyboard object so that we can watch it
        self.keyboard = keyboard

	self.game = game	

        # Call move_player() 60 times a second
        clock.schedule_interval(self.move, 1/60.0)

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

        distance = dt * 200
    
	#locks ship when goes to edge of screen so goes no further
	#unfourtunately locks ship from moving any other way
	if self.game.is_sprite_in_bounds(self): 
        	if self.keyboard[key.RIGHT]:
        	    	self.x += distance
        
        	if self.keyboard[key.LEFT]:
            		self.x -= distance

        	if self.keyboard[key.UP]:
            		self.y += distance

        	if self.keyboard[key.DOWN]:
            		self.y -= distance


class Game(Window):
    def __init__(self):
        """This is run when the game is created"""
        super(Game, self).__init__()

        # A handler that watches the keyboard state
        self.keyboard = key.KeyStateHandler()
        self.set_handlers(self.keyboard)

        # Create the sprites
        self.player = Player(self, self.keyboard, images['arch'], x=100, y=50)

        self.bullet_batch = Batch()
        self.bullets = []

        # Display the current FPS on screen
        self.fps_display = clock.ClockDisplay()

        clock.schedule_interval(self.update_bullets, 1/30.0)
        clock.schedule_interval(self.fire_bullets, 1/15.0)

    def is_sprite_in_bounds(self, sprite, border=0):
        """Returns true if a sprite is in the window"""
        x = sprite.x + sprite.width / 2
        y = sprite.y + sprite.height / 2
        return (border < x < self.width - border
            and border < y < self.height - border)

    def update_bullets(self, dt):
        for bullet in self.bullets:
            bullet.x = bullet.x + dt * 500
            if not self.is_sprite_in_bounds(bullet):
                self.bullets.remove(bullet)

    def fire_bullets(self, dt):
        if self.keyboard[key.SPACE]:
            self.fire()

    def on_draw(self):
        """Clear the window, display the framerate and draw the sprites"""
        self.clear()
        self.fps_display.draw()

        # Draw the sprites
        self.player.draw()
        self.bullet_batch.draw()

    def fire(self):
        """Create a new bullet"""
        bullet = Sprite(images['bullet'], batch=self.bullet_batch)
        
        bullet.x = self.player.x + self.player.width + 10
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
