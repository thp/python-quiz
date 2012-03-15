a=[((1+4*(i%2))*10**(i/2),'IVXLCDM'[i])for i in range(7)];a+=[(x*c,y*c)for x,y in a[::2]for c in[2,3]]+[(a[x+1][0]-a[x/2*2][0],a[x/2*2][1]+a[x+1][1])for x in range(6)];a.sort(reverse=1)
def c(w,v):
 x,e,d=w;g,h=v;i=len(h)
 if d:
  if x>=g:x,e=x-g,e+h
 else:
  if x[:i]==h:x,e=x[i:],e+g
 return x,e,d
for x in __import__('fileinput').input():
 try:x=int(x),'',1
 except:x=x,0,0
 print reduce(c,a,x)[1]
