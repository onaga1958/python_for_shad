# https://en.wikipedia.org/wiki/Collatz_conjecture

current_number = int(raw_input("Enter starting number> "))

while current_number != 1:
    if current_number % 2 == 0:
        current_number /= 2
    else:
        current_number = 3 * current_number + 1

    print current_number,

print
print "Success!"
