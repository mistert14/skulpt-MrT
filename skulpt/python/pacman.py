# Lawrence Strickland
# 11/04/12
# PyMan game (Pacman style game)


import random
import simplegui
import math
import time

BASE_DIR = "http://commondatastorage.googleapis.com/codeskulptor-demos/pyman_assets/"
board=[]
enemies={}
player={}

def reset_everything():
    global enemies, player
    enemies={
    'rixner':{'cur_direction':simplegui.KEY_MAP["left"], 'last_direction':simplegui.KEY_MAP["right"], 'speed':32, 'state':1, 'static_target':(25*16,0), 'mode':'scatter', 'backup_mode':'scatter', 'target':(0,0), 'color':'Red', 'in_slow_zone':False, 'out_of_gate':0, 'out_of_gate_timer':0, 'time_counter':0},
    'warren':{'cur_direction':simplegui.KEY_MAP["left"], 'last_direction':simplegui.KEY_MAP["right"],'speed':32, 'state':1, 'static_target':(2*16,0), 'mode':'scatter', 'backup_mode':'scatter', 'target':(0,0), 'color':'Pink', 'in_slow_zone':False, 'out_of_gate':0, 'out_of_gate_timer':0, 'time_counter':0},
    'greiner':{'cur_direction':simplegui.KEY_MAP["right"], 'last_direction':simplegui.KEY_MAP["left"],'speed':32, 'state':1, 'static_target':(27*16,34*16), 'mode':'housed', 'backup_mode':'housed', 'target':(192,280), 'color':'#00FFFF', 'in_slow_zone':False, 'out_of_gate':140, 'out_of_gate_timer':0, 'time_counter':0},
    'wong':{'cur_direction':simplegui.KEY_MAP["left"], 'last_direction':simplegui.KEY_MAP["right"],'speed':32, 'state':1, 'static_target':(0,34*16), 'mode':'housed', 'backup_mode':'housed', 'target':(256,280), 'color':'Orange', 'in_slow_zone':False, 'out_of_gate':280, 'out_of_gate_timer':0, 'time_counter':0},
    }
    player={
    'lives':3,
    'pellets_eaten':0,
    'powered_up':False,
    'score':0,
    'in_slow_zone':False,
    'in_intro':True,
    'level':0,
    'edibles':[0,0,0,0,0,0,0],
    'edible_available':0,
    'max_speed':22.6,
    'speed':28.25,
    'power_pellet_time':9000,
    'game_over':False,
    'enemies_eaten':0,
    'extra_life_score':10000,
    'enter_initials':False,
    'initials':[0,1,2],
    'underscore_pos':0,
    'underscore_enabled':True,
    'game_id':time.time(),
    'mode':'play',
    'count':[0,0,0,[0,0,0,0]],
    'submit_score':0
    }

reset_everything()
player['mode']='test'

point_displays={}

directions={simplegui.KEY_MAP["up"]:[90,0,-4,1], simplegui.KEY_MAP["down"]:[90,0,4,0], simplegui.KEY_MAP["right"]:[0,4,0,0], simplegui.KEY_MAP["left"]:[0,-4,0,1]}
directions_ordered_for_enemies=[simplegui.KEY_MAP["up"],simplegui.KEY_MAP["left"],simplegui.KEY_MAP["down"],simplegui.KEY_MAP["right"]]
opposite_directions={simplegui.KEY_MAP["up"]:simplegui.KEY_MAP["down"], simplegui.KEY_MAP["down"]:simplegui.KEY_MAP["up"], simplegui.KEY_MAP["right"]:simplegui.KEY_MAP["left"], simplegui.KEY_MAP["left"]:simplegui.KEY_MAP["right"]}
current_direction=simplegui.KEY_MAP["left"]
current_key_pressed={simplegui.KEY_MAP["left"]:False, simplegui.KEY_MAP["right"]:False, simplegui.KEY_MAP["up"]:False, simplegui.KEY_MAP["down"]:False}
level_changes=[1,2,5,21,99999999]
base_url="http://www.sitehacks.com/pyman/index.php?name="
url=[base_url+"&score=0&"+str(time.time()),base_url+"&score=0&"+str(time.time())]
dirs={simplegui.KEY_MAP["up"]:"up", simplegui.KEY_MAP["down"]:"down", simplegui.KEY_MAP["right"]:"right", simplegui.KEY_MAP["left"]:"left"}


def genURL():
    global url, player
    if player['submit_score']==0:
        player['underscore_enabled']=True
        underscore_timer.start()
    else:
        player['underscore_enabled']=False
        underscore_timer.stop()
    url[1]=url[0]
    temp=base_url
    for i in player['initials']:
        temp+=str(i)+","
    temp+="&id="+str(player['game_id'])
    temp+="&score="+str(player['score'])
    temp+="&c="+str(player['count'][0])+","+str(player['count'][1])+","+str(player['count'][2])+","+str(player['count'][3][0])+","+str(player['count'][3][1])+","+str(player['count'][3][2])+","+str(player['count'][3][3])+","+str(player['level'])
    temp+="&s="+str(player['submit_score'])
    url[0]=temp




def draw(canvas):
    background = simplegui.load_image(BASE_DIR + "board.gif")
    canvas.draw_image(background, (225, 289), (450,578), (225,289), (450,578))
    #canvas.draw_text("PyMan", [10,40], 36, "#ff2b97")
    canvas.draw_text("SCORE: "+str(player['score']), [300,20], 16, "White")
    if player['level']==0:
        canvas.draw_text("LEVEL: 1", [306,44], 16, "White")
    else:
        canvas.draw_text("LEVEL: "+str(player['level']), [306,44], 16, "White")


    '''for i in range(0):#36
        canvas.draw_line((0,i*16), (448,i*16), 1, "#00FF00")
    for i in range(28):#28
        #canvas.draw_line((i*16,0), (i*16,576), 1, "#00FF00")
        for j in range(36):
            if board[i][j]==1:
                canvas.draw_circle((i*16+8,j*16+8), 2, 1, "White", "White")
            elif board[i][j]==2:
                canvas.draw_circle((i*16+8,j*16+8), 4, 1, "Yellow", "Yellow")
            elif board[i][j]==9:
                canvas.draw_polygon([(i*16,j*16+7), (i*16,j*16+11), (i*16+16,j*16+11), (i*16+16,j*16+7)], 2, "Pink", "Pink")'''


    #blackout dots eaten, it's more efficient than drawing every dot, lag wise
    for j in range(4,33):
        blackout_range=0
        for i in range(1,28):
            #if board[i][j]==-2:
            #    canvas.draw_polygon([((i-blackout_range)*16,j*16), ((i-blackout_range)*16,j*16+16), (i*16,j*16+16), (i*16,j*16)], 1, "Yellow", "Yellow")
            #if board[i][j]==13:
            #    canvas.draw_polygon([((i-blackout_range)*16,j*16), ((i-blackout_range)*16,j*16+16), (i*16,j*16+16), (i*16,j*16)], 1, "Yellow", "Yellow")
            if board[i][j]==-1 or board[i][j]==-2:
                blackout_range+=1
            else:
                if blackout_range!=0:
                    canvas.draw_polygon([((i-blackout_range)*16,j*16), ((i-blackout_range)*16,j*16+16), (i*16,j*16+16), (i*16,j*16)], 1, "Black", "Black")
                    blackout_range=0

