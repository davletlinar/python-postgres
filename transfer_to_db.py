import sqlalchemy as db
import pandas as pd
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

# Reading and cleaning data from CSV
contacts = pd.read_csv("my_contacts.csv", delimiter=';')
clean_contacts = get_clean_contacts(contacts)

# Writing data to database
clean_contacts.to_sql('contacts', con=engine, if_exists='replace', index=False)

print("Data successfully transferred")

# Close the connection
connection.close()