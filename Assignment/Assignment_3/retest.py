import re


string = 'sadfhaoisdfoaewbfiubseduifohwae.txt'
match = re.search('^\w*.txt$', string)
if match:
    print ('found')
else:
    print ('None')