#            elif board[i][j]==3:
#                canvas.draw_polygon([(i*16+6,j*16), (i*16+10,j*16), (i*16+10,j*16+16), (i*16+6,j*16+16)], 2, "#3366FF", "#3366FF")
#            elif board[i][j]==4:
#                canvas.draw_polygon([(i*16,j*16+6), (i*16,j*16+10), (i*16+16,j*16+10), (i*16+16,j*16+6)], 2, "#3366FF", "#3366FF")
#            elif board[i][j]==5:
#                canvas.draw_polygon([(i*16+7,j*16+15), (i*16+11,j*16+15), (i*16+15,j*16+11), (i*16+15,j*16+7)], 2, "#3366FF", "#3366FF")
#            elif board[i][j]==6:
#                canvas.draw_polygon([(i*16+1,j*16+7), (i*16,j*16+10), (i*16+6,j*16+16), (i*16+10,j*16+15)], 2, "#3366FF", "#3366FF")
#            elif board[i][j]==7:
#                canvas.draw_polygon([(i*16+7,j*16+1), (i*16+10,j*16), (i*16+16,j*16+6), (i*16+15,j*16+10)], 2, "#3366FF", "#3366FF")
#            elif board[i][j]==8:
#                canvas.draw_polygon([(i*16,j*16+6), (i*16+1,j*16+10), (i*16+10,j*16+1), (i*16+6,j*16+0)], 2, "#3366FF", "#3366FF")

    #canvas.draw_polygon([(210,314), (238,314), (238,344), (210,344)], 1, "#444444", "#444444")
    if player['edible_available'] in (1,3):
        image = simplegui.load_image(BASE_DIR + "edibles.png")
        canvas.draw_image(image, (14+(((player['level']-1)%7)*28), 14), (28,28), (224,328), (20,20))
    #points text
    #canvas.draw_polygon([(176,240), (280,240), (280,312), (176,312)], 1, "Yellow", "Yellow")

    for i in sprites:
        if sprites[i]['enabled']:
            sprites[i]['image'] = simplegui.load_image(BASE_DIR+sprites[i]['url'])
            if i=='pyman':
                canvas.draw_image(sprites[i]['image'], ((sprites[i]['original_frame_width']/2)+(sprites[i]['cur_frame']*sprites[i]['original_frame_width']),((sprites[i]['original_frame_height']/2)+(sprites[i]['original_frame_height']*sprites[i]['height_offset']))), (sprites[i]['original_frame_width'],sprites[i]['original_frame_height']), (sprites[i]['pos_x']+3,sprites[i]['pos_y']+1), (sprites[i]['scaled_frame_width'],sprites[i]['scaled_frame_height']), sprites[i]['rotation_in_degrees']*0.0174532925)
            else:
                canvas.draw_image(sprites[i]['image'], ((sprites[i]['original_frame_width']/2)+(sprites[i]['cur_frame']*sprites[i]['original_frame_width']),((sprites[i]['original_frame_height']/2)+(sprites[i]['original_frame_height']*sprites[i]['height_offset']))), (sprites[i]['original_frame_width'],sprites[i]['original_frame_height']), (sprites[i]['pos_x']+3,sprites[i]['pos_y']), (sprites[i]['scaled_frame_width'],sprites[i]['scaled_frame_height']), sprites[i]['rotation_in_degrees']*0.0174532925)
    for i in range(0,player['lives']-1):
        if i<10:
            #print ((sprites['pyman']['original_frame_width']/2)+(2*sprites['pyman']['original_frame_width']),(sprites['pyman']['original_frame_height']/2))
            canvas.draw_image(sprites['pyman']['image'], ((sprites['pyman']['original_frame_width']/2)+(2*sprites['pyman']['original_frame_width']),(sprites['pyman']['original_frame_height']/2)), (sprites['pyman']['original_frame_width'],sprites['pyman']['original_frame_height']), (16+(i*22),558), (20,20), 0*180*0.0174532925)
    #canvas.draw_circle((sprites['pyman']['pos_x'], sprites['pyman']['pos_y']), 8*16, 2, "Orange")
    #canvas.draw_circle((sprites['pyman']['pos_x']+(directions[current_direction][1]*8), sprites['pyman']['pos_y']+(directions[current_direction][2]*8)), 8, 2, "#00FFFF", "#00FFFF")

    for i in range(7):
        if player['edibles'][i]==0:
            canvas.draw_polygon([(252+(i*28),544), (252+(i*28),576), (280+(i*28),576), (280+(i*28),544)], 1, "Black", "Black")
        elif player['edibles'][i]>1:
            canvas.draw_text("x"+str(player['edibles'][i]), [252+14+(i*28),576], 7, "White")
    
    if player['in_intro']:
        canvas.draw_text("READY!", [186,337], 20, "Yellow")
    elif player['game_over']:
        canvas.draw_text("GAME OVER!", [153,337], 20, "Yellow")
    
    #draw points displayed for eating things
    for i in point_displays:
        canvas.draw_text(str(point_displays[i]['value']), [point_displays[i]['pos_x']-10, point_displays[i]['pos_y']+4], 8, "Yellow")
        #canvas.draw_text("100", [214,332], 8, "Yellow")
        
    
    if player['mode']=='test':
        image = simplegui.load_image(url[1])
        canvas.draw_image(image, (112, 136), (224,272), (128+112-16,160+136-16), (224,272))
        image = simplegui.load_image(url[0])
        canvas.draw_image(image, (112, 136), (224,272), (128+112-16,160+136-16), (224,272))
        if player['mode']=='test':
            for i in range(len(player['initials'])):
                #canvas.draw_image(image, (224+16, 16), (32,32), (100,100), (32,32))
                #print (224+(player['initials'][i]%5)*32)+16, int((player['initials'][i]%5-player['initials'][i]/5)*32)+16
                canvas.draw_image(image, ((224+(player['initials'][i]%5)*32)+16, (int(player['initials'][i]/5)*32)+16), (32,32), (164+8+(i*38),358), (32,32))
            if player['underscore_enabled']:
                canvas.draw_image(image, (368, 270), (32,4), (164+8+(player['underscore_pos']*38),358+20), (32,4))
        #canvas.draw_image(image, (368, 270), (32,4), (100,100), (32,4))


    #canvas.draw_polygon([(274,350), (274,366), (308,366), (308,350)], 1, "Red", "Red")


