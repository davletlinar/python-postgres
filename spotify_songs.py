import sqlalchemy as db
import pandas as pd

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

# Reading data from CSV
songs = pd.read_csv("spotify_songs.csv", delimiter=',')

# Writing data to database
songs.to_sql('spotifysongs', con=engine, if_exists='replace', index=False)

print("Data successfully transferred")

# Close the connection
connection.close()