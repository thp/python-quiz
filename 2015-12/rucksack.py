import itertools
import collections


Item = collections.namedtuple('Item', ['value', 'weight'])


def rucksack(items, max_weight):
    # Generate all possible candidate solutions
    def guess():
        for i in range(1, len(items)+1):
            for candidate in itertools.permutations(items, i):
                yield candidate

    # Check if a candidate solution fulfills our constraint
    def check(candidate):
        return sum(item.weight for item in candidate) <= max_weight

    # Determine the total value of a candidate solution
    def valuate(candidate):
        return sum(item.value for item in candidate)

    # Return the valid candidate solution that maximizes the value
    return list(max((candidate for candidate in guess() if check(candidate)),
                    key=valuate, default=[]))


if __name__ == '__main__':
    print(rucksack([Item(value=4, weight=5), Item(value=3, weight=5)], 10))
