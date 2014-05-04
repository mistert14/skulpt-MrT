#modules importes

import document
import turtle

#creation de la tortue
t = turtle.Turtle()

#recupere l'état des cases a cocher
nbits = 3
poids = [128, 64, 32, 16, 8, 4, 2, 1]
inp = [False, False, False, False, False, False, False, False]
for i in range(nbits):
  c = chr(65+i)
  inp[i] = (document.getElementById(c).checked) == 'True';

#calcul equivalent decimal des entrees
valeur = 0
for i in range(nbits):
  valeur += poids[i]* int(inp[i])
print valeur

#equation de la lampe  
lampe = inp[2] and (not(inp[1]) or not(inp[0]))
print "LAMPE: "+str(lampe)

#dessiner les entrées
pos = (500. - (nbits) * 30.) / len(inp)
t.setpos(-250+int(pos), 100)
print len(inp)
t.color('black')
for i in range(nbits):
  if inp[i]:
    t.color('green')
  else:
    t.color('red')
  t.setpos(-116 + int(pos)*i, 130)
  t.write(chr(65+i))
  t.setpos(-112 + int(pos)*i, 100)
  
  t.begin_fill()
  t.circle(10)
  t.end_fill()
#dessiner les sorties
if lampe:
  t.color('green')
else:
  t.color('red')
t.setpos(-118, 30)
t.write('S1')  
t.setpos(-112, 0)
t.begin_fill()
t.circle(10)
t.end_fill()
t.ht()

  
  



