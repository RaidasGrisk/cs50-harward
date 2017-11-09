"""
CS50:          https://cs50.harvard.edu/weeks
Problem set 6: https://docs.cs50.net/2017/x/psets/6/pset6.html
Problem 3:     https://docs.cs50.net/problems/credit/credit.html

The code asks user to provide credit card number and checks its validity (using Hans Peter Luhn algo) as well as type.
More on algorithm: https://en.wikipedia.org/wiki/Luhn_algorithm
"""

# prompt for input
while True:
    print('Number: ', end='')
    number = input()
    if len(str(number)) == 15 and str(number).isdigit():
        break

# convert number into a list of numbers
number_list = [int(digit) for digit in str(number)]

# two list to store intermediate results
times_two = []
times_one = []

# do calculations
for digit_id in range(len(number_list)):

    # if odd
    if digit_id % 2 != 0:

        # if product is two digit
        if number_list[digit_id] * 2 >= 10:
            times_two.append(int((number_list[digit_id] * 2) / 10))
            times_two.append((number_list[digit_id] * 2) % 10)

        # if product is one digit
        else:
            times_two.append(number_list[digit_id] * 2)

    # if even
    else:
        times_one.append(number_list[digit_id])

# print result
card_id = int(str(number_list[0]) + str(number_list[1]))
if (sum(times_one) + sum(times_two)) % 10 != 0:
    print('INVALID')
elif card_id == 34 or 37:
    print('AMEX')
elif card_id == 4:
    print('VISA')
else:
    print('MASTERCARD')