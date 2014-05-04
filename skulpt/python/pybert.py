#-------------------------------------------------------------------------------
# Name:        Py*bert
# Purpose:     A Python port of the game Q*bert to Python Using CodeSkulptor
# Notes  :     Py*bert has been tested and runs well in Windows using Chrome Version 27
#              with hardware acceleration turned off
#              Py*bert runs slow in Firefox and has not been using testing
#              other browsers or operating systems.
# Author:      Jeff Botts
#
# Created:     30/05/2013
#-------------------------------------------------------------------------------
################################################################################
#Define some Global Variables
################################################################################
import simplegui, math, random
WIDTH = 800.0
HEIGHT = 600.0
BLOCK_LENGTH = 80.0
game_on = False
BASE_DIRECTORY = "http://commondatastorage.googleapis.com/codeskulptor-demos/Pybert_assets/"

################################################################################
#Define A Few Helper Functions
################################################################################
def norm(pos1, pos2):
    """Calculate the distance between two Locations pos1 and pos2"""
    return math.sqrt((pos1[0] - pos2[0]) ** 2 + \
                     (pos1[1] - pos2[1]) ** 2)

def angle_to_vector(ang):
    """Calculate the x and y components of a unit vector given an angle"""
    return [math.cos(ang), math.sin(ang)]

def sgn(x):
    """ Determine the Sign on X """
    if x < 0.0:
        return -1.0
    else:
        return 1.0

def quadratic(a, b, c):
    """ Solve the Quadratic Equation """
    d = math.sqrt(b ** 2.0 - 4.0 * a * c)
    sgnb = sgn(b)
    q = - 0.5 * (b + sgnb * d)
    x1 = q / a
    x2 = c / q
    return x1, x2

def delta_max(h, a):
    """ Calculate the Maximum Tolerance for Determination of Character Landing """
    x = quadratic(1, -1, -2.0 * h / a)
    if x[0] <= 0:
        n = round(x[1])
    elif x[1] <= 0:
        n = round(x[0])
    else:
        n = [0, 0]
        n[0] = round(x[0])
        n[1] = round(x[1])
    if type(n) != list:
        y = n * (n - 1) * a / 2.0
    else:
        y = [0, 0]
        y[0] = n[0] * (n[0] - 1) * a / 2.0
        y[1] = n[1] * (n[1] - 1) * a / 2.0
        y = max(y[0], y[1])
    return abs(y - h) + 1

def draw_Pybert(pos, direction, canvas):
    """Draw Py*bert Based on the Current Direction"""
    if direction == 'Down Right':
        #Body
        canvas.draw_line((pos[0] +  0, pos[1] -  8), \
                         (pos[0] + 13, pos[1] -  8), 19, "OrangeRed")
        canvas.draw_circle((pos[0]   , pos[1] -  8), 15, 1, "OrangeRed", "OrangeRed")
        #Left Leg
        canvas.draw_line((pos[0] +  8, pos[1] +  0), \
                         (pos[0] +  8, pos[1] + 18), 3, "OrangeRed")
        canvas.draw_line((pos[0] +  6, pos[1] + 17), \
                         (pos[0] + 19, pos[1] + 18), 3, "OrangeRed")
        #Right Leg
        canvas.draw_line((pos[0] -  8, pos[1] +  0), \
                         (pos[0] -  8, pos[1] + 18), 3, "OrangeRed")
        canvas.draw_line((pos[0] -  9, pos[1] + 17), \
                         (pos[0] +  4, pos[1] + 18), 3, "OrangeRed")
        #Snout
        canvas.draw_line((pos[0] + 14, pos[1] -  8), \
                         (pos[0] + 26, pos[1] +  0), 9, "OrangeRed")
        canvas.draw_circle((pos[0] + 24, pos[1] - 2), 3, 1, "Black", "Black")
        #Eyes
        canvas.draw_circle((pos[0] +  8, pos[1] - 12), 5, 1, "White", "White")
        canvas.draw_circle((pos[0] -  4, pos[1] - 12), 5, 1, "White", "White")
        canvas.draw_circle((pos[0] +  9, pos[1] - 10), 3, 1, "Black", "Black")
        canvas.draw_circle((pos[0] -  2, pos[1] - 10), 3, 1, "Black", "Black")
    elif direction == "Down Left":
        #Body
        canvas.draw_line((pos[0] +  0, pos[1] -  8), \
                         (pos[0] - 13, pos[1] -  8), 19, "OrangeRed")
        canvas.draw_circle((pos[0]   , pos[1] -  8), 15, 1, "OrangeRed", "OrangeRed")
        #Left Leg
        canvas.draw_line((pos[0] -  8, pos[1] +  0), \
                         (pos[0] -  8, pos[1] + 18), 3, "OrangeRed")
        canvas.draw_line((pos[0] -  6, pos[1] + 17), \
                         (pos[0] - 19, pos[1] + 18), 3, "OrangeRed")
        #Right Leg
        canvas.draw_line((pos[0] +  8, pos[1] +  0), \
                         (pos[0] +  8, pos[1] + 18), 3, "OrangeRed")
        canvas.draw_line((pos[0] +  9, pos[1] + 17), \
                         (pos[0] -  4, pos[1] + 18), 3, "OrangeRed")
        #Snout
        canvas.draw_line((pos[0] - 14, pos[1] -  8), \
                         (pos[0] - 26, pos[1] +  0), 9, "OrangeRed")
        canvas.draw_circle((pos[0] - 24, pos[1] - 2), 3, 1, "Black", "Black")
        #Eyes
        canvas.draw_circle((pos[0] -  8, pos[1] - 12), 5, 1, "White", "White")
        canvas.draw_circle((pos[0] +  4, pos[1] - 12), 5, 1, "White", "White")
        canvas.draw_circle((pos[0] -  9, pos[1] - 10), 3, 1, "Black", "Black")
        canvas.draw_circle((pos[0] +  2, pos[1] - 10), 3, 1, "Black", "Black")
    elif direction == 'Up Right':
        #Body
        canvas.draw_line((pos[0] +  0, pos[1] -  8), \
                         (pos[0] + 13, pos[1] -  8), 19, "OrangeRed")
        canvas.draw_circle((pos[0]   , pos[1] -  8), 15, 1, "OrangeRed", "OrangeRed")
        #Left Leg
        canvas.draw_line((pos[0] +  8, pos[1] +  0), \
                         (pos[0] +  8, pos[1] + 18), 3, "OrangeRed")
        canvas.draw_line((pos[0] +  6, pos[1] + 17), \
                         (pos[0] + 19, pos[1] + 18), 3, "OrangeRed")
        #Right Leg
        canvas.draw_line((pos[0] -  8, pos[1] +  0), \
                         (pos[0] -  8, pos[1] + 18), 3, "OrangeRed")
        canvas.draw_line((pos[0] -  9, pos[1] + 17), \
                         (pos[0] +  4, pos[1] + 18), 3, "OrangeRed")
        #Snout
        canvas.draw_line((pos[0] + 14, pos[1] - 10), \
                         (pos[0] + 26, pos[1] - 16), 9, "OrangeRed")
        #Eyes
        canvas.draw_circle((pos[0] +  8, pos[1] - 12), 5, 1, "White", "White")
        canvas.draw_circle((pos[0] +  9, pos[1] - 14), 3, 1, "Black", "Black")
    elif direction == 'Up Left':
        #Body
        canvas.draw_line((pos[0] +  0, pos[1] -  8), \
                         (pos[0] + 13, pos[1] -  8), 19, "OrangeRed")
        canvas.draw_circle((pos[0]   , pos[1] -  8), 15, 1, "OrangeRed", "OrangeRed")
        #Left Leg
        canvas.draw_line((pos[0] -  8, pos[1] +  0), \
                         (pos[0] -  8, pos[1] + 18), 3, "OrangeRed")
        canvas.draw_line((pos[0] -  6, pos[1] + 17), \
                         (pos[0] - 19, pos[1] + 18), 3, "OrangeRed")
        #Right Leg
        canvas.draw_line((pos[0] +  8, pos[1] +  0), \
                         (pos[0] +  8, pos[1] + 18), 3, "OrangeRed")
        canvas.draw_line((pos[0] +  9, pos[1] + 17), \
                         (pos[0] -  4, pos[1] + 18), 3, "OrangeRed")
        #Snout
        canvas.draw_line((pos[0] - 14, pos[1] - 10), \
                         (pos[0] - 26, pos[1] - 16), 9, "OrangeRed")
        #Eyes
        canvas.draw_circle((pos[0] -  8, pos[1] - 12), 5, 1, "White", "White")
        canvas.draw_circle((pos[0] -  9, pos[1] - 14), 3, 1, "Black", "Black")

def draw_ball(pos, radius, color, canvas):
    """Draw the Red, Purple, and Green Balls"""
    canvas.draw_circle(pos, radius, 1, color, color)
    canvas.draw_circle([pos[0] - 5, pos[1] - 5], 2, 1, "White", "White")
    canvas.draw_line([pos[0] + 3, pos[1] + 4], [pos[0] + 7, pos[1]], 1, 'Black')

def character_pause(level):
    """ Increase Game Difficulty by Speeding Up Jump Rate """
    wait = 15
    for i in range(4, level[0]):
        wait -= 1
    return wait

def initial_spawn_pause(character, level):
    """ Define initial and re-spawn rates depending on player level """
    if character in ['Sam', 'Green Ball']:
        if character == 'Sam': #And Slick
            wait = random.randrange(400, 800)
        else: #Green Ball
            wait = random.randrange(500, 1000)
        if player.level[0] >= 3:
            wait //= (player.level[0] // 3)
    else:
        if character == 'Ugg': #And Wrong Way
            wait = random.randrange(100, 500)
        elif character == 'Purple Ball':
            wait = random.randrange(30, 90)
        else: #Red Ball
            wait = random.randrange(60, 360)
        if player.level[0] > 1:
            wait //= (player.level[0] // 2)
    return wait

def xvelocity(dx, n):
    """ Calculate the Velocity in the x-direction given the overall change and frames """
    return dx / n

def yvelocity(dy, n, a):
    """ Calculate the Velocity in the y-direction given the overall change, frames, and
        acceleration """
    num = dy - 0.5 * n * (n - 1) * a
    return num / n

def acc_and_yvelocity(h, dy, n):
    """ Calculate the Acceleration and Velocity in the y-direction given the desired
        max jump height, overall displacement, and number of frames """
    b = n * (n - 1.0)
    a = (b + n) ** 2.0
    c = (dy + 4.0 * b * h) * dy
    v = quadratic(a, b, c)
    if v[1] >= 0:
        v = v[0]
    elif v[0] >= 0:
        v = v[1]
    else:
        v = min(v)
    acc = 2.0 * (dy - n * v) / (n * (n - 1.0))
    acc = round(acc * 1000.0) / 1000.0
    v = yvelocity(dy, n, acc)
    return v, acc

def max_jump_height(v, acc):
    """ Calculate the max jump height given an initial velocity and acceleration """
    n = round(- v / acc + 0.5)
    return n * v + n * (n - 1) * acc / 2.0

################################################################################
# Define the Classes
################################################################################

class Backgrounds:

    def timer_handler(self):
        self.timer_counter = (self.timer_counter + 100) % 1000
        self.arrow[0] = self.timer_counter > 300
        self.arrow[1] = self.timer_counter > 600

    def __init__(self):
        self.arrow = [False, False]
        self.timer_counter = 0
        self.timer = simplegui.create_timer(100, self.timer_handler)

    def draw(self, canvas, board, player, player_number):
        #Write Player Number and Score
        canvas.draw_text("PLAYER ",   ( 25,  75), 48, "Purple", "serif")
        canvas.draw_polygon([[225, 80], [225, 40], [250, 40], [250, 80]], 1, "Red", "Red")
        canvas.draw_text(str(player_number), (225,  75), 48, "White",  "serif")
        score = str(player.score)
        canvas.draw_text(score, ( 25, 125), 48, "Brown", "serif")
        #Write Change To, Level
        canvas.draw_text("CHANGE TO",   ( 25, 175), 32, "Red", "serif")
        canvas.draw_text("LEVEL:  ",    (575, 175), 32, "Green", "serif")
        canvas.draw_text(str(player.level[0]), (700, 175), 32, "Brown", "serif")
        canvas.draw_text("ROUND:  ",    (575, 205), 32, "Purple", "serif")
        canvas.draw_text(str(player.level[1]), (700, 205), 32, "Brown", "serif")
        #Draw Change To Arrows and Example Block
        if self.arrow[0]:
            canvas.draw_polygon([[25, 205], [30, 205], [33, 212], [40, 200], \
                                 [33, 188], [30, 195], [25, 195]], 1, "Pink", "Pink")
        if self.arrow[1]:
            canvas.draw_polygon([[45, 205], [50, 205], [53, 212], [60, 200], \
                                 [53, 188], [50, 195], [45, 195]], 1, "Pink", "Pink")
        canvas.draw_polygon([[105,187], [65, 200], [105, 214], [145, 200]], 1,  \
                             board.starting_color[3], board.starting_color[3])
        canvas.draw_polygon([[ 65, 213], [105, 227], [105, 213], [ 65, 200]], 1,\
                             board.starting_color[1], board.starting_color[1])
        canvas.draw_polygon([[145, 213], [105, 227], [105, 213], [145, 200]], 1,\
                             board.starting_color[2], board.starting_color[2])
        if self.arrow[1]:
            canvas.draw_polygon([[165, 205], [160, 205], [157, 212], [150, 200], \
                                 [157, 188], [160, 195], [165, 195]], 1, "Pink", "Pink")
        if self.arrow[0]:
            canvas.draw_polygon([[185, 205], [180, 205], [177, 212], [170, 200], \
                                 [177, 188], [180, 195], [185, 195]], 1, "Pink", "Pink")
        #Draw Qbert Lives Left (One Per Qbert)
        life_location = [50, 250]
        for life in range(player.lives - 1):
            draw_Pybert(life_location, 'Down Left', canvas)
            life_location[1] += 50
            if life_location[1] > HEIGHT:
                break
        #Display Logo
        canvas.draw_text("PY*BERT", (425, 90), 82, "Blue", "serif")

        #Display Bonus
        if player.wait_time != 0:
            canvas.draw_text("Bonus:  " + str(player.bonus_points(True)),   \
                            ( 350, 575), 32, "Red", "serif")

