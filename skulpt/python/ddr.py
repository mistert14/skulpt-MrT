###########################################################
##
##Hey everybody! This is my stab at programming Dance Dance 
##Revolution the Coursera way. I had SO MUCH FUN building 
##this, and it turned into something that I'm really proud 
##of. There are a few rough edges, but for the most part, 
##I think it's a good reflection of what I've learned in 
##this course. (It's definitely got a better structure than
##my pendulum program (Swing State)! In any case, I hope you 
##enjoy playing it as much as I enjoyed programming it. Cheers!
##
##		Version 0.3: Added second song and choreography, 
##					restructured handling of song choice
##					Has anyone seen any knights...? 
##		Version 0.2: Added functionality for C, V, B, N keys 
##			in addition to the arrow keys. Previous functionality
##			for B now transferred to T. 
##Notes:
##    - Known bugs: 
##		- TextObjs sometimes disappear before reaching
##        their minimum size.
##		- Music fails to play on second runthrough, despite
##		"music.rewind()" in init() function.
##	  - Music loading: Sometimes it takes a while. I haven't been
##		able to fix it, and my best suggestion is just to reload
##		the page and wait longer to start next time.
##    - Legal stuff:
##        - All graphics are by me. You can use them wherever
##        you want. If you do use them, I'd love to see it - 
##        my email is wachtel.emily@gmail.com
##        - Music is by Sevish (http://sevish.com),
#			Auch von eine ganz tolle Deutsche Musikgruppe, "Kangaroo 
#    		MusiQue". (Also by a really cool German band.)
##			Licensing (both songs): Attribution-NonCommercial-ShareAlike 3.0 Unported (CC BY-NC-SA 3.0)
##        Basically, sharing is fine, selling is not. If you distribute
##			or modify the music, it must be under the same CC license.
##
##Thanks, and enjoy!
##
##Emily
##2013-06-06
############################################################
############################################################
import simplegui, math, random, urllib2
#load in media

DIR = "http://commondatastorage.googleapis.com/codeskulptor-demos/DDR_assets/"
music3 = simplegui.load_sound(DIR + "Kangaroo_MusiQue_-_The_Neverwritten_Role_Playing_Game.mp3")
music = simplegui.load_sound(DIR + "Sevish_-__nbsp_.mp3")
music2 = simplegui.load_sound(DIR + "intrmsn.wav")
source1 = urllib2.urlopen("http://mrt2.no-ip.org/skulpt/python/user16_y63HrFTkmy_0.py")
source3 = urllib2.urlopen("http://mrt2.no-ip.org/skulpt/python/user16_bS3pfWuxmW_120.py")

bkgd = simplegui.load_image(DIR + "DDRbkgd.png")
movingArrow = simplegui.load_image(DIR + "MovingArrowDoubleBorder.png")
targetArrow = simplegui.load_image(DIR + "Target.png")
splash_screen = simplegui.load_image(DIR + "SplashScreenMain.png")
splash_screen_choose = simplegui.load_image(DIR + "ChooseSong.png")
splash_screen2 = simplegui.load_image(DIR + "Splash2.png")
win_screen = simplegui.load_image(DIR + "WinScreen.png")

#set dimensions and important coordinates
CANVAS_WIDTH = 600
CANVAS_HEIGHT = 600
LX = CANVAS_WIDTH / 5.0
DX = 2*CANVAS_WIDTH / 5.0
UX = 3*CANVAS_WIDTH / 5.0
RX = 4*CANVAS_WIDTH / 5.0
targetX = [LX, DX, UX, RX] #I know this is repetitive. Experimenting with
                            #new programming styles.
tOffset = 56
TARGET_REGION = [tOffset+40, tOffset-20]
targetPos = [(LX, tOffset),(DX, tOffset), (UX, tOffset),(RX, tOffset)]

#set global variables
time = 0
stats = {'score': 0, 'missed': 0, 'perfects': 0, 'longest_run': 0, 'rows_since_miss': 0,
         'greats': 0, 'goods': 0, 'OKs': 0, 'bads':0, 'total_hits':0, 'final_stats':[]}
