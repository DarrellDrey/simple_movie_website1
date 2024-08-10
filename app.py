from flask import Flask, request, redirect, url_for, render_template
import sqlite3

app = Flask(__name__)
DATABASE = 'movie.db'

def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    db = get_db()
    cur = db.execute('SELECT * FROM movies')
    movies = cur.fetchall()
    db.close()
    return render_template('index.html', movies=movies)

@app.route('/add', methods=['GET', 'POST'])
def add_movie():
    if request.method == 'POST':
        title = request.form['title']
        year = request.form['year']
        db = get_db()
        db.execute('INSERT INTO movies (title, year) VALUES (?, ?)', (title, year))
        db.commit()
        db.close()
        return redirect(url_for('index'))
    return render_template('add_movie.html')

@app.route('/delete/<int:id>')
def delete_movie(id):
    db = get_db()
    db.execute('DELETE FROM movies WHERE id = ?', (id,))
    db.commit()
    db.close()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True, port=5001)
