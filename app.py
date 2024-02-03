from flask import Flask, render_template

app = Flask(__name__)

@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/progress')
def about():
    return render_template('progress.html')

@app.route('/forum')
def contact():
    return render_template('forum.html')

if __name__ == '__main__':
    app.run(debug=True)