score = 0
splash = True
splash_choose = False
splash2 = False
choreography = []
music_on = True
time_to_next = 0
arrowSets = []
arrowVel = 1
array = [False]*4
listening = False
running = False
times_to_play = []
last_press = 0
messageArray = []

#create dictionaries
#create key dictionary (not really a dictionary, but useful for reference)
my_keys = [simplegui.KEY_MAP['left'], 
           simplegui.KEY_MAP['down'],
           simplegui.KEY_MAP['up'],
           simplegui.KEY_MAP['right']]
my_secondary_keys = [simplegui.KEY_MAP['c'],
                     simplegui.KEY_MAP['v'],
                     simplegui.KEY_MAP['b'],
                     simplegui.KEY_MAP['n']]
    
#create scoring dictionary (points:message)
scoring = {50: "Perfect!",
           25: "Great!",
           13: "Good!",
           7:"OK!",
           0: "Er...keep trying!"}

#song 1 is Sevish. Song 3 is Kangaroo Musique
song_list = [music, music3]
dance_list = [source1, source3]
dance_choice = -1
song_choice = -1

#define classes
class ArrowSet:
   'Common base class for each x4 line of arrows'
    
   def __init__(self, array):
       #takes in an array of true/false values, plus that set's time delay
            self.exposed = array[:4] #this slice separates the TF vals from the time integer
            self.exposed_copy = list(array[:4])
            self.yPos = CANVAS_HEIGHT
            self.tagged = [False]*4
            self.accuracy = [0]*4
            
   def get_exposed(self):
                   return self.exposed
   def getYpos(self):
            return self.yPos
   
   def setYpos(self, addend):
            self.yPos -= addend
                  
   def get_tagged(self):
                    return self.tagged
                
   def get_accuracy(self):
                    return self.accuracy
            
   def get_num_correct(self):
                numCorrect  = 0
                for i in range(4):
                    if self.exposed[i]==self.tagged[i]:
                        numCorrect +=1
                return numCorrect
            
   def get_time_after_me(self):
             return self.time_after_me
            
   def set_time_called(self, this_time):
                self.time_called = this_time
                
   def get_time_called(self):
                return self.time_called
            
   def set_time_after_me(self, this_time):
                self.time_after_me = this_time
   
   def get_time_to_play(self):
                    return self.time_to_play
                          
   def draw_self(self, canvas):
        for i in range(4):
            if self.exposed[i]:
                if i==0: drawLArrow(canvas,self.yPos)
                if i==1: drawDownArrow(canvas,self.yPos)
                if i==2: drawUpArrow(canvas,self.yPos)
                if i==3: drawRArrow(canvas,self.yPos)

class TextObj:
    """For drawing dynamic messages during runtime"""
    def __init__(self, words, pos, maximum, minimum, color):
        self.color_front = color
        self.color_back = "#FFFFFF"
        self.min_size = minimum
        self.max_size = maximum
        self.rate = 1
        self.curr_size = int(self.max_size)
        self.message = words
        self.pos = pos
        
    def set_message(self, words):
        self.message = words
        
    def get_message(self):
        return self.message
    
    def __str__(self):
        return self.message + " is at size " +str(self.curr_size) + "."
        
    def draw_self(self, canvas, pos):
        if self.message == "Here we go!":
            self.pos[0] = (600-frame.get_canvas_textwidth(self.message,self.curr_size))/2
        
        canvas.draw_text(self.message, self.pos, self.curr_size, self.color_back)
        canvas.draw_text(self.message, (self.pos[0]+1, self.pos[1]+1), self.curr_size, self.color_front)
        
           #decrease size before next draw round
        if self.curr_size>=self.min_size:
            self.curr_size -= self.rate
            
    def set_rate(self,new_rate):
        self.rate = new_rate
            
