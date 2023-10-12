import pandas as pd
import sqlalchemy as db
from clean_contacts import get_clean_contacts

# Set up the connection URL
host = '193.104.57.46'
port = '5432'
username = 'postgres'
password = '1986'
database_name = 'contacts-tsz'

# Create the connection URL
url = f'postgresql+psycopg2://{username}:{password}@{host}:{port}/{database_name}'

# Create the engine and connect to the database
engine = db.create_engine(url)
connection = engine.connect()

# Get dataframe from remote database
db_contacts = pd.read_sql_table('contacts', con=engine)

# Reorganize order of columns
db_contacts = db_contacts[['apartment_number', 'first_name', 'last_name', 'phone_1', 'phone_2']]

# Sort dataframe by apartment_number
db_contacts = db_contacts.sort_values(by='apartment_number')

print(db_contacts.head(10))
print("Data successfully loaded")

# Save dataframe as csv
csv_file_name = 'db_contacts.csv'
db_contacts.to_csv(csv_file_name, index=False)
print(f"Data successfully saved to {csv_file_name}")

# Close the connection
connection.close()