from flask import Flask,request,redirect,render_template
import sqlite3
import string
import random

app=Flask(__name__)

#Function to generate a short URL
def generate_short_url():
    char = string.ascii_letters + string.digits
    short_url = ''.join(random.choices(char,k=6))
    return short_url

#Function to store URL mapping in the database
def store_url_mapping(original_url, short_url):
    conn = sqlite3.connect('urls.db')
    c = conn.cursor()
    c.execute('INSERT INTO urls (original_url, short_url) VALUES (?, ?)', (original_url, short_url))
    conn.commit()
    conn.close()

#Function to get the original URL from the short URL
def get_original_url(short_url):
    conn = sqlite3.connect('urls.db')
    c = conn.cursor()
    c.execute('SELECT original_url FROM urls WHERE short_url = ?', (short_url,))
    result = c.fetchone()
    conn.close()
    return result[0] if result else None

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        original_url = request.form['original_url']
        short_url = generate_short_url()
        store_url_mapping(original_url, short_url)
        return render_template('index.html', short_url=request.host_url + short_url)
    return render_template('index.html')

@app.route('/<short_url>')
def redirect_to_original(short_url):
    original_url = get_original_url(short_url)
    if original_url:
        return redirect(original_url)
    else:
        return 'URL not found', 404

if __name__ == '__main__':
    app.run(debug=True)