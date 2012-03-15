import re
def c(w,v):
 x,e,d=w;g,h=v;g=int(g);i=len(h)
 if d:
  if x>=g:x,e=x-g,e+h
 else:
  if x[:i]==h:x,e=x[i:],e+g
 return x,e,d
for x in __import__('fileinput').input():
 try:x=int(x),'',1
 except:x=x,0,0
 print reduce(c,re.findall('(\d+)(\D+)','3000MMM2000MM1000M900CM500D400CD300CCC200CC100C90XC50L40XL30XXX20XX10X9IX5V4IV3III2II1I'),x)[1]
