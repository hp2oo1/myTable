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

def get_updated_data(grid, output_widget):
    """Function to get and display the updated data from the grid."""
    with output_widget:
        output_widget.clear_output()
        updated_data = pd.DataFrame(grid.data).to_dict(orient='records')
    return updated_data

# Load the sample data
data = load_data('sample_data.json')

# Convert to DataFrame
df = create_dataframe(data)

# Create DataGrid
grid = create_datagrid(df)

# Output widget for displaying updates
output = widgets.Output()

grid

get_updated_data(grid, output)
