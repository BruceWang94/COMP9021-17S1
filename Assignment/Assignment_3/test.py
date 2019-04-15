import re

class DiffCommandsError(Exception):
    def __init__(self, message):
        self.message = message

class DiffCommands(object):
    # diff as string,
    # the last line without '\n'
    def __init__(self, filename = None):
        self.value = ''
        value = []
        match = re.search('^\w*.txt$', filename)
        if match:
            with open(filename) as file:
                f_list_1 = [] # a list, record the possible line in file1
                f_list_2 = [] # a list, record the possible line in file2
                f1_l1 = f1_l2 = 0 # num1 & num2
                f2_l1 = f2_l2 = 0 # num3 & num4
                prior_f1 = prior_f2 = 0 # record the prior nums in file1 and file2
                for line in file:
                    value.append(line)
                    # match the pattern
                    if not re.match('^(\d*)(,\d*)?c(\d*)(,\d*)?$|^(\d*)a(\d*)(,\d*)?$|^(\d*)(,\d*)?d(\d*)$',line):
                        raise DiffCommandsError('Cannot possibly be the commands for the diff of two files')
                    # match the line
                    if re.match('^(\d*)(,\d*)?d(\d*)$',line): # l1,l2 d l3
                        m = re.search('^(\d*),?(\d*)?d(\d*)$',line).groups()
                        f1_l1, f1_l2, f2_l1 = m
                        f2_l2 = f2_l1 # set num4 = num3
                        if not f1_l2.isnumeric(): # set num2 = num1 if num2 is None
                            f1_l2 = f1_l1
                        for i in range(int(prior_f1), int(f1_l1)):  # file_1
                            f_list_1.append(i)
                        for i in range(int(prior_f2), int(f2_l1) + 1): # file_2
                            f_list_2.append(i)
                        prior_f1, prior_f2 = int(f1_l2) + 1, int(f2_l2) + 1
                        #print ('\t', m)
                        #print ('\t', f1_l1, f1_l2, f2_l1)
                    elif re.match('^(\d*)a(\d*)(,\d*)?$',line): # l1 a l2,l3
                        m = re.search('^(\d*)a(\d*),?(\d*)?$',line).groups()
                        f1_l1 , f2_l1, f2_l2 = m
                        f1_l2 = f1_l1 # set num2 = num1
                        if not f2_l2.isnumeric(): # set num4 = num3 if num4 is None
                            f2_l2 = f2_l1
                        for i in range(int(prior_f1), int(f1_l1) + 1):  # file_1
                            f_list_1.append(i)
                        for i in range(int(prior_f2), int(f2_l1)): # file_2
                            f_list_2.append(i)
                        prior_f1, prior_f2 = int(f1_l2) + 1, int(f2_l2) + 1
                        #print ('\t', m)
                        #print ('\t', f1_l1 , f2_l1, f2_l2)
                    elif re.match('^(\d*)(,\d*)?c(\d*)(,\d*)?$',line): # l1,l2 c l3,l4
                        m = re.search('^(\d*),?(\d*)?c(\d*),?(\d*)?$',line).groups()
                        f1_l1, f1_l2, f2_l1, f2_l2 = m
                        len_1, len_2 = len(f_list_1), len(f_list_2)
                        if not f1_l2.isnumeric(): # set num2 = num1 if num2 is None
                            f1_l2 = f1_l1
                        if not f2_l2.isnumeric(): # set num4 = num3 if num4 is None
                            f2_l2 = f2_l1
                        for i in range(int(prior_f1), int(f1_l1)):  # file_1
                            f_list_1.append(i)
                        for i in range(int(prior_f2), int(f2_l1)): # file_2
                            f_list_2.append(i)
                        prior_f1, prior_f2 = int(f1_l2) + 1, int(f2_l2) + 1
                        if len_1 == len(f_list_1) or len_2 == len(f_list_2):
                            # a problem: does this happen in 'c',
                            # and should it judge whether it is the first step
                            raise DiffCommandsError('Cannot possibly be the commands for the diff of two files')
                        #print ('\t', m)
                        #print ('\t', f1_l1, f1_l2, f2_l1, f2_l2)
                    if len(f_list_1) != len(f_list_2):
                        raise DiffCommandsError('Cannot possibly be the commands for the diff of two files')
            for line in value: # move '\n' in the last line
                if line != value[-1]:
                    self.value += line
                else:
                    self.value += line.strip()
        else:
            self.value = filename

    def __str__(self):
        return self.value

    def split(self, character = ''):
        return self.value.split(character)

