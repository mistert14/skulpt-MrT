import turtle
tortue = turtle.Turtle()
tortue.ht()
#tortue.pu()
tortue.setpos( -150 , -80 )
tortue.color('blue')
tortue.begin_fill()

for _ in range(4):
    tortue.left(90)
    tortue.forward(80)
tortue.end_fill()
tortue.forward(80)
for _ in range(4):
    tortue.left(90)
    tortue.forward(80)
tortue.forward(80)    
tortue.color('red')
tortue.begin_fill()
for _ in range(4):
    tortue.left(90)
    tortue.forward(80)
tortue.end_fill()