class Opening:
    def timer_handler(self):
        self.wait += 1
        self.wait = self.wait % 10
        self.position[0] += 10
        self.spinner.move(10, 0)
        if self.position[0] > 0 and not self.sound:
            self.sound = True
            self.sounds.rewind()
            self.sounds.play()
        if self.position[0] >= 900:
            self.position[0] = -100

    def __init__(self, call):
        self.sound = False
        self.message = "Py*bert"
        self.message2 = "Push 1 for One Player Start"
        self.wait = 0
        self.position = [-100, 300]
        self.complete = False
        self.keylist = []
        if call:
            self.sounds = gamesounds['Spinner']
            self.timer = simplegui.create_timer(100, self.timer_handler)
            self.timer.start()
            self.spinner = Spinner(self.position[0], self.position[1] + 25, 10, 25, 90)
        else:
            self.spinner.__init__(self.position[0], self.position[1] + 25, 10, 25, 90)

    def check(self):
        return self.keylist == [38, 38, 40, 40, 37, 39, 37, 39, 66, 65, 49]

    def draw(self, canvas, start2):
        canvas.draw_text(self.message, [175, 200], 144, "Yellow")
        if self.wait > 5:
            canvas.draw_text(self.message2, [150, 550], 44, "SpringGreen")
        self.spinner.draw(canvas)
        draw_Pybert([self.position[0], self.position[1] + 8], 'Down Right', canvas)
        if self.position[0] > WIDTH:
            self.sounds.pause()
            self.complete = True
            start2.__init__(False)

class Instructions:
    def timer_handler(self):
        self.wait[0] += 1
        self.wait[2] += 1
        if self.wait[2] == 25:
            self.wait[2] = self.wait[2] % 25
            self.wait[1] += 1
        self.wait[0] = self.wait[0] % 10
        self.jump()

    def jump(self):
        if self.stop and not self.curse:
            self.ball_location[1] += self.vy
            self.vy += self.acc
            delta = norm(self.position, self.ball_location)
            if delta < self.radius + 15.0:
                gamesounds['Bop'].rewind()
                gamesounds['Bop'].play()
                self.curse = True
                self.vy = -30.0
                gamesounds['Curse'].rewind()
                gamesounds['Curse'].play()
        elif self.curse:
            self.ball_location[0] += 15.0
            self.ball_location[1] += self.vy
            self.vy += self.acc
            self.wait[3] += 1
            if self.wait[3] % 20 == 0:
                self.ball_location[1] = -20.0
                self.complete = True
        elif self.in_air:
            self.position[0] += self.vx
            self.position[1] += self.vy
            self.vy += self.acc
            delta = abs(self.position[1] - self.draw_position[1])
            if delta < 1.0:
                gamesounds['Hop'].rewind()
                gamesounds['Hop'].play()
                self.in_air = False
                self.position[1] = self.draw_position[1]
        elif self.wait[2] == 20:
            self.in_air = True
            self.vy = -6.21165285216793
            self.vx = +(5.0 + (1.0 / 3.0))

    def __init__(self, call):
        self.message = ["Py*bert",
                        "Push 1 for One Player Start",
                       ["JUMP ON SQUARES TO CHANGE THEM TO", "THE TARGET COLOR"],
                       ["STAY ON PLAYFIELD! JUMPING OFF RESULTS",
                        "IN A FATAL PLUMMET UNLESS A DISK IS THERE"],
                       ["AVOID ALL OBJECTS AND CREATURES THAT", "ARE NOT GREEN"],
                       ["USE SPINNING DISKS TO LURE SNAKE TO", "HIS DEATH"],
                       ["EXTRA LIFE AT 8000", "AND EACH ADDITIONAL 14000"]]
        self.wait = [0, 0, 0, 0]
        self.position = [50.0, 125.0]
        self.draw_position = [125.0, 155.0]
        if call:
            self.timer = simplegui.create_timer(100, self.timer_handler)
        else:
            self.timer.start()
        self.acc = 16.5079876805696
        self.in_air = False
        self.vx = 0.0
        self.vy = 0.0
        self.stop = False
        self.radius = 15.0
        self.ball_location = [0.0, -20.0]
        self.curse = False
        self.complete = False

    def draw(self, canvas, start1):
        canvas.draw_text(self.message[0], [25, 75], 72, "Yellow")
        if self.wait[0] > 5:
            canvas.draw_text(self.message[1], [150, 550], 44, "SpringGreen")
        for j in range(1, 6):
            if self.wait[1] >= j:
                if j == 1:
                    draw_position = [125.0, 155.0]
                else:
                    draw_position[0] += 25.0
                    draw_position[1] += 25.0
                for i in self.message[j+1]:
                    canvas.draw_text(i, draw_position, 28, 'Green')
                    draw_position[1] += 25.0
                self.draw_position[0] = draw_position[0] + 25.0
                self.draw_position[1] = draw_position[1] + 25.0
                if j == 5 and not self.stop:
                    self.stop = True
                    self.vy = 0.0
                    self.ball_location[0] = self.position[0]
        draw_Pybert([self.position[0], self.position[1] + 8], 'Down Right', canvas)
        if self.stop:
            draw_ball(self.ball_location, self.radius, "Red", canvas)
        if self.curse:
            canvas.draw_line([self.position[0] + 30, self.position[1] - 10], \
                             [self.position[0] + 50, self.position[1] - 10], 10, 'White')
            canvas.draw_line([self.position[0] + 50, self.position[1] - 10], \
                             [self.position[0] + 150, self.position[1] - 10], 40, 'White')
            canvas.draw_text('@!#?@!', [self.position[0] + 55, self.position[1] - 3],28, 'Black')
        if self.complete:
            self.timer.stop()
            start1.__init__(False)

class Non_Player_Character:
    """ Parent Class for Sam, Slick, Red Ball, Green Ball, and Purple Ball """
    def __init__(self, player, width, block_length):
        self.location = [width / 2.0, 0.0]
        if random.randrange(0,2):
            self.location[0] -= block_length / 2.0
            self.target = 2
        else:
            self.location[0] += block_length / 2.0
            self.target = 1
        self.block = None
        self.radius = 10.0
        self.direction = 'Left'
        self.vx = 0.0
        self.vy = 0.0
        self.acc = player.acc

    def move_complete(self, board, player):
        if self.block == None:
            c = board.CENTER1[self.target]
            req_delta = delta_max(c[1], self.acc)
        else:
            req_delta = 1.0
        if self.target != None:
            c = board.CENTER1[self.target]
            delta = norm(self.location, c)
            if delta < req_delta:
                self.location = list(c)
                self.block = self.target
                nextblock = board.blockmap[self.block]
                self.post_move(board, player)
                if random.randrange(0,2):
                    self.target = nextblock[0]
                    self.vx = player.get_vx0L()
                    self.direction = 'Left'
                else:
                    self.target = nextblock[1]
                    self.vx = player.get_vx0R()
                    self.direction = 'Right'
                self.vy = player.get_vy0D()
                self.wait = character_pause(player.level)
                self.sound.rewind()
                self.sound.play()

    def post_move(self, board, player):
        pass

    def move(self, player, block_length, board, width, height):
        if self.wait != 0:
            self.wait -= 1
        elif self.block == None:
            self.location[1] += self.vy
            self.vy += self.acc
            self.move_complete(board, player)
        else:
            self.location[0] += self.vx
            self.location[1] += self.vy
            self.vy += self.acc
            if self.location[1] > height:
                self.__init__(player, width, block_length)
            else:
                self.move_complete(board, player)

class Sam(Non_Player_Character):

    def __init__(self, player, width, block_length):
        Non_Player_Character.__init__(self, player, width, block_length)
        self.wait = initial_spawn_pause('Sam', player.level)
        self.sound = gamesounds['Sam']
        self.sound.set_volume(0.2)

    def post_move(self, board, player):
        #Change Block Colors as Applicable
        target_color = board.Board_Color_Scheme(player.level)
        board.change_board_color(self.block, target_color, True, player)

    def draw(self, canvas):
        if self.wait != 0 and self.block == None:
            return
        pos = self.location
        canvas.draw_circle([pos[0], pos[1] - 5], 11, 1, "Green", "Green")
        canvas.draw_circle([pos[0], pos[1] - 1], 9, 1, "Green", "Green")
        canvas.draw_line([pos[0] -  5, pos[1] + 5], [pos[0] -  5, pos[1] + 15], 3, "Green")
        canvas.draw_line([pos[0] +  5, pos[1] + 5], [pos[0] +  5, pos[1] + 15], 3, "Green")
        if self.direction == 'Left':
            canvas.draw_line([pos[0] +  0, pos[1] - 17], [pos[0] + 12, pos[1] - 21], 4, "Orange")
            canvas.draw_line([pos[0] +  4, pos[1] - 13], [pos[0] + 12, pos[1] - 17], 6, "Orange")
            canvas.draw_line([pos[0] +  8, pos[1] - 10], [pos[0] + 14, pos[1] - 15], 8, "Orange")
            canvas.draw_line([pos[0] +  5, pos[1] + 15], [pos[0] +  0, pos[1] + 17], 3, "Green")
            canvas.draw_line([pos[0] -  5, pos[1] + 15], [pos[0] - 10, pos[1] + 17], 3, "Green")
            canvas.draw_circle([pos[0] -  4, pos[1] -  8],  4, 1, "Green", "White")
            canvas.draw_circle([pos[0] +  4, pos[1] -  8],  4, 1, "Green", "White")
            canvas.draw_circle([pos[0] -  5, pos[1] -  7],  2, 1, "Black", "Black")
            canvas.draw_circle([pos[0] +  3, pos[1] -  7],  2, 1, "Black", "Black")
        else:
            canvas.draw_line([pos[0] - 14, pos[1] - 15], [pos[0] -  2, pos[1] - 10], 8, "Orange")
            canvas.draw_line([pos[0] - 10, pos[1] - 17], [pos[0] -  2, pos[1] - 13], 6, "Orange")
            canvas.draw_line([pos[0] -  6, pos[1] - 21], [pos[0] +  0, pos[1] - 17], 4, "Orange")
            canvas.draw_line([pos[0] +  5, pos[1] + 15], [pos[0] + 10, pos[1] + 17], 3, "Green")
            canvas.draw_line([pos[0] -  5, pos[1] + 15], [pos[0] +  0, pos[1] + 17], 3, "Green")
            canvas.draw_circle([pos[0] -  4, pos[1] -  8],  4, 1, "Green", "White")
            canvas.draw_circle([pos[0] +  4, pos[1] -  8],  4, 1, "Green", "White")
            canvas.draw_circle([pos[0] -  3, pos[1] -  7],  2, 1, "Black", "Black")
            canvas.draw_circle([pos[0] +  5, pos[1] -  7],  2, 1, "Black", "Black")
        canvas.draw_line([pos[0] - 5, pos[1] - 1], [pos[0] +  5, pos[1] - 1], 1, "Black")

