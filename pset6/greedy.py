"""
CS50:          https://cs50.harvard.edu/weeks
Problem set 6: https://docs.cs50.net/2017/x/psets/6/pset6.html
Problem 2:     https://docs.cs50.net/problems/credit/credit.html

The code asks user to specify change requared by a customer and prints minimum number of coins with which said change can be made.
"""

def main():

    # initiate variables
    coins = [25, 10, 5, 1]

    # prompt for float
    print('Change owed (example: 1.52 is 1 dollar 52 cents): ', end='')
    while True:
        change = float(input())
        if change <= 0:
            print('Nah! Give me a positive float!')
        else:
            break

    # cast to coins
    change_left = change * 100

    # calculate coins used, change left and print
    print('Qarters, dimes, nickels and cents respectively: ', end='')
    for coin_value in coins:
        coins_used = change_left // coin_value
        change_left -= coins_used * coin_value
        print('{:.0f}, '.format(coins_used), end='')

    print('Change left: {:.2f}'.format(change_left/100))

if __name__ == '__main__':
    main()