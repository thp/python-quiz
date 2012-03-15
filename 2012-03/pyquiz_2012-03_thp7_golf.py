import re
def c(w,v):
 t,h,p=w;g,j=v;g=int(g);i=len(j)
 while p and t>=g:t,h=t-g,h+j
 while 1-p and t[:i]==j:t,h=t[i:],h+g
 return t,h,p
for x in __import__('fileinput').input():
 try:x=int(x),'',1
 except:x=x,0,0
 print reduce(c,re.findall('(\d+)(\D+)',
'1000M900CM500D400CD100C90XC50L40XL10X9IX5V4IV1I'),x)[1]
