e=enumerate;f=lambda n,m='.',s=',':s.join(a if p else''.join(m[(i==0)+(len(a)-i)%3:]+c for i,c in e(a))for p,a in e(n.split('.')))
