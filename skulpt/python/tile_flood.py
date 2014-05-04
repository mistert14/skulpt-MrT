#########################
#						#
#	  	Tile Flood		#
#						#
#########################

#����������������������������
# Version		: 0.4
# Author		: Sergey Efimov
# Email			: efimovsn@gmail.com
# Start date	: 20 May 2013
# Last modified	: 11 June 2013
#����������������������������

#���� Contributors ����������
# Helder Sepulveda:
# � Solved the problem with the lucky restart.
# � Added the great animation.
#����������������������������

#���� Previous versions �����
# v0.3: http://www.codeskulptor.org/#user15_irffeNIZpYqmFLu_15.py
# v0.2: http://www.codeskulptor.org/#user14_irffeNIZpYqmFLu_8.py
# v0.1: http://www.codeskulptor.org/#user14_Jxp4c6tg0v2xxKX_21.py
#����������������������������

#---------- Rules ---------------------------------------
# The object of Tile Flood is to flood all tiles in field
# with one color by using as few turns as possible.
#
# Change the color of the tile in the top-left corner
# to one of adjacent colors, by tapping on one 
# of the 6 colored buttons at the bottom.
# Adjacent tiles with the same color will be flooded.
#--------------------------------------------------------

import math
import simplegui
from random import randrange

color_scheme_inc = 0
difficulty_inc = 1

# constans
WIDTH = 364
HEIGHT = 514
MARGIN_TOP = 50



COLOR_SCHEMES = {'Standart' : ["#5E0D4E","#BD1550","#E97F02","#F8CA00","#8A9B0F","#008888"],
                 'Ocean': ["#001449","#012677","#005BC5","#00B4FC","#17F9FF","#18d5a6"],
                 'Ololo': ["#3B8C88","#F0DDAA","#E47C5D","#E32D40","#152B3C","#668C4D"],
                 'Influenza': ["#410030","#592248","#741958","#C04848","#F07241","#FF9D29"],
                 'Another': ["#004972","#00865A","#A5CF10","#F7CF10","#F76110","Sienna"]}
BUTTON_WIDTH = 44
BUTTON_HEIGHT = 74
BUTTON_START_X = 14
BUTTON_START_Y = MARGIN_TOP * 2 + WIDTH

AREA = [[2, 50], [362, 50], [362, 410], [2, 410]]


# globals
animate = False
record = 3600
record_time = 3600
tile_colors = COLOR_SCHEMES[COLOR_SCHEMES.keys()[color_scheme_inc]]

# ---------------------- helper functions --------------------------

def format_time(t):
    """converts time in seconds into formatted string min:sec"""
    mili = t % 10
    ti = t // 10
    min = ti // 60
    sec = ti % 60
    return '%d:%0.2d.%d' % (min, sec, mili)

def format_score(score):
    """ formats score into string score/max turns"""
    return '%2d/%d' % (score, max_turns)

def format_record(record, time):
    """formats record and time into string 'record \n time' """
    return '%d turns in %s ' % (record, format_time(time))

def calc_area(center, width, height):
    """returns list of corners of rectangle"""
    a = [center[0] - width/2, center[1] - height/2]
    b = [center[0] + width/2, center[1] - height/2]
    c = [center[0] + width/2, center[1] + height/2]
    d = [center[0] - width/2, center[1] + height/2]
    return [a,b,c,d]

def point_inside_rect(point,rect):
    """returns True if point inside rectangle"""
    if point[0] > rect[0][0] and point[0] < rect[1][0] and point[1] > rect[0][1] and (point[0] < rect[3][1]):
        return True
    else:
        return False

def point_inside_list_of_rect(point,list_of_rect):
    """returns index of rectangle if the point inside one of rectangles
    else return None """
    i = 0
    for rect in list_of_rect:
        if point_inside_rect(point,rect):
            return i
        else:    
            i +=1
    return None

def find_neighbors(tiles):
    """Add neighbors tiles in tiles neighbors atribute"""
    bottom_count = tiles_count**2 - tiles_count
    for i in range(len(tiles)):
        neighbors_indexes = []
        if i >= tiles_count:					# have bottom neighbor
            neighbors_indexes.append(i - tiles_count)
        if i < bottom_count:					# have top neighbor
            neighbors_indexes.append(i + tiles_count)
        if i % tiles_count != 0:				# have left neighbor
            neighbors_indexes.append(i - 1)
        if i % tiles_count != tiles_count-1:	# have right neighbor
            neighbors_indexes.append(i + 1)				
        
        neighbors = []
        for index in neighbors_indexes:
            neighbors.append(tiles[index])
        tiles[i].neighbors = neighbors # add neighbors (instances of the Tile class) for each tile  
    
    
