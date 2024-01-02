import psycopg2
import csv
import pandas as pd

# Replace with your PostgreSQL database credentials
db_connection = psycopg2.connect(
    host="localhost",
    database="postgres1",
    user="postgres",
    password="Postgresql@678"
)

# Define the path to your CSV file
csv_file_path = "1.csv"

# Open and read the CSV file to retrieve column names
with open(csv_file_path, 'r') as csv_file:
    csv_reader = csv.reader(csv_file)
    header_row = next(csv_reader)  # Read the header row

# Set all columns to have VARCHAR data type
datatypes = ["VARCHAR(255)"] * len(header_row)

# Create the table dynamically based on column names and datatypes
table_name = "your_dynamic_table"

create_table_sql = f"CREATE TABLE IF NOT EXISTS {table_name} ("

for column_name, datatype in zip(header_row, datatypes):
    create_table_sql += f"{column_name} {datatype}, "

# Remove the trailing comma and space
create_table_sql = create_table_sql.rstrip(', ')
create_table_sql += ");"

# Create a cursor and execute the SQL command to create the table
cursor = db_connection.cursor()
cursor.execute(create_table_sql)
cursor.close()

# Open and read the CSV file again
with open(csv_file_path, 'r') as csv_file:
    csv_reader = csv.reader(csv_file)
    next(csv_reader)  # Skip the header row if it exists

    # Create a cursor and execute INSERT statements for each row
    cursor = db_connection.cursor()

    # Generate column names and placeholders dynamically
    columns = ', '.join(header_row)
    placeholders = ', '.join(['%s'] * len(header_row))

    for row in csv_reader:
        insert_sql = f"""
            INSERT INTO {table_name} ({columns})
            VALUES ({placeholders});
        """
        cursor.execute(insert_sql, tuple(row))

    # Commit the changes and close the cursor and connection
    db_connection.commit()
    cursor.close()


# Define the query to retrieve the data from the PostgreSQL table
query = "SELECT * FROM your_dynamic_table;"

# Load the data into a DataFrame
df = pd.read_sql(query, db_connection)
print(df)
# Close the database connection
db_connection.close()