'''    count=0
    canvas.draw_text("pyman:"+str(sprites['pyman']['pos_x'])+", "+str(sprites['pyman']['pos_y']), [0, 240+(count*40)], 8, "Yellow")
    count=1
    for i in enemies:
        canvas.draw_polygon([(enemies[i]['static_target'][0],enemies[i]['static_target'][1]), (enemies[i]['static_target'][0],enemies[i]['static_target'][1]+16), (enemies[i]['static_target'][0]+16,enemies[i]['static_target'][1]+16), (enemies[i]['static_target'][0]+16,enemies[i]['static_target'][1])], 1, "Black", enemies[i]['color'])
        color="Green"
        if enemies[i]['mode']=="scatter":
            color="White"
        elif enemies[i]['mode']=="eaten":
            color="#444444"
        elif enemies[i]['mode']=="frightened":
            color="Blue"
        canvas.draw_text(i+":"+str(enemies[i]['target'][0])+", "+str(enemies[i]['target'][1]), [0, 240+(count*20)], 8, "Yellow")
        canvas.draw_polygon([(enemies[i]['target'][0],enemies[i]['target'][1]), (enemies[i]['target'][0],enemies[i]['target'][1]+16), (enemies[i]['target'][0]+16,enemies[i]['target'][1]+16), (enemies[i]['target'][0]+16,enemies[i]['target'][1])], 2, enemies[i]['color'], color)
        #canvas.draw_circle((enemies[i]['target'][0],enemies[i]['target'][1]), 16-count, 1, enemies[i]['color'], enemies[i]['color'])
        #canvas.draw_circle((enemies[i]['target'][0]+8,enemies[i]['target'][1]+8), 4, 1, color, color)
        count+=1
        #canvas.draw_polygon([(sprites[i]['pos_x'],sprites[i]['pos_y']), (sprites[i]['pos_x'],sprites[i]['pos_y']+16), (sprites[i]['pos_x']+16,sprites[i]['pos_y']+16), (sprites[i]['pos_x']+16,sprites[i]['pos_y'])], 2, enemies[i]['color'], "Pink")
        #print enemies[i]['target'][0], enemies[i]['target'][1]'''
        
        



def make_sprite_timer_handler(sprite):
    def a_timer_handler():
        global sprites
        if sprites[sprite]['cur_frame']<sprites[sprite]['num_frames']-1:
            sprites[sprite]['cur_frame']+=1
        elif sprites[sprite]['cur_frame']==sprites[sprite]['num_frames']-1:
            sprites[sprite]['cur_frame']=0
            if sprites[sprite]['times_to_loop']!=-1:
                sprites[sprite]['loop_count']+=1
                if sprites[sprite]['loop_count']==sprites[sprite]['times_to_loop']:
                    sprites[sprite]['loop_count']=0
                    sprites[sprite]['enabled']=False
    return a_timer_handler

def make_enemy_timer_handler(i):
    def a_timer_handler():
        make_enemies_move(i)
    return a_timer_handler

#for i in enemies:
#    enemies[i]['enemy_move_timer'] = simplegui.create_timer(enemies[i]['speed'], enemy_mode_timer_handler)

#count=0

#def make_profs_move():
    

def reset_enemy_movement_timer(i):
    global enemy_timers
    enemy_timers[i].stop()
    s=0
    temp=player['level']
    if temp<1:
        temp=1
    for j in range(len(level_changes)):
        if level_changes[j]>temp:
            s=player['max_speed']/[.75,.85,.95,.95][j-1]
            break

    if enemies[i]['mode']=='frightened':
        s=player['max_speed']/[.50,.55,.60,.60][j-1]
    if enemies[i]['in_slow_zone']:
        s=player['max_speed']/[.40,.45,.5,.5][j-1]
    if enemies[i]['mode']=='eaten':
        s=player['max_speed']/2
    #print i+": "+enemies[i]['mode']+":::"+str(s)+":"+str(player['max_speed']/s)
    #print i+" : "+str(s)+" : "+str(enemies[i]['in_slow_zone'])+" : "+str(enemies[i]['mode'])+" : "+str(enemies[i]['target'])
    enemy_timers[i]=simplegui.create_timer(s, make_enemy_timer_handler(i))
    enemy_timers[i].start()


def get_board_coords(x,y):
    return [int(sprites[i]['pos_x']/16), int(sprites[i]['pos_y']/16)]

def make_enemies_move(i):
    global sprites, enemies
    if player['in_intro'] or player['game_over']:
        return

    if enemies[i]['mode']!='housed':
        #if enemies[i]['in_slow_zone']:
            #sprites[i]['pos_x']+=directions[enemies[i]['cur_direction']][1]/4
            
        
        #if 
        
        if enemies[i]['mode']=="scatter":
            enemies[i]['target']=enemies[i]['static_target']
        elif enemies[i]['mode']=="eaten":
            enemies[i]['target']=(228,280)
        elif enemies[i]['mode']=="chase":
            if i=='warren':
                enemies[i]['target']=[sprites['pyman']['pos_x']+(directions[current_direction][1]*16), sprites['pyman']['pos_y']+(directions[current_direction][2]*16)]
            elif i=="greiner":
                tempx=(sprites['pyman']['pos_x']+(directions[current_direction][1]*8)-sprites['rixner']['pos_x'])*2
                tempy=(sprites['pyman']['pos_y']+(directions[current_direction][2]*8)-sprites['rixner']['pos_y'])*2
                enemies[i]['target']=[tempx+sprites['rixner']['pos_x'], tempy+sprites['rixner']['pos_y']]
            elif i=="wong":
                temp=math.sqrt(((int(sprites['pyman']['pos_x']/16)-int(sprites['wong']['pos_x']/16))**2)+((int(sprites['pyman']['pos_y']/16)-int(sprites['wong']['pos_y']/16))**2))
                #print temp
                if temp>8:
                    enemies[i]['target']=[sprites['pyman']['pos_x'], sprites['pyman']['pos_y']]
                else:
                    enemies[i]['target']=enemies[i]['static_target']
            else:
                enemies[i]['target']=[int(sprites['pyman']['pos_x']/16)*16, int(sprites['pyman']['pos_y']/16)*16]
            
            #(176,240), (280,240), (280,312), (176,312)
        elif enemies[i]['mode']=='emerging' and not (sprites[i]['pos_y']>240 and sprites[i]['pos_y']<312 and sprites[i]['pos_x']>176 and sprites[i]['pos_x']<280):
            enemies[i]['mode']='scatter'
            enemies[i]['target']=enemies[i]['static_target']
        #if enemies[i]
        
        if (enemies[i]['mode']=='scatter' or enemies[i]['mode']=='chase') and (sprites[i]['pos_y']>240 and sprites[i]['pos_y']<312 and sprites[i]['pos_x']>176 and sprites[i]['pos_x']<280):
            enemies[i]['mode']='emerging'
            enemies[i]['target']=(224,0)
        
        
        if enemies[i]['mode']=='eaten' and sprites[i]['pos_x']==228 and sprites[i]['pos_y']==280:
            enemies[i]['mode']='emerging'
            enemies[i]['target']=(224,0)
            enemies[i]['state']=1
            sprites[i]['num_frames']=1
            sprites[i]['cur_frame']=0
            reset_enemy_movement_timer(i)
            #enemies[i]['cur_direction']=opposite_directions[enemies[i]['cur_direction']]
        
        
        #change enemy direction
        #print dirs[enemies[i]['cur_direction']], sprites[i]['pos_x']%16, sprites[i]['pos_y']%16 
        new_direction=enemies[i]['cur_direction']
        if not enemies[i]['in_slow_zone'] and sprites[i]['pos_x']%16==8 and sprites[i]['pos_y']%16==8:
            distance_to_target=999
            for j in directions_ordered_for_enemies:
                #print dirs[j]+":::"+str( board[int(sprites[i]['pos_x']/16)+int(directions[j][1]/4)][int(sprites[i]['pos_y']/16)+int(directions[j][2]/4)])
                if j!=opposite_directions[enemies[i]['cur_direction']] and board[int(sprites[i]['pos_x']/16)+int(directions[j][1]/4)][int(sprites[i]['pos_y']/16)+int(directions[j][2]/4)] in (-1,0,1,2,9,-2):
                    if not(j==simplegui.KEY_MAP["down"] and board[int(sprites[i]['pos_x']/16)+int(directions[j][1]/4)][int(sprites[i]['pos_y']/16)+int(directions[j][2]/4)]==9 and enemies[i]['state']!=2) \
                       and not(j==simplegui.KEY_MAP["up"] and int(sprites[i]['pos_x']/16)+int(directions[j][1]/4)>=12 and int(sprites[i]['pos_x']/16)+int(directions[j][1]/4)<=17 and (int(sprites[i]['pos_y']/16)+int(directions[j][2]/4)==13 or int(sprites[i]['pos_y']/16)+int(directions[j][2]/4)==25)):
                        if enemies[i]['mode']=='frightened':
                            temp_distance=random.random()
                        else:
                            temp_distance=math.sqrt(((int(sprites[i]['pos_x']/16)+int(directions[j][1]/4)-int(enemies[i]['target'][0]/16)+int(directions[j][1]/4))**2)+((int(sprites[i]['pos_y']/16)+int(directions[j][2]/4)-int(enemies[i]['target'][1]/16)+int(directions[j][2]/4))**2))
                        if distance_to_target>temp_distance:
                            #print "shortest:"+dirs[j]+":::"+str( board[int(sprites[i]['pos_x']/16)+int(directions[j][1]/4)][int(sprites[i]['pos_y']/16)+int(directions[j][2]/4)])
                            distance_to_target=temp_distance
                            new_direction=j
            if new_direction!=enemies[i]['cur_direction']:
                enemies[i]['last_direction']=enemies[i]['cur_direction']
                enemies[i]['cur_direction']=new_direction
                #if i=='rixner':
                    #print dirs[enemies[i]['cur_direction']]
        
        #divisor=1
        #if enemies[i]['mode']=="frightened":
            #divisor=2
        
        if sprites[i]['pos_x']%16!=8:
            sprites[i]['pos_x']+=directions[enemies[i]['cur_direction']][1]
        elif sprites[i]['pos_x']%16==8:
            if board[int(sprites[i]['pos_x']/16)+int(directions[enemies[i]['cur_direction']][1]/4)][int(sprites[i]['pos_y']/16)] in (-2,-1,0,1,2):
                sprites[i]['pos_x']+=directions[enemies[i]['cur_direction']][1]
                if enemies[i]['in_slow_zone']:
                    enemies[i]['in_slow_zone']=False
                    #enemies[i]['speed']/=2
                    reset_enemy_movement_timer(i)
            elif board[int(sprites[i]['pos_x']/16)+int(directions[enemies[i]['cur_direction']][1]/4)][int(sprites[i]['pos_y']/16)]==10:
                sprites[i]['pos_x']+=416
            elif board[int(sprites[i]['pos_x']/16)+int(directions[enemies[i]['cur_direction']][1]/4)][int(sprites[i]['pos_y']/16)]==11:
                sprites[i]['pos_x']-=416
            elif board[int(sprites[i]['pos_x']/16)+int(directions[enemies[i]['cur_direction']][1]/4)][int(sprites[i]['pos_y']/16)]==12:
                sprites[i]['pos_x']+=directions[enemies[i]['cur_direction']][1]
                enemies[i]['in_slow_zone']=True
                #enemies[i]['speed']/=2
                reset_enemy_movement_timer(i)
        if sprites[i]['pos_y']%16!=8 or (sprites[i]['pos_y']%16==8 and board[int(sprites[i]['pos_x']/16)][int(sprites[i]['pos_y']/16)+int(directions[enemies[i]['cur_direction']][2]/4)] in (-2,-1,0,1,2,9)):
            sprites[i]['pos_y']+=directions[enemies[i]['cur_direction']][2]


