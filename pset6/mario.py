"""
CS50:          https://cs50.harvard.edu/weeks
Problem set 6: https://docs.cs50.net/2017/x/psets/6/pset6.html
Problem 1:     https://docs.cs50.net/problems/mario/more/mario.html

The code asks user to specify pyramid height and then prints out mario-pyramid accordingly.
"""

# prompt for integer
print('Let build a Mario pyramid! Buy how high? Give me a positive int between 1 and 24: ', end='')
while True:
    height = int(input())
    if height < 1 or height > 24:
        print('Nah! Give me an int between 1 and 24!')
    else:
        break

# print the pyramid (semi-readable one liner)
for row in range(height+1):
    print(' ' * (height - row) + '#' * row + '  ' + '#' * row)
