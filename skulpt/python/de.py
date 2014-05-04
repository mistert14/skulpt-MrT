#modules importes

import document
import turtle
import random

#creation de la tortue
t = turtle.Turtle()
#calcul de l'etat des points
de = 1 + random.randrange(0,6)
dessin=[False,False,False,False,False,False,False]
dessin[3] = (de % 2 == 1)
dessin[0] = (de >= 4 ); dessin[6] = (de >= 4)
dessin[1] = (de >= 2 ); dessin[5] = (de >= 2)
dessin[2] = (de == 6); dessin[4] = (de == 6)

print de, dessin
  
#dessiner les sorties
mx = 30
x = [-mx,mx,-mx, 0,mx,-mx, mx]
y = [ mx,mx,  0, 0, 0,-mx,-mx]
t.setpos(-60, 70)
for i in range(4):
  t.forward(120)
  t.right(90)

for i in range(7):
  if dessin[i]:
    t.setpos(x[i], y[i])
    t.begin_fill()
    t.circle(7)
    t.end_fill()

t.ht()

  
  





