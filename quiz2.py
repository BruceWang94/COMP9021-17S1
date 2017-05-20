# Prompts the user for an integer N at least equal to 5,
# computes the largest number l >= 1 such that l consecutive prime numbers
# add up to a prime number at most equal to N,
# and outputs l and the larger such prime number.
#
# Written by *** and Eric Martin for COMP9021


from math import sqrt
import sys

def check_prime_lessN(N):
    L = [2,3]
    for i in range(5, N):
        is_prime = True
        for j in L:
            if j > int(sqrt(i)) + 1:
                break
            if i % j == 0:
                is_prime = False
        if is_prime == True:
            L.append(i)
    return L

def solution(N):
    # Insert your code here
    max_length = 2
    candidate = 5
    list_of_prime = check_prime_lessN(N)
    for i in range(2,len(list_of_prime) - 1): # possible length from 2 to half the total size of list
        for j in range(len(list_of_prime) - i):
            s = sum(list_of_prime[j:j + i + 1])
            if s <= list_of_prime[-1] and s in list_of_prime:
                max_length = i + 1
                candidate = s
    return max_length, candidate

try:
    N = int(input('Enter an integer at least equal to 5: '))
    if N < 5:
        raise ValueError
except ValueError:
    print('Incorrect input, giving up.')
    sys.exit()

max_length, candidate = solution(N)
if max_length:
    print('The largest sequence of consecutive primes that add up\n  '
          'to a prime P equal to {} at most has a length of {}.\n'
          'The largest such P is {}.'.format(N, max_length, candidate))