#methods below here are mostly in alphabetical order, except init() is 
#first and draw(canvas) is last, and the draw methods are grouped but not alphabetized.     
def init():
    """sets up new game and reinitializes all variables. TODO: modify so that you
    can also restart the game from here."""
    global time, messageArray, stats
    global splash, splash2, running

    song_list[song_choice].rewind()
    song_list[song_choice].set_volume(1)

    messageArray = []
    arrowSets = []
    for key in stats:
        stats[key] = 0
    stats['total_hits']=0
    time = 0
    longest_run = []
    read_file()
    start = ArrowSet([False, False, False, False, 1]) #63*2 = appx. an eighth note
    add_set(start)
    timer.start()
    
    song_list[song_choice].play()
    splash = False
    splash2 = False
    running = True
    messageArray.append(TextObj("Here we go!", 
                                [CANVAS_WIDTH-(frame.get_canvas_textwidth("Here we go!",100)) / 2.0 ,CANVAS_HEIGHT / 2.0], 100, 5, "Black"))
 
def add_set(next_set):
    arrowSets.append(next_set)

def centeredX(text):
    """Supposed to give an x value to start at that would center the 
    text in the parameter. I don't think it actually works."""
  
    return (CANVAS_WIDTH / 2.0 - (frame.get_canvas_textwidth(text, 100)) / 2.0)
       
def check_accuracy(offBy):
    """Receives an integer from check_keys representing the difference
    between the target Y point and the Y point at which the user pressed
    the button for a specific arrow. Returns some number of scored points."""
    global stats
    #could rewrite this to be more compact, but I'm not sure I would gain much.
    if offBy <=1:
        stats['perfects'] +=1
        return 50
    elif offBy <=4:
        stats['greats'] +=1
        return 25
    elif offBy <=12:
        stats['goods'] +=1
        return 13
    elif offBy <= 20:
        stats['OKs'] +=1
        return 7
    else:
        # "Miss!"
        stats['bads']+=1
        return 0
    
def mouse_handler(position):
    """Generally, mouse clicks dismiss splash screens. They have other
    functionality based on game state."""
    global splash, splash_choose, splash2, running, my_list, song_choice, dance_choice
    my_list = [0]
    if running: #clicking during regular gameplay is not allowed.
        return
    elif splash:
        #if we're at the home screen, switch to the choose screen
        splash_choose = True
        splash = False
    elif splash_choose and not running:
#         canvas.draw_polygon([(150, 255), (450, 255), (450, 325), (150, 325)], 2, "#297319", "81b276")
#        canvas.draw_polygon([(150, 355), (450, 355), (450, 440), (150, 440)], 2, "#ddd830", "f9f686")
        splash_choose = False
        if position[0]<450 and position[0]>150 and position[1]>255 and position[1]<325:
            song_choice = 0
            dance_choice = 0
        elif position[0]<450 and position[0]>150 and position[1]>355 and position[1]<440:
            song_choice = 1
            dance_choice = 1
        else: 
            splash_choose  = True
            return
        init()
        
    elif splash2: #if something happened to stop the game in the middle though, then it's allowed.
        splash2 = not splash2
        song_list[song_choice].play()
        timer.start()
        running = True
    elif not running and not splash2:
        #win
        splash = True
    
                
def check_keys(key):
    """Handles all key presses and some of the scoring. Depends
    on check_accuracy() for scores."""
   
    global listening, music_on, time, last_press
    
    konami(key)
    #The 'b' key can be used for choreography or debugging. It prints out the 
    #time difference between the current press and the last press.
    if key == simplegui.KEY_MAP['t']:
        print time-last_press
        last_press = time
        
    #the space bar toggles the music and the gameplay
    if key == simplegui.KEY_MAP['space']:
        music_on = not music_on
        if music_on:
            timer.start()
            song_list[song_choice].play()
        if not music_on:
            timer.stop()
            song_list[song_choice].pause()
 
    #if there are no arrows on the screen, or if no arrows are in the target range
    #then ignore key presses
    if len(arrowSets)==0 or not listening:
        return
   
    offBy = math.fabs(tOffset-arrowSets[0].getYpos()) 
   
    
    if key in my_keys: #this section courtesy of Prof. Greiner's programming tips
        this_index = my_keys.index(key)
        arrowSets[0].get_tagged()[this_index] = True
        my_score = check_accuracy(offBy)
        if arrowSets[0].get_exposed()[this_index]:
            arrowSets[0].get_exposed()[this_index] = False
            arrowSets[0].get_accuracy()[this_index] = my_score
            messageArray.append(TextObj(scoring.get(my_score), ((this_index+1)*600 / 5.0 - 5, 100), 40, 5, "Green"))
        else:
            arrowSets[0].get_accuracy()[this_index] = -(.5)*my_score       
    elif key in my_secondary_keys: #this section courtesy of Prof. Greiner's programming tips
        this_index = my_secondary_keys.index(key)
        arrowSets[0].get_tagged()[this_index] = True
        my_score = check_accuracy(offBy)
        if arrowSets[0].get_exposed()[this_index]:
            arrowSets[0].get_exposed()[this_index] = False
            arrowSets[0].get_accuracy()[this_index] = my_score
            messageArray.append(TextObj(scoring.get(my_score), ((this_index+1)*600 / 5.0 - 5, 100), 40, 5, "Green"))
        else:
            arrowSets[0].get_accuracy()[this_index] = -(.5)*my_score
