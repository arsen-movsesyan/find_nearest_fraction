import math


def get_fractional(number, max_denominator=64):
    integer = number // 1
    fraction = number % 1
    if fraction == 0:
        return [int(integer), 1, 1]
    _list = []
    denominator = 2
    max_d = int(math.log(max_denominator, 2))
    for _ in range(0, max_d):
        numerator = round(fraction * denominator)
        if numerator != 0:
            _list.append((abs(fraction - numerator / denominator), numerator, denominator))
            if (fraction * denominator) % 1 == 0:
                break
        denominator *= 2
    min_fraction = min(_list, key=lambda a: a[0])
    return [int(integer), int(min_fraction[1]), int(min_fraction[2])]


# TEST
decimal = 17.29
