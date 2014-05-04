import turtle
tortue = turtle.Turtle()
tortue.ht()
print "Hello, I'm turtle"
tortue.setpos( 40 , -80 )
tortue.color('green')

tortue.begin_fill()

n = 3
for _ in range(n):
    tortue.left(360/n)
    tortue.forward(800/n)
    print tortue.pos()
tortue.end_fill()

# TENTEZ DE CHANGER LA COULEUR DU POLYGONE    
# TESTER CE PROGRAMME AVEC n=3,4,5,6,7,360, ...