class OriginalNewFiles(object):
    # initail the object with two arguement file_1 and file_2
    # save the contact into two list, file_1 & file_2
    def __init__(self, file_1, file_2):
        #self.value = DiffCommands()
        self.file_1 = []
        self.file_2 = []
        with open(file_1) as file:
            for line in file:
                self.file_1.append(line)
        with open(file_2) as file:
            for line in file:
                self.file_2.append(line)
        #print('file_1:\n', self.file_1)
        #print('file_2:\n', self.file_2)

    def is_a_possible_diff(self, diff): # diff is a string
        list_1, list_2 = self.__get_list_of_diff(diff)
        #print ('',list_1, '\n', list_2)
        length = len(list_1)
        for i in range(1, length):
            #print (self.file_1[list_1[i] - 1])
            #print (self.file_2[list_2[i] - 1])
            if self.file_1[list_1[i] - 1] != self.file_2[list_2[i] - 1]:
                print (False)
                break
        else:
            print (True)

    # make two lists from diff, return f_list_1, f_list_2
    def __get_list_of_diff(self, diff):
        diff_split = diff.split('\n')
        f_list_1 = [] # a list, record the possible line in file1
        f_list_2 = [] # a list, record the possible line in file2
        f1_l1 = f1_l2 = 0 # num1 & num2
        f2_l1 = f2_l2 = 0 # num3 & num4
        prior_f1 = prior_f2 = 0 # record the prior nums in file1 and file2
        for line in diff_split:
            # match the line
            if re.match('^(\d*)(,\d*)?d(\d*)$',line): # l1,l2 d l3
                m = re.search('^(\d*),?(\d*)?d(\d*)$',line).groups()
                f1_l1, f1_l2, f2_l1 = m
                f2_l2 = f2_l1 # set num4 = num3
                if not f1_l2.isnumeric(): # set num2 = num1 if num2 is None
                    f1_l2 = f1_l1
                for i in range(int(prior_f1), int(f1_l1)):  # file_1
                    f_list_1.append(i)
                for i in range(int(prior_f2), int(f2_l1) + 1): # file_2
                    f_list_2.append(i)
                prior_f1, prior_f2 = int(f1_l2) + 1, int(f2_l2) + 1
                #print ('\t', m)
                #print ('\t', f1_l1, f1_l2, f2_l1)
            elif re.match('^(\d*)a(\d*)(,\d*)?$',line): # l1 a l2,l3
                m = re.search('^(\d*)a(\d*),?(\d*)?$',line).groups()
                f1_l1 , f2_l1, f2_l2 = m
                f1_l2 = f1_l1 # set num2 = num1
                if not f2_l2.isnumeric(): # set num4 = num3 if num4 is None
                    f2_l2 = f2_l1
                for i in range(int(prior_f1), int(f1_l1) + 1):  # file_1
                    f_list_1.append(i)
                for i in range(int(prior_f2), int(f2_l1)): # file_2
                    f_list_2.append(i)
                prior_f1, prior_f2 = int(f1_l2) + 1, int(f2_l2) + 1
                #print ('\t', m)
                #print ('\t', f1_l1 , f2_l1, f2_l2)
            elif re.match('^(\d*)(,\d*)?c(\d*)(,\d*)?$',line): # l1,l2 c l3,l4
                m = re.search('^(\d*),?(\d*)?c(\d*),?(\d*)?$',line).groups()
                f1_l1, f1_l2, f2_l1, f2_l2 = m
                len_1, len_2 = len(f_list_1), len(f_list_2)
                if not f1_l2.isnumeric(): # set num2 = num1 if num2 is None
                    f1_l2 = f1_l1
                if not f2_l2.isnumeric(): # set num4 = num3 if num4 is None
                    f2_l2 = f2_l1
                for i in range(int(prior_f1), int(f1_l1)):  # file_1
                    f_list_1.append(i)
                for i in range(int(prior_f2), int(f2_l1)): # file_2
                    f_list_2.append(i)
                prior_f1, prior_f2 = int(f1_l2) + 1, int(f2_l2) + 1
        len_of_file_1 = len(self.file_1)
        len_of_file_2 = len(self.file_2)
        for i in range(int(prior_f1), len_of_file_1 + 1):  # file_1
            f_list_1.append(i)
        for i in range(int(prior_f2), len_of_file_2 + 1): # file_2
            f_list_2.append(i)
                #print ('\t', m)
                #print ('\t', f1_l1, f1_l2, f2_l1, f2_l2)
        return f_list_1, f_list_2

    # return five arguement [dca], num1, num2, num3, num4
    def __get_num_in_diff(self, expr):
        if re.match('^(\d*)(,\d*)?d(\d*)$',expr): # l1,l2 d l3
            m = re.search('^(\d*),?(\d*)?d(\d*)$',expr).groups()
            num1, num2, num3 = m
            if not num2.isnumeric():
                num2 = num1
            return 'd', int(num1), int(num2), int(num3), 0
        elif re.match('^(\d*)a(\d*)(,\d*)?$',expr): # l1 a l2,l3
            m = re.search('^(\d*)a(\d*),?(\d*)?$',expr).groups()
            num1, num3, num4 = m
            if not num4.isnumeric():
                num4 = num3
            return 'a', int(num1), 0, int(num3), int(num4)
        elif re.match('^(\d*)(,\d*)?c(\d*)(,\d*)?$',expr): # l1,l2 c l3,l4
            m = re.search('^(\d*),?(\d*)?c(\d*),?(\d*)?$',expr).groups()
            num1, num2, num3, num4 = m
            if not num2.isnumeric():
                num2 = num1
            if not num4.isnumeric():
                num4 = num3
            return 'c', int(num1), int(num2), int(num3), int(num4)

    def output_diff(self, diff):
        diff_split = diff.split('\n')
        for expr in diff_split:
            print (expr)
            character, num1, num2, num3, num4 = self.__get_num_in_diff(expr)
            if character == 'd':
                for i in range(num1 - 1, num2):
                    print('<', self.file_1[i], end = '')
            elif character == 'a':
                for i in range(num3 - 1, num4):
                    print('>', self.file_2[i], end = '')
            elif character == 'c':
                for i in range(num1 - 1, num2):
                    print('<', self.file_1[i], end = '')
                print('---')
                for i in range(num3 - 1, num4):
                    print('>', self.file_2[i], end = '')

    def output_unmodified_from_original(self, diff):
        #print ('length of file 1 is',len(self.file_1))
        file_1_list, file_2_list = self.__get_list_of_diff(diff)
        #print ('file 1 list',file_1_list)
        # if the diff between two lines != 1, there is a '...'
        for i in range(1, len(file_1_list)):
            if file_1_list[i] - file_1_list[i - 1] != 1:
                print ('...')
            print (self.file_1[file_1_list[i] - 1], end = '')

    def output_unmodified_from_new(self, diff):
        #print ('length of file 2 is',len(self.file_2))
        file_1_list, file_2_list = self.__get_list_of_diff(diff)
        #print ('file 2 list',file_2_list)
        # if the diff between two lines != 1, there is a '...'
        for i in range(1, len(file_2_list)):
            if file_2_list[i] - file_2_list[i - 1] != 1:
                print ('...')
            print (self.file_2[file_2_list[i] - 1], end = '')

    def __merge_num_and_num(self, list1, list2): # both list contain number
        len1 = len(list1)
        len2 = len(list2)
        new_merge = []
        for i in range(len1):
            for j in range(len2):
                new_merge.append([list1[i],list2[j]])
        return new_merge

    def __copy(self, list_copy, ele):
        new_list = []
        for i in list_copy:
            new_list.append(i)
        new_list.append(ele)
        return new_list

    def __merge_list_and_num(self, list1, list2): # list1 contain lists, list2 contains number
        len1 = len(list1)
        len2 = len(list2)
        new_merge = []
        for i in range(len1):
            ele1 = list1[i] # ele1 is a list
            for j in range(len2):
                ele2 = list2[j] # ele2 is a number
                new_ele = self.__copy(ele1, ele2)
                new_merge.append(new_ele)
        return new_merge

    # find
    # return [(),(), ... , ()]
    def __find_lcs(self):
        again = False
        #print('\tenter the method __find_lcs:')
        # find the same subsequence
        list_1 = []
        for i in range(len(self.file_1)):
            list_1.append([]) # [[],[],...,[]]
            for j in range(len(self.file_2)):
                if self.file_1[i] == self.file_2[j]:
                    list_1[i].append(j + 1)
        #print ('\tthe same subsequence is', list_1)
        # judge the list whether has the same element, if same, set again = Ture
        for i in range(len(list_1) - 1):
            for j in range(i + 1, len(list_1)):
                if list_1[i] != [] and list_1[i] == list_1[j]:
                    again = True
                    break
            if again:
                break
        # find teh same subsequence Again!
        if again:
            list_1 = []
            for i in range(len(self.file_2)):
                list_1.append([]) # [[],[],...,[]]
                for j in range(len(self.file_1)):
                    if self.file_2[i] == self.file_1[j]:
                        list_1[i].append(j + 1)
            #print ('\tfind the same element, find the subsequence again!')
            #print ('\tthe same subsequence is', list_1)
        length_of_list1 = len(list_1)
        #print ('length of list 1 is', length_of_list1)
        # count the longest length, non-empty list in the list_1
        max_length = 0
        for pair in list_1:
            if pair != []:
                max_length += 1
        #print ('the length must be',max_length)
        # record the postion in the file 1
        same_file_1 = []
        for i in range(length_of_list1):
            if list_1[i] != []:
                same_file_1.append(i + 1)
        #print ('file 1 the list is', same_file_1)
        # remove the empty list from the list_1
        for _ in range(length_of_list1 - max_length):
            list_1.remove([])
        #print(list_1)
        # combanation the possible result from the list_1
        length_of_list1 = len(list_1)
        if length_of_list1 >= 2:
            new_merge = self.__merge_num_and_num(list_1[0], list_1[1])
            for i in range(2, length_of_list1):
                new_merge = self.__merge_list_and_num(new_merge, list_1[i])
            #print (new_merge)
        else:
            new_merge =[]
            for i in list_1[0]:
                new_merge.append([i])
            #print (new_merge)
        # remove the reserve sort of the new_merge
        for subsequence in new_merge:
            for i in range(1, len(subsequence)):
                if subsequence[i - 1] > subsequence[i]:
                    new_merge.remove(subsequence)
        if again:
            return new_merge, same_file_1
        else:
            return same_file_1, new_merge
        #print(new_merge)

    # list1 contain number, however list2 contain serial lists(each possibel match)
    # Or list2 contain number, however list1 contain serial lists(each possibel match)
    def __get_the_pattern_from_lcs(self, list1, list2):
        len_of_file_1 = len(self.file_1)
        len_of_file_2 = len(self.file_2)
        txts = []
        # list1 contain number, however list2 contain serial lists(each possibel match)
        if type(list1[0]) == int:
            possible = len(list2)
            #print ('length of file 1 is %d, length of file 1 is %d' %(len_of_file_1, len_of_file_2))
            for j in range(possible):
                #print ('********************')
                f1_start = f2_start = 0
                txts.append('')
                #print(list1)
                #print(list2[j])
                for i in range(len(list1)):
                    f1 = list1[i]
                    f2 = list2[j][i]
                    diff_1 = f1 - f1_start
                    diff_2 = f2 - f2_start
                    #print ('former  f1, f2 : %d, %d' %(f1_start,f2_start))
                    #print ('current f1, f2 : %d, %d' %(f1,f2))
                    if diff_1 == 1: # 'a'
                        if diff_2 == 1:
                            f1_start, f2_start = f1, f2
                            continue
                        elif diff_2 == 2: # num1 a num3
                            txts[j] += str(f1_start) + 'a' + str(f2_start + 1) + '\n'
                            f1_start, f2_start = f1, f2
                        else: # num1 a num3,num4
                            txts[j] += str(f1_start) + 'a' + str(f2_start + 1) + ',' + str(f2 - 1) + '\n'
                            f1_start, f2_start = f1, f2
                    elif diff_2 == 1: # 'd'
                        if diff_1 == 1:
                            f1_start, f2_start = f1, f2
                            continue
                        elif diff_1 == 2: # num1 d num3
                            txts[j] += str(f1_start + 1) + 'd' + str(f2_start) + '\n'
                            f1_start, f2_start = f1, f2
                        else: # num1,num2 d num3
                            txts[j] += str(f1_start + 1) + ',' + str(f1 -1) + 'd' + str(f2_start) + '\n'
                            f1_start, f2_start = f1, f2
                    else: # 'c'
                        if diff_1 == 2 and diff_2 == 2: # num1 c num3
                            txts[j] += str(f1_start + 1) + 'c' + str(f2_start + 1) + '\n'
                            f1_start, f2_start = f1, f2
                        else: # num1,num2 c num3, num4
                            txts[j] += str(f1_start + 1) + ',' + str(f1 - 1) + 'c' + \
                                        str(f2_start + 1) + ',' + str(f2 - 1) + '\n'
                            f1_start, f2_start = f1, f2
                    #print(str(txts[j]))
                diff_1 = len_of_file_1 - f1_start
                diff_2 = len_of_file_2 - f2_start
                if f1_start == len_of_file_1 and f2 != len_of_file_2: # num1 a num2
                    if diff_2 == 1: # num1 a num3
                        txts[j] += str(f1_start) + 'a' + str(f2_start + 1) + '\n'
                    else: # num1 a num3,num4
                        txts[j] += str(f1_start) + 'a' + str(f2_start + 1) + ',' + str(len_of_file_2) + '\n'
                elif f1_start != len_of_file_1 and f2 == len_of_file_2:
                    if diff_1 == 1: # num1 d num3
                        txts[j] += str(f1_start + 1) + 'd' + str(f2_start) + '\n'
                    else: # num1,num2 d num3
                        txts[j] += str(f1_start + 1) + ',' + str(len_of_file_1) + 'd' + str(f2_start) + '\n'
                #print(str(txts[j]))
        else: # list2 contain number
            possible = len(list1)
            #print ('length of file 1 is %d, length of file 1 is %d' %(len_of_file_1, len_of_file_2))
            for j in range(possible):
                #print ('********************')
                f1_start = f2_start = 0
                txts.append('')
                #print(list1)
                #print(list2[j])
                for i in range(len(list2)):
                    f1 = list1[j][i]
                    f2 = list2[i]
                    diff_1 = f1 - f1_start
                    diff_2 = f2 - f2_start
                    #print ('former  f1, f2 : %d, %d' %(f1_start,f2_start))
                    #print ('current f1, f2 : %d, %d' %(f1,f2))
                    if diff_1 == 1: # 'a'
                        if diff_2 == 1:
                            f1_start, f2_start = f1, f2
                            continue
                        elif diff_2 == 2: # num1 a num3
                            txts[j] += str(f1_start) + 'a' + str(f2_start + 1) + '\n'
                            f1_start, f2_start = f1, f2
                        else: # num1 a num3,num4
                            txts[j] += str(f1_start) + 'a' + str(f2_start + 1) + ',' + str(f2 - 1) + '\n'
                            f1_start, f2_start = f1, f2
                    elif diff_2 == 1: # 'd'
                        if diff_1 == 1:
                            f1_start, f2_start = f1, f2
                            continue
                        elif diff_1 == 2: # num1 d num3
                            txts[j] += str(f1_start + 1) + 'd' + str(f2_start) + '\n'
                            f1_start, f2_start = f1, f2
                        else: # num1,num2 d num3
                            txts[j] += str(f1_start + 1) + ',' + str(f1 -1) + 'd' + str(f2_start) + '\n'
                            f1_start, f2_start = f1, f2
                    else: # 'c'
                        if diff_1 == 2 and diff_2 == 2: # num1 c num3
                            txts[j] += str(f1_start + 1) + 'c' + str(f2_start + 1) + '\n'
                            f1_start, f2_start = f1, f2
                        else: # num1,num2 c num3, num4
                            txts[j] += str(f1_start + 1) + ',' + str(f1 - 1) + 'c' + \
                                        str(f2_start + 1) + ',' + str(f2 - 1) + '\n'
                            f1_start, f2_start = f1, f2
                    #print(str(txts[j]))
                diff_1 = len_of_file_1 - f1_start
                diff_2 = len_of_file_2 - f2_start
                if f1_start == len_of_file_1 and f2 != len_of_file_2: # num1 a num2
                    if diff_2 == 1: # num1 a num3
                        txts[j] += str(f1_start) + 'a' + str(f2_start + 1) + '\n'
                    else: # num1 a num3,num4
                        txts[j] += str(f1_start) + 'a' + str(f2_start + 1) + ',' + str(len_of_file_2) + '\n'
                elif f1_start != len_of_file_1 and f2 == len_of_file_2:
                    if diff_1 == 1: # num1 d num3
                        txts[j] += str(f1_start + 1) + 'd' + str(f2_start) + '\n'
                    else: # num1,num2 d num3
                        txts[j] += str(f1_start + 1) + ',' + str(len_of_file_1) + 'd' + str(f2_start) + '\n'
                #print(str(txts[j]))
        txts.sort()
        return txts
        #for txt in txts:
        #    print(str(txt))

    def get_all_diff_commands(self):
        file1, file2 = self.__find_lcs()
        txts = self.__get_the_pattern_from_lcs(file1, file2)
        #self.value = self.__get_the_pattern_from_lcs(file1, file2)
        commands = []
        for txt in txts:
            commands.append(DiffCommands(txt))
        return commands

