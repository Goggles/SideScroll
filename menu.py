"""Menu for sidescroll game"""
import pyglet
from pyglet.gl import *
from pyglet.window import Window, key, mouse
from pyglet import clock
from pyglet.window.key import KeyStateHandler


class Selection():
	def __init__(self, keyboard, *args, **kwargs):
		super(Selection, self).__init__(*args, **kwargs)
	
		#Reference the keyboard object so that we can wacth it
		self.keyboard = keyboard		

		#call select 60 times a second	
		clock.schedule_interval(self.select, 1/60.0)

	def select(self, dt):
		"""This is called every update

		Uses keyboard UP and DOWN keys to select 
		items from the menu and the ENTER key to select them"""

            	if self.keyboard[key.UP]:
                	print 'up'

            	if self.keyboard[key.DOWN]:
                	print 'down'
	
	
class Main_menu(Window):
	def __init__(self):
	        """This is run when the game is created"""
		super(Main_menu, self).__init__()
		
		self.menu = pyglet.text.Label('Menu', font_size=24,
                                                x=self.width//2,
                                                y=self.height//1.2,
                                                anchor_x='center',
                                                )

			
		#A key handler that watches the keyboard state
		self.keyboard = key.KeyStateHandler()
		self.set_handlers(self.keyboard)

		# Call update() 60 times a second
	        #clock.schedule_interval(self.update, 1/60.0)

#	def on_key_press(symbol, modifiers):
#           if self.keyboard[key.UP]:
#              print 'up'
#
#   	    if self.keyboard[key.DOWN]:
#                print 'down'   

	def on_draw(self):
	    self.clear()
	    self.menu.draw();

	def update(self, dt):	
		"""Called on each update"""
		if self.keyboard[key.RIGHT]:
			pass
	

window = Main_menu() 
pyglet.app.run()



