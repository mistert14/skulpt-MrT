#
import turtle
radius = 150
t = turtle.Turtle()
t.ht()
t.setpos(0,-130) 

t.color('yellow')
t.begin_fill()
t.circle(radius) 
t.end_fill()
t.setpos(radius,-130)
t.color('white')
t.begin_fill()
t.circle(radius) 
t.end_fill()

t.setpos(100,100)
#
# VOUS DEVEZ MAINTENANT TENTER DE PRODUIRE 
# LES AUTRES FORMES DE LUNE
#
