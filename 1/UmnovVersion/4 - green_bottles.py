# https://en.wikipedia.org/wiki/Ten_Green_Bottles

NUMBERS_WORDS = [
    'no',
    'one',
    'two',
    'three',
    'four',
    'five',
    'six',
    'seven',
    'eight',
    'nine',
    'ten',
]


def bottles_word(bottles_count):
    if bottles_count == 1:
        return "bottle"
    else:
        return "bottles"


def start_line(bottles_count):
    return (NUMBERS_WORDS[bottles_count].title() +
            " green " +
            bottles_word(bottles_count) +
            " hanging on a wall,")


def end_line(bottles_count):
    return ("There'll be " +
            NUMBERS_WORDS[bottles_count] +
            " green " +
            bottles_word(bottles_count) +
            " hanging on a wall,")


bottles_count = 10

while bottles_count > 0:
    for _ in range(2):
        print start_line(bottles_count)
    print "If that one green bottle should accidentally fall,"
    bottles_count -= 1
    print end_line(bottles_count)
