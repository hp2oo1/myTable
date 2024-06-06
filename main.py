from editable_data_grid import EditableDataGrid
from datetime import datetime

# Sample data
data = [
    {"name": "Alice", "age": 30, "city": "New York", "hobbies": ["reading", "hiking", "coding"], "birthday": datetime(1993, 1, 15), "scores": [85.5, 92.3, 78.8]},
    {"name": "Bob", "age": 25, "city": "San Francisco", "hobbies": ["swimming", "gaming"], "birthday": datetime(1998, 4, 22), "scores": [88.0, 76.4]},
    {"name": "Charlie", "age": 35, "city": "Chicago", "hobbies": ["running", "cooking", "travelling", "photography"], "birthday": datetime(1989, 11, 30), "scores": [91.2, 89.5, 95.3, 82.4]}
]

# Example usage:
editable_grid = EditableDataGrid(data)

editable_grid.get_updated_data()


