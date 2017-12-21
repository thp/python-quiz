from itertools import permutations
from hashlib import sha1

groups = ''.join(x for x in open('greeting.dump').readlines() if not x.startswith('#')).strip().split('\n\n')
sha1sum = groups.pop(0)
groups.pop(0)

for ordering in permutations([bytes(int(x, 16) for x in group.split()) for group in groups]):
    candidate = b''.join(ordering)
    if sha1(candidate).hexdigest() == sha1sum:
        open('greeting.py', 'wb').write(candidate)
        break
