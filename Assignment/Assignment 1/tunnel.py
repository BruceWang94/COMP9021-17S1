import os.path
import sys
from collections import deque

def make_matrix(ceiling, floor, matrix):
    for j in range(len(ceiling)):
        for i in range(10):
            if i >= floor[j] and i < ceiling[j]:
                matrix[9-i].append(1)
            else:
                matrix[9-i].append(0)
    return matrix

def find_west(matrix,length):
    for i in range(10):
        if matrix[i][0] != 1:
            continue
        else:
            row = matrix[i]
            value = 1
            stop = False
            j = 1
            while not stop:
                if row[j] == 1 and j < length:
                    value += 1
                    j +=1
                else:
                    stop = True
    return value

def find_succesive(row, length):
    L = []
    if sum(row) == 0:
        return 0
    s = ''
    for e in row:
        s += str(e)
    s = s.split('0')
    num = 0
    for i in range(len(s)):
        if num < len(s[i]):
            num = len(s[i])
    return num

def find_inside(matrix,length):
    value = 0
    for i in range(10):
        if value < find_succesive(matrix[i], length):
            value = find_succesive(matrix[i], length)
    return value

file_name = input('Please enter the name of the file you want to get data from: ')

if not os.path.exists(file_name):
    print ('Sorry, there is no such file.')
    sys.exit()
else:
    initial_txt = []
    with open(file_name) as file:
        for lines in file:
            L = []
            if not lines.split():
                continue
            lines = ' '.join(lines.split())
            for e in lines.split():
                L.append(e)
            initial_txt.append(L)

    try:
        if len(initial_txt) != 2:
            raise ValueError
        ceiling, floor = initial_txt[0], initial_txt[1]
        if len(ceiling) != len(floor) or len(ceiling) < 2:
            raise ValueError
        for i in range(len(ceiling)):
            if not int(ceiling[i]) or not int(floor[i]):
                raise ValueError
            ceiling[i] = int(ceiling[i])
            floor[i] = int(floor[i])
        for i in range(len(ceiling)):
            if ceiling[i] <= floor[i]:
                raise ValueError
    except ValueError:
        print('Sorry, input file does not store valid data.')
        sys.exit()

    initial_matrix = [[],[],[],[],[],[],[],[],[],[]]
    matrix = make_matrix(ceiling, floor, initial_matrix)

    length = len(ceiling)
    west = find_west(matrix,length)
    inside = find_inside(matrix,length)
    print('From the west, one can into the tunnel over a distance of', west)
    print('Inside the tunnel, one can into the tunnel over a maximum distance of', inside)
