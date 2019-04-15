
import sys

try:
    superpower = input('Please input the heroes\' powers: ')
    superpower = superpower.split(' ')
    for i in range(len(superpower)):
        if not int(superpower[i]):
            raise ValueError
except ValueError:
    print('Sorry, these are not valid power values.')
    sys.exit()

try:
    nb_of_swiches = int(input('Please input the number of power flips: '))
    if nb_of_swiches < 0 or nb_of_swiches > len(superpower):
        raise ValueError
except ValueError:
    print('Sorry, this is not a valid number of power flips.')
    sys.exit()

for i in range(len(superpower)):
    superpower[i] = int(superpower[i])

# def a fct to output num of negative number and a list of them position
def find_num_of_negative(L):
    n = 0
    length = len(L)
    l = [0] # save the postion of negative number, l[0] is the smallest one
    for i in range(length):
        if L[i] < 0:
            n += 1
            l.append(i)
            if l[0] > L[i]:
                l[0] = i
    return n,l

q1 = superpower.copy()
q1.sort()

for i in range(nb_of_swiches):
    q1[0] = -q1[0]
    q1.sort()
print ('Possibly flipping the power of the same hero many times, the greatest achievable power is %d.' % sum(q1))

q2 = superpower.copy()
q2.sort()

for i in range(nb_of_swiches):
    q2[i] = -q2[i]
print('Flipping the power of the same hero at most once, the greatest achievable power is %d.' % sum(q2))

q3 = superpower.copy()
l = [0] * 2 # list save the inital and the sum
for i in range(len(q3) - nb_of_swiches + 1):
    s = sum(q3[i: i + nb_of_swiches])
    if l[1] > s:
        l[0] = i
        l[1] = s
for i in range(nb_of_swiches):
    q3[l[0] + i] = -q3[l[0] + i]
#print ('q3 is',q3)
print ('Flipping the power of nb_of_flips many consecutive heroes, the greatest achievable power is %d.' % sum(q3))


q4 = superpower.copy()

length = 0; add = 0; begin = 0
for l in range(1, nb_of_swiches + 1):
    for i in range(len(q4) - l + 1):
        if sum(q4[i: i + l]) < add:
            length = l
            add = sum(q4[i: i + l])
            begin = i
for i in range(begin, begin + length):
    q4[i] = -q4[i]
print ('Flipping the power of arbitrarily many consecutive heroes, the greatest achievable power is %d.' % sum(q4))
