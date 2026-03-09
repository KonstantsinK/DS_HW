#data_vizualization
import math
import matplotlib.pyplot as plt
import seaborn as sns
def Hist(df):
  sns.histplot(data = df, x="Price", kde = True, bins = 30)
  plt.show()

def Pairplt(df, x1, y1):
  sns.scatterplot(df, x=x1, y=y1, palette = 'Set2', hue = 'Result')

def reg_line_coll(df, x1, y1):
    sns.lmplot(x=x1, y=y1, data=df)

def plot_all_countplot(df):
#Графики всех значений
    num_cols = df.select_dtypes(include="object").columns
    n_cols = 2
    n_rows = math.ceil(len(num_cols) / n_cols)

    plt.figure(figsize = (10 * n_cols, 5 * n_rows))

    for i, col in enumerate(num_cols, 1):
        plt.subplot(n_rows, n_cols, i)
        sns.countplot(x=df[col])
        plt.title(f"{col}")
        plt.xlabel("")
        plt.ylabel("")

    plt.tight_layout()
    plt.show()
def core(df,numerical_cols):
#Распределение и кореляция числовых данных
    sns.set(style="ticks", palette='cividis')  # Optional: nice style
    sns.pairplot(df[numerical_cols], diag_kind='kde')  # KDE for smooth distribution
    plt.suptitle("Распределение и корреляция числовых характеристик", fontsize=16, y=1.02)
    plt.show()

def outlier(df,feach):
    # обнаружение выбросов (Price)
    sns.boxplot(data = df, y = feach)
    plt.show()

def data_comparation(df, comparison_cols):
    #Сравнение цены c характеристиками ноутбуков
    sns.set(style="whitegrid")
    fig, axes = plt.subplots(4, 2, figsize=(18, 24))
    fig.suptitle("Панель сравнения данных: цены на ноутбуки с характеристиками",
                 fontsize=18, fontweight='bold')
    for ax, col in zip(axes.flatten(), comparison_cols):
        sns.boxplot(
            x=col,
            y='Price',
            data=df,
            ax=ax,
            palette='cividis'
        )
        ax.set_title(f"Price Comparison by {col}")
        ax.set_xlabel(col)
        ax.set_ylabel("Price")
        ax.tick_params(axis='x', rotation=45)

    plt.tight_layout(rect=[0, 0, 1, 0.96])
    plt.show()