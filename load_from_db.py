import pandas as pd
import sqlalchemy as db

# Set up the connection URL
host = '193.104.57.46'
port = '5432'
username = 'postgres'
password = '1986'
database_name = 'postgres'

# Create the connection URL
url = f'postgresql+psycopg2://{username}:{password}@{host}:{port}/{database_name}'

# Create the engine and connect to the database
engine = db.create_engine(url)
connection = engine.connect()

# Get dataframe from remote database
songs = pd.read_sql_table('spotifysongs', con=engine)
songs = songs.iloc[:,:8]

# query spotifysongs with sql
# query = "SELECT * FROM spotifysongs where track_artist = 'Sia'"
# songs = pd.read_sql_query(query, con=engine)

print(songs.info())
print(songs.head(10))
print("Data successfully loaded")

# Save dataframe as csv
# csv_file_name = 'songs.csv'
# songs.to_csv(csv_file_name, index=False)
# print(f"Data successfully saved to {csv_file_name}")

# Close the connection
connection.close()