from bowling import *
from bowling_small import *
from bowling_golf import *

from nose.tools import *

# from http://pyug.at/PythonDojo/KataBowling
TEST_CASES = (
    ('X X X X X X X X X X X X', 300),
    ('9-9-9-9-9-9-9-9-9-9-', 90),
    ('5/5/5/5/5/5/5/5/5/5/5', 150),
    ('X7/729/XXX236/7/3', 168),
    ('--------------------', 0),
    ('-1 27 3/ X  5/ 7/ 34 54 -- X  7-', 113),
    ('X  7/ 9- X  -8 8/ -6 X  X  X  81', 167),
    ('', 0),
)

FUNCTIONS = (
    calculate_score,
    calculate_score_small,
    calculate_score_golf,
)

def test_cases_bowling():
    def test_case(func, rolls, score):
        eq_(func(rolls), score)

    for func in FUNCTIONS:
        for rolls, score in TEST_CASES:
            yield test_case, func, rolls, score
