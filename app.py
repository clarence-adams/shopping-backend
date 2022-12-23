import configparser
from flask import Flask, session
import psycopg_pool

# Get secrets from the config file
# TODO: Handle exceptions if config file does not exist
config = configparser.ConfigParser()
config.read("config.ini")
secrets = config["secrets"]
session_secret = secrets["SessionSecret"]
connection_string = secrets["ConnectionString"]

app = Flask(__name__)

app.secret_key = session_secret

# Connect to the database
try:
    psql_pool = psycopg_pool.ConnectionPool(connection_string)
# TODO: Make this a better error
except:
    print("No database connection")


@app.get("/list")
def get_list():
    with psql_pool.connection() as conn:
        records = conn.execute("SELECT * FROM items;").fetchall()
        return records


@app.post("/list")
def create_list():
    return "You added a thingy!"


@app.put("/list")
def update_list():
    return "You updated a thingy!"


@app.delete("/list")
def delete_list():
    return "You deleted a thingy!"


if __name__ == "__main__":
    app.run()