'''
if __name__ == '__main__':

    print ('*** L = []')
    L = []
    print ('*** print (type(L))')
    print (type(L))
    print ('*****************************************')

    print ('>>> DiffCommands(\'diff_1.txt\')')
    DiffCommands('diff_1.txt')

    print ('*** print (type(DiffCommands(\'diff_1.txt\')))')
    print (type(DiffCommands('diff_1.txt')))

    print ('*****************************************')

    print ('>>> pair_of_files = OriginalNewFiles(\'file_1_1.txt\',\'file_1_2.txt\')')
    pair_of_files = OriginalNewFiles('file_1_1.txt','file_1_2.txt')

    print ('>>> pair_of_files.get_all_diff_commands()')
    pair_of_files.get_all_diff_commands()

    print ('>>> diffs = pair_of_files.get_all_diff_commands()')
    diffs = pair_of_files.get_all_diff_commands()

    print ('*** print (type(diffs))')
    print (type(diffs))

    print ('*** print (type(diffs[0]))')
    print (type(diffs[0]))

    print ('>>> len(diffs)')
    print (len(diffs))

    print ('>>> print(diffs[0])')
    print(diffs[0])

    print ('*****************************************')

    print ('>>> pair_of_files = OriginalNewFiles(\'file_1_2.txt\',\'file_1_1.txt\')')
    pair_of_files = OriginalNewFiles('file_1_2.txt','file_1_1.txt')

    print ('>>> diffs = pair_of_files.get_all_diff_commands()')
    diffs = pair_of_files.get_all_diff_commands()

    print ('*****************************************')

    print ('>>> pair_of_files = OriginalNewFiles(\'file_1_1.txt\',\'file_1_1.txt\')')
    pair_of_files = OriginalNewFiles('file_1_1.txt','file_1_1.txt')

    print ('>>> diffs = pair_of_files.get_all_diff_commands()')
    diffs = pair_of_files.get_all_diff_commands()

    print ('*****************************************')

    print ('>>> pair_of_files = OriginalNewFiles(\'file_2_2.txt\',\'file_2_1.txt\')')
    pair_of_files = OriginalNewFiles('file_2_2.txt','file_2_1.txt')

    print ('>>> pair_of_files.get_all_diff_commands()')
    pair_of_files.get_all_diff_commands()

    print ('*****************************************')

    print ('>>> pair_of_files = OriginalNewFiles(\'file_3_1.txt\',\'file_3_2.txt\')')
    pair_of_files = OriginalNewFiles('file_3_1.txt','file_3_2.txt')

    print ('>>> pair_of_files.get_all_diff_commands()')
    pair_of_files.get_all_diff_commands()

    print ('*****************************************')

    print ('>>> pair_of_files = OriginalNewFiles(\'file_3_2.txt\',\'file_3_1.txt\')')
    pair_of_files = OriginalNewFiles('file_3_2.txt','file_3_1.txt')

    print ('>>> pair_of_files.get_all_diff_commands()')
    pair_of_files.get_all_diff_commands()

    print ('*****************************************')

'''
'''
    print ('>>> len(diffs)')
    len(diffs)

    print ('>>> print(diffs[0])')
    print(diffs[0])

    print ('>>> pair_of_files = OriginalNewFiles(\'file_1_2.txt\',\'file_1_1.txt\')')
    pair_of_files = OriginalNewFiles('file_1_2.txt', 'file_1_1.txt')

    print ('>>> diffs = pair_of_files.get_all_diff_commands()')
    diffs = pair_of_files.get_all_diff_commands()

    print ('>>> len(diffs)')
    len(diffs)

    print ('>>> print(diffs[0])')
    print(diffs[0])

    print ('>>> pair_of_files = OriginalNewFiles(\'file_1_1.txt\',\'file_1_1.txt\')')
    pair_of_files = OriginalNewFiles('file_1_1.txt', 'file_1_1.txt')

    print ('>>> diffs = pair_of_files.get_all_diff_commands()')
    diffs = pair_of_files.get_all_diff_commands()

    print ('>>> len(diffs)')
    len(diffs)

    print ('>>> print(diffs[0])')
    print(diffs[0])
'''


