#
# SIMULATION DE CIRCUITS LOGIQUE
# CE CIRCUIT MONTRE UNE FONCTION LOGIQUE ET
# VOTRE MISSION: TRANSFORMER CE CODE
# POUR CABLER UNE FONCTION LOGIQUE OU
# BON COURAGE ...

import turtle
tortue = turtle.Turtle()
#tortue.ht()

# VOUS DEVEZ ICI CHANGER L'ETAT DE L'INTERRUPTEUR
# False ou True SONT LES DEUX VALEURS ADMISES
interrupteur = False
interrupteur2 = False
lampe = interrupteur and interrupteur2

tortue.setpos( -105 , 30 )
tortue.write("INT1 = "+str(int(interrupteur)))

tortue.setpos( -10 , 30 )
tortue.write("INT2 = "+str(int(interrupteur2)))

tortue.setpos( 80 , 30 )
tortue.write("LAMPE = "+str(int(lampe)))

tortue.setpos( -160 , 0 )
#premier trait
tortue.forward(50)

tortue.color('red')
#interrupteur
if interrupteur == False:
  tortue.left(25)
  tortue.forward(50)
  tortue.right(25)
else:
  tortue.forward(50)
  
tortue.color('black')

#2nd trait
tortue.setpos( -60 , 0 )
tortue.forward(50)
#interrupteur2
tortue.color('red')
if interrupteur2 == False:
  tortue.left(25)
  tortue.forward(50)
  tortue.right(25)
else:
  tortue.forward(50)
  
tortue.color('black')

#3eme trait
tortue.setpos(40 , 0 )
tortue.forward(50)
#lampe
tortue.setpos( 110 , -20 )
if lampe:
  tortue.color('yellow')
else:
  tortue.color('grey')
  
tortue.begin_fill()
tortue.circle(20)
tortue.end_fill()
tortue.color('black')
tortue.circle(20)
tortue.setpos( 130 , 0 )

#dernier trait
tortue.forward(50)
tortue.ht()