def make_pyman_move():
    global sprites, count, board, player, timer, enemies
    #print player['count']
    if player['in_intro'] or player['game_over']:
        return
    #in the slow zone
    #if player['in_slow_zone']:
        #sprites['pyman']['pos_x']+=directions[current_direction][1]/2
    
    #increment points displayed based on player speed, then delete if over than time limit
    for i in point_displays:
        point_displays[i]['count']+=1
        if point_displays[i]['count']>750/player['speed']:
            del point_displays[i]
    
    if player['mode']=='play' and player['score']>player['extra_life_score']:
        player['extra_life_score']*=2
        player['lives']+=1
        extralifesound.play()
    
    #if (sprites['pyman']['pos_x'], sprites['pyman']['pos_y']) in ((sprites['rixner']['pos_x'], sprites['rixner']['pos_y']),(sprites['warren']['pos_x'], sprites['warren']['pos_y']),(sprites['greiner']['pos_x'], sprites['greiner']['pos_y']),(sprites['wong']['pos_x'], sprites['wong']['pos_y'])):
    #print "----------------"
    for i in enemies:
        #print i+" : "+enemies[i]['mode']+" : "+str(enemies[i]['target'])+" : "+str(sprites[i]['pos_x'])+", "+str(sprites[i]['pos_y'])
        if math.fabs(sprites['pyman']['pos_x']-sprites[i]['pos_x'])<=8 and math.fabs(sprites['pyman']['pos_y']-sprites[i]['pos_y'])<=8:
            if enemies[i]['state']==1:
                a=12
                player_died()
                return
            elif enemies[i]['state']==0:
                player['enemies_eaten']+=1
                if player['mode']=='play':
                    ediblesound.rewind()
                    ediblesound.play()
                    player['count'][3][player['enemies_eaten']-1]+=1
                    player['score']+=(2**player['enemies_eaten'])*100
                    #print (2**player['enemies_eaten'])*100
                enemies[i]['state']=2
                enemies[i]['mode']="eaten"
                enemies[i]['target']=(228,280)
                sprites[i]['num_frames']=1
                sprites[i]['cur_frame']=3
                point_displays[str(time.time())]={'value':(2**player['enemies_eaten'])*100, 'pos_x':sprites[i]['pos_x']+3, 'pos_y':sprites[i]['pos_y'], 'count':0}
                reset_enemy_movement_timer(i)
        
        
        
    if player['edible_available'] in (1,3) and sprites['pyman']['pos_x']==224 and sprites['pyman']['pos_y']==328:
        player['edible_available']+=1
        if player['mode']=='play':
            player['count'][2]+=player['level']
            player['edibles'][(player['level']-1)%7]+=1
            ediblesound.rewind()
            ediblesound.play()
            player['score']+=100*player['level']
        point_displays[str(time.time())]={'value':100*player['level'], 'pos_x':224, 'pos_y':328, 'count':0}
    
    
    if board[int(sprites['pyman']['pos_x']/16)][int(sprites['pyman']['pos_y']/16)] == 1:
        board[int(sprites['pyman']['pos_x']/16)][int(sprites['pyman']['pos_y']/16)] = -1
        if player['mode']=='play':
            player['count'][0]+=1
            chompsound.play()
            player['score']+=10
            player['pellets_eaten']+=1
        #print player['edible_available'], player['edible_available'], player['pellets_eaten'], (30*((player['level']-1)%7)+30), player['edible_available']==0 and player['pellets_eaten']>=(30*((player['level']-1)%7)+30)
        if player['pellets_eaten'] in (70,170):
            player['edible_available']+=1
    elif board[int(sprites['pyman']['pos_x']/16)][int(sprites['pyman']['pos_y']/16)] == 2:
        board[int(sprites['pyman']['pos_x']/16)][int(sprites['pyman']['pos_y']/16)] = -1
        if player['mode']=='play':
            player['count'][1]+=1
            supersound.play()
            player['score']+=50
            player['pellets_eaten']+=1
        
        power_pellet_timer_handler(True, False, False)
        if player['mode']=='play':
            supersound.play()
        
        for i in enemies:
            #print i+" : "+dirs[enemies[i]['cur_direction']]+" : "+dirs[enemies[i]['last_direction']]
            if enemies[i]['state']==1 and enemies[i]['mode']!='housed' and enemies[i]['mode']!='emerging':
                enemies[i]['state']=0
                sprites[i]['cur_frame']=1
                if enemies[i]['mode']!='frightened':
                    enemies[i]['backup_mode']=enemies[i]['mode']
                    enemies[i]['mode']='frightened'
                #enemies[i]['speed']/=2
                reset_enemy_movement_timer(i)
                #enemies[i]['in_slow_zone']=True
                #temp=enemies[i]['last_direction']
                #enemies[i]['last_direction']=enemies[i]['cur_direction']
                if not enemies[i]['in_slow_zone']:
                    enemies[i]['cur_direction']=opposite_directions[enemies[i]['cur_direction']]
        
        power_pellet_timer.start()
        flash_enemies_starter.start()
    if (player['mode']=='test' and player['pellets_eaten']==216) or (player['mode']=='play' and player['pellets_eaten']==244):
        sprites['pyman']['num_frames']=1
        sprites['pyman']['cur_frame']=1
        init_turn_start()
        return
    
    for i in directions:
        if current_key_pressed[i]!=False:
            keydown_handler(i)

    if player['mode']=='test' and sprites['pyman']['pos_x']%16==8 and sprites['pyman']['pos_y']%16==8:
        change_direction(current_direction)

    if sprites['pyman']['pos_x']%16!=8:
        sprites['pyman']['pos_x']+=directions[current_direction][1]
    elif sprites['pyman']['pos_x']%16==8:
        if board[int(sprites['pyman']['pos_x']/16)+int(directions[current_direction][1]/4)][int(sprites['pyman']['pos_y']/16)] in (-1,0,1,2,12):
            sprites['pyman']['pos_x']+=directions[current_direction][1]
            #player['in_slow_zone']=False
        elif board[int(sprites['pyman']['pos_x']/16)+int(directions[current_direction][1]/4)][int(sprites['pyman']['pos_y']/16)]==10:
            sprites['pyman']['pos_x']+=416
        elif board[int(sprites['pyman']['pos_x']/16)+int(directions[current_direction][1]/4)][int(sprites['pyman']['pos_y']/16)]==11:
            sprites['pyman']['pos_x']-=416
        #elif board[int(sprites['pyman']['pos_x']/16)+int(directions[current_direction][1]/4)][int(sprites['pyman']['pos_y']/16)]==12:
            #player['in_slow_zone']=True
    if sprites['pyman']['pos_y']%16!=8 or (sprites['pyman']['pos_y']%16==8 and board[int(sprites['pyman']['pos_x']/16)][int(sprites['pyman']['pos_y']/16)+int(directions[current_direction][2]/4)]<3):
        sprites['pyman']['pos_y']+=directions[current_direction][2]

    #print board[int(sprites['pyman']['pos_x']/16)+int(directions[current_direction][1]/4)][int(sprites['pyman']['pos_y']/16)]

