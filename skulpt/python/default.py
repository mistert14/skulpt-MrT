import mistert
import document

print mistert.doc()
geom = []
geom.append(mistert.Geometrie(-55,20,45,'blue','blue',True))
geom.append(mistert.Geometrie(0,20,45,'black','blue',True))
geom.append(mistert.Geometrie(55,20,45,'red','blue',True))
geom.append(mistert.Geometrie(-30,0,45,'yellow','blue',True))
geom.append(mistert.Geometrie(30,0,45,'green','blue',True))

ch = document.getElementById('chk')
print ch.checked

for geo in geom:
     geo.cercle(25, False)
     if ch.checked == 'True':
         geo.cacher()
