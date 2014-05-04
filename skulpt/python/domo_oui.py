#default
import document
import turtle

A = document.getElementById('A').checked
A = (A == 'True') 
print A

import turtle
tortue = turtle.Turtle()
#tortue.ht()

# VOUS DEVEZ ICI CHANGER L'ETAT DE L'INTERRUPTEUR
# False ou True SONT LES DEUX VALEURS ADMISES

lampe = A

tortue.setpos( -65 , 30 )
tortue.write("INT1 = "+str(int(A)))
tortue.setpos( 25 , 30 )
tortue.write("LAMPE = "+str(int(lampe)))

tortue.setpos( -120 , 0 )
tortue.forward(50)
tortue.color('red')
if A == False:
  tortue.left(25)
  tortue.forward(50)
  tortue.right(25)
else:
  tortue.forward(50)
tortue.color('black')  
tortue.setpos( -20 , 0 )
tortue.forward(50)
tortue.setpos( 50 , -20 )
if lampe:
  tortue.color('yellow')
else:
  tortue.color('grey')
  
tortue.begin_fill()
tortue.circle(20)
tortue.end_fill()
tortue.color('black')
tortue.circle(20)
tortue.setpos( 70 , 0 )
tortue.forward(50)
tortue.ht()

#

