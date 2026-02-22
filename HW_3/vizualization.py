#data_vizualization
import matplotlib.pyplot as plt
import seaborn as sns
def Hist(df):
  df.hist(bins=10, figsize=(13, 12))
  plt.show()
def Pairplt(df, x1, y1):
  sns.scatterplot(df, x=x1, y=y1, palette = 'Set2', hue = 'Result')


