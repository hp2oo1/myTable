import json
import pandas as pd
import ipywidgets as widgets
from ipydatagrid import DataGrid
from IPython.display import display

def load_data(file_path):
    """Load data from a JSON file."""
    with open(file_path) as file:
        return json.load(file)

def create_dataframe(data):
    """Convert a list of dictionaries to a pandas DataFrame."""
    return pd.DataFrame(data)

def create_datagrid(dataframe):
    """Create an editable DataGrid from a DataFrame."""
    return DataGrid(dataframe, editable=True)

def get_updated_data(change=None):
    """Function to get and display the updated data from the grid."""
    with output:
        output.clear_output()
        updated_data = pd.DataFrame(grid.data).to_dict(orient='records')
    return updated_data

def add_row(button):
    """Duplicate the last row and add it to the grid."""
    if len(grid.data) > 0:
        last_row = pd.DataFrame(grid.data).iloc[-1].to_dict()
        grid.data = pd.concat([pd.DataFrame(grid.data), pd.DataFrame([last_row])]).reset_index(drop=True)
    else:
        new_row = {col: None for col in df.columns}  # Create a new row with None values if grid is empty
        grid.data = pd.concat([pd.DataFrame(grid.data), pd.DataFrame([new_row])]).reset_index(drop=True)

def remove_row(button):
    """Remove the last row from the grid."""
    if len(grid.data) > 1:
        updated_df = pd.DataFrame(grid.data).iloc[:-1].reset_index(drop=True)
        grid.data = updated_df
        get_updated_data()
    else:
        with output:
            output.clear_output()
            print("Cannot remove the last remaining row.")

# Load the sample data
data = load_data('sample_data.json')

# Convert to DataFrame
df = create_dataframe(data)

# Create DataGrid
grid = create_datagrid(df)

# Output widget for displaying updates
output = widgets.Output()

# Buttons for adding and removing rows
add_row_button = widgets.Button(description='Add Row')
remove_row_button = widgets.Button(description='Remove Row')

# Assign functions to button clicks
add_row_button.on_click(add_row)
remove_row_button.on_click(remove_row)

# Function to capture the updated data when the grid changes
grid.observe(get_updated_data, names='data')

# Display the buttons, grid, and output widget
display(widgets.HBox([add_row_button, remove_row_button]), grid, output)

get_updated_data()


