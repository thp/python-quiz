# pyquiz_2012-03_thp9_yield.py
# Thomas Perl <m@thp.io>; 2012-03-21

import fileinput


class Converter:
    PAIRS = [
        (1000, 'M'), (900, 'CM'), (500, 'D'), (400, 'CD'),
        (100, 'C'), (90, 'XC'), (50, 'L'), (40, 'XL'),
        (10, 'X'), (9, 'IX'), (5, 'V'), (4, 'IV'), (1, 'I')
    ]
    TRANSLATE = {}

    def step(remainder, pairs):
        for arabic, roman in pairs:
            while remainder >= arabic:
                remainder -= arabic
                yield roman

    for arabic in range(1, 4000):
        result = ''.join(step(arabic, PAIRS))
        TRANSLATE.update({str(arabic): result, result: arabic})

    @classmethod
    def convert(cls, value):
        return cls.TRANSLATE[value.strip()]

if __name__ == '__main__':
    for line in fileinput.input():
        print(Converter.convert(line))
