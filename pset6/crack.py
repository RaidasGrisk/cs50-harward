"""
CS50:          https://cs50.harvard.edu/weeks
Problem set 6: https://docs.cs50.net/2017/x/psets/6/pset6.html
Problem 4:     https://docs.cs50.net/problems/crack/crack.html

The code cracks passwords using crypt() hashes (cyphertext) using brute force.
"""

import crypt
from itertools import permutations

# prompt for hash
print('Hash: ', end='')
while True:
    hash = input()
    if len(hash) != 13:
        print('Hash: ', end='')
    else:
        break

# define alphabet
alphabet = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'

# iterate over each possible comination when i defines length of a word
for i in range(1, 5):
    for word in [''.join(x) for x in permutations(alphabet, i)]:
        if crypt.crypt(word=word, salt=hash[0:2]) == hash:
            print('Pass: {}'.format(word))
            exit(0)

# if cound not find a match
print('No result')
exit(1)
