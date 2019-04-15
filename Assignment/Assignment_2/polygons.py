from argparse import ArgumentParser
from re import sub
import sys

# return True if ij is 1; othwerwise, return 0
def check1(i,j):
    if i >= 0 and i < row and j >= 0 and j < column: # ij in grid
        if grid[i][j] == 1: # number is 1
            return True
        else: # number is not 1
            return False
    else: # ij not in grid
        return False

#   dir:   Beging - 0
#   NE - 8      N - 1      NE - 2
#    E - 7                  E - 3
#   SE - 6      S - 5      SE - 4
# path contain the i+j+dir(00+00+0)
# before call the fct, [i][j] = 1
def find_polygons(path,i,j,enter_dir):
    # enter is 3, begin is 1; enter is 1, begin is 7;
    # 3 - 1, 4 - 2, 5 - 3, 6 - 4, 7 - 5, 8 - 6, 1 - 7, 2 - 8
    ij0 = i * 1000 + j * 10
    ijd = i * 1000 + j * 10 + enter_dir

    subring = []
    if ij0 in path: # find the polygon if the point equal the fist one, namely path[0]
        #print ('got it')
        #print ('path is ',path)
        for point in path:
            i = point // 1000
            j = point // 10 % 100
            grid[i][j] = 0
        return path
    elif ij0 + 1 in path or ij0 + 2 in path or ij0 + 3 in path or \
        ij0 + 4 in path or ij0 + 5 in path or ij0 + 6 in path or \
        ij0 + 7 in path or ij0 + 8 in path or ij0 + 9 in path : # find a subring
        #print ('a subring. point is',ij0)
        wrong_path_point = path.pop()
        while wrong_path_point // 10 != ij0 // 10:
            wrong_path_point = path.pop()
        wrong_dir = wrong_path_point % 10
        wrong_i = wrong_path_point // 1000
        wrong_j = (wrong_path_point) // 10 % 100
        if wrong_dir == 1:
            i = wrong_i + 1
            j = wrong_j
            if check1(i-1,j+1) == 1: # north east
                path = find_polygons(path,i-1,j+1,2)
            elif check1(i,j+1) == 1: # east
                path = find_polygons(path,i,j+1,3)
            elif check1(i+1,j+1) == 1: # south east
                path = find_polygons(path,i+1,j+1,4)
            elif check1(i+1,j) == 1: # south
                path = find_polygons(path,i+1,j,5)
            elif check1(i+1,j-1) == 1: # south west
                path = find_polygons(path,i+1,j-1,6)
            elif check1(i,j-1) == 1: # west
                path = find_polygons(path,i,j-1,7)
            elif check1(i-1,j-1) == 1: # north west
                path = find_polygons(path,i-1,j-1,8)
        elif wrong_dir == 2:
            i = wrong_i + 1
            j = wrong_j - 1
            if check1(i,j+1) == 1: # east
                path = find_polygons(path,i,j+1,3)
            elif check1(i+1,j+1) == 1: # south east
                path = find_polygons(path,i+1,j+1,4)
            elif check1(i+1,j) == 1: # south
                path = find_polygons(path,i+1,j,5)
            elif check1(i+1,j-1) == 1: # south west
                path = find_polygons(path,i+1,j-1,6)
            elif check1(i,j-1) == 1: # west
                path = find_polygons(path,i,j-1,7)
            elif check1(i-1,j-1) == 1: # north west
                path = find_polygons(path,i-1,j-1,8)
            elif check1(i-1,j) == 1: # north
                path = find_polygons(path,i-1,j,1)
        elif wrong_dir == 3:
            i = wrong_i
            j = wrong_j - 1
            if check1(i+1,j+1) == 1: # south east
                path = find_polygons(path,i+1,j+1,4)
            elif check1(i+1,j) == 1: # south
                path = find_polygons(path,i+1,j,5)
            elif check1(i+1,j-1) == 1: # south west
                path = find_polygons(path,i+1,j-1,6)
            elif check1(i,j-1) == 1: # west
                path = find_polygons(path,i,j-1,7)
            elif check1(i-1,j-1) == 1: # north west
                path = find_polygons(path,i-1,j-1,8)
            elif check1(i-1,j) == 1: # north
                path = find_polygons(path,i-1,j,1)
            elif check1(i-1,j+1) == 1: # north east
                path = find_polygons(path,i-1,j+1,2)
        elif wrong_dir == 4:
            i = wrong_i - 1
            j = wrong_j - 1
            if check1(i+1,j) == 1: # south
                path = find_polygons(path,i+1,j,5)
            elif check1(i+1,j-1) == 1: # south west
                path = find_polygons(path,i+1,j-1,6)
            elif check1(i,j-1) == 1: # west
                path = find_polygons(path,i,j-1,7)
            elif check1(i-1,j-1) == 1: # north west
                path = find_polygons(path,i-1,j-1,8)
            elif check1(i-1,j) == 1: # north
                path = find_polygons(path,i-1,j,1)
            elif check1(i-1,j+1) == 1: # north east
                path = find_polygons(path,i-1,j+1,2)
            elif check1(i,j+1) == 1: # east
                path = find_polygons(path,i,j+1,3)
        elif wrong_dir == 5:
            i = wrong_i - 1
            j = wrong_j
            if check1(i+1,j-1) == 1: # south west
                path = find_polygons(path,i+1,j-1,6)
            elif check1(i,j-1) == 1: # west
                path = find_polygons(path,i,j-1,7)
            elif check1(i-1,j-1) == 1: # north west
                path = find_polygons(path,i-1,j-1,8)
            elif check1(i-1,j) == 1: # north
                path = find_polygons(path,i-1,j,1)
            elif check1(i-1,j+1) == 1: # north east
                path = find_polygons(path,i-1,j+1,2)
            elif check1(i,j+1) == 1: # east
                path = find_polygons(path,i,j+1,3)
            elif check1(i+1,j+1) == 1: # south east
                path = find_polygons(path,i+1,j+1,4)
        elif wrong_dir == 6:
            i = wrong_i - 1
            j = wrong_j + 1
            if check1(i,j-1) == 1: # west
                path = find_polygons(path,i,j-1,7)
            elif check1(i-1,j-1) == 1: # north west
                path = find_polygons(path,i-1,j-1,8)
            elif check1(i-1,j) == 1: # north
                path = find_polygons(path,i-1,j,1)
            elif check1(i-1,j+1) == 1: # north east
                path = find_polygons(path,i-1,j+1,2)
            elif check1(i,j+1) == 1: # east
                path = find_polygons(path,i,j+1,3)
            elif check1(i+1,j+1) == 1: # south east
                path = find_polygons(path,i+1,j+1,4)
            elif check1(i+1,j) == 1: # south
                path = find_polygons(path,i+1,j,5)
        elif wrong_dir == 7:
            i = wrong_i
            j = wrong_j + 1
            if check1(i-1,j-1) == 1: # north west
                path = find_polygons(path,i-1,j-1,8)
            elif check1(i-1,j) == 1: # north
                path = find_polygons(path,i-1,j,1)
            elif check1(i-1,j+1) == 1: # north east
                path = find_polygons(path,i-1,j+1,2)
            elif check1(i,j+1) == 1: # east
                path = find_polygons(path,i,j+1,3)
            elif check1(i+1,j+1) == 1: # south east
                path = find_polygons(path,i+1,j+1,4)
            elif check1(i+1,j) == 1: # south
                path = find_polygons(path,i+1,j,5)
            elif check1(i+1,j-1) == 1: # south west
                path = find_polygons(path,i+1,j-1,6)
        elif wrong_dir == 8:
            i = wrong_i + 1
            j = wrong_j + 1
            if check1(i-1,j) == 1: # north
                path = find_polygons(path,i-1,j,1)
            elif check1(i-1,j+1) == 1: # north east
                path = find_polygons(path,i-1,j+1,2)
            elif check1(i,j+1) == 1: # east
                path = find_polygons(path,i,j+1,3)
            elif check1(i+1,j+1) == 1: # south east
                path = find_polygons(path,i+1,j+1,4)
            elif check1(i+1,j) == 1: # south
                path = find_polygons(path,i+1,j,5)
            elif check1(i+1,j-1) == 1: # south west
                path = find_polygons(path,i+1,j-1,6)
            elif check1(i,j-1) == 1: # west
                path = find_polygons(path,i,j-1,7)
        return path
    else: # extend the point
        #print ('extend the point ',ijd)
        path.append(ijd)
        #print (path)
    # check the enter direction
    if enter_dir == 0:# point is begin
        if check1(i-1,j) == 1: # north
            path = find_polygons(path,i-1,j,1)
        elif check1(i-1,j+1) == 1: # north east
            path = find_polygons(path,i-1,j+1,2)
        elif check1(i,j+1) == 1: # east
            path = find_polygons(path,i,j+1,3)
        elif check1(i+1,j+1) == 1: # south east
            path = find_polygons(path,i+1,j+1,4)
        elif check1(i+1,j) == 1: # south
            path = find_polygons(path,i+1,j,5)
        elif check1(i+1,j-1) == 1: # south west
            path = find_polygons(path,i+1,j-1,6)
        elif check1(i,j-1) == 1: # west
            path = find_polygons(path,i,j-1,7)
        elif check1(i-1,j-1) == 1: # north west
            path = find_polygons(path,i-1,j-1,8)
    if enter_dir == 1:# from north
        if check1(i,j-1) == 1: # west
            path = find_polygons(path,i,j-1,7)
        elif check1(i-1,j-1) == 1: # north west
            path = find_polygons(path,i-1,j-1,8)
        elif check1(i-1,j) == 1: # north
            path = find_polygons(path,i-1,j,1)
        elif check1(i-1,j+1) == 1: # north east
            path = find_polygons(path,i-1,j+1,2)
        elif check1(i,j+1) == 1: # east
            path = find_polygons(path,i,j+1,3)
        elif check1(i+1,j+1) == 1: # south east
            path = find_polygons(path,i+1,j+1,4)
        elif check1(i+1,j) == 1: # south
            path = find_polygons(path,i+1,j,5)
        elif check1(i+1,j-1) == 1: # south west
            path = find_polygons(path,i+1,j-1,6)
    if enter_dir == 2:# from north east
        if check1(i-1,j-1) == 1: # north west
            path = find_polygons(path,i-1,j-1,8)
        elif check1(i-1,j) == 1: # north
            path = find_polygons(path,i-1,j,1)
        elif check1(i-1,j+1) == 1: # north east
            path = find_polygons(path,i-1,j+1,2)
        elif check1(i,j+1) == 1: # east
            path = find_polygons(path,i,j+1,3)
        elif check1(i+1,j+1) == 1: # south east
            path = find_polygons(path,i+1,j+1,4)
        elif check1(i+1,j) == 1: # south
            path = find_polygons(path,i+1,j,5)
        elif check1(i+1,j-1) == 1: # south west
            path = find_polygons(path,i+1,j-1,6)
        elif check1(i,j-1) == 1: # west
            path = find_polygons(path,i,j-1,7)
    if enter_dir == 3:# from east; same as direction = 0
        if check1(i-1,j) == 1: # north
            path = find_polygons(path,i-1,j,1)
        elif check1(i-1,j+1) == 1: # north east
            path = find_polygons(path,i-1,j+1,2)
        elif check1(i,j+1) == 1: # east
            path = find_polygons(path,i,j+1,3)
        elif check1(i+1,j+1) == 1: # south east
            path = find_polygons(path,i+1,j+1,4)
        elif check1(i+1,j) == 1: # south
            path = find_polygons(path,i+1,j,5)
        elif check1(i+1,j-1) == 1: # south west
            path = find_polygons(path,i+1,j-1,6)
        elif check1(i,j-1) == 1: # west
            path = find_polygons(path,i,j-1,7)
        elif check1(i-1,j-1) == 1: # north west
            path = find_polygons(path,i-1,j-1,8)
    if enter_dir == 4:# from south east
        if check1(i-1,j+1) == 1: # north east
            path = find_polygons(path,i-1,j+1,2)
        elif check1(i,j+1) == 1: # east
            path = find_polygons(path,i,j+1,3)
        elif check1(i+1,j+1) == 1: # south east
            path = find_polygons(path,i+1,j+1,4)
        elif check1(i+1,j) == 1: # south
            path = find_polygons(path,i+1,j,5)
        elif check1(i+1,j-1) == 1: # south west
            path = find_polygons(path,i+1,j-1,6)
        elif check1(i,j-1) == 1: # west
            path = find_polygons(path,i,j-1,7)
        elif check1(i-1,j-1) == 1: # north west
            path = find_polygons(path,i-1,j-1,8)
        elif check1(i-1,j) == 1: # north
            path = find_polygons(path,i-1,j,1)
    if enter_dir == 5:# from south
        if check1(i,j+1) == 1: # east
            path = find_polygons(path,i,j+1,3)
        elif check1(i+1,j+1) == 1: # south east
            path = find_polygons(path,i+1,j+1,4)
        elif check1(i+1,j) == 1: # south
            path = find_polygons(path,i+1,j,5)
        elif check1(i+1,j-1) == 1: # south west
            path = find_polygons(path,i+1,j-1,6)
        elif check1(i,j-1) == 1: # west
            path = find_polygons(path,i,j-1,7)
        elif check1(i-1,j-1) == 1: # north west
            path = find_polygons(path,i-1,j-1,8)
        elif check1(i-1,j) == 1: # north
            path = find_polygons(path,i-1,j,1)
        if check1(i-1,j+1) == 1: # north east
            path = find_polygons(path,i-1,j+1,2)
    if enter_dir == 6:# from south west
        if check1(i+1,j+1) == 1: # south east
            path = find_polygons(path,i+1,j+1,4)
        elif check1(i+1,j) == 1: # south
            path = find_polygons(path,i+1,j,5)
        elif check1(i+1,j-1) == 1: # south west
            path = find_polygons(path,i+1,j-1,6)
        elif check1(i,j-1) == 1: # west
            path = find_polygons(path,i,j-1,7)
        elif check1(i-1,j-1) == 1: # north west
            path = find_polygons(path,i-1,j-1,8)
        elif check1(i-1,j) == 1: # north
            path = find_polygons(path,i-1,j,1)
        elif check1(i-1,j+1) == 1: # north east
            path = find_polygons(path,i-1,j+1,2)
        elif check1(i,j+1) == 1: # east
            path = find_polygons(path,i,j+1,3)
    if enter_dir == 7:# from west
        if check1(i+1,j) == 1: # south
            path = find_polygons(path,i+1,j,5)
        elif check1(i+1,j-1) == 1: # south west
            path = find_polygons(path,i+1,j-1,6)
        elif check1(i,j-1) == 1: # west
            path = find_polygons(path,i,j-1,7)
        elif check1(i-1,j-1) == 1: # north west
            path = find_polygons(path,i-1,j-1,8)
        elif check1(i-1,j) == 1: # north
            path = find_polygons(path,i-1,j,1)
        elif check1(i-1,j+1) == 1: # north east
            path = find_polygons(path,i-1,j+1,2)
        elif check1(i,j+1) == 1: # east
            path = find_polygons(path,i,j+1,3)
        elif check1(i+1,j+1) == 1: # south east
            path = find_polygons(path,i+1,j+1,4)
    if enter_dir == 8:# from north west
        if check1(i+1,j-1) == 1: # south west
            path = find_polygons(path,i+1,j-1,6)
        elif check1(i,j-1) == 1: # west
            path = find_polygons(path,i,j-1,7)
        elif check1(i-1,j-1) == 1: # north west
            path = find_polygons(path,i-1,j-1,8)
        elif check1(i-1,j) == 1: # north
            path = find_polygons(path,i-1,j,1)
        elif check1(i-1,j+1) == 1: # north east
            path = find_polygons(path,i-1,j+1,2)
        elif check1(i,j+1) == 1: # east
            path = find_polygons(path,i,j+1,3)
        elif check1(i+1,j+1) == 1: # south east
            path = find_polygons(path,i+1,j+1,4)
        elif check1(i+1,j) == 1: # south
            path = find_polygons(path,i+1,j,5)
    return path

