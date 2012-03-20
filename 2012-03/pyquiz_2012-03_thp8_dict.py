import re,fileinput as f
def c(w,v):
 t,h=w;g,j=v;g=int(g)
 while t>=g:t,h=t-g,h+j
 return t,h
d,k={},re.findall('(\d+)(\D+)','1000M900CM500D400CD100C90XC50L40XL10X9IX5V4IV1I')
for i in range(1,4000):x=reduce(c,k,(i,''))[1];d[x]=i;d[str(i)]=x
for x in f.input():print d[x.strip()]
