import pandas as pd
import ipywidgets as widgets
from ipydatagrid import DataGrid
from IPython.display import display

class EditableDataGrid:
    def __init__(self, data):
        self.df = self.create_dataframe(data)
        self.grid = self.create_datagrid(self.df)
        self.output = widgets.Output()
        
        # Buttons for adding and removing rows
        self.add_row_button = widgets.Button(description='Add Row')
        self.remove_row_button = widgets.Button(description='Remove Row')
        
        # Assign functions to button clicks
        self.add_row_button.on_click(self.add_row)
        self.remove_row_button.on_click(self.remove_row)
        
        # Function to capture the updated data when the grid changes
        self.grid.observe(self.get_updated_data, names='data')
        
        # Display the buttons, grid, and output widget
        self.display_widgets()
    
    def create_dataframe(self, data):
        """Convert a list of dictionaries to a pandas DataFrame."""
        return pd.DataFrame(data)
    
    def create_datagrid(self, dataframe):
        """Create an editable DataGrid from a DataFrame."""
        return DataGrid(dataframe, editable=True)
    
    def get_updated_data(self, change=None):
        """Function to get and display the updated data from the grid."""
        with self.output:
            self.output.clear_output()
            updated_data = pd.DataFrame(self.grid.data).to_dict(orient='records')
        return updated_data
    
    def add_row(self, button):
        """Duplicate the last row and add it to the grid."""
        if len(self.grid.data) > 0:
            last_row = pd.DataFrame(self.grid.data).iloc[-1].to_dict()
            self.grid.data = pd.concat([pd.DataFrame(self.grid.data), pd.DataFrame([last_row])]).reset_index(drop=True)
        else:
            new_row = {col: None for col in self.df.columns}  # Create a new row with None values if grid is empty
            self.grid.data = pd.concat([pd.DataFrame(self.grid.data), pd.DataFrame([new_row])]).reset_index(drop=True)
    
    def remove_row(self, button):
        """Remove the last row from the grid."""
        if len(self.grid.data) > 1:
            updated_df = pd.DataFrame(self.grid.data).iloc[:-1].reset_index(drop=True)
            self.grid.data = updated_df
            self.get_updated_data()
        else:
            with self.output:
                self.output.clear_output()
                print("Cannot remove the last remaining row.")
    
    def display_widgets(self):
        """Display the widgets."""
        display(widgets.HBox([self.add_row_button, self.remove_row_button]), self.grid, self.output)
