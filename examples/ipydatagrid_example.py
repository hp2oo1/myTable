import ipydatagrid
from ipydatagrid import DataGrid
from IPython.display import display
import pandas as pd
import ipywidgets as widgets

# Sample data
data = [
    {"name": "Alice", "age": 30, "city": "New York"},
    {"name": "Bob", "age": 25, "city": "San Francisco"},
    {"name": "Charlie", "age": 35, "city": "Los Angeles"}
]

# Convert the list of dictionaries to a pandas DataFrame
df = pd.DataFrame(data)

# Create a DataGrid from the DataFrame
grid = DataGrid(df, editable=True)

# Function to get the updated data from the grid
def get_updated_data(grid):
    # Convert the grid to a pandas DataFrame
    df = pd.DataFrame(grid.data)
    # Convert the DataFrame back to a list of dictionaries
    updated_data = df.to_dict(orient='records')
    return updated_data

# Create a button to retrieve updated data
update_button = widgets.Button(description="Get Updated Data")

# Output widget to display updated data
output = widgets.Output()

# Button click handler
def on_button_click(b):
    with output:
        output.clear_output()
        updated_data = get_updated_data(grid)
        print(updated_data)

update_button.on_click(on_button_click)

# Display the grid, button, and output
display(grid, update_button, output)
