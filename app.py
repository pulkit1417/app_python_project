import json
import os
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

DATA_FILE = 'library.json'

# Load library data from JSON file
def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as file:
            return json.load(file)
    return []

# Save library data to JSON file
def save_data(library):
    with open(DATA_FILE, 'w') as file:
        json.dump(library, file)

@app.route('/')
def index():
    search_query = request.args.get('search', '')
    sort_by = request.args.get('sort', 'title')
    library = load_data()
    
    # Filter and sort the library
    books = [book for book in library if search_query.lower() in book['title'].lower()]
    books.sort(key=lambda x: x[sort_by])
    
    return render_template('index.html', books=books, search_query=search_query)

@app.route('/add', methods=['POST'])
def add_book():
    title = request.form.get('title')
    author = request.form.get('author')
    category = request.form.get('category')
    rating = request.form.get('rating', 0)
    library = load_data()
    library.append({'title': title, 'author': author, 'category': category, 'rating': rating})
    save_data(library)
    return redirect(url_for('index'))

@app.route('/delete/<int:book_id>', methods=['POST'])
def delete_book(book_id):
    library = load_data()
    if 0 <= book_id < len(library):
        del library[book_id]
        save_data(library)
    return redirect(url_for('index'))

@app.route('/edit/<int:book_id>', methods=['GET', 'POST'])
def edit_book(book_id):
    library = load_data()
    book = library[book_id]
    if request.method == 'POST':
        book['title'] = request.form.get('title')
        book['author'] = request.form.get('author')
        book['category'] = request.form.get('category')
        book['rating'] = request.form.get('rating', 0)
        save_data(library)
        return redirect(url_for('index'))
    return render_template('edit.html', book=book)

@app.route('/details/<int:book_id>')
def book_details(book_id):
    library = load_data()
    book = library[book_id]
    return render_template('details.html', book=book)

if __name__ == '__main__':
    app.run(debug=True)
