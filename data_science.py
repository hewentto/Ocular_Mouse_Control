import pandas as pd
import ast
import seaborn as sns
import matplotlib.pyplot as plt
from screeninfo import get_monitors

# Get the screen resolution
monitor = get_monitors()[0]
screen_width = monitor.width
screen_height = monitor.height

# take all the "target" x and y coordinates form data.csv and put them into a dataframe
df = pd.read_csv('data2.csv')

# take the x and y coordinates from the 'target' tuple and put them into a list
target_x = []
target_y = []
for i in range(len(df)):
    target_tuple = ast.literal_eval(df['target'][i])
    target_x.append(target_tuple[0])
    target_y.append(target_tuple[1])

# create a figure with the screen resolution
fig = plt.figure(figsize=(screen_width / 80, screen_height / 80), dpi=80)

# now create a heatmap of the target x and y coordinates

# create a heatmap of the target x coordinates
sns.kdeplot(x=target_x, y=target_y, fill=True, thresh=False)

# set the min and max limits for both axes based on the data
plt.xlim(min(target_x), max(target_x))
plt.ylim(min(target_y), max(target_y))

# save the heatmap as a png
plt.savefig('heatmap.png')

# display the heatmap in full screen
manager = plt.get_current_fig_manager()
manager.full_screen_toggle()
plt.show()