# get the direction list
def get_dri(path):
    Dri = []
    for point in path:
        Dri.append(point % 10)
    x0 = path[0] // 1000
    y0 = path[0] // 10 % 100
    xn = path[-1] // 1000
    yn = path[-1] // 10 % 100
    if y0 - yn == 1:
        if x0 - xn == -1:
            Dri.append(2)
        elif x0 - xn == 0:
            Dri.append(3)
        elif x0 - xn == 1:
            Dri.append(4)
    elif y0 - yn == -1:
        if x0 - xn == -1:
            Dri.append(8)
        elif x0 - xn == 0:
            Dri.append(7)
        elif x0 - xn == 1:
            Dri.append(6)
    elif y0 - yn == 0:
        if x0 - xn == -1:
            Dri.append(1)
        elif x0 - xn == 1:
            Dri.append(5)
    return Dri

def path_is_clockwise(path):
    Dri = get_dri(path)[1:]
    if Dri[0] > 5:
        return False
    else:
        return True

def change_path(path):
    new_path = []
    new_path.append(path[0])
    #print ('original path is', path)
    path.reverse()
    #print ('reverse path is', path[:-1])
    for i in path[:-1]:
        i_x = i // 1000
        i_y = i // 10 % 100
        x = new_path[-1] // 1000
        y = new_path[-1] // 10 % 100
        if i_y - y == 1:
            if i_x - x == -1:
                new_path.append(i // 10 * 10 + 2)
            elif i_x - x == 0:
                new_path.append(i // 10 * 10 + 3)
            elif i_x - x == 1:
                new_path.append(i // 10 * 10 + 4)
        elif i_y - y == -1:
            if i_x - x == -1:
                new_path.append(i // 10 * 10 + 8)
            elif i_x - x == 0:
                new_path.append(i //10 * 10 + 7)
            elif i_x - x == 1:
                new_path.append(i // 10 * 10 + 6)
        elif i_y - y == 0:
            if i_x - x == -1:
                new_path.append(i // 10 * 10 + 1)
            elif i_x - x == 1:
                new_path.append(i // 10 * 10 + 5)
    return new_path

def count_perimeter(path):
    Dri = []
    for point in path:
        Dri.append(point % 10)
    x0 = path[0] // 1000
    y0 = path[0] // 10 % 100
    xn = path[-1] // 1000
    yn = path[-1] // 10 % 100
    if (y0 - yn) * (xn - x0) == 0:
        Dri.append(1)
    else:
        Dri.append(2)
    l = s = 0 # s = sqrt(2) * l
    for D in Dri[1:]:
        if D % 2 == 1:
            l +=1
        else:
            s +=1
    return l,s

def count_area(path):
    X = [] ; Y = []
    for point in path:
        x = point // 1000; y = point // 10 % 100
        X.append(x); Y.append(y)
    X.append(X[0])
    Y.append(Y[0])

    length = len(X) - 1
    sum_x = 0 ; i = 0
    while i < length:
        sum_x += X[i] * Y[i + 1]
        i += 1
    sum_y = 0 ; i = 0
    while i < length:
        sum_y += Y[i] * X[i + 1]
        i += 1
    area_unit = (sum_x - sum_y) / 2

    if area_unit < 0:
        area_unit = -area_unit
    return area_unit * 0.16

def convex(path, original_area):
    for i in range(len(path)):
        new_path = path.copy()
        new_path.pop(i)
        if count_area(new_path) > original_area:
            return 'no'
            break
    else:
        return 'yes'

# path has total_number of element
# n is continue numebr, N = total_number / n is the group
# (0....n-1, n....2n-1, 2n....3n-1, ...., (N-1)n....Nn-1)
def check_change(Dri,change,nb_group,nb_group_member): # (a + change) % 8 == b
    for row in range(1, nb_group):
        for column in range((row - 1) * nb_group_member, row * nb_group_member):
            if (Dri[column] + change) % 8 != Dri[column + nb_group_member] % 8:
                return False
    return True

def num_of_invaritant(path):
    Dri = get_dri(path)[1:]
    total_number = len(path)
    nb_group_member = 1
    while nb_group_member < total_number // 2 + 1:
        if total_number % nb_group_member != 0: # n is not a factor of total_number
            nb_group_member += 1
            continue
        else: # n is a factor of total_number
            nb_group = total_number // nb_group_member
            change_dir = Dri[nb_group_member] - Dri[0]
            if change_dir < 0:
                change_dir += 8
            if check_change(Dri, change_dir, nb_group, nb_group_member):
                return nb_group
                break
            else:
                nb_group_member += 1
    else:
        return 1

def change_1to0(path):
    for point in path:
        point_x = point // 1000
        point_y = point // 10 % 100
        grid[point_x][point_y] = 0

def depth(polygon_list, postion):
    #print('\tpath is',path)
    #print('\tpolygon_list is',polygon_list)
    path = polygon_list[postion]
    num_of_polygon = len(polygon_list)
    test_x = path[0] // 1000
    test_y = path[0] // 10 % 100
    if postion == 0:
        #print ('\tthere is no polygon in the list')
        polygon_list[postion].append(0)
        #print('\tappden polygon_list',polygon_list)
        return 0
    else:
        depth = 0
        for n in range(postion):
            polygon = polygon_list[n]
            length = len(polygon) - 1
            flag = False
            i = 0
            l = len(polygon_list[n]) - 1
            j = l - 1
            while i < l:
                sx = polygon[i] // 1000
                sy = polygon[i] // 10 % 100
                tx = polygon[j] // 1000
                ty = polygon[j] // 10 % 100
                if sy < test_y and ty >= test_y or sy >= test_y and ty < test_y:
                    x = sx + (test_y - sy) * (tx - sx) / (ty - sy)
                    if x > test_x:
                        flag = not flag
                j = i
                i += 1
            if flag:
                current_depth = polygon[-1] + 1
                if current_depth > depth:
                    depth = current_depth
        polygon_list[postion].append(depth)
        return depth

parser = ArgumentParser()
parser.add_argument('--file', dest = 'file_filename', required = True)
parser.add_argument('-print', action = 'store_true')
args = parser.parse_args()

filename = args.file_filename

with open(filename) as file:
    grid = []
    for line in file:
        row = []
        if not line.split():
            continue
        else:
            line = ' '.join(line.split())
            for e in line:
                if e != ' ':
                    row.append(int(e))
        if row != []:
            grid.append(row)

filename = sub('\..*$', '', filename)
output_filename = filename + '_my_output.txt'

row = len(grid)
column = len(grid[0])
if row < 2 or row > 50 or column < 2 or column > 50:
    print ('Incorrect input.')
    sys.exit()
#print ('This is a %d * %d grid' %(row,column))
for rows in grid:
    for element in rows:
        if element not in [0,1]:
            print ('Incorrect input.')
            sys.exit()

polygon_list = [] # record the polygons
for i in range(row):
    for j in range(column):
        if grid[i][j] == 1:
            path = []
            path = find_polygons(path,i,j,0)
            if len(path) != 1 and len(path) != 2:
                if not path_is_clockwise(path):
                    path = change_path(path)
            change_1to0(path)
            polygon_list.append(path)

for polygons in polygon_list:
    if len(polygons) == 1 or len(polygons) == 2:
        print ('Cannot get polygons as expected.')
        sys.exit()

for i in range(len(polygon_list)):
    path = polygon_list[i]
    print('Polygon %d:' %(i + 1))
    l,s = count_perimeter(path)
    if l == 0:
        print ('    Perimeter: %d*sqrt(.32)' %(s))
    elif s == 0:
        print ('    Perimeter: %.1f' %(l * 0.4))
    else:
        print ('    Perimeter: %.1f + %d*sqrt(.32)' %(l * 0.4,s))
    print ('    Area: %.2f' %(count_area(path)))
    print ('    Convex: %s' %(convex(path,count_area(path))))
    print ('    Nb of invariant rotations: %d' %(num_of_invaritant(path)))
    dep= depth(polygon_list,i)
    print ('    Depth: %d' %(dep))

depth_dic = {}
for i in range(len(polygon_list)):
    polygons = polygon_list[i]
    depth = polygons[-1]
    if depth not in depth_dic:
        depth_dic[depth] = [i]
    else:
        depth_dic[depth].append(i)

area_polygons = []
for polygons in polygon_list:
    area = count_area(polygons[:-1])
    area_polygons.append(round(area,2))

max_area = max(area_polygons)
min_area = min(area_polygons)
diff_area = max_area - min_area

vertex_polygons = []
for n in range(len(polygon_list)):
    ver_poly = []
    polygons = polygon_list[n][:-1]
    Dri = get_dri(polygons)
    for i in range(len(Dri) - 1):
        if Dri[i] != Dri[i + 1]:
            xyd = polygons[i]
            ver_poly.append(xyd // 10)
    vertex_polygons.append(ver_poly)
#print('vertex of polygons is', vertex_polygons)

if args.print == True:
    tex_filename = filename + '.tex'
    with open(tex_filename, 'w') as tex_file:
        print('\\documentclass[10pt]{article}\n'
              '\\usepackage{tikz}\n'
              '\\usepackage[margin=0cm]{geometry}\n'
              '\\pagestyle{empty}\n'
              '\n'
              '\\begin{document}\n'
              '\n'
              '\\vspace*{\\fill}\n'
              '\\begin{center}\n'
              '\\begin{tikzpicture}[x=0.4cm, y=-0.4cm, thick, brown]', file = tex_file)

        print('\\draw[ultra thick] (0, 0) -- (%d, 0) -- (%d, %d) -- (0, %d) -- cycle;' %(column-1, column-1, row-1, row-1), file = tex_file)

        depth_list = []
        for key in depth_dic.keys():
            depth_list.append(key)
        depth_list.sort()
#        print(depth_list)
        for depth in depth_list:
            print('%'+'Depth %d' %(depth), file = tex_file)
            nb_of_polygon = depth_dic[depth]
            for nb in nb_of_polygon:
                print('\\' + 'filldraw[fill=orange!%1.f!yellow]' %(((max_area - area_polygons[nb]) / diff_area) * 100), end = '', file = tex_file)
                vertexs = vertex_polygons[nb]
                for xy in vertexs:
                    print(' (%d, %d) --' %(xy % 100, xy // 100), end = '', file = tex_file)
                print(' cycle;', file = tex_file)

        print('\\end{tikzpicture}\n'
              '\\end{center}\n'
              '\\vspace*{\\fill}\n'
              '\n'
              '\\end{document}', file = tex_file)