def find_clusters(tiles):
    """Cuts the field to clusters"""
    global clusters
    cluster_number = 0
    clusters = []
    for tile in tiles:
        
        if not tile.in_cluster:
            cluster = [tile] # add tile to cluster
            tile.just_found = True
            tile.in_cluster = True
            tile.cluster_number = cluster_number
            same_color_neighbors_found = True
            while same_color_neighbors_found:
                same_color_neighbors_found = False
                just_found_list = [t for t in cluster if t.just_found]  # to reduce loop items
                for t in just_found_list:
                    t.just_found = False
                    for neighbor in t.neighbors:
                        if not neighbor.in_cluster:
                            if t.color == neighbor.color:
                                cluster.append(neighbor) # add neighbor to cluster
                                neighbor.just_found = True
                                neighbor.in_cluster = True
                                neighbor.cluster_number = cluster_number
                                same_color_neighbors_found = True
            clusters.append(cluster)
            cluster_number += 1
    
    
def fill_cluster(cluster):
    for tile in cluster:
        tile.filled = True
        
                    
def fill_clusters(tiles,color):
    filled_tiles = [tile for tile in tiles if tile.filled]
    for tile in filled_tiles:
        for neighbor in tile.neighbors:
            if not neighbor.filled and neighbor.color == color:
                fill_cluster(clusters[neighbor.cluster_number])
                

    filled_tiles = [tile for tile in tiles if tile.filled]
    for tile in filled_tiles:
        tile.color = color
    
       

def has_unfilled_tiles(tiles):
    """True if the frame has unfilled tiles"""
    for tile in tiles:
        if not tile.filled:
            return True
    return False
    
    
    
# ---------------------- Classes --------------------------
# Tile class
class Tile:
    def __init__(self, index, center, color, size, filled = False):
        self.index = index
        self.color = color
        self.center = center
        self.size = size
        self.filled = filled
        self.mid_left = [self.center[0] - self.size/2, self.center[1]]
        self.mid_right = [self.mid_left[0] + self.size, self.center[1]]
        self.just_found = False
        self.just_filled = False
        self.in_cluster = False
        
        
    
    def fill(self):
        if self.filled != True:
            self.filled = True
 
    def setColor(self,color):
        self.color = color
        
    def draw(self, canvas):
        canvas.draw_line(self.mid_left, self.mid_right, self.size, tile_colors[self.color])
      
# Button class        
class Button:
    def __init__(self, index, center, color, width = BUTTON_WIDTH, height = BUTTON_HEIGHT):
        self.index = index
        self.center = center
        self.width = width
        self.height = height
        self.color = color
        self.area = calc_area(self.center, self.width, self.height)
    
    def draw(self, canvas, inc):
        area = self.area
        if inc != 0:
            area = calc_area(self.center, self.width + inc, self.height + inc)
        canvas.draw_polygon(area, 1, "White", tile_colors[self.color])

        
# Difficulty class
class Difficulty:
    def __init__(self,name, tiles_count, max_turns, lucky_clusters_count):
        self.name = name
        self.tiles_count = tiles_count
        self.max_turns = max_turns
        self.lucky_clusters_count = lucky_clusters_count
        self.record = self.max_turns
        self.record_time = 10000
        self.record_header = None
        self.record_label = None
        

easy = Difficulty("Easy",6, 10, 20)
medium = Difficulty("Medium",12,22,88)
hard = Difficulty("Hard",18,34, 210)
extreme = Difficulty("Extreme", 30, 56, 710)
sparta = Difficulty("SPARTA!!!",60,110,2800)

difficulties = [easy, medium, hard, extreme, sparta]
difficulty = difficulties[difficulty_inc]

        # ---------------------- event handlers --------------------------

def new_game():
    """reset globals, init tiles and buttons"""
    global tiles, buttons, turn, time, last_filled_color, end_game_message, tiles_count, max_turns
    restart_animation()
    # reset globals
    turn = 0
    time = 0
    last_filled_color = None
    end_game_message = ''
    timer.stop()
    
    tiles_count = difficulty.tiles_count
    max_turns = difficulty.max_turns
    tile_size = (AREA[1][0] - AREA[0][0]) // tiles_count
    
    # init tiles
    tiles = [] 
    for j in range(tiles_count):
        for i in range(tiles_count):
            tile_center = [2 + (i + 0.5) * tile_size, MARGIN_TOP + (j + 0.5) * tile_size]
            tile_color = randrange(0,6)
            tiles.append(Tile([i, j], tile_center, tile_color, tile_size))
        
    
    # init buttons
    buttons = [Button(i, [BUTTON_START_X * (i+1) + (i + 0.5) * BUTTON_WIDTH,  BUTTON_START_Y], i) for i in range(6)]    
            
    # find neighbor tiles for all tiles
    find_neighbors(tiles)
    
    # find same-color neighbor tiles for all tiles
    find_clusters(tiles)
       
    # fill top-left tile
    tiles[0].fill()
    
    # fill adjacent tiles for top-left tile
    fill_clusters(tiles,tiles[0].color)
    
    last_filled_color = tiles[0].color

