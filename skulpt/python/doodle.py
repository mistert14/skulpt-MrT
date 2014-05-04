"""
Simple Doodle Jump clone - use arrow keys to move
"""

import simplegui
import random

# Constants
CANVAS_WIDTH = 800
CANVAS_HEIGHT = 600
CLEARANCE = 300
REBOUND_VELOCITY = 7
NUM_PLAT = 50
PLATFORM_SPACING = 100

# load bounce sound - hamster republic
BOUNCE_SOUND = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/jump.ogg") 


# classes
class DoodleJumper:
    """
    Representation for doodle jumper
    """
    def __init__(self, pos):
        """
        Initialize doodle
        """
        self.pos = pos
        self.vel = [0, 0]
    
    def nudge_horiz(self, bump):
        """
        Method to push doodle to left or right
        """
        self.vel[0] += bump
                
    def update(self, state):
        """
        Update doodle in draw handler, all physics done here
        """
        
        self.pos[0] = (self.pos[0] + self.vel[0]) % CANVAS_WIDTH
        plat_index = min(self.pos[1] // PLATFORM_SPACING, NUM_PLAT - 1)
        
        # bounce if you collide with platform below you
        if self.collide(state.platform_list[plat_index]):           
            BOUNCE_SOUND.play()
            self.vel[1] = max(-self.vel[1], REBOUND_VELOCITY)
            if random.random()> .7: 	
                state.platform_list[plat_index].remove()
        else:
            self.pos[1] += self.vel[1]
            
        # accelerate due to gravity
        self.vel[1] -= .1
        
        # if doodle gets near top of frame, update camera_pos[1] to move camera up
        if self.pos[1] - state.camera_pos[1] > CANVAS_HEIGHT - CLEARANCE:
            state.camera_pos[1] = self.pos[1] - (CANVAS_HEIGHT - CLEARANCE)
        
        # restart if fall below screen
        if self.pos[1] - state.camera_pos[1] < -50:
            state.start_game()

    def collide(self, platform):
        """ 
        Test whether a doodle jumper collides with a platform
        """
        if (self.pos[1] > platform.height > self.pos[1] + self.vel[1]) and platform.exists:
            return platform.left < self.pos[0] < platform.right
        else:
            return False
                            
    def draw_doodle(self, canvas, state):
        """
        Draw a doodle jumper, offset by camera position, invert horizontal
        """
        canvas.draw_circle([self.pos[0] - state.camera_pos[0], 
                            CANVAS_HEIGHT - (self.pos[1] - state.camera_pos[1])], 5, 2, "White")

class Platform:
    """
    Class representation for platform
    """
    
    def __init__(self, height):
        """
        Create a platform with left and right boundaries and existence flag
        """
        width = random.randrange(100, 160)
        self.left = random.randrange(25, CANVAS_WIDTH -(25 + width))
        self.right = self.left + width
        self.height = height
        self.exists = True

    def remove(self):
        """
        Make a platform disappear
        """
        self.exists = False
        
    def restore(self):
        """
        Restore a platform
        """
        self.exists = True
        
    def draw_platform(self, canvas, state):
        """
        Draw a platform, offset by camera position, invert horizontal
        """
        draw_height = CANVAS_HEIGHT -(self.height- state.camera_pos[1])
        if self.exists:
            canvas.draw_line([self.left - state.camera_pos[0], draw_height],
                             [self.right - state.camera_pos[0],draw_height], 4, "Red")
        canvas.draw_text(str(self.height), [CANVAS_WIDTH - 50 - state.camera_pos[0], draw_height], 12, "Green")
        


class Game:
    """
    Game class to encapsulate content
    """

    def __init__(self):
        """
        Create a game
        """
        self.frame = simplegui.create_frame("Doodle Jump", CANVAS_WIDTH, CANVAS_HEIGHT)
        self.frame.set_keydown_handler(self.keydown)
        self.frame.set_keyup_handler(self.keyup)
        self.frame.set_draw_handler(self.draw)
        self.camera_pos = [0, 0]
        self.platform_list = [Platform(idx * PLATFORM_SPACING) for idx in range(0, NUM_PLAT)]
        self.my_doodle = DoodleJumper([(self.platform_list[0].left + self.platform_list[0].right) / 2, 200])
        self.frame.start()

    def start_game(self):
        """
        Start a game
        """
        self.camera_pos = [0, 0]
        self.platform_list = [Platform(idx * PLATFORM_SPACING) for idx in range(0, NUM_PLAT)]
        self.my_doodle = DoodleJumper([(self.platform_list[0].left + self.platform_list[0].right) / 2, 200])

    # define event handlers for game
            
    def keydown(self, key):
        """
        Adjust horizontal velocity of doodle on keydown
        """
        if key == simplegui.KEY_MAP["left"]:
            self.my_doodle.nudge_horiz(-2.5)
        elif key == simplegui.KEY_MAP["right"]:
            self.my_doodle.nudge_horiz(2.5)
            
    def keyup(self, key):
        """
        Adjust horizontal velocity of doodle on keyup
        """
        if key == simplegui.KEY_MAP["left"]:
            self.my_doodle.nudge_horiz(2.5)
        elif key == simplegui.KEY_MAP["right"]:
            self.my_doodle.nudge_horiz(-2.5)
       
    def draw(self, canvas):
        """
        Update doodle position, draw doodle, draw platforms that are visible and their heights
        """
        
        # update and draw doodle
        self.my_doodle.update(self)
        self.my_doodle.draw_doodle(canvas, self)
        
        # enumerate visible platforms and draw
        for plat_index in range(int(self.camera_pos[1] // PLATFORM_SPACING), 
                           int((CANVAS_HEIGHT + self.camera_pos[1]) // PLATFORM_SPACING) + 1):
            if plat_index < NUM_PLAT:
                self.platform_list[plat_index].draw_platform(canvas, self)
            
# Fire up game        
Game()  

