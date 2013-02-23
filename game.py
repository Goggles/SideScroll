"""SideScroll game"""

from pyglet import app, clock, image
from pyglet.sprite import Sprite
from pyglet.window import Window, key, mouse

# The images used for sprites
images = {
    'arch':   image.load('sprites/arch-rotated.png'),
    'bullet': image.load('sprites/tilde.png'),
    'star':   image.load('sprites/star.png'),
}

class Player(Sprite):
    def __init__(self, keyboard, *args, **kwargs):
        super(Player, self).__init__(*args, **kwargs)

        # Reference the keyboard object so that we can watch it
        self.keyboard = keyboard

        # Call move_player() 60 times a second
        clock.schedule_interval(self.move, 1/60.0)

        # Fire three times a second
        clock.schedule_interval(self.fire, 1/3.0)
    
    def move(self, dt):
        """This is called on every update

        It uses the keyboard input to move the player
        at around 200 pixels per second"""

        distance = dt * 200

        if self.keyboard[key.RIGHT]:
            self.x += distance

        if self.keyboard[key.LEFT]:
            self.x -= distance

        if self.keyboard[key.UP]:
            self.y += distance

        if self.keyboard[key.DOWN]:
            self.y -= distance

    def fire(self, dt):
        """Fire if the space bar is pressed"""
        if self.keyboard[key.SPACE]:
            print "Fire!"

class Game(Window):
    def __init__(self):
        """This is run when the game is created"""
        super(Game, self).__init__()

        # A handler that watches the keyboard state
        self.keyboard = key.KeyStateHandler()
        self.set_handlers(self.keyboard)

        # Create the sprites
        self.player = Player(self.keyboard, images['arch'], x=50, y=50)
        self.bullet = Sprite(images['bullet'], x=-50, y=-50)

        # Display the current FPS on screen
        self.fps_display = clock.ClockDisplay()

    def on_draw(self):
        """Clear the window, display the framerate and draw the sprites"""
        self.clear()
        self.fps_display.draw()

        # Draw the sprites
        self.player.draw()
        self.bullet.draw()

    def on_mouse_press(self, x, y, button, modifiers):
        """This is run when a mouse button is pressed"""
        if button == mouse.LEFT:
            print "The left mouse button was pressed."
        elif button == mouse.RIGHT:
            print "The right mouse button was pressed."

window = Game()
app.run()