'''
    # return two lists: c and flag
    def __lcs(self, list_1, list_2):
        len_of_list_1 = len(list_1)
        len_of_list_2 = len(list_2)
        c = [[0 for _ in range(len_of_list_2 + 1)] for _ in range(len_of_list_1 + 1)]
        # flag contain x rows and y colunms,
        # which x is len of list1 + 1 and y is len of list2 + 1
        flag = [[0 for _ in range(len_of_list_2 + 1)] for _ in range(len_of_list_1 + 1)]
        for i in range(len_of_list_1):
            for j in range(len_of_list_2):
                if list_1[i] == list_2[j]:
                    c[i + 1][j + 1] = c[i][j] + 1
                    flag[i + 1][j + 1] = ' OK '
                elif c[i + 1][j] > c[i][j - 1]:
                    c[i + 1][j + 1] = c[i + 1][j]
                    flag[i + 1][j + 1] = 'left'
                elif c[i + 1][j] < c[i][j - 1]:
                    c[i + 1][j + 1] = c[i][j + 1]
                    flag[i + 1][j + 1] = ' up '
                elif c[i + 1][j] == c[i][j - 1]:
                    c[i + 1][j + 1] = c[i + 1][j]
                    flag[i + 1][j + 1] = 'u&le'
        return c, flag

    def __get_list(self, flag, i, j, list1, list2):
        if i == 0 or j == 0:
            print (list1)
            print (list2)
            return
            #return (list1, list2)
        print ('i is %d, j is %d' %(i,j))
        if flag[i][j] == ' OK ':
            list1.append(i)
            list2.append(j)
            self.__get_list(flag, i - 1, j - 1, list1, list2)
            #print(self.file_1[i - 1], end = '')
        elif flag[i][j] == 'left':
            self.__get_list(flag, i, j - 1, list1, list2)
        elif flag[i][j] == 'up':
            self.__get_list(flag, i - 1, j, list1, list2)
        elif flag[i][j] == 'u&le':
            self.__get_list(flag, i - 1, j, list1, list2)
            self.__get_list(flag, i - 1, j, list1, list2)


'''
