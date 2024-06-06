import pandas as pd
from ipydatagrid import DataGrid, TextRenderer

# Create a simple DataFrame
data = {'Column 1': [1, 2, 3],
        'Column 2': ['A', 'B', 'C']}
df = pd.DataFrame(data)

# Create a DataGrid from the DataFrame
grid = DataGrid(df, editable=True)

# Optionally, customize the text renderer to allow editing
text_renderer = TextRenderer(editable=True)
grid.cell_renderers = {
    'Column 1': text_renderer,
    'Column 2': text_renderer
}

grid