def mouseclick_handler(point):
    global player

    if player['submit_score']==0 and point[0]>=274 and point[0]<=308 and point[1]>=350 and point[1]<=366:
        player['submit_score']=1
        player['mode']='test'
        genURL()
        #init_turn_start()
    elif player['mode']=='test' and point[0]>=168 and point[0]<=285 and point[1]>=384 and point[1]<=399:
        player['mode']='play'
        player['level']=0
        player['score']=0
        player['count']=[0,0,0,[0,0,0,0]]
        player['pellets_eaten']=0
        player['edible_available']=0
        player['enemies_eaten']=0
        player['submit_score']=0
        player['game_over']=False
        player['game_id']=time.time()
        #print player['game_id']
        reset_everything()
        init_turn_start()


def keydown_handler(key):
    global sprites, current_direction, key_timer, current_key, current_key_pressed, player
    #print key
    
    if player['mode']=='test':
        if key==simplegui.KEY_MAP["down"]:
            player['initials'][player['underscore_pos']]+=1
        elif key==simplegui.KEY_MAP["up"]:
            player['initials'][player['underscore_pos']]-=1
        elif key==simplegui.KEY_MAP["right"]:
            player['underscore_pos']+=1
        elif key==simplegui.KEY_MAP["left"]:
            player['underscore_pos']-=1
        if player['underscore_pos']>2:
            player['underscore_pos']=0
        elif player['underscore_pos']<0:
            player['underscore_pos']=2
        if player['initials'][player['underscore_pos']]>39:
            player['initials'][player['underscore_pos']]=0
        if player['initials'][player['underscore_pos']]<0:
            player['initials'][player['underscore_pos']]=39
        if key==simplegui.KEY_MAP["space"]:
            player['submit_score']=1
            player['mode']='test'
            genURL()
        return
    
    
#    if key==simplegui.KEY_MAP["space"]:
#        for i in enemies:
#            print i, enemies[i]
    if player['mode']!='test' and key in directions:
        current_key_pressed[key]=True
        for i in directions:
            if i!=key:
                current_key_pressed[i]=False
        #change_direction(key)
        if not player['in_intro']:
            if key==simplegui.KEY_MAP["up"] and (current_direction==simplegui.KEY_MAP["down"] or (current_direction!=simplegui.KEY_MAP["up"] and sprites['pyman']['pos_x']%16==8)):
                change_direction(key)
            elif key==simplegui.KEY_MAP["down"] and (current_direction==simplegui.KEY_MAP["up"] or (current_direction!=simplegui.KEY_MAP["down"] and sprites['pyman']['pos_x']%16==8)):
                change_direction(key)
            elif key==simplegui.KEY_MAP["left"] and (current_direction==simplegui.KEY_MAP["right"] or (current_direction!=simplegui.KEY_MAP["left"] and sprites['pyman']['pos_y']%16==8)):
                change_direction(key)
            elif key==simplegui.KEY_MAP["right"] and (current_direction==simplegui.KEY_MAP["left"] or (current_direction!=simplegui.KEY_MAP["right"] and sprites['pyman']['pos_y']%16==8)):
                change_direction(key)
#            else:
#                current_key=key
#                key_timer.start()

'''def keyup_handler_old(key):
    if player['in_intro']:
        return
    global key_timer
    key_timer.stop()'''
    
    
def keyup_handler(key):
    global current_key_pressed
    current_key_pressed[key]=False

#def key_timer():
#    if player['in_intro']:
#        return
#    keydown_handler(current_key)

def change_direction(key):
    if player['in_intro'] or player['game_over']:
        return
    global sprites, current_direction, timer
    
    #print sprites['pyman']['pos_x'], sprites['pyman']['pos_y']
    #if sprites['pyman']['pos_x']>428:
        #sprites['pyman']['pos_x']=0
    #if int(sprites['pyman']['pos_x']/16)+int(directions[key][1]/4)==28:
        #sprites['pyman']['pos_x']=16
