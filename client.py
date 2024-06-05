from excel_like_table import create_table

# Use create_table function
data = [
    {'name': 'John', 'birthday': '1990-01-01', 'age': 30, 'city': ['New York', 'Los Angeles']},
    {'name': 'Jane', 'birthday': '1995-05-10', 'age': 25, 'city': ['San Francisco', 'Chicago']}
]
app = create_table(data)

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)

# Check data
app.data
