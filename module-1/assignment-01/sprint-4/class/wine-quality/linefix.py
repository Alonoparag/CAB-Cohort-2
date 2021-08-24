import os
import sys
import re
import string


names  = ['red','white']
for name in names:
    old = open(f'wine_quality_{name}.csv', 'r')
    lines = []
    for index, line in enumerate(old):
        if index == 0:
            line = re.sub(r';',',',line)
            line = re.sub(r'"','',line)
            lines.append(line)
        else:
            line = re.sub(r';',',',line)
            lines.append(line)
    old.close()
    new = open(f'wine_quality_{name}.csv', 'w')
    for line in lines:
        new.write(line)
    new.close()
# old = open(f'wine_quality_red_test.csv', 'r')
# lines = []
# for index, line in enumerate(old):
#     if index == 0:
#         line = re.sub(r'";"',',',line)
#         line = re.sub(r'"','',line)
#         lines.append(line)
#     else:
#         line=re.sub(';',',',line)
#         lines.append(line)
# old.close()
# new = open(f'wine_quality_red_test.csv', 'w')
# for line in lines:
#     new.write(line)

# new.close()