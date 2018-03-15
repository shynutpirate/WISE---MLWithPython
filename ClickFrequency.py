import numpy as np
import pandas as pd
import datetime
import os

import time

import matplotlib.pyplot as plt
import seaborn as sns
%matplotlib inline

sns.set(rc={'figure.figsize':(12,5)});
plt.figure(figsize=(12,5));


train_smp = pd.read_csv('C:/Users/Bhagavathi/Downloads/train_sample.csv')

train_smp.head(7)

train_smp['click_time'] = pd.to_datetime(train_smp['click_time'])
train_smp['attributed_time'] = pd.to_datetime(train_smp['attributed_time'])

train_smp['click_rnd']=train_smp['click_time'].dt.round('H')  

train_smp[['click_rnd','is_attributed']].groupby(['click_rnd'], as_index=True).count().plot()
plt.title('HOURLY CLICK FREQUENCY');
plt.ylabel('Number of Clicks');