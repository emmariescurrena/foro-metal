"""Mathematical operations functions"""


def add(*numbers):
    """Sums undefined quantity of numbers"""

    total = 0
    for n in numbers:
        total += n

    return total


def substract(*numbers):
    """
    Substract undefined quantity of numbers. To sum a number, add a '-'
    before it (-15)
    """

    total = 0
    for n in numbers:
        total -= n

    return total


def multiply(*numbers):
    """Multiplies undefined quantity of numbers"""

    total = 1
    for n in numbers:
        total *= n

    return total


def divide(*numbers):
    """
    Divides undefined quantity of numbers. The first number is divided by the
    others
    """

    total = numbers[0]
    for n in numbers[1:]:
        total /= n

    return total
