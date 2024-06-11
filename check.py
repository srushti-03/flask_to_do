import sqlite3

# Connect to the database
conn = sqlite3.connect('todo.db')
cursor = conn.cursor()

# Execute SQL query to select all records from Todo table
cursor.execute("SELECT * FROM todo")

# Fetch all rows and print them
rows = cursor.fetchall()
for row in rows:
    print(row)

# Close the connection
conn.close()
