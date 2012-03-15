import re
def c(w,v):
 t,h,p=w;g,j=v;g=int(g);i=len(j)
 if p:
  if t>=g:t,h=t-g,h+j
 else:
  if t[:i]==j:t,h=t[i:],h+g
 return t,h,p
for x in __import__('fileinput').input():
 try:x=int(x),'',1
 except:x=x,0,0
 print reduce(c,re.findall('(\d+)(\D+)','3000MMM2000MM1000M900CM500D400CD300CCC200CC100C90XC50L40XL30XXX20XX10X9IX5V4IV3III2II1I'),x)[1]