class Slick(Sam):

    def __init__(self, player, width, block_length):
        Sam.__init__(self, player, width, block_length)
        self.sound = gamesounds['Slick']
        self.sound.set_volume(0.2)

    def draw(self, canvas):
        if self.wait != 0 and self.block == None:
            return
        pos = self.location
        canvas.draw_circle([pos[0], pos[1] - 5], 11, 1, "Green", "Green")
        canvas.draw_circle([pos[0], pos[1] - 1], 9, 1, "Green", "Green")
        canvas.draw_line([pos[0] -  5, pos[1] + 5], [pos[0] -  5, pos[1] + 15], 3, "Green")
        canvas.draw_line([pos[0] +  5, pos[1] + 5], [pos[0] +  5, pos[1] + 15], 3, "Green")
        if self.direction == 'Left':
            canvas.draw_line([pos[0] +  0, pos[1] - 17], [pos[0] + 12, pos[1] - 21], 4, "Green")
            canvas.draw_line([pos[0] +  4, pos[1] - 13], [pos[0] + 12, pos[1] - 17], 6, "Green")
            canvas.draw_line([pos[0] +  8, pos[1] - 10], [pos[0] + 14, pos[1] - 15], 8, "Green")
            canvas.draw_line([pos[0] +  5, pos[1] + 15], [pos[0] +  0, pos[1] + 17], 3, "Green")
            canvas.draw_line([pos[0] -  5, pos[1] + 15], [pos[0] - 10, pos[1] + 17], 3, "Green")
            canvas.draw_line([pos[0] +  5, pos[1] -  7], [pos[0] - 10, pos[1] -  9], 2, 'Black')
            canvas.draw_line([pos[0] +  3, pos[1] -  7], [pos[0] + 10, pos[1] - 11], 2, 'Black')
        else:
            canvas.draw_line([pos[0] - 14, pos[1] - 15], [pos[0] -  8, pos[1] - 10], 8, "Green")
            canvas.draw_line([pos[0] - 12, pos[1] - 17], [pos[0] -  4, pos[1] - 13], 6, "Green")
            canvas.draw_line([pos[0] - 12, pos[1] - 21], [pos[0] +  0, pos[1] - 17], 4, "Green")
            canvas.draw_line([pos[0] +  5, pos[1] + 15], [pos[0] + 10, pos[1] + 17], 3, "Green")
            canvas.draw_line([pos[0] -  5, pos[1] + 15], [pos[0] +  0, pos[1] + 17], 3, "Green")
            canvas.draw_line([pos[0] + 10, pos[1] - 11], [pos[0] +  3, pos[1] -  7], 2, 'Black')
            canvas.draw_line([pos[0] - 10, pos[1] -  9], [pos[0] +  5, pos[1] -  7], 2, 'Black')
        canvas.draw_circle([pos[0] -  4, pos[1] -  8],  3, 1, "Black", "Black")
        canvas.draw_circle([pos[0] +  4, pos[1] -  8],  3, 1, "Black", "Black")
        canvas.draw_line([pos[0] - 4, pos[1] -  8], [pos[0] +  4, pos[1] -  8], 2, 'Black')
        canvas.draw_line([pos[0] - 5, pos[1] -  1], [pos[0] +  5, pos[1] -  1], 1, "Black")

class Green_Ball(Non_Player_Character):

    def __init__(self, player, width, block_length):
        Non_Player_Character.__init__(self, player, width, block_length)
        self.wait = initial_spawn_pause('Green Ball', player.level)
        self.sound = gamesounds['Ball Bounce']
        self.sound.set_volume(0.25)

    def draw(self, canvas):
        if self.wait != 0 and self.block == None:
            return
        draw_ball(self.location, self.radius, 'Green', canvas)

