import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.stats.multicomp import pairwise_tukeyhsd
import seaborn as sns
import os
import sys

# print(os.getcwd())

for root,dirs,files in os.walk('datasets/cbs-tableau'):
    # print('Roots:',root)
    # print('Dirs:',dirs)
    # print('Files:',files)
    if root.split('/')[-1]=='after':
        with open(root+'/'+'after_merged.csv','w') as outfile:
            print('in after')
            for i,file in enumerate(files):
                print('processing',file,'\n')
                with open(root+'/'+file,'r') as infile:
                    lines=infile.readlines()
                    if i==0:
                        for line in lines:
                            outfile.write(line)
                    else:
                        for line in lines[1:]:
                            outfile.write(line)
    elif root.split('/')[-1]=='before':
        with open(root+'/'+'before_merged.csv','w') as outfile:
            print('in before')
            for i,file in enumerate(files):
                print('processing',file,'\n')
                with open(root+'/'+file,'r') as infile:
                    lines=infile.readlines()
                    if i==0:
                        for line in lines:
                            outfile.write(line)
                    else:
                        for line in lines[1:]:
                            outfile.write(line)