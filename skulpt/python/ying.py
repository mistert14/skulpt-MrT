#
import turtle

t = turtle.Turtle()
t.ht()

radius = 150
color1 = "black"
color2 = "white"

t.color(color1)
t.begin_fill()
t.circle(radius/2., 180)
t.circle(radius, 180)
t.left(180)
t.circle(-radius/2., 180)
t.color(color1)
t.left(90)
t.up()
t.forward(radius*0.375)
t.end_fill()
t.right(90)
t.down()
t.color(color2)
t.begin_fill()
t.circle(radius*0.125)
t.end_fill()
t.left(90)
t.up()
t.backward(radius*0.375)
t.down()
t.left(90)

# A VOUS DE POURSUIVRE CE DESSIN BIEN CONNU
