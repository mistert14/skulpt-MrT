#
import turtle

t = turtle.Turtle()
t.ht()
#DECLARATION DES VARIABLES ENTREES ET SORTIE
# porte fermee -> porte = True
# porte ouverte -> porte = False
porte = True
fenetre = True
sirene = not(porte) or not(fenetre)

#DESSIN DE LA SIRENE
#ROUGE = Sirene a 0
#BLEU = Sirene a 1

if sirene == True:
  t.color('red')
else:
  t.color('blue')
t.setpos(50,0)
t.begin_fill()
t.circle(24)
t.end_fill()
t.color('white')
t.setpos(50,20)
t.begin_fill()
t.circle(5)
t.end_fill()

#t.goto(4,4)

#DESSIN DE LA PORTE EN FONCTION DE LA VARIABLE porte
t.color('blue')
t.setpos(-250,0)
t.left(90)
t.forward(90)
t.right(90)
t.forward(45)
t.right(90)
t.forward(90)
t.right(90)
t.forward(45)
if (porte == False):
   t.left(270)
   t.forward(90)
   t.right(75)
   t.forward(45)
   t.right(105)
   t.forward(90)
   t.right(75)
   t.forward(45)
print "A vous de jouer"

# DESSIN DE LA FENETRE EN FONCTION DE LA VARIABLE fenetre
# A REALISER PAR VOS SOINS
# DESSINE LE CADRE DE FENETRE
# AJOUTER UN CADRE EN PERSPECDTIVE 3D POUR MONTRER
# LA FENETRE OUVERTE SI fenetre = False 
# VOIR LE CODE POUR LA PORTE


