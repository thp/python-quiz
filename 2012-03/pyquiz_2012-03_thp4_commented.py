import fileinput

# Single values (1, 50, 10, 50, 100, 500, 1000)
a = [((1+4*(i%2))*10**(i/2), 'IVXLCDM'[i]) for i in range(7)]

# Double/triple values (II, III, XX, ...)
a += [(x*c, y*c) for x, y in a for c in [2,3] if y in'IXCM']

# Subtraction values (IV, IX, ...)
a += [(a[x+1][0]-a[x/2*2][0], a[x/2*2][1]+a[x+1][1]) for x in range(6)]

# Sort, highest value first
a.sort(reverse=True)

def first(input_value):
    try:
        return int(input_value), '', True
    except ValueError:
        return input_value, 0, False

def step(intermediate, current_try):
    input_value, output_value, arabic = intermediate
    avalue, rvalue = current_try

    if arabic and input_value >= avalue:
        input_value -= avalue
        output_value += rvalue

    if not arabic and input_value.startswith(rvalue):
        input_value = input_value[len(rvalue):]
        output_value += avalue

    return input_value, output_value, arabic

for input_value in fileinput.input():
    rest, result, arabic = reduce(step, a, first(input_value))
    assert ((rest == 0) or (rest.strip() == ''))
    print result

