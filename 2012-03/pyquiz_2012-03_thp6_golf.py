import re
def c(w,v):
 t,h,p=w;g,j=v;g=int(g);i=len(j)
 if p:
  if t>=g:w=t-g,h+j,p
 elif t[:i]==j:w=t[i:],h+g,p
 return w
for x in __import__('fileinput').input():
 try:x=int(x),'',1
 except:x=x,0,0
 print reduce(c,re.findall('(\d+)(\D+)','3000MMM2000MM1000M900CM500D400CD300CCC200CC100C90XC50L40XL30XXX20XX10X9IX5V4IV3III2II1I'),x)[1]
