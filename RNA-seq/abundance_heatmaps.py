# -*- coding: utf-8 -*-
"""
Created on Wed Jan 30 16:03:15 2019

@author: mstambou
"""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
#%matplotlib inline

in_1 = 'SRR8309842_abundance.txt'
in_2 = 'SRR8309843_abundance.txt'
in_3 = 'SRR8309844_abundance.txt'

in_1_df = pd.read_csv(in_1, sep = '\t')
in_2_df = pd.read_csv(in_2, sep = '\t')
in_3_df = pd.read_csv(in_3, sep = '\t')

all_samples_df = pd.DataFrame(columns= ['gene', 'SRR8309842', 'SRR8309843', 'SRR8309844'])

all_samples_df['gene'] = list(in_1_df['genome_id'])
all_samples_df['SRR8309842'] = list(in_1_df['total_abundance'])
all_samples_df['SRR8309843'] = list(in_2_df['total_abundance'])
all_samples_df['SRR8309844'] = list(in_3_df['total_abundance'])
all_samples_abundance = all_samples_df[['SRR8309842', 'SRR8309843', 'SRR8309844']].copy()
all_samples_abundance.index = list(all_samples_df['gene'])
#plt.pcolor(all_samples_abundance)

#sns.heatmap(all_samples_abundance, annot=True)

all_samples_df.to_csv('all_samples_abundance.txt', sep = '\t', index = False)