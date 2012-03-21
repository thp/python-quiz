
import fileinput
import _roman as roman

for line in fileinput.input():
    print roman.decode(line.strip())

