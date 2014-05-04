#
# CE PROGRAMME MONTRE L'UTILITE DES BOUCLES
# ON DESSINNE ICI UN ECHIQUIER
#

import turtle
t = turtle.Turtle()

W = 500.
t.setpos(-250,250)

for i in range(8):
  t.setpos(-250,250-(i)*(W/8.))
  for j in range(8):
    if ((j+ ( i % 2 )) % 2 == 0):
      t.color('blue')
    else:
      t.color('red')
    t.begin_fill()
    for k in range(4):
      print i,j,k
      t.forward(W/8.)
      t.right(90)
    t.end_fill()
    t.forward(W/8.)
  
t.ht()