def check_listening():
    """Determines whether an arrow set is within the target region. 
    Called by tick()."""
    global listening
    currYpos = arrowSets[0].getYpos()
    
    if currYpos>TARGET_REGION[0]:
        #arrow set is below target region - not listening
        listening = False
    
    elif currYpos<=TARGET_REGION[0] and currYpos>=TARGET_REGION[1]:
        #if we're in the target region, we are listening
        listening = True
    else:
        #we're past the target region. Not listening
        listening = False
        
def drawLArrow(canvas, start):
    canvas.draw_image(movingArrow, [31,31], [63,63], [LX,start],[70,70])
    
def drawUpArrow(canvas, start):
    canvas.draw_image(movingArrow, [31,31], [63,63], [UX, start], [70,70], math.pi/2)
      
def drawDownArrow(canvas, start):
    canvas.draw_image(movingArrow, [31,31], [63,63], [DX, start], [70,70], -math.pi/2)
    
def drawRArrow(canvas, start):
    canvas.draw_image(movingArrow, [31, 31], [63,63], [RX, start], [70,70], math.pi)
        
def drawTargets(canvas):
    
    #draw left 
    canvas.draw_image(targetArrow, [31,31], [63,63], [LX,tOffset],[70,70])
    
    #draw up
    canvas.draw_image(targetArrow, [31,31], [63,63], [UX, tOffset], [70,70], math.pi/2)
    
    #draw down
    canvas.draw_image(targetArrow, [31,31], [63,63], [DX, tOffset], [70,70], -math.pi/2)
    
    #draw right
    canvas.draw_image(targetArrow, [31, 31], [63,63], [RX, tOffset], [70,70], math.pi)

