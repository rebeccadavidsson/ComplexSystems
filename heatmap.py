import pandas as pd
import seaborn as sns
sns.set()

df = pd.read_pickle("./df_heatmap.pkl")
print(df)
sns.heatmap(df, annot=True, fmt="g", cmap='viridis')
plt.show()
