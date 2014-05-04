# Rubik's Cube in 3D - Karen Ward and Dennis della Corte, Coursera, Fall 2013

import simplegui
import math
import random

#global variables  
rot_ctr = 0        
oldpos = [-1,0]
rotation_axis = 0
label = "3D Rubics Cube. Drag mouse to rotate the hole cube. Rotate a side around rotation axis with 'Up' or 'Down' or by clicking unto the canvas buttons. Select rotation axis with 'Left' or 'Right' or by clicking into the canvas buttons. Use control buttons to Shuffle the cube and to reset. ENJOY! "
not_clicked = True
ROTSPEED = math.pi/8.
colors = ['White','Orange','Green','Red','Blue','Yellow','White','White']
shift = 60
shuffle_steps = 0

#class cube
class cube:
    def __init__(self, trans = [0, 200, 200], scale = 100):
        self.rotation_speed = ROTSPEED
        self.scale = scale
        self.translation = trans
        self.line_thickness = 5
        
        c0 = [self.translation[0]+0,self.translation[1]+0,self.translation[2]+0]
        c1 = [self.translation[0]+0,self.translation[1]+self.scale*1,self.translation[2]+0]
        c2 = [self.translation[0]+0,self.translation[1]+self.scale*1,self.translation[2]+self.scale*1]
        c3 = [self.translation[0]+0,self.translation[1]+0,self.translation[2]+self.scale*1]
        c4 = [self.translation[0]+self.scale*1,self.translation[1]+0,self.translation[2]+0]
        c5 = [self.translation[0]+self.scale*1,self.translation[1]+self.scale*1,self.translation[2]+0]
        c6 = [self.translation[0]+self.scale*1,self.translation[1]+self.scale*1,self.translation[2]+self.scale*1]
        c7 = [self.translation[0]+self.scale*1,self.translation[1]+0,self.translation[2]+self.scale*1]
        self.corners = [c0,c1,c2,c3,c4,c5,c6,c7]
        self.yellow  = [[self.corners[0][1],self.corners[0][2]],[self.corners[1][1],self.corners[1][2]],[self.corners[2][1],self.corners[2][2]],[self.corners[3][1],self.corners[3][2]]]        
        self.white   = [[self.corners[4][1],self.corners[4][2]],[self.corners[5][1],self.corners[5][2]],[self.corners[6][1],self.corners[6][2]],[self.corners[7][1],self.corners[7][2]]]
        self.red     = [[self.corners[0][1],self.corners[0][2]],[self.corners[4][1],self.corners[4][2]],[self.corners[7][1],self.corners[7][2]],[self.corners[3][1],self.corners[3][2]]]
        self.orange  = [[self.corners[1][1],self.corners[1][2]],[self.corners[2][1],self.corners[2][2]],[self.corners[6][1],self.corners[6][2]],[self.corners[5][1],self.corners[5][2]]]
        self.green   = [[self.corners[3][1],self.corners[3][2]],[self.corners[7][1],self.corners[7][2]],[self.corners[6][1],self.corners[6][2]],[self.corners[2][1],self.corners[2][2]]]
        self.blue    = [[self.corners[0][1],self.corners[0][2]],[self.corners[1][1],self.corners[1][2]],[self.corners[5][1],self.corners[5][2]],[self.corners[4][1],self.corners[4][2]]]
        
        self.center  = [.5 * self.scale,self.translation[1]+.5 * self.scale,self.translation[2]+.5 * self.scale]
        self.order   = ['y','b','o','r','g','w']
        
        self.tilt_ctr = 0
        
    def sanity_check(self):
        #somehow does the cube shrink... so one of the operations must change the length of a side of the cube
        print self.v_len(self.corners[0],self.corners[1])
        print self.v_len(self.corners[0],self.corners[3])
        print self.v_len(self.corners[0],self.corners[4])
        
        print self.v_len(self.corners[7],self.corners[4])
        print self.v_len(self.corners[7],self.corners[6])
        print self.v_len(self.corners[7],self.corners[3])

        print self.v_len(self.corners[5],self.corners[4])
        print self.v_len(self.corners[5],self.corners[1])
        print self.v_len(self.corners[5],self.corners[6])

        print self.v_len(self.corners[2],self.corners[6])
        print self.v_len(self.corners[2],self.corners[1])
        print self.v_len(self.corners[2],self.corners[3])
        print
        
    def get_center_coords(self):
        x = self.corners[0][0] + (self.corners[6][0] - self.corners[0][0]) / 2.
        y = self.corners[0][1] + (self.corners[6][1] - self.corners[0][1]) / 2.
        z = self.corners[0][2] + (self.corners[6][2] - self.corners[0][2]) / 2.
        return [x,y,z]
        
    def set_rotation_point(self, vec):
        #to allow the cube to turn around any point in space
        self.center = vec
    
    def v_len(self,v1, v2):
        sum = 0
        for i in range(3):
            sum += (v1[i]-v2[i]) * (v1[i]-v2[i])
        return math.sqrt(sum)
        
    def sort(self):
        c_yellow = (self.corners[0][0] + self.corners[2][0]) /2.
        c_blue   = (self.corners[0][0] + self.corners[5][0]) /2.
        c_orange = (self.corners[1][0] + self.corners[6][0]) /2.
        c_red    = (self.corners[0][0] + self.corners[7][0]) /2.
        c_green  = (self.corners[3][0] + self.corners[6][0]) /2.
        c_white  = (self.corners[4][0] + self.corners[6][0]) /2.
        self.centers = [c_yellow,c_blue,c_orange,c_red,c_green,c_white]
        #now sort self.order according to self.centers
        l = list(self.centers)
        l.sort()
      
        for i in range(6):
            if l[i] == c_yellow:
                self.order[i] = 'y'
            elif l[i] == c_blue:
                self.order[i] = 'b'
            elif l[i] == c_orange:
                self.order[i] = 'o'
            elif l[i] == c_red:
                self.order[i] = 'r'
            elif l[i] == c_green:
                self.order[i] = 'g'
            elif l[i] == c_white:
                self.order[i] = 'w'
     
    def get_depth(self):
        return self.get_center_coords()[0]
                
    def print_corners(self):
        for i in self.corners:
            print i
        print
        print self.order

    def rotate_around_axis(self, spoint, axis):
        for i in range(8):
            self.corners[i] = self.rot_fct(self.corners[i], spoint, axis)
  
        self.project()        
        self.sort()

    def rot_fct(self, vec, spoint,axis):
        #fct that gets the new coords for a vec rotated around an arbitray axis
        #no good from http://inside.mines.edu/fs_home/gmurray/ArbitraryAxisRotation/
        x = vec[0]
        y = vec[1]
        z = vec[2]
        a = spoint[0]
        b = spoint[1]
        c = spoint[2]
        u = axis[0]
        v = axis[1]
        w = axis[2]
        L = u*u+v*v+w*w
        self.set_rotation_speed()
        alpha = self.rotation_speed
        vec[0] = ((a*(v*v+w*w)-u*(b*v+c*w-u*x-v*y-w*z))*(1-math.cos(alpha))+L * x * math.cos(alpha) + math.sqrt(L)*(-c*v+b*w-w*y+v*z)*math.sin(alpha))/float(L)
        vec[1] = ((b*(u*u+w*w)-v*(a*u+c*w-u*x-v*y-w*z))*(1-math.cos(alpha))+L * y * math.cos(alpha) + math.sqrt(L)*( c*u-a*w+w*x-u*z)*math.sin(alpha))/float(L)
        vec[2] = ((c*(u*u+v*v)-w*(a*u+b*v-u*x-v*y-w*z))*(1-math.cos(alpha))+L * z * math.cos(alpha) + math.sqrt(L)*(-b*u+a*v-v*x+u*y)*math.sin(alpha))/float(L)
        return vec
        
    def set_rotation_speed(self):
        self.rotation_speed = ROTSPEED
        
    def rotate(self, angle_vec):
        #first i need to move the center of the cube into the origin, then rotate then move back
        self.into_origin()

        for i in range(8):
            if angle_vec[0] != 0:
                self.corners[i] = self.xrot(self.corners[i], angle_vec[0])
            if angle_vec[1] != 0:
                self.corners[i] = self.yrot(self.corners[i], angle_vec[1])        
            if angle_vec[2] != 0:
                self.corners[i] = self.zrot(self.corners[i], angle_vec[2])
                
        self.push_back()
        self.project()        
        self.sort()

    
    def into_origin(self):
        #translate box into origin for rotation        
        for i in range(8):
            for ii in range(3):
                self.corners[i][ii] = self.corners[i][ii] - self.center[ii]
            
    def push_back(self):
        #transaltes the box back after rotation
        for i in range(8):
            for ii in range(3):
                self.corners[i][ii] = self.corners[i][ii] + self.center[ii]
        
    def test(self):
        test_vec = [ 25, 25, 25]
        test_vec_2 = [0, 0, 0]
        angle = math.pi/4.
        print self.v_len(test_vec,test_vec_2)
        print test_vec
        test_vec = self.xrot(test_vec, angle)
        print self.v_len(test_vec,test_vec_2)
        print test_vec
        
    def xrot(self, vec, phi):
        #rotation around x axis
        x1 = vec[0]
        y1 = vec[1]
        z1 = vec[2]
        x = 1 * x1
        y = math.cos(phi) * y1 - math.sin(phi) * z1
        z = math.sin(phi) * y1 + math.cos(phi) * z1
        return [x,y,z]

    def yrot(self, vec, phi):
        #rotation around y axis
        x1 = vec[0]
        y1 = vec[1]
        z1 = vec[2]
        x = math.cos(phi) * x1 + math.sin(phi) * z1
        y = y1
        z = -math.sin(phi) * x1 + math.cos(phi) * z1
        return [x,y,z]
    
    def zrot(self, vec, phi):
        #rotation around z axis
        x1 = vec[0]
        y1 = vec[1]
        z1 = vec[2]
        x = math.cos(phi) * x1 - math.sin(phi) * y1
        y = math.sin(phi) * x1 + math.cos(phi) * y1
        z = z1
        return [x,y,z]
    
    def project(self):
        #projects the 3d data points into the y-z plane, i guess that x is just used to order them
        #idea is to use just the y and z coords of each data point
        #use x to draw first back, right, left, bottom, top, front
        self.yellow = [[self.corners[0][1],self.corners[0][2]],[self.corners[1][1],self.corners[1][2]],[self.corners[2][1],self.corners[2][2]],[self.corners[3][1],self.corners[3][2]]]        
        self.white = [[self.corners[4][1],self.corners[4][2]],[self.corners[5][1],self.corners[5][2]],[self.corners[6][1],self.corners[6][2]],[self.corners[7][1],self.corners[7][2]]]
        self.red = [[self.corners[0][1],self.corners[0][2]],[self.corners[4][1],self.corners[4][2]],[self.corners[7][1],self.corners[7][2]],[self.corners[3][1],self.corners[3][2]]]
        self.orange = [[self.corners[1][1],self.corners[1][2]],[self.corners[2][1],self.corners[2][2]],[self.corners[6][1],self.corners[6][2]],[self.corners[5][1],self.corners[5][2]]]
        self.green = [[self.corners[3][1],self.corners[3][2]],[self.corners[7][1],self.corners[7][2]],[self.corners[6][1],self.corners[6][2]],[self.corners[2][1],self.corners[2][2]]]
        self.blue = [[self.corners[0][1],self.corners[0][2]],[self.corners[1][1],self.corners[1][2]],[self.corners[5][1],self.corners[5][2]],[self.corners[4][1],self.corners[4][2]]]
        
    def draw(self, canvas):
        #it needs to draw in the right order...
        #canvas.draw_polygon(point_list, line_width, line_color, fill_color = color)
        for i in self.order:
            if i == 'y':
                canvas.draw_polygon(self.yellow,self.line_thickness,'black','yellow')
            elif i == 'b':
                canvas.draw_polygon(self.blue,self.line_thickness,'black','blue')
            elif i == 'o':
                canvas.draw_polygon(self.orange,self.line_thickness,'black','orange')
            elif i == 'r':
                canvas.draw_polygon(self.red,self.line_thickness,'black','red')
            elif i == 'g':
                canvas.draw_polygon(self.green,self.line_thickness,'black','green')
            elif i == 'w':
                canvas.draw_polygon(self.white,self.line_thickness,'black','white')

        self.tilt_ctr += 1
        if self.tilt_ctr % 1 == 0:
            #self.rotate([random.randrange(0,2)*math.pi/180,random.randrange(0,2)*math.pi/180.,random.randrange(0,2)* math.pi/180])
            self.tilt_ctr = 0

