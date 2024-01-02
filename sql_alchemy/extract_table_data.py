from ast import NameConstant
import csv
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import urllib

# Define your actual password
password = "Postgresql@678"

# Replace special characters in the password for URL encoding
encoded_password = urllib.parse.quote_plus(password)

# Replace the placeholder in the db_url with the actual password using string formatting
db_url = f"postgresql://postgres:{encoded_password}@localhost/DATA2"

# Create an SQLAlchemy engine
engine = create_engine(db_url)

# Define a base class for declarative models
Base = declarative_base()

# Read the CSV file and extract column names
csv_filename = "color_srgb.csv"  # Replace with your CSV file path

with open(csv_filename, "r") as csv_file:
    csv_reader = csv.reader(csv_file)
    header = next(csv_reader)
for name in header:
    print(name)
# Define a dynamic SQLAlchemy model based on the CSV columns
class DynamicModel(Base):
    __tablename__ = "dynamic_table"

    id = Column(Integer, primary_key=True, autoincrement=True)
    # Define columns dynamically based on the CSV header
    columns = [Column(String, name) for name in header]

# Create the table in the database
Base.metadata.create_all(engine)

# Create a session to interact with the database
Session = sessionmaker(bind=engine)
session = Session()

# Insert data from the CSV file into the table
with open(csv_filename, "r") as csv_file:
    csv_reader = csv.DictReader(csv_file)
    for row in csv_reader:
        new_data = DynamicModel(**row)
        session.add(new_data)

session.commit()

# Query data from the table
result = session.query(DynamicModel).first()
if result:
    print(f"ID: {result.id}, Data: {result.__dict__}")
else:
    print("No data found")

# Close the session
session.close()
