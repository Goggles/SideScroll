"""Menu for sidescroll game"""
import pyglet
#import game

from pyglet.sprite import Sprite
from pyglet.graphics import Batch

#from pyglet.gl import *
from pyglet.window import Window, key, mouse
from pyglet import clock, image, app
from pyglet.window.key import KeyStateHandler

#menu sprites
images = {
	'arch': image.load('sprites/arch-rotated.png'),
	'title': image.load('sprites/sidescroll.gif'),
}

class Select(Sprite):
    def __init__(self, main_menu, keyboard, *args, **kwargs):
        super(Select, self).__init__(*args, **kwargs)

        # Reference the keyboard object so that we can watch it
        self.keyboard = keyboard

	self.main_menu = main_menu

        # Call move_player() 60 times a second
        clock.schedule_interval(self.move, 1/60.0)

    def move(self, dt):
        """This is called on every update

        It uses the keyboard input to move the player
        at around 200 pixels per second"""

        #Edges dont seem to be at the same size of window.....
        #locks ships x axis, can not go off screen in x direction
        if self.keyboard[key.UP] and self.y != self.main_menu.height-160:
		self.y += 50

        if self.keyboard[key.DOWN] and self.y != self.main_menu.height-210:
                self.y -= 50

	if self.keyboard[key.ENTER]:
		if self.y == self.main_menu.height-160:
			print 'cake'
				


	
class Main_menu(Window):
	def __init__(self):
	        """This is run when the game is created"""
		super(Main_menu, self).__init__()

		# A handler that watches the keyboard state
	        self.keyboard = key.KeyStateHandler()
        	self.set_handlers(self.keyboard)

	        #loads arch ship at half original size used for selecting
		self.select = Select(self, self.keyboard, images['arch'], 
					x=(self.width//2)-90, y=self.height-160)
		self.select.scale = 0.5

		#menu selection items	
		self.menu = pyglet.text.Label('Side_Scroll', font_size=24,
                                                x=self.width//2,
                                                y=self.height//1.2,
                                                anchor_x='center',
                                                )

		self.start_game = pyglet.text.Label('Start Game!', font_size= 14,
						    x=self.width//2,
						    y=self.height-150,
						    anchor_x='center',
						   ) 
		
                self.option2 = pyglet.text.Label('Option2', font_size= 14,
                                                    x=self.width//2,
                                                    y=self.height-200,
                                                    anchor_x='center',
                                                    )


		#A key handler that watches the keyboard state
		
#		self.player = Selection(self, self.keyboard, images['arch'], x=100, y=100)
		# Call update() 60 times a second
	        #clock.schedule_interval(self.update, 1/60.0)


	def on_draw(self):
	    """clear window and draw menu items and pointer"""
	    self.clear()
	    self.menu.draw()
	    self.start_game.draw()
	    self.option2.draw()
	    self.select.draw()
#	    print self.select.y
#	    self.player.draw()

#	def update(self, dt):	
#		"""Called on each update"""
#		if self.keyboard[key.RIGHT]:
#			pass
	

window = Main_menu() 
pyglet.app.run()