class rubics:
    def __init__(self):
    #consists of 26 cubes, has 7 rotational points.
        size = 100
        offset = [0, 150, 150]
        c0 = cube([0, offset[1] + 0     , offset[2] + 0     ], size)
        c1 = cube([0, offset[1] + size  , offset[2] + 0     ], size)
        c2 = cube([0, offset[1] + 2*size, offset[2] + 0     ], size)
        c3 = cube([0, offset[1] + 0     , offset[2] + size  ], size)
        c4 = cube([0, offset[1] + size  , offset[2] + size  ], size)
        c5 = cube([0, offset[1] + 2*size, offset[2] + size  ], size)
        c6 = cube([0, offset[1] + 0     , offset[2] + 2*size], size)
        c7 = cube([0, offset[1] + size  , offset[2] + 2*size], size)
        c8 = cube([0, offset[1] + 2*size, offset[2] + 2*size], size)

        c9  = cube([size, offset[1] + 0     , offset[2] + 0], size)
        c10 = cube([size, offset[1] + size  , offset[2] + 0], size)
        c11 = cube([size, offset[1] + 2*size, offset[2] + 0], size)
        c12 = cube([size, offset[1] + 0     , offset[2] + size], size)
        c13 = cube([size, offset[1] + size  , offset[2] + size], size)
        c14 = cube([size, offset[1] + 2*size, offset[2] + size], size)
        c15 = cube([size, offset[1] + 0     , offset[2] + 2*size], size)
        c16 = cube([size, offset[1] + size  , offset[2] + 2*size], size)
        c17 = cube([size, offset[1] + 2*size, offset[2] + 2*size], size)

        c18  = cube([2*size, offset[1] + 0     , offset[2] + 0], size)
        c19 = cube([2*size, offset[1] + size  , offset[2] + 0], size)
        c20 = cube([2*size, offset[1] + 2*size, offset[2] + 0], size)
        c21 = cube([2*size, offset[1] + 0     , offset[2] + size], size)
        c22 = cube([2*size, offset[1] + size  , offset[2] + size], size)
        c23 = cube([2*size, offset[1] + 2*size, offset[2] + size], size)
        c24 = cube([2*size, offset[1] + 0     , offset[2] + 2*size], size)
        c25 = cube([2*size, offset[1] + size  , offset[2] + 2*size], size)
        c26 = cube([2*size, offset[1] + 2*size, offset[2] + 2*size], size)


        self.elements = [c0,c1,c2,c3,c4,c5,c6,c7,c8,c9,c10,c11,c12,c13,c14,c15,c16,c17,c18,c19,c20,c21,c22,c23,c24,c25,c26]
        
        #define the rotational points
        self.rot_yellow = [1/2.*size,offset[1]+ 3/2.*size,offset[2]+ 3/2.*size]
        self.rot_white  = [5/2.*size,offset[1]+ 3/2.*size,offset[2]+ 3/2.*size]
        self.rot_orange = [3/2.*size,offset[1]+ 5/2.*size,offset[2]+ 3/2.*size]
        self.rot_red    = [3/2.*size,offset[1]+ 1/2.*size,offset[2]+ 3/2.*size]
        self.rot_blue   = [3/2.*size,offset[1]+ 3/2.*size,offset[2]+ 1/2.*size]
        self.rot_green  = [3/2.*size,offset[1]+ 3/2.*size,offset[2]+ 5/2.*size]
  
        #put them in one list
        self.rot_point_list = [self.rot_yellow,self.rot_red,self.rot_blue,self.rot_orange,self.rot_green,self.rot_white]
        
        self.rot_center = [3/2.*size,offset[1]+ 3/2.*size,offset[2]+ 3/2.*size]
                           
        self.set_rotation_center(self.rot_center)
        self.print_order = []
        self.sort_cubes()
        
        self.right_angle = [0,math.pi/4., 0]
        
    def xrot(self, vec, phi):
        #rotation around x axis
        x1 = vec[0]
        y1 = vec[1]
        z1 = vec[2]
        x = 1 * x1
        y = math.cos(phi) * y1 - math.sin(phi) * z1
        z = math.sin(phi) * y1 + math.cos(phi) * z1
        return [x,y,z]

    def yrot(self, vec, phi):
        #rotation around y axis
        x1 = vec[0]
        y1 = vec[1]
        z1 = vec[2]
        x = math.cos(phi) * x1 + math.sin(phi) * z1
        y = y1
        z = -math.sin(phi) * x1 + math.cos(phi) * z1
        return [x,y,z]
    
    def zrot(self, vec, phi):
        #rotation around z axis
        x1 = vec[0]
        y1 = vec[1]
        z1 = vec[2]
        x = math.cos(phi) * x1 - math.sin(phi) * y1
        y = math.sin(phi) * x1 + math.cos(phi) * y1
        z = z1
        return [x,y,z]    
        
    def draw(self,canvas):
        for i in self.print_order:
            self.elements[i].draw(canvas)

    def into_origin(self, vec):
        #translate box into origin for rotation        
        for i in range(3):
           vec[i] = vec[i] - self.rot_center[i]
        return vec
            
    def push_back(self, vec):
        #transaltes the box back after rotation
        for i in range(3):
           vec[i] = vec[i] + self.rot_center[i]
        return vec
    
    def rotate_vector(self, vec, angle_vec):
        vec = self.into_origin(vec)
        if angle_vec[0] != 0:
            vec = self.xrot(vec, angle_vec[0])
        if angle_vec[1] != 0:
            vec = self.yrot(vec, angle_vec[1])
        if angle_vec[2] != 0:
            vec = self.zrot(vec, angle_vec[2])            
        return self.push_back(vec)
            
    def rotate(self, angle_vec):
        for cube in self.elements:
            cube.rotate(angle_vec)
        for i in range(6):
            self.rot_point_list[i] = self.rotate_vector(self.rot_point_list[i],angle_vec)
        self.sort_cubes()
        
    def get_rotation_group(self, rot_point, axis):
        #if one rotation point is selected this will dynamically find the 9 cubes that have to rotate
        #the idea is, that i use a connection vecotr orthoganol on axis to find the center of the next cube
        ctr = 0
        group = []
        distance_list = []
        #maybe i need to simply find the cubes furthest away...
        for cube in self.elements:
            center = cube.get_center_coords()
            vec = [center[0] - rot_point[0],center[1] - rot_point[1],center[2] - rot_point[2]]
            #if vec != axis: #ignore the center one!
            distance_list.append(math.sqrt(self.vec_prod(vec,vec)))            
        l = list(distance_list)
        l.sort()
        l.reverse()
        for i in range(9):
            for ii in range(27):
                if l[i] == distance_list[ii]:
                    group.append(ii)   
                    distance_list[ii] = -1
                    break  
        return group
    
    def vec_prod(self, vec1, vec2):
        return vec1[0]*vec2[0]+vec1[1]*vec2[1]+vec1[2]*vec2[2]
            
    def rotate_axis(self, rot_pointer):
        rot_point = self.rot_point_list[rot_pointer]

        axis = [rot_point[0] - self.rot_center[0],rot_point[1] - self.rot_center[1],rot_point[2] - self.rot_center[2]]
        rot_group = self.get_rotation_group(rot_point, axis)
        for i in rot_group:
            self.elements[i].rotate_around_axis(rot_point,axis) 
        self.set_rotation_center(self.rot_center)
        self.sort_cubes()
            
    def set_rotation_center(self, center):
        for cube in self.elements:
            cube.set_rotation_point(center)
    
    def print_cubes(self):   
        for cube in self.elements:
            cube.print_corners()
  
    def sort_cubes(self):
    #this will sort the cubes depending on the left corners x position(depth) for right order drawing         
        depths = []
        for cube in self.elements:
            depths.append(cube.get_depth())
        l = list(depths)
        l.sort()
        self.print_order = []		
        
        for i in range(len(l)):
            for ii in range(len(l)):
                if depths[ii] == l[i]:
                    self.print_order.append(ii)

