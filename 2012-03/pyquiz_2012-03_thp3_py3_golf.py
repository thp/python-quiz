import fileinput as f,functools as u;a=[((1+4*(i%2))*10**(i//2),'IVXLCDM'[i])for i in range(7)];a+=[(a[x+1][0]-a[x//2*2][0],a[x//2*2][1]+a[x+1][1])for x in range(6)]
def c(n):
 x=n and int(i)or i
 for y,z in reversed(sorted(a)):
  while(n and x>=y)or(not n and x.startswith(z)):yield(n and z or y);x=((x-y)if n else x[len(z):])
for i in filter(None,map(str.strip,f.input())):print(u.reduce(lambda d,e:d+e,c(i.isdigit())))
