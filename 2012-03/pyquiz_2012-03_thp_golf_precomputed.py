import re;a=[(int(x),y)for x,y in re.findall('(\d+)(\D+)','1000M900CM500D400CD100C90XC50L40XL10X9IX5V4IV1I')]
def c(n):
 x=n and int(i)or i
 for y,z in a:
  while (n and x>=y)or(not n and x[:len(z)]==z):yield(n and z or y);x=(x-y)if n else x[len(z):]
for i in filter(None,map(str.strip,__import__('fileinput').input())):print reduce(lambda d,e:d+e,c(i.isdigit()))