#create the rubics cube
rc = rubics()
            

#mouse handler
def mouse_handler(pos):
    global oldpos
    if oldpos[0] == -1:
        oldpos = pos
    else:
        z_change = oldpos[0] - pos[0]
        y_change = oldpos[1] - pos[1]
        rc.rotate([0,  y_change * math.pi/360., -z_change * math.pi/360.])
            
        oldpos = pos
        
def mouse_click_handler(pos):
    global oldpos, not_clicked, rotation_axis
    oldpos = [-1,0]
    not_clicked = False
    if pos[1] < 45:
        #clicked into the active site
        x = pos[0]
        for i in range(6):
            if x > 130 + i * shift and x < 160 + i * shift:
                rotation_axis = i
        
        if x > 130 + 6 * shift and x < 160 + 6 * shift:
            rotate_up()        

        if x > 130 + 7 * shift and x < 160 + 7 * shift:
            rotate_down()        
    
#timer and buttons    
def rotate_cube_timer():
        rc.rotate([math.pi/360., math.pi/360., math.pi/360.])
        
def rot():
    rotate_timer.start()
    
def rot_stop():
    rotate_timer.stop()
  

def rotate_up():
    global rotation_axis, ROTSPEED
    rotate_timer_axis.start()
    ROTSPEED = -math.pi/8.

