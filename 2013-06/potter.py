#!/usr/bin/python3
# -*- coding: utf-8 -*-

# https://pyug.at/PythonQuiz/2013-06
# http://www.codingdojo.org/cgi-bin/wiki.pl?KataPotter

# One copy of any of the five books costs 8 EUR.
BOOK_PRICE = 8

# If, however, you buy two different books from the series,
# you get a 5% discount on those two books. If you buy 3
# different books, you get a 10% discount. With 4 different
# books, you get a 20% discount. If you go the whole hog,
# and buy all 5, you get a huge 25% discount.
DISCOUNTS = [0, 5, 10, 20, 25]

# Discount factors
DISCOUNT_FACTORS = [1 - (discount / 100) for discount in DISCOUNTS]

def possible_sets(count, max_possible=5):
    """Generate possible combinations of 5 or less books from a count"""

    # Base case: 0 books - we're done
    if count == 0:
        yield []
        return

    # Alternate case: Generate all possible sets
    for p in range(max_possible, 0, -1):
        if count >= p:
            for s in possible_sets(count - p, p):
                yield [p] + s

def sets_price(sets):
    """Price for sets of unique books taking discount into account"""
    return sum(BOOK_PRICE * count * DISCOUNT_FACTORS[count-1]
            for count in sets)

def can_build_sets(sets, basket):
    """Can we build a sets configuration from this basket?"""
    assert sum(sets) == len(basket)

    # Copy lists, as we mutate our copies below
    queue = list(sets)
    remaining = list(basket)

    while queue:
        target_set = queue.pop(0)

        # can build target set from remaining?
        candidates = list(set(remaining))
        if len(candidates) < target_set:
             # Cannot build target set from remaining
            return False

        # Remove only target_set number of books here
        for item in candidates[:target_set]:
            remaining.remove(item)

    return True

def potter(books):
    # Generate all possible sets of books based on the amount of
    # books, then sort them by their price (lowest first) and check
    # if we can build the requested set configuration from the books
    # we have. Return the price for that set.
    for sets in sorted(possible_sets(len(books)), key=sets_price):
        if can_build_sets(sets, books):
            return sets_price(sets)

#def debug(count):
#    for sets in sorted(possible_sets(count), key=sets_price):
#        print('%8.02f' % sets_price(sets), sets)
#debug(8)

basket = [0, 0, 1, 1, 2, 2, 3, 4]
print('%.2f' % potter(basket))

