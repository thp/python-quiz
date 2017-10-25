from bowling import *

from nose.tools import *


def test_cases():
    # from http://pyug.at/PythonDojo/KataBowling
    TEST_CASES = (
        ('XXXXXXXXXXXX', 300),
        ('9-9-9-9-9-9-9-9-9-9-', 90),
        ('5/5/5/5/5/5/5/5/5/5/5', 150),
        ('X7/729/XXX236/7/3', 168),
        ('--------------------', 0),
        ('-1273/X5/7/3454--X7-', 113),
        ('X7/9-X-88/-6XXX81', 167),
    )

    def test_case(rolls, score):
        eq_(calculate_score(rolls), score)

    for rolls, score in TEST_CASES:
        yield test_case, rolls, score
