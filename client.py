from editable_data_grid import EditableDataGrid

# Sample data
data = [
    {"name": "Alice", "age": 30, "city": ["New York", "Boston"], "birthday": "1993-01-01"},
    {"name": "Bob", "age": 25, "city": ["San Francisco", "Seattle"], "birthday": "1998-05-15"},
    {"name": "Charlie", "age": 35, "city": ["Los Angeles", "Chicago"], "birthday": "1988-10-22"}
]

# Example usage:
editable_grid = EditableDataGrid(data)

editable_grid.get_updated_data()
