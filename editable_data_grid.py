import pandas as pd
import ipywidgets as widgets
from ipydatagrid import DataGrid
from IPython.display import display
from datetime import datetime

class EditableDataGrid:
    def __init__(self, data):
        self.column_types = self.detect_column_types(data)
        self.df = self.preprocess_data(data)
        self.grid = self.create_datagrid(self.df)
        self.output = widgets.Output()

        # Buttons for adding and removing rows
        self.add_row_button = widgets.Button(description='+ row')
        self.remove_row_button = widgets.Button(description='- row')

        # Assign functions to button clicks
        self.add_row_button.on_click(self.add_row)
        self.remove_row_button.on_click(self.remove_row)

        # Function to capture the updated data when the grid changes
        self.grid.observe(self.get_updated_data, names='data')

        # Display the buttons, grid, and output widget
        self.display_widgets()

    def detect_column_types(self, data):
        """Detect and store the column types from the original data."""
        df = pd.DataFrame(data)
        column_types = {}
        for column in df.columns:
            if pd.api.types.is_datetime64_any_dtype(df[column]):
                column_types[column] = 'datetime'
            elif isinstance(df[column].iloc[0], list) and all(isinstance(i, (int, float)) for i in df[column].iloc[0]):
                column_types[column] = 'list_of_doubles'
            else:
                column_types[column] = 'other'
        return column_types

    def preprocess_data(self, data):
        """Preprocess the input data for display in the DataGrid."""
        df = pd.DataFrame(data)
        for column, col_type in self.column_types.items():
            if col_type == 'datetime':
                df[column] = df[column].dt.strftime('%Y-%m-%d')  # Convert to string with date format
            elif col_type == 'list_of_doubles':
                df[column] = df[column].apply(lambda x: ', '.join(map(str, x)))  # Convert list of doubles to string
        return df

    def postprocess_data(self, dataframe):
        """Convert the DataFrame back to the original format."""
        df = dataframe.copy()
        for column, col_type in self.column_types.items():
            if col_type == 'datetime':
                df[column] = pd.to_datetime(df[column])  # Convert string dates back to datetime
            elif col_type == 'list_of_doubles':
                df[column] = df[column].apply(lambda x: list(map(float, x.split(', '))) if isinstance(x, str) else x)  # Convert string lists back to lists of doubles
        return df.to_dict(orient='records')

    def create_datagrid(self, dataframe):
        """Create an editable DataGrid from a DataFrame."""
        grid = DataGrid(dataframe, editable=True, auto_fit_columns=True)
        return grid

    def get_updated_data(self, change=None):
        """Function to get and display the updated data from the grid."""
        with self.output:
            self.output.clear_output()
            updated_data = pd.DataFrame(self.grid.data)
            original_format_data = self.postprocess_data(updated_data)
        return original_format_data

    def add_row(self, button):
        """Duplicate the last row and add it to the grid."""
        if len(self.grid.data) > 0:
            last_row = pd.DataFrame(self.grid.data).iloc[-1].to_dict()
            self.grid.data = pd.concat([pd.DataFrame(self.grid.data), pd.DataFrame([last_row])]).reset_index(drop=True)
        else:
            new_row = {col: None for col in self.df.columns}  # Create a new row with None values if grid is empty
            self.grid.data = pd.concat([pd.DataFrame(self.grid.data), pd.DataFrame([new_row])]).reset_index(drop=True)
        self.grid.auto_fit_columns = True  # Ensure auto-fit columns is enabled after adding a row

    def remove_row(self, button):
        """Remove the last row from the grid."""
        if len(self.grid.data) > 1:
            updated_df = pd.DataFrame(self.grid.data).iloc[:-1].reset_index(drop=True)
            self.grid.data = updated_df
            self.get_updated_data()
            self.grid.auto_fit_columns = True  # Ensure auto-fit columns is enabled after removing a row
        else:
            with self.output:
                self.output.clear_output()
                print("Cannot remove the last remaining row.")

    def display_widgets(self):
        """Display the widgets."""
        display(widgets.HBox([self.add_row_button, self.remove_row_button]), self.grid, self.output)
