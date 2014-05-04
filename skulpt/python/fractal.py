import turtle
import random

t = turtle.Turtle()
t.setpos(-200,0)
def fractale(length, depth):
   global t
   if depth == 0:
     t.forward(length)
   else:
     fractale(length/3, depth-1)
     t.right(60)
     fractale(length/3, depth-1)
     t.left(120)
     fractale(length/3, depth-1)
     t.right(60)
     fractale(length/3, depth-1)

fractale(400, 4)