def rotate_down():
    global rotation_axis, ROTSPEED
    rotate_timer_axis.start()
    ROTSPEED = math.pi/8.

def rotate_cube_timer_axis():
    global rot_ctr
    if rot_ctr < 4:
        rc.rotate_axis(rotation_axis)
        rot_ctr += 1
    else:
        rot_ctr = 0
        rotate_timer_axis.stop()

def next_side():
    global rotation_axis
    rotation_axis += 1
    rotation_axis %= 6
    
def former_side():
    global rotation_axis
    rotation_axis -= 1
    rotation_axis %= 6    

def key_down(key):
    if key == simplegui.KEY_MAP['down']:
        if not rotate_timer_axis.is_running():
            rotate_down()
    elif key == simplegui.KEY_MAP['up']:
        if not rotate_timer_axis.is_running():
            rotate_up()
    elif key == simplegui.KEY_MAP['right']:
        if not rotate_timer_axis.is_running():
            next_side()
    elif key == simplegui.KEY_MAP['left']:
        if not rotate_timer_axis.is_running():
            former_side()
    
def reset():
    global rc
    rc = 0 
    rc = rubics()
 
def shuffle_timer_fct():
    global rotation_axis, shuffle_steps
    shuffle_steps += 1
    rotation_axis = random.randrange(6)
    if random.randrange(2) == 0:
        rotate_up()
    else:
        rotate_down()
    if shuffle_steps == 20:
        shuffle_timer.stop()
        rot_stop()
        shuffle_steps = 0
      
