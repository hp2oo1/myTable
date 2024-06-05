from datetime import date
import dash
from dash import html, dcc
from dash.dependencies import Input, Output, State
from dash import dash_table
import pandas as pd
import copy

def determine_column_types(data):
    # Determine the type of each column by inspecting the first row
    column_types = {key: type(value) for key, value in data[0].items()}
    return column_types

def preprocess_data(data, column_types):
    # Convert list of strings to a single string for columns that contain lists
    for row in data:
        for key, value in row.items():
            if column_types[key] == list:
                row[key] = ', '.join(value)
    return data

def postprocess_data(data, column_types):
    # Convert a single string to a list of strings for columns that contain lists
    processed_data = []
    for row in data:
        if not all(value == '' for value in row.values()):  # Check if all values are empty
            for key, value in row.items():
                if column_types[key] == list and isinstance(value, str):
                    row[key] = value.split(', ')
            processed_data.append(row)
    return processed_data

def create_table(data):
    # Determine the column types
    column_types = determine_column_types(data)

    # Preprocess the data
    data = preprocess_data(data, column_types)

    # Create a Dash app
    app = dash.Dash(__name__)
    app.data = postprocess_data(copy.deepcopy(data), column_types)

    df = pd.DataFrame(data)

    # Define the layout of the app
    app.layout = html.Div([
        html.Button('+ row', id='add-row-button'),
        html.Button('- row', id='remove-row-button'),
        dash_table.DataTable(
            id='table',
            columns=[{"name": i, "id": i} for i in df.columns],
            data=df.to_dict('records'),
            editable=True,
            row_deletable=True
        )
    ])

    @app.callback(
        Output('table', 'data'),
        [Input('table', 'data_timestamp'), Input('table', 'selected_rows'), Input('add-row-button', 'n_clicks'), Input('remove-row-button', 'n_clicks')],
        [State('table', 'data'), State('table', 'columns')]
    )
    def update_rows(timestamp, selected_rows, n_clicks_add, n_clicks_remove, rows, columns):
        ctx = dash.callback_context

        if ctx.triggered[0]['prop_id'] == 'add-row-button.n_clicks':
            if n_clicks_add:
                # Append an empty row
                rows.append({c['id']: '' for c in columns})
        elif ctx.triggered[0]['prop_id'] == 'remove-row-button.n_clicks':
            if n_clicks_remove:
                if len(rows) > 1:  # Ensure there's always at least one row
                    rows.pop()
        elif ctx.triggered[0]['prop_id'] == 'table.data_timestamp':
            if timestamp:
                rows.append({c['id']: '' for c in columns})
        elif ctx.triggered[0]['prop_id'] == 'table.selected_rows':
            if selected_rows:
                rows = [i for j, i in enumerate(rows) if j not in selected_rows]

        app.data = postprocess_data(copy.deepcopy(rows), column_types)
        return rows

    return app
