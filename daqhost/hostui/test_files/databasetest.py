import sqlite3

# Connect to the SQLite database
conn = sqlite3.connect('daq.db')

# Create a cursor object
cursor = conn.cursor()

# To empty the database
# cursor.execute("DELETE FROM PINDATA") 
# conn.commit()

# Execute a SELECT query to fetch data
cursor.execute("SELECT * FROM PINDATA")

# Fetch all rows of the result
rows = cursor.fetchall()

# Iterate over the rows and print or process each row
for row in rows:
    print(row)  # Or process the row as needed

# Close the cursor and connection
cursor.close()
conn.close()