def shuffle():
    rot()
    shuffle_timer.start()
    
# Handler to draw on canvas
def draw(canvas):
    rc.draw(canvas)
    for i in range(6):
        if i == rotation_axis:
            canvas.draw_polygon([[130+i*shift, 10], [160+i*shift, 10], [160+i*shift, 40], [130+i*shift, 40]], 5, 'Purple', colors[i])
        else:
            canvas.draw_polygon([[130+i*shift, 10], [160+i*shift, 10], [160+i*shift, 40], [130+i*shift, 40]], 5, 'Black', colors[i])
    i = 6    
    canvas.draw_polygon([[130+i*shift, 10], [160+i*shift, 10], [160+i*shift, 40], [130+i*shift, 40]], 5, 'Black', colors[i])
    canvas.draw_polygon([[118+7*shift, 10], [170+7*shift, 10], [170+7*shift, 40], [118+7*shift, 40]], 5, 'Black', colors[i])
 
    canvas.draw_text('Rotation Axis', (10, 30), 20, 'Purple')
    canvas.draw_text('UP', (495, 30), 15, 'Purple')
    canvas.draw_text('DOWN', (540, 30), 15, 'Purple')
    if shuffle_steps != 0:
        canvas.draw_text('SHUFFLE!!!', (450, 500), 30, 'Black')
        canvas.draw_text(str(20-shuffle_steps), (500, 550), 50, 'Black')

    
# Create a frame and assign callbacks to event handlers
frame = simplegui.create_frame("Home", 600, 600)
frame.add_button("Auto Rotation", rot)
frame.add_button("Stop Rotation", rot_stop)

frame.add_button("Shuffle!", shuffle)


frame.add_button("Rotate Up", rotate_up)
frame.add_button("Rotate Down", rotate_down)
frame.add_button("Next Axis", next_side)
frame.add_button("Last Axis", former_side)

frame.add_button("Reset", reset)

frame.set_draw_handler(draw)
frame.set_canvas_background('grey')
frame.set_mousedrag_handler(mouse_handler)
frame.set_mouseclick_handler(mouse_click_handler)
rotate_timer = simplegui.create_timer(50, rotate_cube_timer)
rotate_timer_axis = simplegui.create_timer(25, rotate_cube_timer_axis)
shuffle_timer = simplegui.create_timer(1000, shuffle_timer_fct)

frame.set_keydown_handler(key_down)

label = frame.add_label(label)
# Start the frame animation
frame.start()

