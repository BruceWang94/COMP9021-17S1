import os.path
import sys

from collections import defaultdict

def check_diff(diff, dictionary): # input diff and dictionary
    has = False # if find set True
    num = 0 # the largest number of diff, otherwise 0
    # dictionary include diff and num
    for key in dictionary:
        if key == diff:
            has = True
            num = dictionary[key]
    return has, num

def find_longest_keep(L):
    value = 0
    for dictionary in L:
        if value < max(dictionary.values()):
            value = max(dictionary.values())
    return value

def find_longest_good_ride(L):
    # list the diff of the list
    L_new = []
    for i in range(len(L) - 1):
        L_new.append(L[i + 1] - L[i])
    # count the longest same diff
    length = 0
    for i in range(len(L_new) - 1):
        j = i + 1
        l = 1
        while j < len(L_new) and L_new[j] == L_new[i]:
            l += 1
            j += 1
        if length < l:
            length = l
    return length

file_name = input('Please enter the name of the file you want to get data from: ')

L = []
if not os.path.exists(file_name):
    print ('Sorry, there is no such file.')
    sys.exit()
else:
    with open(file_name) as file:
        for lines in file:
            if not lines.split():
                continue
            lines = ' '.join(lines.split())
            for e in lines.split(' '):
                L.append(e)

    try:
        if len(L) < 2:
            raise ValueError
        for i in range(len(L)):
            if not int(L[i]):
                raise ValueError
            L[i] = int(L[i])
    except ValueError:
        print('Sorry, input file does not store valid data.')
        sys.exit()

    records = []
    # check the list
    for i in range(1,len(L)):
        records.append({})
        for j in range(i - 1,-1,-1):
            diff = L[i] - L[j]
            check, num = check_diff(diff, records[j - 1])
            if not check:
                records[i - 1][diff] = 1
            else:
                records[i - 1][diff] = num + 1

    q2 = find_longest_good_ride(L)
    q3 = find_longest_keep(records)

    if len(L) == (q3 + 1):
        print('The ride is perfect!')
    else:
        print('The ride could be better...')
    print('The longest good ride has a length of:', q2)
    print('The minimal number of pillars to remove to build a perfect ride from the rest is:', len(L) - q3 - 1)
