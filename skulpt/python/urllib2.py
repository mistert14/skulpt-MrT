import urllib2
url = "http://mrt2.no-ip.org/skulpt/python/toto.py"
t = urllib2.urlopen(url)
text =  t.readlines()
s = ""
for t in text:
  s += t
  
print s