class Allies:
    def __init__(self):
        self.Green_Balls = []
        self.Slick       = []
        self.Sam         = []
        self.wait        = 0
        self.spawn_rate  = 300

    def distance(self, ally, player):
        r = 15
        delta = norm(player.position, ally.location)
        return delta <= r + ally.radius

    def check_collisions(self, player):
        #Check to see if they are within their own radius
        for green in self.Green_Balls:
            if self.distance(green, player):
                self.Green_Balls.remove(green)
                return 1
        for slick in self.Slick:
            if self.distance(slick, player):
                self.Slick.remove(slick)
                return 2
        for sam in self.Sam:
            if self.distance(sam, player):
                self.Sam.remove(sam)
                return 3
        return 0

    def spawn(self, player):
        self.spawn_rate += 60 *(len(self.Sam) + len(self.Slick) + len(self.Green_Balls))
        self.spawn_rate -= 10 * player.level[1]

    def generate_allies(self, player, WIDTH, BLOCK_LENGTH):
        if (player.level[0] == 1 and player.level[1] == 1) or \
           (player.level[0] == 1 and player.level[1] == 2):
            return
        self.wait += 1
        if self.wait % (self.spawn_rate // player.level[0]) == 0:
            #Randomly Generate an Ally!
            v = random.randrange(0, 3)
            if v == 0 and len(self.Green_Balls) == 0:
                self.Green_Balls.append(Green_Ball(player, WIDTH, BLOCK_LENGTH))
                self.spawn(player)
            if v == 1 and len(self.Sam) == 0 and len(self.Slick) == 0:
                self.Sam.append(Sam(player, WIDTH, BLOCK_LENGTH))
                self.spawn(player)
            if v == 2 and len(self.Sam) == 0 and len(self.Slick) == 0:
                self.Slick.append(Slick(player, WIDTH, BLOCK_LENGTH))
                self.spawn(player)

    def move(self, BLOCK_LENGTH, board, WIDTH, HEIGHT, player):
        for green_ball in self.Green_Balls:
            green_ball.move(player, BLOCK_LENGTH, board, WIDTH, HEIGHT)
        for sam in self.Sam:
            sam.move(player, BLOCK_LENGTH, board, WIDTH, HEIGHT)
        for slick in self.Slick:
            slick.move(player, BLOCK_LENGTH, board, WIDTH, HEIGHT)

    def draw(self, canvas, player, WIDTH, BLOCK_LENGTH):
        #Generate New Enemies (if applicable)
        self.generate_allies(player, WIDTH, BLOCK_LENGTH)
        for green_ball in self.Green_Balls:
            green_ball.draw(canvas)
        for slick in self.Slick:
            slick.draw(canvas)
        for sam in self.Sam:
            sam.draw(canvas)

class Ugg:

    def determine_start_location(self, board, width):
        self.target = 27
        c = board.CENTER3[self.target]
        dx = c[0] - width
        x = quadratic(1, -1, -2.0 * dx / self.vxx)
        if x[0] <= 0:
            n = round(x[1])
        elif x[1] <= 0:
            n = round(x[0])
        else:
            n = [0, 0]
            n[0] = round(x[0])
            n[1] = round(x[1])
            n = max(n)
        dy = n * (n - 1.0) * self.vyy / 2.0
        self.location = [width, c[1] - dy]
        x = width + n * (n - 1.0) * self.vxx / 2.0
        y = c[1] - dy + n * (n - 1.0) * self.vyy / 2.0
        self.req_delta = norm([x, y], c) + 1.0

    def __init__(self, width, player, block_length):
        self.fx, self.fy = angle_to_vector(60.0 / 180.0 * math.pi)
        self.block = None
        self.radius = 10.0
        self.vx = 0.0
        self.vy = 0.0
        self.vxx = -player.acc * self.fx
        self.vyy = -player.acc * self.fy
        self.determine_start_location(board, width)
        self.v0U = [yvelocity(-block_length / 2.0,       player.frames_per_jump, self.vxx),
                    yvelocity(-block_length * 2.0 / 3.0, player.frames_per_jump, self.vyy)]
        self.v0L = [yvelocity(-block_length,             player.frames_per_jump, self.vxx),
                    yvelocity(0.0,                       player.frames_per_jump, self.vyy)]
        self.wait = initial_spawn_pause('Ugg', player.level)
        self.direction = 'Left'
        self.sound = gamesounds['Ugg']
        self.sound.set_volume(0.2)

    def move_complete(self, board, player):
        if self.block == None:
            req_delta = 0.0 + self.req_delta
        else:
            req_delta = 1.0
        if self.target != None:
            c = board.CENTER3[self.target]
            delta = norm(self.location, c)
            if delta < req_delta:
                self.location[0] = c[0]
                self.location[1] = c[1]
                self.block = self.target
                nextblock = board.blockmap2[self.block]
                if random.randrange(0,2):
                    self.target = nextblock[2]
                    self.vx = self.v0U[0]
                    self.vy = self.v0U[1]
                    self.direction = 'Up'
                else:
                    self.target = nextblock[3]
                    self.vx = self.v0L[0]
                    self.vy = self.v0L[1]
                    self.direction = 'Left'
                self.wait = character_pause(player.level)

    def move(self, player, board, width, block_length):
        if self.wait != 0:
            self.wait -= 1
            if self.wait == 0 and self.block == None:
                self.sound.rewind()
                self.sound.play()
        elif self.block == None:
            self.location[0] += self.vx
            self.location[1] += self.vy
            self.vx += self.vxx
            self.vy += self.vyy
            self.move_complete(board, player)
        else:
            self.location[0] += self.vx
            self.location[1] += self.vy
            self.vx += self.vxx
            self.vy += self.vyy
            if self.location[0] < 0 or self.location[1] < 0:
                self.__init__(width, player, block_length)
            else:
                self.move_complete(board, player)

    def draw(self, canvas):
        if self.wait != 0 and self.block == None:
            return
        pos = self.location
        canvas.draw_circle([pos[0] + 15, pos[1]], 13, 1, "Purple", "Purple")
        canvas.draw_circle([pos[0] + 9, pos[1]], 15, 1, "Purple", "Purple")
        canvas.draw_line([pos[0] +  3, pos[1] - 2], [pos[0] - 10, pos[1] -  2], 5, "Purple")
        canvas.draw_line([pos[0] +  3, pos[1] + 5], [pos[0] - 15, pos[1] +  5], 5, "Purple")
        if self.direction == 'Up':
            canvas.draw_line([pos[0] - 10, pos[1]  - 2], [pos[0] - 10, pos[1] - 12], 3, "Purple")
            canvas.draw_line([pos[0] - 15, pos[1]  + 5], [pos[0] - 15, pos[1] -  5], 3, 'Purple')
            canvas.draw_line([pos[0] + 12, pos[1] -  8], [pos[0] + 12, pos[1] - 19], 10, "Purple")
            canvas.draw_circle([pos[0] + 14, pos[1] - 6], 5, 1, "Purple", "White")
            canvas.draw_circle([pos[0] + 14, pos[1] - 8], 2, 1, "Black", "Black")
        else:
            canvas.draw_line([pos[0] - 10, pos[1] - 2], [pos[0] - 14, pos[1] - 12], 3, "Purple")
            canvas.draw_line([pos[0] - 15, pos[1] + 5], [pos[0] - 19, pos[1] + 15], 3, 'Purple')
            canvas.draw_polygon([[pos[0] + 8, pos[1] - 6], [pos[0] + 8, pos[1] + 6], \
                                 [pos[0] + 2, pos[1] + 6], [pos[0] + 2, pos[1] - 6]], 1, 'Black', 'Purple')
            canvas.draw_circle([pos[0] +  5, pos[1] -  2],  1, 1, "Black", "Black")
            canvas.draw_circle([pos[0] +  5, pos[1] +  2],  1, 1, "Black", "Black")
            canvas.draw_circle([pos[0] + 14, pos[1] -  4],  5, 1, "Purple", "White")
            canvas.draw_circle([pos[0] + 14, pos[1] +  4],  5, 1, "Purple", "White")
            canvas.draw_circle([pos[0] + 12, pos[1] -  4],  2, 1, "Black", "Black")
            canvas.draw_circle([pos[0] + 12, pos[1] +  4],  2, 1, "Black", "Black")

class WrongWay:

    def determine_start_location(self, board):
        self.target = 21
        c = board.CENTER2[self.target]
        dx = c[0]
        x = quadratic(1, -1, -2.0 * dx / self.vxx)
        if x[0] <= 0:
            n = round(x[1])
        elif x[1] <= 0:
            n = round(x[0])
        else:
            n = [0, 0]
            n[0] = round(x[0])
            n[1] = round(x[1])
            n = max(n)
        dy = n * (n - 1.0) * self.vyy / 2.0
        self.location = [0, c[1] - dy]
        x = n * (n - 1.0) * self.vxx / 2.0
        y = c[1] - dy + n * (n - 1.0) * self.vyy / 2.0
        self.req_delta = norm([x, y], c) + 1.0

    def __init__(self, player, block_length):
        self.fx, self.fy = angle_to_vector(60.0 / 180.0 * math.pi)
        self.block = None
        self.radius = 10.0
        self.vx = 0.0
        self.vy = 0.0
        self.vxx = +player.acc * self.fx
        self.vyy = -player.acc * self.fy
        self.determine_start_location(board)
        self.v0U = [yvelocity(block_length / 2.0,        player.frames_per_jump, self.vxx),
                    yvelocity(-block_length * 2.0 / 3.0, player.frames_per_jump, self.vyy)]
        self.v0R = [yvelocity(block_length,              player.frames_per_jump, self.vxx),
                    yvelocity(0.0,                       player.frames_per_jump, self.vyy)]
        self.wait = initial_spawn_pause('Ugg', player.level)
        self.direction = 'Right'
        self.sound = gamesounds['Wrong Way']
        self.sound.set_volume(0.2)

    def move_complete(self, board, player):
        if self.block == None:
            req_delta = 0.0 + self.req_delta
        else:
            req_delta = 1.0
        if self.target != None:
            c = board.CENTER2[self.target]
            delta = norm(self.location, c)
            if delta < req_delta:
                self.location[0] = c[0]
                self.location[1] = c[1]
                self.block = self.target
                nextblock = board.blockmap2[self.block]
                if random.randrange(0,2):
                    self.target = nextblock[0]
                    self.vx = self.v0U[0]
                    self.vy = self.v0U[1]
                    self.direction = 'Up'
                else:
                    self.target = nextblock[1]
                    self.vx = self.v0R[0]
                    self.vy = self.v0R[1]
                    self.direction = 'Right'
                self.wait = character_pause(player.level)

    def move(self, player, board, width, block_length):
        if self.wait != 0:
            self.wait -= 1
            if self.wait == 0 and self.block == None:
                self.sound.rewind()
                self.sound.play()
        elif self.block == None:
            self.location[0] += self.vx
            self.location[1] += self.vy
            self.vx += self.vxx
            self.vy += self.vyy
            self.move_complete(board, player)
        else:
            self.location[0] += self.vx
            self.location[1] += self.vy
            self.vx += self.vxx
            self.vy += self.vyy
            if self.location[0] > width or self.location[1] < 0:
                self.__init__(player, block_length)
            else:
                self.move_complete(board, player)

    def draw(self, canvas):
        if self.wait != 0 and self.block == None:
            return
        pos = self.location
        canvas.draw_circle([pos[0] - 15, pos[1]], 13, 1, "Purple", "Purple")
        canvas.draw_circle([pos[0] - 9, pos[1]], 10, 1, "Purple", "Purple")
        canvas.draw_line([pos[0] -  3, pos[1] - 2], [pos[0] + 10, pos[1] -  2], 3, "Purple")
        canvas.draw_line([pos[0] -  3, pos[1] + 5], [pos[0] + 15, pos[1] +  5], 3, "Purple")
        if self.direction == 'Up':
            canvas.draw_line([pos[0] + 10, pos[1] - 2], [pos[0] + 10, pos[1] - 12], 3, "Purple")
            canvas.draw_line([pos[0] + 15, pos[1] + 5], [pos[0] + 15, pos[1] -  5], 3, 'Purple')
            canvas.draw_circle([pos[0] - 11, pos[1] - 8], 5, 1, "White", "White")
            canvas.draw_line([pos[0]   - 13, pos[1] + 5], [pos[0] - 13, pos[1] - 13], 5, 'Purple')
            canvas.draw_polygon([[pos[0] - 13, pos[1] - 13], [pos[0] - 13, pos[1] - 8], [pos[0] - 8, pos[1] - 8]],\
                                1, 'Black', 'Black')
            canvas.draw_circle([pos[0] - 20, pos[1] - 5], 5, 1, "Purple", "White")
            canvas.draw_circle([pos[0] - 20, pos[1] - 7], 2, 1, "Black", "Black")
        else:
            canvas.draw_line([pos[0] + 10, pos[1] - 2], [pos[0] + 14, pos[1] - 12], 3, "Purple")
            canvas.draw_line([pos[0] + 15, pos[1] + 5], [pos[0] + 19, pos[1] + 15], 3, 'Purple')
            canvas.draw_circle([pos[0] - 12, pos[1]], 7, 1, "White", "White")
            canvas.draw_line([pos[0] - 16, pos[1] + 7], [pos[0] - 16, pos[1] -  7], 7, 'Purple')
            canvas.draw_polygon([[pos[0] - 13, pos[1] + 7], [pos[0] - 13, pos[1] - 0], [pos[0] - 10, pos[1] + 3]],\
                                 3, 'Black', 'Black')
            canvas.draw_polygon([[pos[0] - 13, pos[1] + 0], [pos[0] - 13, pos[1] - 7], [pos[0] - 10, pos[1] - 3]],\
                                 1, 'Black', 'Black')
            canvas.draw_circle([pos[0] - 20, pos[1] -  4],  5, 1, "Purple", "White")
            canvas.draw_circle([pos[0] - 20, pos[1] +  4],  5, 1, "Purple", "White")
            canvas.draw_circle([pos[0] - 18, pos[1] -  4],  2, 1, "Black", "Black")
            canvas.draw_circle([pos[0] - 18, pos[1] +  4],  2, 1, "Black", "Black")

class Coily:

    def Coily_Logic(self, option1, option2, player, board):
        c1 = board.CENTER1[option1]
        c2 = board.CENTER1[option2]
        c3 = board.CENTER1[player.block]
        dx1 = norm(c1, c3)
        dx2 = norm(c2, c3)
        if dx1 < dx2:
            self.target = option1
        elif dx2 < dx1:
            self.target = option2
        else:
            self.target = random.choice([option1, option2])

    def jump(self, current, player):
        for i in range(4):
            if self.target == current[i]:
                self.direction = self.jump_map[i][0]
                self.vy        = self.jump_map[i][1]()
                self.vx        = self.jump_map[i][2]()
                break
        self.wait = character_pause(player.level)

    def predict_motion(self, player, board):
        if player.on_spinner and self.block == player.block:
            self.offboard = True
            if player.direction == 'Up Left':
                index = 2
            else:
                index = 3
            self.direction = self.jump_map[index][0]
            self.vy        = self.jump_map[index][1]()
            self.vx        = self.jump_map[index][2]()
            gamesounds['Coily Off Board'].rewind()
            gamesounds['Coily Off Board'].play()
        else:
            ## Use Player's Position to Choose Path ##
            current = board.blockmap[self.block]
            if self.block < player.block:
                #Jump Down Unless Deadly!
                if current[0] == None and current[1] == None:
                    if current[2] == None:
                        self.target = current[3] #Last Option
                    elif current[3] == None:
                        self.target = current[2] #Ditto
                    else: #Choose Best Route!
                        if current[2] == self.last:
                            self.target = current[3]
                        elif current[3] == self.last:
                            self.target = current[2]
                        else:
                            self.Coily_Logic(current[2], current[3], player, board)
                elif current[0] == None:
                    self.target = current[1]
                elif current[1] == None:
                    self.target = current[0]
                else: #Choose Best Route!
                    if current[0] == player.block and self.target != self.block:
                        self.target = current[0]
                    elif current[1] == player.block and self.target != self.block:
                        self.target = current[1]
                    else:
                        if current[0] == self.last:
                            self.target = current[1]
                        elif current[1] == self.last:
                            self.target = current[0]
                        else:
                            self.Coily_Logic(current[1], current[0], player, board)
            else:
                #Jump Up Unless Deadly!
                if current[2] == None and current[3] == None:
                    if current[0] == None:
                        self.target = current[1] #Last Option
                    elif current[1] == None:
                        self.target = current[0] #Ditto
                    else: #Choose Best Route!
                        if current[0] == self.last:
                            self.target = current[1]
                        elif current[1] == self.last:
                            self.target = current[0]
                        else:
                            self.Coily_Logic(current[0], current[1], player, board)
                elif current[2] == None:
                    self.target = current[3]
                elif current[3] == None:
                    self.target = current[2]
                else: #Choose Best Route!
                    if current[2] == player.block and self.target != self.block:
                        self.target = current[2]
                    elif current[3] == player.block and self.target != self.block:
                        self.target == current[3]
                    else:
                        if current[2] == self.last:
                            self.target = current[3]
                        elif current[3] == self.last:
                            self.target = current[2]
                        else:
                            self.Coily_Logic(current[2], current[3], player, board)
            self.jump(current, player)

    def __init__(self, player, board, block):
        self.wait = 0
        self.block = block
        self.target = None
        self.direction = None
        self.last = None
        c = board.CENTER1[self.block]
        self.location = list(c)
        self.radius = 12.0
        self.vx = 0.0
        self.vy = 0.0
        self.acc = player.acc
        self.offboard = False
        self.dead = False
        self.jump_map = {0 : keymap['Z'],
                         1 : keymap['M'],
                         2 : keymap['Q'],
                         3 : keymap['O'],
                        }
        self.predict_motion(player, board)

    def move_complete(self, player, board):
        req_delta = 2.0
        if self.target != None:
            c = board.CENTER1[self.target]
            delta = norm(self.location, c)
            if delta < req_delta:
                self.location[0] = c[0]
                self.location[1] = c[1]
                self.last = self.block
                self.block = self.target
                self.predict_motion(player, board)

    def move(self, player, block_length, board, width, height, enemies, allies):
        if self.wait != 0:
            self.wait -= 1
            if self.wait == 0:
                gamesounds['Coily Hop'].rewind()
                gamesounds['Coily Hop'].play()
        elif self.block == None:
            self.location[1] += self.vy
            self.vy += self.acc
            self.move_complete(player, board)
        elif self.target == None:
            #Stuck?
            x = self.location[0]
            for i in range(21, 28):
                c = board.CENTER1[i]
                if abs(x - c[0]) <= 10:
                    self.block = i
                    current = board.blockmap[i]
                    self.target = current[random.randrange(2,4)]
                    break
            self.jump(current, player)
        else:
            self.location[0] += self.vx
            self.location[1] += self.vy
            self.vy += self.acc
            if self.location[1] > height:
                if self.dead:
                    for key in gamesounds:
                        gamesounds[key].pause()
                    enemies.__init__()
                    allies.__init__()
                else:
                    player.scoring('Coily Killed')
                    self.dead = True
            else:
                self.move_complete(player, board)

    def draw(self, canvas):
        if self.wait != 0 and self.block == None:
            return
        pos = self.location
        if self.direction == 'Down Left' or self.direction == 'Up Left':
            canvas.draw_line([pos[0] +  0, pos[1] +  5], [pos[0] - 15, pos[1] + 15],  4, 'Purple')
            canvas.draw_line([pos[0] +  0, pos[1] +  5], [pos[0] + 15, pos[1] -  5],  8, 'Purple')
            canvas.draw_line([pos[0] + 15, pos[1] -  5], [pos[0] - 15, pos[1] - 15],  8, 'Purple')
            canvas.draw_line([pos[0] - 15, pos[1] - 15], [pos[0] + 15, pos[1] - 25],  8, 'Purple')
            canvas.draw_line([pos[0] + 15, pos[1] - 25], [pos[0] - 15, pos[1] - 35],  8, 'Purple')
            canvas.draw_circle([pos[0] - 12, pos[1] - 35], 10, 1, 'Purple', 'Purple')
            canvas.draw_circle([pos[0] - 13, pos[1] - 35],  3, 1, 'Black', 'Black')
            canvas.draw_line([pos[0] - 13, pos[1] - 35], [pos[0] - 13, pos[1] - 30], 2, 'White')
        else:
            canvas.draw_line([pos[0] +  0, pos[1] +  5], [pos[0] + 15, pos[1] + 15],  4, 'Purple')
            canvas.draw_line([pos[0] +  0, pos[1] +  5], [pos[0] - 15, pos[1] -  5],  8, 'Purple')
            canvas.draw_line([pos[0] - 15, pos[1] -  5], [pos[0] + 15, pos[1] - 15],  8, 'Purple')
            canvas.draw_line([pos[0] + 15, pos[1] - 15], [pos[0] - 15, pos[1] - 25],  8, 'Purple')
            canvas.draw_line([pos[0] - 15, pos[1] - 25], [pos[0] + 15, pos[1] - 35],  8, 'Purple')
            canvas.draw_circle([pos[0] + 12, pos[1] - 35], 10, 1, 'Purple', 'Purple')
            canvas.draw_circle([pos[0] + 13, pos[1] - 35],  3, 1, 'Black', 'Black')
            canvas.draw_line([pos[0] + 13, pos[1] - 35], [pos[0] + 13, pos[1] - 30], 2, 'White')

class Purple_Ball(Non_Player_Character):

    def __init__(self, player, width, block_length):
        Non_Player_Character.__init__(self, player, width, block_length)
        self.wait = initial_spawn_pause('Purple Ball', player.level)
        self.hatch = 0
        self.sound = gamesounds['Ball Bounce']
        self.sound.set_volume(0.25)

    def move(self, player, block_length, board, width, height):
        if self.wait != 0:
            self.wait -= 1
        elif self.block == None:
            self.location[1] += self.vy
            self.vy += self.acc
            self.move_complete(board, player)
        elif self.target == None:
            self.hatch += 1
        else:
            self.location[0] += self.vx
            self.location[1] += self.vy
            self.vy += self.acc
            if self.location[1] > height:
                self.__init__(player, width, block_length)
            else:
                self.move_complete(board, player)

    def draw(self, canvas):
        if self.wait != 0 and self.block == None:
            return
        draw_ball(self.location, 15, "Purple", canvas)

class Red_Ball(Non_Player_Character):

    def __init__(self, player, width, block_length):
        Non_Player_Character.__init__(self, player, width, block_length)
        self.wait = initial_spawn_pause('Red Ball', player.level)
        self.sound = gamesounds['Ball Bounce']
        self.sound.set_volume(0.25)

    def draw(self, canvas):
        if self.wait != 0 and self.block == None:
            return
        draw_ball(self.location, 15, "Red", canvas)

class Enemies:
    def __init__(self):
        self.Red_Whammies = []
        self.Purple_Egg   = []
        self.Coily        = []
        self.Ugg          = []
        self.Wrong_Way    = []
        self.wait = 0
        self.coily_wait = 0
        self.spawn_rate = 90

    def distance(self, enemy, player):
        r = 10.0
        delta = norm(player.position, enemy.location)
        return delta <= r + enemy.radius

    def check_collisions(self, player):
        #Check to see if they are within their own radius
        for red in self.Red_Whammies:
            if self.distance(red, player):
                return 1
        for purple in self.Coily:
            if self.distance(purple, player):
                return 2
        for purple in self.Purple_Egg:
            if self.distance(purple, player):
                return 3
        for ugg in self.Ugg:
            if self.distance(ugg, player):
                return 4
        for wrongway in self.Wrong_Way:
            if self.distance(wrongway, player):
                return 5
        return 0

    def spawn(self, player):
        self.spawn_rate += 30 *(len(self.Purple_Egg) + len(self.Coily) + \
                                len(self.Red_Whammies) + len(self.Ugg) + \
                                len(self.Wrong_Way))
        self.spawn_rate -= 10 * player.level[1]

    def generate_enemies(self, player, board, WIDTH, BLOCK_LENGTH):
        total_enemies = len(self.Purple_Egg) + len(self.Coily) + \
                        len(self.Red_Whammies) + len(self.Ugg) + len(self.Wrong_Way)
        if len(self.Purple_Egg) == 1:
            if self.Purple_Egg[0].hatch > 0 and self.Purple_Egg[0].hatch % 180 == 0:
                #Spawn Coily
                self.Coily.append(Coily(player, board, self.Purple_Egg[0].block))
                self.Purple_Egg = []
        self.wait += 1
        if self.wait % (self.spawn_rate // player.level[0]) == 0:
            if self.wait > 300 and (len(self.Purple_Egg) + len(self.Coily)) == 0:
                v = 1 #Spawn Coily!
            else:
                #Randomly Generate an Enemy!
                if player.level[0] == 1 and player.level[1] != 3:
                    v = random.randrange(0, 6 - player.level[1])
                elif player.level[0] == 1 and player.level[1] == 3:
                    v = random.randrange(1, 4)
                else:
                    v = random.randrange(0, 4)
            if v == 0 and len(self.Red_Whammies) < 3 and total_enemies < player.max_enemies:
                if (player.level[0] == 1 and player.level[1] == 3) or \
                   (player.level[0] == 2 and player.level[1] == 1) or \
                   (player.level[0] == 2 and player.level[1] == 2) or \
                   (player.level[0] == 3 and player.level[1] == 2):
                    return
                else:
                    self.Red_Whammies.append(Red_Ball(player, WIDTH, BLOCK_LENGTH))
                    self.spawn(player)
            if v == 1 and len(self.Purple_Egg) + len(self.Coily) == 0:
                self.Purple_Egg.append(Purple_Ball(player, WIDTH, BLOCK_LENGTH))
                self.spawn(player)
            if v == 2 and len(self.Ugg) < 2 and total_enemies < player.max_enemies:
                if (player.level[0] == 1 and player.level[1] == 1) or \
                   (player.level[0] == 1 and player.level[1] == 2) or \
                   (player.level[0] == 1 and player.level[1] == 4) or \
                   (player.level[0] == 2 and player.level[1] == 3) or \
                   (player.level[0] == 3 and player.level[1] == 1) or \
                   (player.level[0] == 4 and player.level[1] == 1) or \
                   (player.level[0] == 4 and player.level[1] == 3):
                    return
                else:
                    self.Ugg.append(Ugg(WIDTH, player, BLOCK_LENGTH))
                    self.spawn(player)
            if v == 3 and len(self.Wrong_Way) < 2 and total_enemies < player.max_enemies:
                if (player.level[0] == 1 and player.level[1] == 1) or \
                   (player.level[0] == 1 and player.level[1] == 2) or \
                   (player.level[0] == 1 and player.level[1] == 4) or \
                   (player.level[0] == 2 and player.level[1] == 3) or \
                   (player.level[0] == 3 and player.level[1] == 1) or \
                   (player.level[0] == 4 and player.level[1] == 1) or \
                   (player.level[0] == 4 and player.level[1] == 3):
                    return
                else:
                    self.Wrong_Way.append(WrongWay(player, BLOCK_LENGTH))
                    self.spawn(player)

    def move(self, BLOCK_LENGTH, board, WIDTH, HEIGHT, player, enemies, allies):
        for red_enemies in self.Red_Whammies:
            red_enemies.move(player, BLOCK_LENGTH, board, WIDTH, HEIGHT)
        for purple_enemies in self.Purple_Egg:
            purple_enemies.move(player, BLOCK_LENGTH, board, WIDTH, HEIGHT)
        for purple_enemies in self.Coily:
            purple_enemies.move(player, BLOCK_LENGTH, board, WIDTH, HEIGHT, enemies, allies)
        for ugg in self.Ugg:
            ugg.move(player, board, WIDTH, BLOCK_LENGTH)
        for wrongway in self.Wrong_Way:
            wrongway.move(player, board, WIDTH, BLOCK_LENGTH)

    def draw(self, canvas, player, board, WIDTH, BLOCK_LENGTH):
        #Generate New Enemies (if applicable)
        self.generate_enemies(player, board, WIDTH, BLOCK_LENGTH)
        for red_enemies in self.Red_Whammies:
            red_enemies.draw(canvas)
        for purple_enemies in self.Purple_Egg:
            purple_enemies.draw(canvas)
        for purple_enemies in self.Coily:
            if not purple_enemies.offboard or purple_enemies.vy <= 0:
                purple_enemies.draw(canvas)
        for ugg in self.Ugg:
            ugg.draw(canvas)
        for wrongway in self.Wrong_Way:
            wrongway.draw(canvas)

class Qbert:

    def jump_speed(self):
        """ Speed up the jump rate with the level """
        global keymap
        if self.level[0] <= 4:
            self.frames_per_jump = 32.0 - 2.0 * self.level[1]
        elif self.level[0] <= 7:
            self.frames_per_jump = 30.0 - 2.0 * self.level[1]
        else:
            self.frames_per_jump = 28.0 - 2.0 * self.level[1]
        #X-Velocity Given the Block Length and Frames per Jump
        self.vx0L = xvelocity(-BLOCK_LENGTH / 2.0, self.frames_per_jump)
        self.vx0R = xvelocity(+BLOCK_LENGTH / 2.0, self.frames_per_jump)
        #Y-Velocity Given the Block Length, Acceleration, Frames Per Jump
        if self.level == [1, 1]:
            self.acc = 0.275 #pixels per frame per frame initial acceleration
            self.vy0U = yvelocity(-BLOCK_LENGTH*2.0/3.0, self.frames_per_jump, self.acc)
            self.vy0D = yvelocity(+BLOCK_LENGTH*2.0/3.0, self.frames_per_jump, self.acc)
            self.max_height = max_jump_height(self.vy0D, self.acc)
        else:
            self.vy0D, self.acc = acc_and_yvelocity(self.max_height,
                                    +BLOCK_LENGTH*2.0/3.0, self.frames_per_jump)
            self.vy0U = yvelocity(-BLOCK_LENGTH*2.0/3.0, self.frames_per_jump, self.acc)

    def get_vx0L(self):
        return self.vx0L

    def get_vx0R(self):
        return self.vx0R

    def get_vy0U(self):
        return self.vy0U

    def get_vy0D(self):
        return self.vy0D

    def set_vx(self, value):
        self.vx = value

    def set_vy(self, value):
        self.vy = value

    def spinner_properties(self):
        self.max_spinner_wait_time = 200.0 * self.frames_per_jump / 30.0
        self.spinner_vy = -1.875 * (2.5 - self.frames_per_jump / 20.0)
        self.spinner_vx = +1.5 * (2.5 - self.frames_per_jump / 20.0)

    def __init__(self, width, check = False):
        self.level = [1, 1]
        self.jump_speed()
        self.max_enemies = 3
        self.direction = "Down Left"
        self.vx = 0.0
        self.vy = 0.0
        self.block = 0
        self.position = [width / 2.0, 160.0]
        self.score = 0
        self.in_air = False
        self.lives = 3
        if check:
            self.lives *= 10
        self.extra = 0
        self.wait_time  = 0
        self.all_ok = False
        self.death_wait_time = 0
        self.reset_board = False
        self.freeze_board_wait_time = 0
        self.game_over_wait_time = 0
        self.on_spinner = False
        self.spinner_wait_time = 0
        self.pause_spawn = False
        self.dyingsound = False
        self.lastkey = [40, False]
        self.spinner_properties()

    def restart(self, board):
        gamesounds['Pybert Off Board'].pause()
        self.dyingsound = False
        self.vx = 0.0
        self.vy = 0.0
        self.in_air = False
        c = board.CENTER1[self.block]
        self.position[0] = c[0]
        self.position[1] = c[1]
        self.reset_board = False
        self.wait_time = 0
        self.death_wait_time = 0
        self.on_spinner = False
        self.spinner_wait_time = 0
        if self.lastkey[1]:
            keydown(self.lastkey[0])

    def new_game(self, width, start_screen3, start_screen1):
        self.__init__(width, start_screen1.check())
        start_screen3.show_display(width, self.level)

    def extra_man(self):
        #Extra Man at 8000 and every 14000 pts afterwards
        if self.extra == 0 and self.score >= 8000:
            self.extra += 1
            self.lives += 1
            gamesounds['Extra Man'].rewind()
            gamesounds['Extra Man'].play()
        elif self.score >= self.extra * 14000 + 8000:
            self.extra += 1
            self.lives += 1
            gamesounds['Extra Man'].rewind()
            gamesounds['Extra Man'].play()

    def death(self, width, death_type):
        frame.set_canvas_background("Black")
        self.lives -= 1
        if death_type == 'Off Board':
            self.position = [width / 2.0, 160.0]
            if self.lives == 0:
                self.game_over_wait_time += 1
        elif death_type == 'Collision':
            self.death_wait_time += 1
            self.reset_board = True

    def new_level(self, width, board, start_screen3):
        frame.set_canvas_background("Black")
        self.direction = 'Down Left'
        self.vx = 0.0
        self.vy = 0.0
        self.all_ok = False
        self.position = [width / 2.0, 160.0]
        self.block = 0
        self.level[1] += 1
        if self.level[1] % 5 == 0:
            self.level[0] += 1
            self.level[1] = 1
            if self.level[0] > 9: #Max Level Reached!
                self.level[0] = 9
        self.jump_speed()
        if self.level[0] == 9:
            self.max_enemies = 6
        elif self.level[0] >= 7:
            self.max_enemies = 5
        elif self.level[0] >= 4:
            self.max_enemies = 4
        self.spinner_properties()
        board.Board_Colors(self.level)
        board.Set_Spinners(self.level, BLOCK_LENGTH)
        board.bonus_color = 0
        if self.level[1] == 1:
            start_screen3.show_display(width, self.level)
        if self.lastkey[1]:
            keydown(self.lastkey[0])

    def scoring(self, Action):
        scoring = {'Coily Killed' : 500,
                   'Slick'        : 300,
                   'Sam'          : 300,
                   'Green Ball'   : 100,
                   'Cubes'        :  25,
                   'Intermediate' :  15,
                   'Unused Disks' :  50,
                  }
        self.score += scoring[Action]
        self.extra_man()

    def bonus_points(self, flag):
        bonus = 1000
        additional = (self.level[0] - 1)* 4 + self.level[1] % 5 - 1
        bonus += additional * 250
        if bonus > 5000:
            bonus = 5000
        if flag:
            return bonus
        else:
            self.score += bonus
            self.extra_man()

    def move(self, width, height, board, enemies = None, allies = None, start_screen3 = None):
        #Get the Player's Target Block Value
        next_block = board.new_block(self.block, self.direction)
        if self.wait_time != 0:
            Order = True
            self.wait_time += 1
            self.wait_time = self.wait_time % 270
            if self.wait_time == 0:
                for unused in board.spinners:
                    self.scoring('Unused Disks')
                self.bonus_points(False)
                self.new_level(width, board, start_screen3)
                enemies.__init__()
                allies.__init__()
            return Order
        elif self.on_spinner:
            if (enemies and len(enemies.Coily) == 1 and enemies.Coily[0].location[1] > height) \
                or self.pause_spawn:
                for key in gamesounds:
                    if not key in ['Spinner', 'Extra Man', 'Freeze Board']:
                        gamesounds[key].pause()
                enemies.Red_Whammies = []
                enemies.Purple_Egg   = []
                enemies.Coily        = []
                enemies.Ugg          = []
                enemies.Wrong_Way    = []
                allies.Green_Balls   = []
                allies.Slick         = []
                allies.Sam           = []
                self.pause_spawn     = True
            if self.spinner_wait_time >= self.max_spinner_wait_time:
                gamesounds['Spinner'].pause()
                #Remove Spinner from Spinner List!
                if self.block in board.spinnerlocs and self.block != 0:
                    index = board.spinnerlocs.index(self.block)
                    board.spinnerlocs.pop(index)
                    board.spinnerpos.pop(index)
                    board.spinners.pop(index)
                elif self.block in board.spinnerlocs and \
                     self.direction == 'Up Left' and 'Left' in board.spinnerlocs:
                    index1 = board.spinnerlocs.index('Left')
                    index = len(board.spinnerlocs) - index1 - 1
                    board.spinnerlocs.pop(index1)
                    board.spinnerlocs.pop(index)
                    board.spinnerpos.pop(index)
                    board.spinners.pop(index)
                elif self.block in board.spinnerlocs and \
                     self.direction == 'Up Right' and 'Right' in board.spinnerlocs:
                    index1 = board.spinnerlocs.index('Right')
                    index = len(board.spinnerlocs) - index1 - 1
                    board.spinnerlocs.pop(index1)
                    board.spinnerlocs.pop(index)
                    board.spinnerpos.pop(index)
                    board.spinners.pop(index)
                #Free Fall back to Start!
                self.position[1] += self.vy
                self.vy += self.acc
                c2 = board.CENTER1[0]
                delta = norm(self.position, c2)
                if delta < delta_max(100.0, self.acc):
                    gamesounds['Hop'].rewind()
                    gamesounds['Hop'].play()
                    if self.pause_spawn:
                        self.pause_spawn = False
                        enemies.__init__()
                        allies.__init__()
                    self.direction = 'Down Left'
                    self.spinner_wait_time = 0
                    self.on_spinner = False
                    self.in_air = False
                    self.position[0] = c2[0]
                    self.position[1] = c2[1]
                    self.block = 0
                    # Determine if the Block Color Should Change
                    target_color = board.Board_Color_Scheme(self.level)
                    board.change_board_color(0, target_color, False, self)
                    #Check for level complete status
                    self.all_ok = True
                    for color in board.board_color:
                        if color != target_color[3]:
                            self.all_ok = False
                            break
                    if self.all_ok:
                        self.in_air = False
                        self.wait_time += 1
                        self.freeze_board_wait_time = 0
                        for key in gamesounds:
                            gamesounds[key].pause()
                        gamesounds['Board Clear'].rewind()
                        gamesounds['Board Clear'].play()
                    elif self.lastkey[1]:
                        keydown(self.lastkey[0])
            else:
                self.set_vx(self.spinner_vx)
                if self.direction != 'Up Left':
                    self.vx = -self.vx
                    if self.position[0] + self.vx <= width / 2.0:
                        self.position[0] = width / 2.0
                        self.vx = 0.0
                else:
                    if self.position[0] + self.vx >= width / 2.0:
                        self.position[0] = width / 2.0
                        self.vx = 0.0
                self.set_vy(self.spinner_vy)
                if self.position[1] + self.vy <= 60.0:
                    self.position[1] = 60.0
                    self.vy = 0.0
                self.position[0] += self.vx
                self.position[1] += self.vy
                self.spinner_wait_time += 1
                #Also Move Spinner!
                if self.block == 0:
                    if self.direction == 'Up Left':
                        index1 = board.spinnerlocs.index('Left')
                        index = len(board.spinnerlocs) - index1 - 1
                    else:
                        index1 = board.spinnerlocs.index('Right')
                        index = len(board.spinnerlocs) - index1 - 1
                else:
                    index = board.spinnerlocs.index(self.block)
                board.spinners[index].move(self.vx, self.vy)
            return True
        elif next_block == None:
            #Player Jumped off the Pyramid
            #Check to see if player is jumping onto a spinner
            if self.block in board.spinnerlocs and self.direction in ['Up Left', 'Up Right']:
                if self.block == 0:
                    if self.direction == 'Up Left' and 'Left' in board.spinnerlocs:
                        index = board.spinnerlocs.index('Left')
                        index = len(board.spinnerlocs) - index - 1
                    elif self.direction == 'Up Right' and 'Right' in board.spinnerlocs:
                        index = board.spinnerlocs.index('Right')
                        index = len(board.spinnerlocs) - index - 1
                    else: #Plummet to Death!
                        self.all_ok = False
                        c2 = None
                        if self.vy < 0 or self.block > 20:
                            Order = True
                        else:
                            Order = False
                        self.position[0] += self.vx
                        self.position[1] += self.vy
                        self.vy += self.acc
                        if self.position[1] > height:
                            self.reset_board = True
                            self.in_air = False
                            self.death(width, 'Off Board')
                            self.block = 0
                        if not self.dyingsound:
                            self.dyingsound = True
                            gamesounds['Pybert Off Board'].rewind()
                            gamesounds['Pybert Off Board'].play()
                        return Order
                else:
                    index = board.spinnerlocs.index(self.block)
                self.position[0] += self.vx
                self.position[1] += self.vy
                self.vy += self.acc
                c2 = board.spinnerpos[index]
                delta = norm(self.position, c2)
                if delta < 1.0:
                    self.on_spinner = True
                    self.spinner_wait_time += 1
                    gamesounds['Spinner'].rewind()
                    gamesounds['Spinner'].play()
                Order = True
            else:
                self.all_ok = False
                c2 = None
                if self.vy < 0 or self.block > 20:
                    Order = True
                else:
                    Order = False
                self.position[0] += self.vx
                self.position[1] += self.vy
                self.vy += self.acc
                if self.position[1] > height:
                    self.reset_board = True
                    self.in_air = False
                    self.death(width, 'Off Board')
                    self.block = 0
                if not self.dyingsound:
                    self.dyingsound = True
                    gamesounds['Pybert Off Board'].rewind()
                    gamesounds['Pybert Off Board'].play()
            return Order
        else:
            self.all_ok = True
            Order = True
            c1 = board.CENTER1[self.block]
            c2 = board.CENTER1[next_block]
            self.position[0] += self.vx
            self.position[1] += self.vy
            self.vy += self.acc
            delta = norm(self.position, c2)
            target_color = board.Board_Color_Scheme(self.level)
            if delta < 1.0:
                gamesounds['Hop'].rewind()
                gamesounds['Hop'].play()
                self.in_air = False
                self.position[0] = c2[0]
                self.position[1] = c2[1]
                self.block    = next_block
                # Determine if the Block Color Should Change
                board.change_board_color(next_block, target_color, False, self)
            #Check for level complete status
            for color in board.board_color:
                if color != target_color[3]:
                    self.all_ok = False
                    break
            if self.all_ok:
                self.in_air = False
                self.wait_time += 1
                self.freeze_board_wait_time = 0
                for key in gamesounds:
                    gamesounds[key].pause()
                gamesounds['Board Clear'].rewind()
                gamesounds['Board Clear'].play()
            elif self.lastkey[1]:
                keydown(self.lastkey[0])
            return Order

    def collisions(self, width, allies, enemies, enemies_frozen):
        if self.in_air and board.new_block(self.block, self.direction) == None:
            return #Prevent Collisions While Jumping to Spinner from Block 0
        if not enemies_frozen:
            result = enemies.check_collisions(self)
            if result != 0:
                for key in gamesounds:
                    gamesounds[key].pause()
                if result == 1:   #Collision with red ball
                    gamesounds['Bop'].rewind()
                    gamesounds['Bop'].play()
                elif result == 2: #Collision with coily
                    gamesounds['Coily Attack'].rewind()
                    gamesounds['Coily Attack'].play()
                elif result == 3: #Collision with purple egg
                    gamesounds['Bop'].rewind()
                    gamesounds['Bop'].play()
                elif result == 4: #Collision with Ugg
                    pass
                else: #Collision with Wrong-Way
                    pass
                gamesounds['Curse'].rewind()
                gamesounds['Curse'].play()
                self.death(width, 'Collision')
        result = allies.check_collisions(self)
        if result != 0: #Increase Score!
            if result == 1:   #Green Ball
                self.freeze_board_wait_time += 1
                for key in gamesounds:
                    gamesounds[key].pause()
                gamesounds['Freeze Board'].rewind()
                gamesounds['Freeze Board'].play()
                self.scoring('Green Ball')
            elif result == 2: #Slick
                self.scoring('Slick')
            else:             #Sam
                self.scoring('Sam')

    def draw(self, canvas):
        draw_Pybert(self.position, self.direction, canvas)

class Board:

    def __init__(self, width, block_length):
        """Generate the Playing Board"""
        top_center = [width / 2.0, 160.0]
        self.BOARD_POSITION1 = [] #TOPS
        self.BOARD_POSITION2 = [] #LEFT SIDES
        self.BOARD_POSITION3 = [] #RIGHT SIDES
        self.CENTER1 = []         #Top Center
        self.CENTER2 = []         #Left Center
        self.CENTER3 = []         #Right Center
        for i in range(7):
            for j in range(i+1):
                x0, y0 = top_center[0], top_center[1]
                x1, y1 = x0 - block_length / 2.0, y0 + block_length / 6.0
                x2, y2 = x0, y0 + block_length / 3.0
                x3, y3 = x0 + block_length / 2.0, y0 + block_length / 6.0
                self.BOARD_POSITION1.append([[x0, y0], [x1, y1], [x2, y2], [x3, y3]])
                self.CENTER1.append([x0, y0])
                x5, y5 = x3, y3
                x4, y4 = x3, y3 + block_length - block_length / 2.0
                x3, y3 = x2, y2
                x0, y0 = x1, y1
                x1, y1 = x1, y1 + block_length - block_length / 2.0
                x2, y2 = x2, y2 + block_length - block_length / 2.0
                self.BOARD_POSITION2.append([[x0, y0], [x1, y1], [x2, y2], [x3, y3]])
                self.CENTER2.append([x1 + block_length / 6.0, y2 - block_length / 3.0])
                self.BOARD_POSITION3.append([[x5, y5], [x3, y3], [x2, y2], [x4, y4]])
                self.CENTER3.append([x1 + 5.0 * block_length / 6.0, y2 - block_length / 3.0])
                if j == i:
                    if i % 2 == 0:
                        top_center[0] += block_length / 2.0
                    else:
                        top_center[0] -= block_length / 2.0
                elif i % 2 == 0:
                    top_center[0] += block_length
                else:
                    top_center[0] -= block_length
            top_center[1] += block_length * 2.0 / 3.0
        self.blockmap = { 0 : [   2,    1, None, None],
                          1 : [   4,    5,    0, None],
                          2 : [   3,    4, None,    0],
                          3 : [   9,    8, None,    2],
                          4 : [   8,    7,    2,    1],
                          5 : [   7,    6,    1, None],
                          6 : [  13,   14,    5, None],
                          7 : [  12,   13,    4,    5],
                          8 : [  11,   12,    3,    4],
                          9 : [  10,   11, None,    3],
                         10 : [  20,   19, None,    9],
                         11 : [  19,   18,    9,    8],
                         12 : [  18,   17,    8,    7],
                         13 : [  17,   16,    7,    6],
                         14 : [  16,   15,    6, None],
                         15 : [  26,   27,   14, None],
                         16 : [  25,   26,   13,   14],
                         17 : [  24,   25,   12,   13],
                         18 : [  23,   24,   11,   12],
                         19 : [  22,   23,   10,   11],
                         20 : [  21,   22, None,   10],
                         21 : [None, None, None,   20],
                         22 : [None, None,   20,   19],
                         23 : [None, None,   19,   18],
                         24 : [None, None,   18,   17],
                         25 : [None, None,   17,   16],
                         26 : [None, None,   16,   15],
                         27 : [None, None,   15, None],
                        }
            #        current :   Wrong-Way     Ugg
        self.blockmap2 = { 0 : [None, None, None, None],
                           1 : [None, None,    0,    2],
                           2 : [   0,    1, None, None],
                           3 : [   2,    4, None, None],
                           4 : [   1,    5,    2,    3],
                           5 : [None, None,    1,    4],
                           6 : [None, None,    5,    7],
                           7 : [   5,    6,    4,    8],
                           8 : [   4,    7,    3,    9],
                           9 : [   3,    8, None, None],
                          10 : [   9,   11, None, None],
                          11 : [   8,   12,    9,   10],
                          12 : [   7,   13,    8,   11],
                          13 : [   6,   14,    7,   12],
                          14 : [None, None,    6,   13],
                          15 : [None, None,   14,   16],
                          16 : [  14,   15,   13,   17],
                          17 : [  13,   16,   12,   18],
                          18 : [  12,   17,   11,   19],
                          19 : [  11,   18,   10,   20],
                          20 : [  10,   19, None, None],
                          21 : [  20,   22, None, None],
                          22 : [  19,   23,   20,   21],
                          23 : [  18,   24,   19,   22],
                          24 : [  17,   25,   18,   23],
                          25 : [  16,   26,   17,   24],
                          26 : [  15,   27,   16,   25],
                          27 : [None, None,   15,   26],
                         }
        #      	     Level.Round :  Top,          Left,          Right,           Change To,    Intermediate
        self.block_colors = {1.1 : ["Blue",       "Cyan",        "Gray",          "Yellow",        None         ],
                             1.2 : ["Tan",        "Brown",       "Orange",        "Blue",          None         ],
                             1.3 : ["LightGrey",  "Silver",      "Gray",          "DarkSlateGray", None         ],
                             1.4 : ["Blue",       "Gray",        "DarkBlue",      "Yellow",        None         ],
                             2.1 : ["Blue",       "Brown",       "Orange",        "Green",         "Tan"        ],
                             2.2 : ["#6C2DC7",    "Gray",        "DarkBlue",      "Yellow",        "Cyan"       ],
                             2.3 : ["Pink",       "LightGrey",   "DarkGray",      "Yellow",        "Blue"       ],
                             2.4 : ["Yellow",     "Black",       "Black",         "Pink",          "Blue"       ],
                             3.1 : ["DodgerBlue", "YellowGreen", "LightCoral",    "DarkBlue",      None         ],
                             3.2 : ["Gray",       "Silver",      "DarkSlateGray", "LightGrey",     None         ],
                             3.3 : ["Blue",       "Brown",       "Orange",        "YellowGreen",   None         ],
                             3.4 : ["Yellow",     "Teal",        "Silver",        "Blue",          None         ],
                             4.1 : ["Green",      "Brown",       "Tomato",        "Blue",          "YellowGreen"],
                             4.2 : ["Blue",       "Black",       "Black",         "Yellow",        "Pink"       ],
                             4.3 : ["Yellow",     "Teal",        "Gray",          "Blue",          "Pink"       ],
                             4.4 : ["#6C2DC7",     "Gray",        "DarkBlue",      "Yellow",       "LightCyan"  ],
                             5.1 : ["Pink",       "Teal",        "Silver",        "Blue",          "Yellow"     ],
                             5.2 : ["Green",      "Brown",       "Tan",           "YellowGreen",   "Blue"       ],
                             5.3 : ["Gray",       "Silver",      "DarkSlateGray", "LightGrey",     "Blue"       ],
                             5.4 : ["Yellow",     "LightGrey",   "DarkBlue",      "#6C2DC7",       "Blue"       ],
                             6.1 : ["Green",      "Brown",       "Tomato",        "LightGrey",     "Blue"       ],
                             6.2 : ["Blue",       "Silver",      "DarkBlue",      "Yellow",        "#6C2DC7"    ],
                             6.3 : ["Pink",       "Teal",        "Gray",          "Blue",          "Yellow"     ],
                             6.4 : ["Pink",       "Black",       "Black",         "Yellow",        "Blue"       ],
                             7.1 : ["DarkBlue",   "YellowGreen", "LightCoral",    "#6C2DC7",       "LightCyan"  ],
                             7.2 : ["LightGrey",  "Silver",      "DarkSlateGray", "Blue",          "Gray"       ],
                             7.3 : ["Green",      "Brown",       "Orange",        "LightGrey",     "Blue"       ],
                             7.4 : ["Yellow",     "Teal",        "Gray",          "Pink",          "Blue"       ],
                             8.1 : ["Blue",       "Brown",       "Orange",        "Green",         "LightGrey"  ],
                             8.2 : ["Pink",       "Black",       "Black",         "Yellow",        "Blue"       ],
                             8.3 : ["Yellow",     "Teal",        "Gray",          "Pink",          "Blue"       ],
                             8.4 : ["Yellow",     "Silver",      "DarkBlue",      "#6C2DC7",       "LightCyan"  ],
                             9.1 : ["Blue",       "Teal",        "Gray",          "Yellow",        "Pink"       ],
                             9.2 : ["LightGrey",  "Brown",       "Orange",        "Blue",          "Green"      ],
                             9.3 : ["#6C2DC7",    "YellowGreen", "Tomato",        "Blue",          "DarkBlue"   ],
                             9.4 : ["#6C2DC7",    "Silver",      "DarkBlue",      "LightCyan",     "Yellow"     ],
                            }
        self.board_color = []
        self.starting_color = []
        self.bonus_color = 0
        self.spinnermap = {1.1 : [10, 14],
                           1.2 : [20, 27],
                           1.3 : [ 9, 15],
                           1.4 : [ 0, 27, 'Left'],
                           2.1 : [ 0,  9,    14,  'Right'],
                           2.2 : [ 0, 15,    20,  'Right'],
                           2.3 : [ 3, 15],
                           2.4 : [ 2,  6],
                           3.1 : [ 3,  5,     6,       10],
                           3.2 : [ 3,  6,     9,       15],
                           3.3 : [ 0,  3,    14,   'Left'],
                           3.4 : [ 1, 14,    27],
                           4.1 : [ 0,  1,     9,       15,     20,  27, 'Left'],
                           4.2 : [ 0,  1,    10,       15,     20,  27, 'Left'],
                           4.3 : [ 1,  3,     5,       10,     14],
                           4.4 : [ 0,  2,     6,       27, 'Left'],
                           5.1 : [ 0,  0,     2,        5,      9,  20,     27, 'Left', 'Right'],
                           5.2 : [ 0,  1,     6,       10,     14,  20, 'Left'],
                           5.3 : [ 3,  5,     6,       10,     27],
                           5.4 : [ 3,  5,     6,       10,     27],
                           6.1 : [ 3,  5,     6,       10,     27],
                           6.2 : [ 3,  5,     6,       10,     27],
                           6.3 : [ 3,  5,     6,       10,     27],
                           6.4 : [ 3,  5,     6,       10,     27],
                           7.1 : [ 3,  5,     6,       10,     27],
                           7.2 : [ 3,  5,     6,       10,     27],
                           7.3 : [ 3,  5,     6,       10,     27],
                           7.4 : [ 3,  5,     6,       10,     27],
                           8.1 : [ 3,  5,     6,       10,     27],
                           8.2 : [ 3,  5,     6,       10,     27],
                           8.3 : [ 3,  5,     6,       10,     27],
                           8.4 : [ 3,  5,     6,       10,     27],
                           9.1 : [ 3,  5,     6,       10,     27],
                           9.2 : [ 3,  5,     6,       10,     27],
                           9.3 : [ 3,  5,     6,       10,     27],
                           9.4 : [ 3,  5,     6,       10,     27],
                          }
        self.spinners = []
        self.spinnerlocs = []
        self.spinnerpos = []
        self.next_block_map = {'Down Left'  : 0,
                               'Down Right' : 1,
                               'Up Left'    : 2,
                               'Up Right'   : 3,
                              }

    def Set_Spinners(self, level, block_length):
        leftmap = [2, 3, 9, 10, 20, 21]
        yoffset = block_length * 2.0 / 3.0
        locations = self.spinnermap[level[0] + level[1] / 10.0]
        self.spinners = []
        self.spinnerlocs = []
        self.spinnerpos = []
        index = 0
        for loc in locations:
            xoffset = block_length / 2.0
            if loc == 'Left' or loc == 'Right':
                self.spinnerlocs.append(loc)
                continue
            elif loc == 0: #Determine Right Side or Left side
                pos = self.CENTER1[index]
                if locations[-(index+1)] == 'Left':
                    xoffset = -xoffset
            else:
                for block in leftmap:
                    if loc == block:
                        xoffset = -xoffset
                        break
            pos = self.CENTER1[loc]
            self.spinners.append(Spinner(pos[0] + xoffset, \
                                         pos[1] - yoffset + block_length * 1.0 / 4.0, 10, 25, 90))
            self.spinnerpos.append([pos[0] + xoffset, pos[1] - yoffset])
            self.spinnerlocs.append(loc)
            index += 1

    def Board_Color_Scheme(self, level):
        """Define the Board Color Scheme"""
        return self.block_colors[level[0] + level[1] / 10.0]

    def new_block(self, current, direction):
        """Return The Block The Player is Trying to Jump To"""
        new = self.blockmap[current]
        value = self.next_block_map[direction]
        return new[value]

    def Board_Colors(self, level):
        """Color the Board"""
        self.board_color = []
        self.starting_color = self.Board_Color_Scheme(level)
        for board in self.BOARD_POSITION1:
            self.board_color.append(self.starting_color[0])

    def change_board_color(self, next_block, target_color, Ally, player):
        """ Change Board Color on Jump """
        if Ally:
            if self.board_color[next_block] != target_color[0]:
                if player.level[0] == 2 and self.board_color[next_block] == target_color[3]:
                    self.board_color[next_block] = target_color[4]
                else:
                    self.board_color[next_block] = target_color[0]
        else:
            if self.board_color[next_block] == target_color[0]:
                if target_color[4] != None:
                    self.board_color[next_block] = target_color[4]
                    player.scoring('Intermediate')
                else:
                    self.board_color[next_block] = target_color[3]
                    player.scoring('Cubes')
            elif self.board_color[next_block] != target_color[3]:
                self.board_color[next_block] = target_color[3]
                player.scoring('Cubes')
            elif player.level[0] == 3:
                self.board_color[next_block] = target_color[0]
            elif player.level[0] == 4:
                self.board_color[next_block] = target_color[4]
            elif player.level[0] >= 5:
                self.board_color[next_block] = target_color[0]

    def draw(self, player, canvas):
        """Draw the Board"""
        if player.wait_time != 0:
            bonus_color = self.Board_Color_Scheme(player.level)
            if player.wait_time % 10 == 0:
                self.bonus_color += 1
                if bonus_color[4] == None:
                    self.bonus_color = self.bonus_color % 4
                else:
                    self.bonus_color = self.bonus_color % 5
            for block in self.BOARD_POSITION1:
                canvas.draw_polygon(block, 1, bonus_color[self.bonus_color], bonus_color[self.bonus_color])
        else:
            count = 0
            for block in self.BOARD_POSITION1:
                canvas.draw_polygon(block, 1, self.board_color[count], self.board_color[count])
                count += 1
        for block in self.BOARD_POSITION2:
            canvas.draw_polygon(block, 1, self.starting_color[1], self.starting_color[1])
        for block in self.BOARD_POSITION3:
            canvas.draw_polygon(block, 1, self.starting_color[2], self.starting_color[2])
        #Draw the spinners
        for spinner in self.spinners:
            spinner.draw(canvas)

class Spinner:

    def __init__(self, x, y, a, b, angle):
        steps = 120
        beta = -angle * (math.pi / 180.0);
        sinbeta = math.sin(beta);
        cosbeta = math.cos(beta);
        alpha = []
        sinalpha = []
        cosalpha = []
        temp = 0.0
        for i in range(steps):
            sinalpha.append(math.sin(temp * math.pi / 180.0))
            cosalpha.append(math.cos(temp * math.pi / 180.0))
            temp += 360.0 / (steps - 1.0)
        X = []
        Y = []
        for i in range(steps):
            X.append(x + (a * cosalpha[i] * cosbeta - b * sinalpha[i] * sinbeta));
            Y.append(y + (a * cosalpha[i] * sinbeta + b * sinalpha[i] * cosbeta));
        self.position = []
        self.color1loc = []
        self.color2loc = []
        self.color3loc = []
        self.color4loc = []
        for i in range(len(X)):
            self.position.append([X[i], Y[i]])
            if   X[i] < x and Y[i] > y:
                self.color1loc.append([x, y])
                self.color1loc.append([X[i], Y[i]])
            elif X[i] < x and Y[i] < y:
                self.color2loc.append([x, y])
                self.color2loc.append([X[i], Y[i]])
            elif X[i] > x and Y[i] > y:
                self.color3loc.append([x, y])
                self.color3loc.append([X[i], Y[i]])
            elif X[i] > x and Y[i] < y:
                self.color4loc.append([x, y])
                self.color4loc.append([X[i], Y[i]])
        self.count = 0
        self.colorlist = {1: ['Yellow', 'Green',  'Blue',   'Purple'],
                          2: ['Green',  'Blue',   'Purple', 'Yellow'],
                          3: ['Blue',   'Purple', 'Yellow', 'Green'],
                          4: ['Purple', 'Yellow', 'Green',  'Blue']}

    def move(self, dx, dy):
        for i in range(0, len(self.position)):
            self.position[i][0] += dx
            self.position[i][1] += dy
        for i in range(0, len(self.color1loc)):
            self.color1loc[i][0] += dx
            self.color1loc[i][1] += dy
        for i in range(0, len(self.color2loc)):
            self.color2loc[i][0] += dx
            self.color2loc[i][1] += dy
        for i in range(0, len(self.color3loc)):
            self.color3loc[i][0] += dx
            self.color3loc[i][1] += dy
        for i in range(0, len(self.color4loc)):
            self.color4loc[i][0] += dx
            self.color4loc[i][1] += dy

    def draw(self, canvas):
        #Draw Outer Edge
        if self.count < 5:
            colors = self.colorlist[1]
        elif self.count < 10:
            colors = self.colorlist[4]
        elif self.count < 15:
            colors = self.colorlist[2]
        else:
            colors = self.colorlist[3]
        canvas.draw_polyline(self.color1loc, 1, colors[0])
        canvas.draw_polyline(self.color2loc, 1, colors[1])
        canvas.draw_polyline(self.color3loc, 1, colors[2])
        canvas.draw_polyline(self.color4loc, 1, colors[3])
        canvas.draw_polyline(self.position,  3, 'DarkSlateGray')
        self.count += 1
        self.count = self.count % 20

class Leveltransition:

    def __init__(self, width, block_length):
        self.miniboard = Board(width, block_length)
        self.qbert  = Qbert(width)
        self.display = False
        self.movelist = ['Down Left', 'Down Right', 'Up Right', 'Down Left', \
                         'Up Left', 'Down Right', 'Down Right']
        self.vel = {'Down Left'  : [keymap['Z'][2], keymap['Z'][1]],
                    'Down Right' : [keymap['M'][2], keymap['M'][1]],
                    'Up Right'   : [keymap['O'][2], keymap['O'][1]],
                    'Up Left'    : [keymap['Q'][2], keymap['Q'][1]],
                   }
        self.movenumber = 0
        self.initial_wait = 0
        self.wait = 0
        self.level = None

    def show_display(self, WIDTH, level):
        self.initial_wait = 1
        self.wait         = 0
        self.display = True
        self.movenumber = 0
        self.qbert.__init__(WIDTH)
        self.qbert.level = level
        self.qbert.jump_speed()
        self.miniboard.Board_Colors(level)
        self.level = level
        for key in gamesounds:
            gamesounds[key].pause()
        start_screen1.sounds.pause()
        gamesounds['Level Start'].rewind()
        gamesounds['Level Start'].play()

    def move(self, width, height):
        if self.movenumber == len(self.movelist):
            self.wait += 1
            self.wait = self.wait % 30
            if self.wait == 0:
                self.display = False
        elif self.initial_wait !=  0:
            gamesounds['Spinner'].pause()
            self.initial_wait += 1
            self.initial_wait = self.initial_wait % 60
        else:
            if self.qbert.in_air:
                self.qbert.move(width, height, self.miniboard)
            else:
                direction = self.movelist[self.movenumber]
                self.qbert.direction = direction
                self.qbert.vx = self.vel[direction][0]()
                self.qbert.vy = self.vel[direction][1]()
                self.qbert.in_air = True
                self.qbert.move(width, height, self.miniboard)
                self.movenumber += 1

    def draw(self, canvas):
        """Draw the Board"""
        for count in range(5):
            if count != 3:
                canvas.draw_polygon(self.miniboard.BOARD_POSITION1[count], 1, \
                                    self.miniboard.board_color[count], \
                                    self.miniboard.board_color[count])
                canvas.draw_polygon(self.miniboard.BOARD_POSITION2[count], 1, \
                                    self.miniboard.starting_color[1], \
                                    self.miniboard.starting_color[1])
                canvas.draw_polygon(self.miniboard.BOARD_POSITION3[count], 1, \
                                    self.miniboard.starting_color[2], \
                                    self.miniboard.starting_color[2])
        self.qbert.draw(canvas)
        canvas.draw_text("LEVEL", (230, 450), 112, "Purple", "serif")
        canvas.draw_text(str(self.level[0]), (385, 550), 96, 'White')
        canvas.draw_circle([410, 520], 60, 10, "Purple")

################################################################################
# Load Sounds, Courtesy of http://www.universal-soundbank.com, If Possible
################################################################################
gamesounds = {'Bop'              : simplegui.load_sound(BASE_DIRECTORY + "14010.mp3"),
              'Hop'              : simplegui.load_sound(BASE_DIRECTORY + "7410.mp3"),
              'Spinner'          : simplegui.load_sound(BASE_DIRECTORY + "3522.mp3"),
              'Coily Hop'        : simplegui.load_sound(BASE_DIRECTORY + "8955.mp3"),
              'Coily Attack'     : simplegui.load_sound(BASE_DIRECTORY + "19503.mp3"),
              'Pybert Off Board' : simplegui.load_sound(BASE_DIRECTORY + "13558.mp3"),
              'Coily Off Board'  : simplegui.load_sound(BASE_DIRECTORY + "1209.mp3"),
              'Freeze Board'     : simplegui.load_sound(BASE_DIRECTORY + "2737.mp3"),
              'Level Start'      : simplegui.load_sound(BASE_DIRECTORY + "9344.mp3"),
              'Ball Bounce'      : simplegui.load_sound(BASE_DIRECTORY + "12243.mp3"),
              'Extra Man'        : simplegui.load_sound(BASE_DIRECTORY + "1764.mp3"),
              'Curse'            : simplegui.load_sound(BASE_DIRECTORY + "421.mp3"),
              'Slick'            : simplegui.load_sound(BASE_DIRECTORY + "1257.mp3"),
              'Sam'              : simplegui.load_sound(BASE_DIRECTORY + "4037.mp3"),
              'Ugg'              : simplegui.load_sound(BASE_DIRECTORY + "97.mp3"),
              'Wrong Way'        : simplegui.load_sound(BASE_DIRECTORY + "8094.mp3"),
              'Board Clear'      : simplegui.load_sound(BASE_DIRECTORY + "18419.mp3"),
              }
gamesounds['Coily Hop'].set_volume(0.1)
gamesounds['Extra Man'].set_volume(0.1)
gamesounds['Pybert Off Board'].set_volume(0.1)
gamesounds['Spinner'].set_volume(0.2)

################################################################################
# Initialize Key Variables                                                     #
################################################################################
# Create Player, Board, Background, Enemies, and Allies
player = Qbert(WIDTH)
board = Board(WIDTH, BLOCK_LENGTH)
background = Backgrounds()
enemies = Enemies()
allies  = Allies()

################################################################################
# PLAYER INPUT MODULE                                                          #
################################################################################
# Event Handlers
keymap = {'down'  : ['Down Left',  player.get_vy0D, player.get_vx0L],
          'up'    : ['Up Right',   player.get_vy0U, player.get_vx0R],
          'right' : ['Down Right', player.get_vy0D, player.get_vx0R],
          'left'  : ['Up Left',    player.get_vy0U, player.get_vx0L],
          'Z'     : ['Down Left',  player.get_vy0D, player.get_vx0L],
          'O'     : ['Up Right',   player.get_vy0U, player.get_vx0R],
          'M'     : ['Down Right', player.get_vy0D, player.get_vx0R],
          'Q'     : ['Up Left',    player.get_vy0U, player.get_vx0L],
         }

def keydown(key):
    global game_on
    if not game_on:
        start_screen1.keylist.append(key)
        if key == simplegui.KEY_MAP['1']:
            frame.set_canvas_background("Black")
            game_on = True
            init()
    elif player.death_wait_time != 0:
        return
    else:
        if player.in_air or player.wait_time != 0 or \
           start_screen3.display or player.on_spinner:
            for keys in keymap:
                if key == simplegui.KEY_MAP[keys]:
                    player.lastkey =  [key, True]
                    break
            return
        for keys in keymap:
            if key == simplegui.KEY_MAP[keys]:
                player.vy = keymap[keys][1]()
                player.vx = keymap[keys][2]()
                player.direction = keymap[keys][0]
                player.in_air = True
                player.lastkey =  [key, True]
                break

def keyup(key):
    if player.lastkey[0] == key:
        player.lastkey =  [key, False]
################################################################################
# GAME PLAY LOOP                                                               #
################################################################################
def draw(canvas):
    global game_on
    if not game_on:
        if not start_screen1.complete:
            start_screen1.draw(canvas, start_screen2)
        else:
            start_screen2.draw(canvas, start_screen1)
    elif start_screen3.display:
        start_screen3.move(WIDTH, HEIGHT)
        start_screen3.draw(canvas)
    elif player.death_wait_time != 0:
        player.death_wait_time += 1
        player.death_wait_time = player.death_wait_time % 210
        board.draw(player, canvas)
        player.draw(canvas)
        canvas.draw_line([player.position[0] + 30, player.position[1] - 10], \
                         [player.position[0] + 50, player.position[1] - 10], 10, 'White')
        canvas.draw_line([player.position[0] + 50, player.position[1] - 10], \
                         [player.position[0] + 150, player.position[1] - 10], 40, 'White')
        canvas.draw_text('@!#?@!', [player.position[0] + 55, \
                                    player.position[1] - 3],28, 'Black')
        #Draw the Backgrounds
        background.draw(canvas, board, player, 1)
        if player.lives == 0:
            canvas.draw_text('Game Over', [WIDTH/2 - 100, HEIGHT/2], 42, 'Purple')
            start_screen1.__init__(False)
            start_screen2.complete = True
    elif player.game_over_wait_time != 0:
        player.game_over_wait_time += 1
        player.game_over_wait_time = player.game_over_wait_time % 210
        board.draw(player, canvas)
        #Draw the Backgrounds
        background.draw(canvas, board, player, 1)
        canvas.draw_text('Game Over', [WIDTH/2 - 100, HEIGHT/2], 42, 'Purple')
        start_screen1.__init__(False)
        start_screen2.complete = True
    elif player.reset_board:
        board.draw(player, canvas)
        player.draw(canvas)
        enemies.__init__()
        allies.__init__()
        #Draw the Backgrounds
        frame.set_canvas_background("Black")
        background.draw(canvas, board, player, 1)
        player.reset_board = False
        player.restart(board)
    elif player.freeze_board_wait_time != 0:
        player.freeze_board_wait_time += 1
        player.freeze_board_wait_time = player.freeze_board_wait_time % 300
        if player.freeze_board_wait_time == 0:
            gamesounds['Freeze Board'].pause()
            frame.set_canvas_background("Black")
        elif player.freeze_board_wait_time % 30 == 0:
            frame.set_canvas_background("MidnightBlue")
        elif player.freeze_board_wait_time % 15 == 0:
            frame.set_canvas_background("Black")
        Order = True
        if player.in_air or player.wait_time != 0:
            Order = player.move(WIDTH, HEIGHT, board)
        if Order:
            if enemies and len(enemies.Coily) > 0 and \
               enemies.Coily[0].offboard and enemies.Coily[0].vy > 0:
                enemies.Coily[0].draw(canvas)
            board.draw(player, canvas)
            player.draw(canvas)
        else:
            player.draw(canvas)
            if enemies and len(enemies.Coily) > 0 and \
               enemies.Coily[0].offboard and enemies.Coily[0].vy > 0:
                enemies.Coily[0].draw(canvas)
            board.draw(player, canvas)
        enemies.draw(canvas, player, board, WIDTH, BLOCK_LENGTH)
        allies.draw(canvas, player, WIDTH, BLOCK_LENGTH)
        player.collisions(WIDTH, allies, enemies, True)
        #Draw the Backgrounds
        background.draw(canvas, board, player, 1)
    else:
        if player.lives == 0: #Game Over Man, Game Over
            game_on = False
            canvas.draw_text('Game Over', [WIDTH/2 - 100, HEIGHT/2], 42, 'Purple')
            frame.set_canvas_background("MidnightBlue")
        #Get the Player Move and Status as Applicable
        Order = True
        if player.in_air:
            Order = player.move(WIDTH, HEIGHT, board, enemies, allies)
        elif player.wait_time != 0:
            Order = player.move(WIDTH, HEIGHT, board, enemies, allies, start_screen3)
        if Order:
            if enemies and len(enemies.Coily) > 0 and \
               enemies.Coily[0].offboard and enemies.Coily[0].vy > 0:
                enemies.Coily[0].draw(canvas)
            board.draw(player, canvas)
            player.draw(canvas)
        else:
            player.draw(canvas)
            if enemies and len(enemies.Coily) > 0 and \
               enemies.Coily[0].offboard and enemies.Coily[0].vy > 0:
                enemies.Coily[0].draw(canvas)
            board.draw(player, canvas)
        if not player.all_ok:
            #Generate Enemies, Update their Moves
            enemies.move(BLOCK_LENGTH, board, WIDTH, HEIGHT, player, enemies, allies)
            enemies.draw(canvas, player, board, WIDTH, BLOCK_LENGTH)
            allies.move(BLOCK_LENGTH, board, WIDTH, HEIGHT, player)
            allies.draw(canvas, player, WIDTH, BLOCK_LENGTH)
            if not player.on_spinner:
                #Check for Collisions
                player.collisions(WIDTH, allies, enemies, False)
        #Draw the Backgrounds
        background.draw(canvas, board, player, 1)

################################################################################
# INITIALIZE SIMPLEGUI AND REGISTER EVENT HANDLERS
################################################################################
# Create a frame and assign callbacks to event handlers
frame = simplegui.create_frame("Py*bert", 800, 600)
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)
frame.set_canvas_background("MidnightBlue")

# Write Instructions
frame.add_label("Game Play Instructions for Controlling Py*bert")
frame.add_label("")
frame.add_label("Downward Right Direction - M or Right Arrow Key")
frame.add_label("")
frame.add_label("Downward Left Direction - Z or Down Arrow Key")
frame.add_label("")
frame.add_label("Upward Left Direction - Q or Left Arrow Key")
frame.add_label("")
frame.add_label("Upward Right Direction - O or Up Arrow Key")

################################################################################
# Game Initiation Code
################################################################################
# Generate Start Screens
start_screen1 = Opening(True)
start_screen2 = Instructions(True)
start_screen3 = Leveltransition(WIDTH, BLOCK_LENGTH)

def init():
    player.new_game(WIDTH, start_screen3, start_screen1)
    board.Board_Colors(player.level)
    board.Set_Spinners(player.level, BLOCK_LENGTH)
    background.timer.start()
    for key in gamesounds:
        gamesounds['Spinner'].pause()

# Start the frame animation
frame.start()
