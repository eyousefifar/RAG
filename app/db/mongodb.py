from pymongo import MongoClient
import os

# MOVE to a config file
database_url = os.getenv("DATABASE_URL")
if database_url:
    print(f"Database URL: {database_url}")
else:
    print("DATABASE_URL environment variable is not set.")

# def create_user():
#     client = MongoClient(database_url)

#     # Specify the database where the user will be created
#     db = client["admin"]

#     # Create the new user with readWrite role on the specified database
#     db.command("createUser", "root",
#                pwd="example",  # Replace with your desired password
#                roles=[{"role": "readWrite", "db": "rag"}])

#     print("User 'root' created successfully with readWrite role on 'rag' database")





def get_database():

    client = MongoClient(database_url)
    return client["admin"]


