import plotly.express as px
import pandas as pd

data = {'X': [1, 2, 3, 4, 5],
        'Y': [10, 11, 12, 13, 14]}

fig = px.scatter(data, x='X', y='Y', title='Simple Scatter Plot')
fig.show()

#BARPLOT

data = {'Category': ['A', 'B', 'C', 'D'],
        'Value': [10, 20, 15, 25]}
fig = px.bar(data, x='Category', y='Value', title='Sample Bar Chart')
fig.show()


