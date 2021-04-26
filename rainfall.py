import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import norm
import statistics
import numpy as np

df = pd.read_csv('110rainfall.csv')
df = df.fillna(50)
print(df)


list = df['Sept']
print(list)
min = min(list)
max = max(list)
mean = statistics.mean(list)
stdev = statistics.stdev(list)
print(min, max, mean, stdev)
domain = np.linspace(min,max,10)
s = np.random.normal(mean, stdev, 10)
print(s)


df1 = pd.DataFrame()
df1['Rfsamples'] = s

df1.to_csv('Rfsamples.csv')



'''plt.plot(domain, norm.pdf(domain,mean,stdev))
plt.show()'''
