#
# OBJECTIF ICI: INVENTEZ VOTRE LOGO EN UTILISANT
# LES COMMANDES DE TURTLE
# UN EXEMPLE EST DONNE ICI
#

#
import turtle

t = turtle.Turtle()

#TRACER UN ROND ROUGE PLEIN
t.setpos(0, -200)
t.begin_fill()
t.color('red')
t.circle(200)
t.end_fill()

#TRACER LA BOUCHE
t.setpos(-120,-60)
t.color('white')
t.begin_fill()
t.right(90)
t.circle(120,180)
t.end_fill()

#TRACER LES YEUX
t.setpos(-30,60)
t.begin_fill()
t.circle(50)
t.end_fill()

t.setpos(120,60)
t.begin_fill()
t.circle(50)
t.end_fill()

t.ht()