#    elif board[int(sprites['pyman']['pos_x']/16)+int(directions[key][1]/4)][int(sprites['pyman']['pos_y']/16)]==0:
#        sprites['pyman']['pos_x']=432
    
    #print key, sprites['pyman']['pos_x']/16, directions[key][1]/4, sprites['pyman']['pos_y']/16, int(sprites['pyman']['pos_x']/16)+int(directions[key][1]/4), int(sprites['pyman']['pos_y']/16)
    
    
    if player['mode']=='test':
        distance_to_target=0
        for j in directions_ordered_for_enemies:
            if j!=opposite_directions[current_direction] and board[int(sprites['pyman']['pos_x']/16)+int(directions[j][1]/4)][int(sprites['pyman']['pos_y']/16)+int(directions[j][2]/4)] in (-1,0,1,2,12):

                temp_distance=0
                count=0
#                if random.random()>.5:
#                    for i in enemies:
#                        temp_distance+=math.sqrt(((int(sprites['pyman']['pos_x']/16)+int(directions[j][1]/4)-int(sprites[i]['pos_x']/16))**2)+((int(sprites['pyman']['pos_y']/16)+int(directions[j][2]/4)-int(sprites[i]['pos_y']/16))**2))
#                    print dirs[j], temp_distance
#                else:
                temp_distance=random.random()
                if distance_to_target<temp_distance:
                    distance_to_target=temp_distance
                    key=j

    if (key==simplegui.KEY_MAP["left"] or key==simplegui.KEY_MAP["right"]) and board[int(sprites['pyman']['pos_x']/16)+int(directions[key][1]/4)][int(sprites['pyman']['pos_y']/16)] in (-1,0,1,2,12):
        sprites['pyman']['rotation_in_degrees']=directions[key][0]
        sprites['pyman']['height_offset']=directions[key][3]
        current_direction=key
    elif (key==simplegui.KEY_MAP["up"] or key==simplegui.KEY_MAP["down"]) and board[int(sprites['pyman']['pos_x']/16)][int(sprites['pyman']['pos_y']/16)+int(directions[key][2]/4)] in (-1,0,1,2,12):
        sprites['pyman']['rotation_in_degrees']=directions[key][0]
        sprites['pyman']['height_offset']=directions[key][3]
        current_direction=key

    #print (key==simplegui.KEY_MAP["left"] or key==simplegui.KEY_MAP["right"]) and board[int(sprites['pyman']['pos_x']/16)+int(directions[current_direction][1]/4)][int(sprites['pyman']['pos_y']/16)] < 3, (key==simplegui.KEY_MAP["up"] or key==simplegui.KEY_MAP["down"]) and board[int(sprites['pyman']['pos_x']/16)][int(sprites['pyman']['pos_y']/16)+int(directions[current_direction][2]/4)] < 3

    '''timer.stop()
    print sprites['pyman']['pos_x'], sprites['pyman']['pos_y']
    print sprites['pyman']['pos_x']%4, sprites['pyman']['pos_x']%8, sprites['pyman']['pos_x']%16, sprites['pyman']['pos_x']%24, sprites['pyman']['pos_x']%32
    print sprites['pyman']['pos_y']%4, sprites['pyman']['pos_y']%8, sprites['pyman']['pos_y']%16, sprites['pyman']['pos_y']%24, sprites['pyman']['pos_y']%32'''

def player_died():
    global player, sprites, sprite_timers
    for i in enemies:
        sprites[i]['enabled']=False
    sprites['pyman']['num_frames']=10
    sprites['pyman']['cur_frame']=2
    sprites['pyman']['ms_per_frame']=200
    sprites['pyman']['times_to_loop']=1
    sprite_timers['pyman'].stop()
    sprite_timers['pyman']=simplegui.create_timer(sprites['pyman']['ms_per_frame'], make_sprite_timer_handler('pyman'))
    sprite_timers['pyman'].start()
    #player['in_intro']=True
    player_died_timer.start()
    timer.stop()
    if player['mode']=='play':
        theygotchasound.play()

    
def player_died_handler():
    player_died_timer.stop()
    init_turn_start(False)
    

def power_pellet_timer_handler(reset_kill_dict=True, reset_eatability=False, restore_backup_mode=True):
    global sprites, enemies, player
    player['enemies_eaten']=0
    supersound.rewind()
    power_pellet_timer.stop()
    flash_enemies_timer.stop()
    flash_enemies_starter.stop()
    if reset_kill_dict:
        for i in enemies:
            #print i, enemies[i]['state']
            if enemies[i]['state']!=2 or reset_eatability:
                enemies[i]['state']=1
                if restore_backup_mode:
                    enemies[i]['mode']=enemies[i]['backup_mode']
                    enemies[i]['target']=enemies[i]['static_target']
                sprites[i]['cur_frame']=0
                #sprites[i]['in_slow_zone']=False
                reset_enemy_movement_timer(i)



def flash_enemies():
    global sprites
    for i in enemies:
        if enemies[i]['state']==0 and enemies[i]['mode']!='housed':
            if sprites[i]['cur_frame']==1:
                sprites[i]['cur_frame']=2
            else:
                sprites[i]['cur_frame']=1

def flash_enemies_timer_handler():
    global flash_enemies_timer, flash_enemies_starter
    flash_enemies_timer.start()
    flash_enemies_starter.stop()

