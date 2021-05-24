import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
from statsmodels.stats.multicomp import pairwise_tukeyhsd


d = sns.load_dataset('tips')

tk = pairwise_tukeyhsd('tip')