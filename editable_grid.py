import pandas as pd
from ipydatagrid import DataGrid
from datetime import datetime
import json
from IPython.display import display as ipy_display
import ipywidgets as widgets
from ipywidgets import HBox, VBox

class EditableGrid:
    def __init__(self, data, columns=None):
        """
        Initialize the EditableGrid with data.

        Parameters:
        data (list of dicts): The data to be displayed in the grid.
        columns (list of str, optional): The columns to be displayed. If None, all columns will be displayed.
        """
        self.original_data = data
        self.processed_data = self.preprocess_data(data)
        self.column_types = self.detect_column_types()
        
        if columns:
            self.processed_data = self.processed_data[columns]
        
        self.grid = DataGrid(self.processed_data, editable=True, auto_fit_columns=True)
        self.grid.on_cell_change(self._on_data_change)
        self.grid.on_cell_click(self._on_cell_click)
        
        # Add Row Button
        self.add_button = widgets.Button(description="+ row", layout=widgets.Layout(width='auto', height='auto'))
        self.remove_button = widgets.Button(description="- row", layout=widgets.Layout(width='auto', height='auto'))
        
        self.add_button.on_click(self.on_add_button_clicked)
        self.remove_button.on_click(self.on_remove_button_clicked)
        
        # DatePicker for editing dates
        self.date_picker = widgets.DatePicker(description='Pick a Date', disabled=False)
        self.date_picker.layout.display = 'none'  # Hide it initially
        
        # Combine buttons and date picker in one HBox
        self.controls = HBox([self.add_button, self.remove_button, self.date_picker])
        
        self.display()
    
    def preprocess_data(self, data):
        """
        Preprocess data for the grid.
        - Convert datetime objects to strings.
        - Convert lists to JSON strings.
        
        Parameters:
        data (list of dicts): The original data.
        
        Returns:
        pd.DataFrame: Preprocessed data.
        """
        processed_data = []
        for row in data:
            processed_row = row.copy()
            for key, value in row.items():
                if isinstance(value, datetime):
                    processed_row[key] = value.strftime('%Y-%m-%d')
                elif isinstance(value, list):
                    processed_row[key] = json.dumps(value)
            processed_data.append(processed_row)
        return pd.DataFrame(processed_data)

    def postprocess_data(self, df):
        """
        Post-process data from the grid.
        - Convert strings back to datetime objects.
        - Convert JSON strings back to lists.
        
        Parameters:
        df (pd.DataFrame): The dataframe from the grid.
        
        Returns:
        list of dicts: Post-processed data.
        """
        postprocessed_data = []
        for _, row in df.iterrows():
            postprocessed_row = row.to_dict()
            for key, value in postprocessed_row.items():
                if isinstance(value, str):
                    try:
                        postprocessed_row[key] = datetime.strptime(value, '%Y-%m-%d')
                    except ValueError:
                        try:
                            postprocessed_row[key] = json.loads(value)
                        except json.JSONDecodeError:
                            pass
            postprocessed_data.append(postprocessed_row)
        return postprocessed_data
    
    def detect_column_types(self):
        """Detect column types of the original data."""
        column_types = {}
        for row in self.original_data:
            for key, value in row.items():
                column_types[key] = type(value).__name__
        return column_types
    
    def display(self):
        """Display the controls, grid, and date picker."""
        ipy_display(VBox([self.controls, self.grid]))
    
    def get_data(self):
        """Get the current data from the grid."""
        return self.postprocess_data(self.grid.data)

    def add_row(self):
        """Add a new row to the grid by duplicating the last row."""
        if not self.processed_data.empty:
            last_row = self.processed_data.iloc[-1].copy()
            new_row = pd.DataFrame([last_row])
            self.processed_data = pd.concat([self.processed_data, new_row], ignore_index=True)
            self.grid.data = self.processed_data
            self._on_data_change(None)

    def remove_row(self):
        """Remove the last row from the grid, if more than one row exists."""
        if len(self.processed_data) > 1:
            self.processed_data = self.processed_data.iloc[:-1].reset_index(drop=True)
            self.grid.data = self.processed_data
            self._on_data_change(None)
    
    def _on_data_change(self, e):
        if e is None:
            return
        
        """Handle data changes in the grid."""
        row = e['row']
        col = e['column_index']
        new_value = e['value']
        
        # Check if the edited cell is a date column
        if self.column_types[self.processed_data.columns[col]] == 'datetime':
            # Try to parse the new value as a date
            try:
                datetime.strptime(new_value, '%Y-%m-%d')
                self.processed_data.iat[row, col] = new_value
                self.date_picker.value = datetime.strptime(new_value, '%Y-%m-%d')
            except ValueError:
                # If the value is not a valid date, reset to the original value
                self.grid.data = self.processed_data
        
        updated_data = self.get_data()
        print("Grid data updated:")
        print(updated_data)
    
    def on_add_button_clicked(self, b):
        """Handler for add row button click."""
        self.add_row()
    
    def on_remove_button_clicked(self, b):
        """Handler for remove row button click."""
        self.remove_row()

    def _on_cell_click(self, e):
        """Handle cell click event."""
        col = e['column_index']
        row = e['row']
        
        # Complete previous date edit if any
        if hasattr(self, 'editing_cell'):
            self._complete_date_edit()
        
        try:
            cell_value = self.processed_data.iloc[row, col]
            if self.column_types[self.processed_data.columns[col]] == 'datetime' and self._is_date_string(cell_value):
                self.date_picker.layout.display = 'block'  # Show the date picker
                self.date_picker.value = datetime.strptime(cell_value, '%Y-%m-%d')
                self.editing_cell = (row, col)
                self.date_picker.observe(self._on_date_change, names='value')
            else:
                self.date_picker.layout.display = 'none'  # Hide the date picker if the cell is not a date cell
        except (ValueError, IndexError, KeyError) as ex:
            print(f"Error handling cell click: {ex}")

    def _complete_date_edit(self):
        """Complete the editing of a date cell."""
        if hasattr(self, 'editing_cell'):
            row, col = self.editing_cell
            current_value = self.processed_data.iat[row, col]
            # If the date picker has a value, update the cell if it has changed
            if self.date_picker.value:
                new_value = self.date_picker.value.strftime('%Y-%m-%d')
                if current_value != new_value:
                    self.processed_data.iat[row, col] = new_value
                    self.grid.data = self.processed_data
                    self._on_data_change(None)
            self.date_picker.unobserve(self._on_date_change, names='value')
            del self.editing_cell
            self.date_picker.layout.display = 'none'  # Hide the date picker after editing

    def _is_date_string(self, value):
        """Check if the value is a string formatted as '%Y-%m-%d'."""
        try:
            datetime.strptime(value, '%Y-%m-%d')
            return True
        except (ValueError, TypeError):
            return False
    
    def _on_date_change(self, change):
        """Handle date picker change event."""
        if hasattr(self, 'editing_cell'):
            self._complete_date_edit()
