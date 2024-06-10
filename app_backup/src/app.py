from flask import Flask, render_template
import psycopg2

app = Flask(__name__)

# Function to get a database connection
def get_db_connection():
    conn = psycopg2.connect(
        dbname="main_newsdb",
        user="main_newsuser",
        password="main_password",
        host="main_db",
        port="5432",
    )
    return conn

# Route for the main page
@app.route('/')
def main_page():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM news")
    news_rows = cur.fetchall()
    cur.close()
    conn.close()
    return render_template('index.html', news_rows=news_rows)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
