import pandas as pd
import ast

# take all the "target" x and y coordinates form data.csv and put them into a dataframe
df = pd.read_csv('data.csv')

# take the x and y coordinates from the 'target' tuple and put them into a list
target_x = []
target_y = []
for i in range(len(df)):
    target_tuple = ast.literal_eval(df['target'][i])
    target_x.append(target_tuple[0])
    target_y.append(target_tuple[1])

# now create a heatmap of the target x and y coordinates
import seaborn as sns
import matplotlib.pyplot as plt

# create a heatmap of the target x coordinates
sns.kdeplot(x=target_x, y=target_y, shade=True, shade_lowest=False)

# save the heatmap as a png
plt.savefig('heatmap.png')
