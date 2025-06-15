from flask import Flask, request, render_template, jsonify
import sqlite3

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('reviews.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/reviews', methods = ['GET'])
def get_reviews():
    conn = get_db_connection()
    reviews = conn.execute('''
        SELECT reviews.id, books.title, books.author, reviews.rating, reviews.review
        FROM reviews
        JOIN books ON reviews.book_id = books.id
    ''').fetchall()
    conn.close()
    return jsonify([dict(r) for r in reviews])

@app.route('/reviews', methods = ['POST'])
def add_review():
    data = request.json
    title = data['title']
    author = data['author']
    rating = data['rating']
    review_text = data['review']

    conn = get_db_connection()
    book = conn.execute('SELECT id FROM books WHERE title = ? AND author = ?', (title, author)).fetchone()
    if not book:
        conn.execute('INSERT INTO books (title, author) VALUES (?, ?)', (title, author))
        conn.commit()
        book = conn.execute('SELECT id FROM books WHERE title = ? AND author = ?', (title, author)).fetchone()

    conn.execute('INSERT INTO reviews (user_id, book_id, rating, review) VALUES (?, ?, ?, ?)', (1, book['id'], rating, review_text))
    conn.commit()
    conn.close()

    return jsonify({'status':'success'}), 201


if __name__ == '__main__':
    app.run(debug = True)