def init_turn_start(new_level = True):
    global player, sprites, timer, board, intro_timer, current_direction, sprite_timers, power_pellet_timer, flash_enemies_starter, enemies
    timer.stop()
    #enemytimer.stop()
    if new_level or (not new_level and player['lives']>1):
        power_pellet_timer_handler(True, True, False)
        timer = simplegui.create_timer(player['speed'], make_pyman_move)
        theygotchasound.rewind()
        supersound.rewind()
        player['in_intro']=True
        
        reset_sprites()
        sprite_timers['pyman'].stop()
        sprite_timers['pyman']=simplegui.create_timer(sprites['pyman']['ms_per_frame'], make_sprite_timer_handler('pyman'))
        sprite_timers['pyman'].start()
        
        enemy_mode_timer.stop()
        if player['mode']=='test':
            new_level=True

        if new_level:
            if player['mode']=='play':
                intromusic.play()
                player['level']+=1
                intro_timer = simplegui.create_timer(4761, intro_timer_handler)
            else:
                intro_timer = simplegui.create_timer(1000, intro_timer_handler)
                #player['level']=1
                #player['score']=0
            #if player['speed']>20:
                #player['speed']-=5
            player['pellets_eaten']=0
            #print player
            if player['level']<=8 and player['mode']=='play':
                player['power_pellet_time']-=1000
            for j in range(len(level_changes)):
                if level_changes[j]>player['level']:
                    player['speed']=player['max_speed']/[.80,.90,1.0,.90][j-1]
                    #print 'pyman: '+str(player['speed'])+":"+str(player['max_speed']/player['speed'])
                    break
            '''for j in range(player['level']):
                if level_changes[j]==player['level']:
                    player['speed']=player['max_speed']/[.80,.90,.100,.90][j]
                    print 'pyman: '+str(player['speed'])+":"+str(player['max_speed']/player['speed'])
                    break'''
            power_pellet_timer = simplegui.create_timer(player['power_pellet_time'], power_pellet_timer_handler)
            temp=player['power_pellet_time']-2500
            if temp<=0:
                temp=1
            #print player['power_pellet_time'], temp
            flash_enemies_starter = simplegui.create_timer(temp, flash_enemies_timer_handler)
            player['edible_available']=0
            board=[
            [0,0,0,5,3,3,3,3,3,3,3,3,7,0,0,0,4,10,4,0,0,0,5,3,3,3,3,7,5,3,3,3,3,7,0,0],
            [0,0,0,4,1,1,2,1,1,1,1,1,4,0,0,0,4,12,4,0,0,0,4,1,1,1,2,4,4,1,1,1,1,4,0,0],
            [0,0,0,4,1,5,3,7,1,5,7,1,4,0,0,0,4,12,4,0,0,0,4,1,5,7,1,6,8,1,5,7,1,4,0,0],
            [0,0,0,4,1,4,0,4,1,4,4,1,4,0,0,0,4,12,4,0,0,0,4,1,4,4,1,1,1,1,4,4,1,4,0,0],
            [0,0,0,4,1,4,0,4,1,4,4,1,4,0,0,0,4,12,4,0,0,0,4,1,4,6,3,3,7,1,4,4,1,4,0,0],
            [0,0,0,4,1,6,3,8,1,6,8,1,6,3,3,3,8,0,6,3,3,3,8,1,6,3,3,3,8,1,4,4,1,4,0,0],
            [0,0,0,4,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,4,4,1,4,0,0],
            [0,0,0,4,1,5,3,7,1,5,3,3,3,3,3,3,7,0,5,3,3,3,7,1,5,7,1,5,3,3,8,4,1,4,0,0],
            [0,0,0,4,1,4,0,4,1,6,3,3,7,5,3,3,8,0,6,3,3,3,8,1,4,4,1,6,3,3,7,4,1,4,0,0],
            [0,0,0,4,1,4,0,4,1,1,1,1,4,4,0,0,0,0,0,0,0,0,0,1,4,4,1,1,1,1,4,4,1,4,0,0],
            [0,0,0,4,1,4,0,4,1,5,7,1,4,4,0,5,3,3,3,7,0,5,7,1,4,4,1,5,7,1,4,4,1,4,0,0],
            [0,0,0,4,1,6,3,8,1,4,4,1,6,8,0,4,0,0,0,4,0,4,4,1,6,8,1,4,4,1,6,8,1,4,0,0],
            [0,0,0,4,1,1,1,1,1,4,4,1,0,0,0,4,0,0,0,4,0,4,4,1,1,1,1,4,4,1,1,1,1,4,0,0],
            [0,0,0,6,3,3,3,7,1,4,6,3,3,7,0,9,0,0,0,4,0,4,6,3,3,7,0,4,6,3,3,7,1,4,0,0],
            [0,0,0,5,3,3,3,8,1,4,5,3,3,8,0,9,0,0,0,4,0,4,5,3,3,8,0,4,5,3,3,8,1,4,0,0],
            [0,0,0,4,1,1,1,1,1,4,4,1,0,0,0,4,0,0,0,4,0,4,4,1,1,1,1,4,4,1,1,1,1,4,0,0],
            [0,0,0,4,1,5,3,7,1,4,4,1,5,7,0,4,0,0,0,4,0,4,4,1,5,7,1,4,4,1,5,7,1,4,0,0],
            [0,0,0,4,1,4,0,4,1,6,8,1,4,4,0,6,3,3,3,8,0,6,8,1,4,4,1,6,8,1,4,4,1,4,0,0],
            [0,0,0,4,1,4,0,4,1,1,1,1,4,4,0,0,0,0,0,0,0,0,0,1,4,4,1,1,1,1,4,4,1,4,0,0],
            [0,0,0,4,1,4,0,4,1,5,3,3,8,6,3,3,7,0,5,3,3,3,7,1,4,4,1,5,3,3,8,4,1,4,0,0],
            [0,0,0,4,1,6,3,8,1,6,3,3,3,3,3,3,8,0,6,3,3,3,8,1,6,8,1,6,3,3,7,4,1,4,0,0],
            [0,0,0,4,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,4,4,1,4,0,0],
            [0,0,0,4,1,5,3,7,1,5,7,1,5,3,3,3,7,0,5,3,3,3,7,1,5,3,3,3,7,1,4,4,1,4,0,0],
            [0,0,0,4,1,4,0,4,1,4,4,1,4,0,0,0,4,12,4,0,0,0,4,1,4,5,3,3,8,1,4,4,1,4,0,0],
            [0,0,0,4,1,4,0,4,1,4,4,1,4,0,0,0,4,12,4,0,0,0,4,1,4,4,1,1,1,1,4,4,1,4,0,0],
            [0,0,0,4,1,6,3,8,1,6,8,1,4,0,0,0,4,12,4,0,0,0,4,1,6,8,1,5,7,1,6,8,1,4,0,0],
            [0,0,0,4,1,1,2,1,1,1,1,1,4,0,0,0,4,12,4,0,0,0,4,1,1,1,2,4,4,1,1,1,1,4,0,0],
            [0,0,0,6,3,3,3,3,3,3,3,3,8,0,0,0,4,11,4,0,0,0,6,3,3,3,3,8,6,3,3,3,3,8,0,0],
            [0,0,0,5,3,3,3,3,3,3,3,3,7,0,0,0,4,10,4,0,0,0,5,3,3,3,3,7,5,3,3,3,3,7,0,0],
            ]
            if player['mode']=='test':
                #sprites['rixner']['pos_x']=16+8
                #sprites['rixner']['pos_y']=80+8
                #sprites['warren']['pos_x']=416+8
                #sprites['warren']['pos_y']=80+8
                board[9][9]=-2
                board[18][9]=-2
                board[7][17]=-2
                board[20][17]=-2
                board[7][23]=-2
                board[20][23]=-2
                board[12][25]=-2
                board[15][25]=-2

                
            count=5
            for i in enemies:
                enemies[i]['out_of_gate']=math.floor(enemies[i]['out_of_gate']/2)
                if i!='rixner' and i!='warren' and enemies[i]['out_of_gate']<count:
                    enemies[i]['out_of_gate']=count
                    count+=5
        else:
            intro_timer = simplegui.create_timer(2000, intro_timer_handler)
            if player['mode']=='play':
                player['lives']-=1
                count=5
                for i in enemies:
                    if i!='rixner' and i!='warren':
                        enemies[i]['out_of_gate']=count
                        count+=10

        current_direction=simplegui.KEY_MAP["left"]
        intro_timer.start()
    else:
        player['game_over']=True
        player['edible_available']=0
        gaveover_timer.start()
        genURL()

