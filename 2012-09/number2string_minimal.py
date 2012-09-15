e=enumerate;f=lambda n,m='.',s=',':s.join(a if p else''.join(m*(i and(len(a)-i)%3==0)+c for i,c in e(a))for p,a in e(n.split('.')))
if __name__=='__main__':print'\n'.join(f(n.strip())for n in __import__('fileinput').input())