# Animate the buttons after some time of inactivity
def tick_animate_buttons():
    global animate
    animate = True

def restart_animation():
    global animate
    animate = False
    timer_animate_buttons.stop()
    timer_animate_buttons.start()
    
def tick_new_lucky_game():
    """Restarts the game until clusters will not decrease """
    new_game()
    clusters_count = len(clusters)
    if clusters_count <= difficulty.lucky_clusters_count:
        timer_new_lucky_game.stop()

def new_lucky_game():    
    timer_new_lucky_game.start()
    
def change_difficulty():
    """ Increments difficulty_inc and starts new game"""
    global difficulty_inc, difficulty
    difficulty_inc = (difficulty_inc + 1)% len(difficulties)
    difficulty = difficulties[difficulty_inc]
    difficulty_button.set_text(difficulty.name)
    new_game()    

# change color button handler
def change_color_scheme():
    global tile_colors, color_scheme_inc
    restart_animation()
    color_scheme_inc = (color_scheme_inc + 1) % len(COLOR_SCHEMES.keys())
    
    tile_colors = COLOR_SCHEMES[COLOR_SCHEMES.keys()[color_scheme_inc]]
    change_color_button.set_text(COLOR_SCHEMES.keys()[color_scheme_inc])
    
# timer handler
def tick():
    global time
    time += 1    
    
# draw handler 
def draw(canvas):
    # draw time
    canvas.draw_text(format_time(time), [15, 32], 26, "White") 
    
    # draw score
    canvas.draw_text(format_score(turn),[WIDTH - 68, 32], 26, "White") 
    
    # draw the frame
    canvas.draw_polygon(AREA, 4, "White") 
    
    # draw tiles
    for tile in tiles:
        tile.draw(canvas)
            
    # draw buttons
    for button in buttons:
        increase = 0
        if animate:
            if randrange(0,6) == 0:
                increase = math.sin(time/5)*3
        button.draw(canvas, increase)
        
    # draw endgame message
    canvas.draw_text(end_game_message, [70, HEIGHT/2 - 20], 60, "White")
    
# mouseclick handler 
def click(position):
    global turn, last_filled_color, end_game_message
    # restart the animation timer
    restart_animation()
    if turn < max_turns:
        #start the timer
        if turn < 1:
            timer.start()
        
        # find on what button player clicked   
        color_of_clicked_button = point_inside_list_of_rect(position, [button.area for button in buttons])
        
        # fill neighbors if button is clicked
        if color_of_clicked_button != None and color_of_clicked_button != last_filled_color:
            fill_clusters(tiles,color_of_clicked_button)
            last_filled_color = color_of_clicked_button                        
            turn += 1
            
        # check for end game
        if not has_unfilled_tiles(tiles):
            timer.stop()
            if turn < difficulty.record or (turn == difficulty.record and time < difficulty.record_time):
                end_game_message = ' Record!'
                difficulty.record = turn
                difficulty.record_time = time
                
                if difficulty.record_header == None:
                    difficulty.record_header = frame.add_label('%s:' % difficulty.name)
                    difficulty.record_label =frame.add_label(format_record(difficulty.record, difficulty.record_time))
                else:                    
                    difficulty.record_header.set_text('%s:' % difficulty.name)
                    difficulty.record_label.set_text(format_record(difficulty.record, difficulty.record_time))
                
                    
            else:
                end_game_message = 'You win!'
        else:
            if turn == max_turns:
                timer.stop()
                end_game_message = 'You lose!'
           
# create frame
frame = simplegui.create_frame("Tile flood", WIDTH, HEIGHT, 120)

frame.set_draw_handler(draw)
frame.set_mouseclick_handler(click)

timer = simplegui.create_timer(100, tick)
timer_new_lucky_game = simplegui.create_timer(50, tick_new_lucky_game)
timer_animate_buttons = simplegui.create_timer(3000, tick_animate_buttons)

restart_button = frame.add_button('Restart', new_game, 120)

frame.add_label('')
lucky_button = frame.add_button('Lucky restart', new_lucky_game, 120)
frame.add_label('')
frame.add_label('')
frame.add_label('Game difficulty:')
difficulty_button = frame.add_button(difficulty.name, change_difficulty, 120)
frame.add_label('')
frame.add_label('Color scheme:')
change_color_button = frame.add_button(COLOR_SCHEMES.keys()[color_scheme_inc],change_color_scheme, 120)
frame.add_label('')
frame.add_label('--- RECORDS ---')

# start frame and new game
timer_animate_buttons.start()
frame.start()
new_game()

#---------- To Do ----------------------------
# 1. Levels (easy, medium, hard)	+ 
# 2. More color schemes				+
# 3. Records table					+
# 4. Music and sounds
# 5. Lucky button					+
#---------------------------------------------
    
