
from flask import Flask, render_template
import psycopg2

app = Flask(__name__)

# Define the name of the table and columns in the database
table_name = "sreality"
name_column = "Names"
image_column = "Images"

@app.route("/")
def index():
    conn = psycopg2.connect(
        host="host.docker.internal",
        database="sreality_db",
        user="postgres",
        password="password",
        port="5555"
    )
    cursor = conn.cursor()
    select_query = f"SELECT {name_column}, {image_column} FROM {table_name}"
    cursor.execute(select_query)
    data = []
    for row in cursor.fetchall():
        item = {"title": row[0], "image": row[1]}
        data.append(item)
    cursor.close()
    conn.close()
    return render_template("index.html", data=data)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080, debug = True)
