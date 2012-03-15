import fileinput as f;r=range;a=[((1+4*(i%2))*10**(i/2),'IVXLCDM'[i])for i in r(7)];a+=[(x*c,y*c)for x,y in a for c in[2,3]if y in'IXCM']+[(a[x+1][0]-a[x/2*2][0],a[x/2*2][1]+a[x+1][1])for x in r(6)];a.sort(reverse=1)
def g(a):
 global x;y,z=a
 if(n and x<y)or not(n or x.startswith(z)):y,z=0,''
 x,r=n and(x-y,z)or(x[len(z):],y);return r
for x in f.input():
 try:x,n=int(x),1
 except:n=0
 print reduce(lambda d,e:d+e,map(g,a))