sprites={}
def reset_sprites():
    global sprites
    sprites={
    'rixner':{'enabled':True, 'pos_x':224, 'pos_y':232, 'height_offset':0, 'rotation_in_degrees':0, 'times_to_loop':0, 'loop_count':0, 'num_frames':1, 'cur_frame':0, 'original_frame_width':32, 'original_frame_height':32, 'scaled_frame_width':32, 'scaled_frame_height':32, 'ms_per_frame':300, 'url':'rixner.png'},
    'warren':{'enabled':True, 'pos_x':224, 'pos_y':280, 'height_offset':0, 'rotation_in_degrees':0, 'times_to_loop':0, 'loop_count':0, 'num_frames':1, 'cur_frame':0, 'original_frame_width':32, 'original_frame_height':32, 'scaled_frame_width':32, 'scaled_frame_height':32, 'ms_per_frame':300, 'url':'warren.png'},
    'greiner':{'enabled':True, 'pos_x':192, 'pos_y':280, 'height_offset':0, 'rotation_in_degrees':0, 'times_to_loop':0, 'loop_count':0, 'num_frames':1, 'cur_frame':0, 'original_frame_width':32, 'original_frame_height':32, 'scaled_frame_width':32, 'scaled_frame_height':32, 'ms_per_frame':300, 'url':'greiner.png'},
    'wong':{'enabled':True, 'pos_x':256, 'pos_y':280, 'height_offset':0, 'rotation_in_degrees':0, 'times_to_loop':0, 'loop_count':0, 'num_frames':1, 'cur_frame':0, 'original_frame_width':32, 'original_frame_height':32, 'scaled_frame_width':32, 'scaled_frame_height':32, 'ms_per_frame':300, 'url':'wong.png'},
    'pyman':{'enabled':True, 'pos_x':224, 'pos_y':424, 'height_offset':1, 'rotation_in_degrees':0, 'times_to_loop':-1, 'loop_count':0, 'num_frames':1, 'cur_frame':0, 'original_frame_width':20, 'original_frame_height':20, 'scaled_frame_width':20, 'scaled_frame_height':20, 'ms_per_frame':70, 'url':'pyman.png'},
    }

def intro_timer_handler():
    global player, intromusic, sprites, intro_timer, timer, enemies
    player['in_intro']=False
    intromusic.rewind()
    sprites['pyman']['num_frames']=4
    sprites['pyman']['cur_frame']=0
    intro_timer.stop()
    timer.start()
    for i in enemy_timers:
        enemies[i]['state']=1
        enemies[i]['cur_direction']=simplegui.KEY_MAP["left"]
        enemies[i]['mode']='housed'
        enemies[i]['backup_mode']='housed'
        enemies[i]['target']=(224,0)
        enemies[i]['in_slow_zone']=False
        enemies[i]['out_of_gate_timer']=0
        enemies[i]['time_counter']=0
        reset_enemy_movement_timer(i)
    enemy_mode_timer.start()




scatter_chase=[
[7,27,34,54,59,79,84,999999999],
[5,25,30,50,55,999999999]
]
def enemy_mode_timer_handler():
    global enemies
    for i in enemies:
        if enemies[i]['out_of_gate']>enemies[i]['out_of_gate_timer']:
            enemies[i]['out_of_gate_timer']+=1
        elif enemies[i]['mode']=='housed':
            enemies[i]['mode']='emerging'
            enemies[i]['backup_mode']='emerging'
            enemies[i]['target']=(224,0)
        if enemies[i]['out_of_gate']<=enemies[i]['out_of_gate_timer'] and enemies[i]['mode']!='frightened' and enemies[i]['mode']!='eaten' and enemies[i]['mode']!='housed' and enemies[i]['mode']!='emerging':
            enemies[i]['time_counter']+=1
            sc=scatter_chase[0]
            if player['level']>=5:
                sc=scatter_chase[1]
            if enemies[i]['time_counter']/10 in sc:
                for j in range(len(sc)):
                    if sc[j]*10>enemies[i]['time_counter']:
                        break
                if j%2==0:
                    enemies[i]['mode']='scatter'
                elif j%2==1:
                    enemies[i]['mode']='chase'
                enemies[i]['cur_direction']=opposite_directions[enemies[i]['cur_direction']]

def underscore_timer_handler():
    global player
    player['underscore_enabled']=not player['underscore_enabled']

def gameover_timer_handler():
    global player
    player['game_over']=False
    player['mode']='test'
    player['underscore_enabled']=True
    gaveover_timer.stop()
    player['lives']=3
    init_turn_start()

#create the simplegui frame
frame = simplegui.create_frame("Pythonman", 448, 576,300)
frame.set_canvas_background("#000000")
intro_timer = simplegui.create_timer(4761, intro_timer_handler)
timer = simplegui.create_timer(player['speed'], make_pyman_move)
player_died_timer = simplegui.create_timer(2278, player_died_handler)
power_pellet_timer = simplegui.create_timer(player['power_pellet_time'], power_pellet_timer_handler)
flash_enemies_timer = simplegui.create_timer(250, flash_enemies)
flash_enemies_starter = simplegui.create_timer(6000, flash_enemies_timer_handler)
enemy_mode_timer = simplegui.create_timer(100, enemy_mode_timer_handler)
underscore_timer = simplegui.create_timer(250, underscore_timer_handler)
underscore_timer.start()
gaveover_timer = simplegui.create_timer(2000, gameover_timer_handler)
#sound pulled from lecture video :)
intromusic = simplegui.load_sound(BASE_DIR+"intromusic.ogg")

#sound from http://www.playonloop.com/
supersound = simplegui.load_sound(BASE_DIR+"ateapill.ogg")

#below sounds from http://www.noiseforfun.com
chompsound = simplegui.load_sound(BASE_DIR+"eatpellet.ogg")
ediblesound = simplegui.load_sound(BASE_DIR+"eatedible.ogg")
theygotchasound = simplegui.load_sound(BASE_DIR+"theygotcha.ogg")
extralifesound = simplegui.load_sound(BASE_DIR+"extralife.ogg")
enemy_timers={}
sprite_timers={}
reset_sprites()
for i in sprites:
    sprite_timers[i]=simplegui.create_timer(sprites[i]['ms_per_frame'], make_sprite_timer_handler(i))
    sprite_timers[i].start()
for i in enemies:
    enemy_timers[i]=simplegui.create_timer(enemies[i]['speed'], make_enemy_timer_handler(i))
init_turn_start()
frame.set_draw_handler(draw)
frame.set_mouseclick_handler(mouseclick_handler)
frame.set_keydown_handler(keydown_handler)
frame.set_keyup_handler(keyup_handler)
frame.add_label("Welcome to PyMan!")
frame.add_label("")
frame.add_label("Instructions:")
frame.add_label("1. Click New Game to start a new game")
frame.add_label("2. Use the arrow keys to move PyMan")
frame.add_label("3. Avoid the Professors")
frame.add_label("4. Eat a large pellet to make the Professors edible")
frame.add_label("5. Eat all the pellets to go to the next level")
frame.add_label("6. Try to get a high score :)")
frame.add_label("7. High score isn't submitted until you click Go")
frame.add_label("")
frame.add_label("Points:")
frame.add_label("Small pellets = 10 pts")
frame.add_label("Large pellets = 50 pts")
frame.add_label("Bonuses = level x 100 pts")
frame.add_label("1st Ghost = 200 pts")
frame.add_label("2nd Ghost = 400 pts")
frame.add_label("3rd Ghost = 800 pts")
frame.add_label("4th Ghost = 1600 pts")
frame.add_label("")
frame.add_label("Credits:")
frame.add_label("Intro Music - the lecture videos")
frame.add_label("Professor Mugshots - the class info page")
frame.add_label("Power Pellet Music - playonloop.com")
frame.add_label("Sound Effects - noiseforfun.com")
frame.add_label("Other Images - clker.com")
print sprites.keys()
frame.start()