def end_game():
    """Called by tick() when there are no more arrows. Calculates final accuracy stats
    and triggers display of win screen."""
    global splash, running, stats, song_choice
    song_list[song_choice].pause()
    running = False
    stats['final_stats']={}
    stats['total_hits'] = stats['perfects']+stats['greats']+stats['goods']+stats['OKs']+stats['bads']
    if stats['total_hits']==0:
        stats['total_hits']=1 #to make the math below work if there aren't any hits.
        stats['longest_run']=0
    
    for key in stats:
        if key in ['perfects','greats','goods','OKs','bads']:
            percentage = (((stats[key] / float(stats['total_hits']))* 10000)//1)/100
            stats['final_stats'][key]=percentage
            
    if stats['longest_run']==0 and stats['missed'] ==0:
        stats['longest_run'] = len(choreography) #length of choreography
    song_list[song_choice].rewind()
    song_choice = -1
    
def eval_round():
    """Takes in info about the topmost arrow set and determines score, stats, 
    and combos. Called by tick()."""
    global combos, missed, stats
    num_correct = 0
    for i in range(4):
        
        if arrowSets[0].get_tagged()[i]==arrowSets[0].exposed_copy[i]:
            num_correct += 1
   
    if True in arrowSets[0].get_exposed():
        #if there are any arrows left showing by the time the set exits the target region
        #subtract some number of points per arrow
        stats['score'] -=25*arrowSets[0].get_exposed().count(True)
        if stats['rows_since_miss']>stats['longest_run']:
            stats['longest_run'] = stats['rows_since_miss']
        stats['rows_since_miss']=0
       
        for i in range(len(arrowSets[0].get_exposed())):
            if arrowSets[0].get_exposed()[i]:
                messageArray.append(TextObj("Miss!", ((i+1)*CANVAS_WIDTH / 5.0, 100), 45, 5, "Red"))
                stats['missed'] +=1
    else: stats['rows_since_miss']+=1
        
    if stats['rows_since_miss']%10 ==0 and not stats['rows_since_miss'] == 0: 
        stats['score']+=50
        messageArray.append(TextObj(str(stats['rows_since_miss'])+ " combos!", [180,205], 60,5,"Blue"))
        messageArray[-1].set_rate(0.5)
        
    #accuracy is set in check_keys. 
    for element in arrowSets[0].get_accuracy():
        stats['score'] += element
    
def gen_new_set(): 
    """UNUSED. Generates a random set of arrows."""
    arrowSets.append(ArrowSet(gen_random_arrows()))
    
list_of_stuff = [38,38,40,40,37,39,37,39,66,65] 
my_list = [0]
def konami(key):
    """Do some stuff here."""
    global my_list, splash2, running
    my_list.append(key)
    count = 0
    if not running:
        return
    
    if len(my_list) > 10:
        my_list.pop(0)
        
        for i in range(10):
            if my_list[i] == list_of_stuff[i]: 
                count+=1
    
    if count == 10: 
        splash2 = True
        running = False
        timer.stop()
        song_list[song_choice].pause()
        music2.play()
        #gameplay resumes on mouse click. See mouse_handler.
    
def next_from_file():
    """Takes the "bottommost" arrow set and puts it into the 
    array that is displayed by the draw handler."""
    global game_over, choreography, next_time
    if len(choreography)>0:
        #add the next arrow set from the text file
        add_set(ArrowSet(choreography.pop(0)))
    else:
        game_over = True
        
def read_file():
    """Takes text file from URL (currently a codeskulptor file) and 
    separates the text into sets of 4 truth values and one integer in 
    milliseconds."""
    global choreography, times_to_play, dance_choice
    
    print dance_list, dance_choice, dance_list[dance_choice]
    source = dance_list[dance_choice].read()
    
    source = list(source.split('\r\n'))
    time_count = []
    
    
    for i in range(len(source)):
        next_list = []
        if source[i] == "":
            continue
        arrows = source[i][:4]
        
        if dance_choice == 0:
            multiplier = 1
        elif dance_choice == 1:
            multiplier = 0.99
            
        time_val = multiplier*(int)(source[i][4:])
        
        
        for j in range(4):
            if arrows[j] == 'T':
                next_list.append(True)
            else:
                next_list.append(False)
        next_list.append(int(time_val))
        time_count.append(int(time_val))
        choreography.append(next_list)
        
    
    for i in range(len(time_count)):
        times_to_play.append(sum(time_count[0:i])) 
        #times are absolute, not relative
        
        
    times_to_play[0] = 55 #magic number. This is a placeholder - its value doesn't mean anything.
    
def remove_topmost_set():
    """Removes the set closest to the target region."""
    arrowSets.pop(0)
    
def tick():
    """Increments time, contains logic to end game. Also calls functions to:
    - queue arrow sets at the appropriate time
    - toggle receptivity of key handler
    - update all arrow positions"""
    global time, times_to_play, last_press
    time +=1
    
    
    if len(times_to_play)==0:
        trigger = 10000000000000 # Very large magic number! So far unable to eliminate.
        
    else:
        trigger = times_to_play[0]
        
    
    if len(arrowSets)==0:
        timer.stop()
        song_list[song_choice].set_volume(0)
        end_game()
        return

    if time == trigger:
        next_from_file()
        times_to_play.pop(0) 
    
    #loop through all displayed arrows and move them upward
    update_arrow_sets()
        
    #set global variable "listening" if the topmost arrowSet
    #is within the target region
    check_listening()
    
                                 
    if arrowSets[0].getYpos()<TARGET_REGION[1]:
        eval_round()
        remove_topmost_set()
     
def update_arrow_sets():
    """Advances each arrow set in the set of arrow sets."""
    for aSet in arrowSets:
        aSet.setYpos(arrowVel)
         
def draw(canvas):
    #draw the background
    if splash: #start splash screen
        canvas.draw_image(splash_screen, (300,300), (600,600), (300,300), (600,600))
    elif splash_choose:
        canvas.draw_image(splash_screen_choose, (300,300), (600,600), (300,300), (600,600))
        canvas.draw_polygon([(150, 255), (450, 255), (450, 325), (150, 325)], 2, "#297319", "81b276")
        canvas.draw_polygon([(150, 355), (450, 355), (450, 440), (150, 440)], 2, "#ddd830", "f9f686")
        canvas.draw_text("'Untitled'", (170, 280), 20, "Black", "monospace")
        canvas.draw_text("by Sevish", (170, 310), 12, "Black", "monospace")
        canvas.draw_text("'The Neverwritten Role", (170, 380), 20, "Black", "monospace")
        canvas.draw_text("Playing Game'", (170, 400), 20, "Black", "monospace")
        canvas.draw_text("by Kangaroo MusiQue", (170, 430), 12, "Black", "monospace")
    elif not running and not splash2: #game over, win screen
        font_size = 20
        start = 220
        spacer = 20
        canvas.draw_image(win_screen, (300,300), (600,600), (300,300), (600,600))
        canvas.draw_text("Score:                " + str(int(stats['score'])), (160,220), font_size, "Black", 'monospace')
        canvas.draw_text("Arrows missed:        " + str(stats['missed']), (160,start+spacer), font_size, "Black", 'monospace')
        canvas.draw_text("Perfect hits:         " + str(stats['perfects']), (160,start+2*spacer), font_size, "Black", 'monospace')
        canvas.draw_text("Longest run:          " + str(stats['longest_run']), (160, start+3*spacer), font_size, "Black", 'monospace')
        canvas.draw_text("Accuracy:  ", (160, start+5*spacer), font_size, "Black", 'monospace')
        canvas.draw_text("Perfect:          "+str(stats['final_stats']['perfects']) + "%", (190, start+ 6*spacer), font_size-6, "Black", 'monospace')
        canvas.draw_text("Great:            "+str(stats['final_stats']['greats']) + "%", (190, start+ 7*spacer), font_size-6, "Black", 'monospace')
        canvas.draw_text("Good:             "+str(stats['final_stats']['goods']) + "%", (190, start+ 8*spacer), font_size-6, "Black", 'monospace')
        canvas.draw_text("OK:               "+str(stats['final_stats']['OKs']) + "%", (190, start+ 9*spacer), font_size-6, "Black", 'monospace')
        canvas.draw_text("Really bad:       " + str(stats['final_stats']['bads']) + "%", (190, start+10*spacer), font_size-6, "Black", 'monospace')
    else: #runtime
        canvas.draw_image(bkgd, (300,300), (600,600), (300, 300), (600,600))
        drawTargets(canvas)
        canvas.draw_text("Score: " + str(int(stats['score'])), (475,595), 20, "White")
    
    #draw all the arrows that have been added to the list of visible arrows
    for i in range(len(arrowSets)):
        arrowSets[i].draw_self(canvas)
        
    if splash2:
        canvas.draw_image(splash_screen2, (300,300), (600,600), (300,300), (600,600))
        canvas.draw_text("Click to resume.", (440,590), 15, "Black", 'monospace')
        
    #draw whatever message is appropriate
    for i in range(len(messageArray)):
        messageArray[i].draw_self(canvas, (300,300))
    
    #combine these two for loops for efficency after debugging
    for i in range(len(messageArray)):
        #remove messages that have reached their minimum size.
        #doing this sequentially because removing both at once was 
        #giving me a headache.
        
        if messageArray[0].curr_size == messageArray[0].min_size:
            messageArray.pop()
            
  
# Create a frame and assign callbacks to event handlers
frame = simplegui.create_frame("DDR", CANVAS_WIDTH, CANVAS_HEIGHT)
timer = simplegui.create_timer(10, tick)
frame.set_draw_handler(draw)
frame.set_keydown_handler(check_keys)
frame.set_mouseclick_handler(mouse_handler)

#frame.add_button("New set", gen_new_set)
#frame.add_button("Read from file", read_file)



# Start the frame animation
frame.start()

