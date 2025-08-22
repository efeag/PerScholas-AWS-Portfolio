
from flask import Flask, request, jsonify 
from flask_cors import CORS 
import psycopg2 
import os


app = Flask(__name__) 
CORS(app) 
 
DB_HOST = os.environ['DB_HOST'] 
DB_NAME = os.environ['DB_NAME'] 
DB_USER = os.environ['DB_USER'] 
DB_PASS = os.environ['DB_PASS']

conn = psycopg2.connect(host=DB_HOST, database=DB_NAME, 
user=DB_USER, password=DB_PASS) 
cur = conn.cursor() 
cur.execute("""CREATE TABLE IF NOT EXISTS posts ( 
    id SERIAL PRIMARY KEY, 
    title TEXT, 
    content TEXT 
)""") 
conn.commit() 
 
@app.route('/posts', methods=['GET']) 
def get_posts(): 
    cur.execute("SELECT title, content FROM posts ORDER BY id DESC") 
    posts = cur.fetchall() 
    return jsonify([{"title": t, "content": c} for t, c in posts]) 
 
@app.route('/posts', methods=['POST']) 
def create_post(): 
    data = request.get_json() 
    cur.execute("INSERT INTO posts (title, content) VALUES (%s, %s)", 
                (data['title'], data['content'])) 
    conn.commit() 
    return jsonify({"status": "success"}), 201 
 
if __name__ == '__main__': 
    app.run(host='0.0.0.0')