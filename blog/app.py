from flask import Flask, render_template, redirect, url_for, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
# Initializing app
app = Flask(__name__)

# Configuring database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'

# Creating db object
db = SQLAlchemy(app)

# Creating model
class Post(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    author = db.Column(db.String(50), nullable = False)
    title = db.Column(db.String(50), nullable = False)
    short_description = db.Column(db.String(100), nullable = False)
    detailed_description = db.Column(db.Text)
    date_created = db.Column(db.DateTime, nullable=False, default_value = datetime.utcnow )

@app.route('/', methods=['GET', 'POST'])
def home():
    posts = Post.query.order_by(Post.date_created).all()
    return render_template('home.html', posts=posts)

@app.route('/add_post', methods=['POST'])
def add_post():
    if request.method == 'POST':
        author = request.form['author']
        title = request.form['title']
        short_description = request.form['short_description']
        detailed_description = request.form['detailed_description']
        new_post = Post(author=author, title=title, short_description=short_description, detailed_description=detailed_description, date_created = datetime.now())
        db.session.add(new_post)
        db.session.commit()
    return redirect(url_for('home'))

@app.route('/display_post/<int:id>', methods=['GET', 'POST'])
def display_post(id):
    post = Post.query.get(id)
    return render_template('display_post.html', post=post)

if __name__ == '__main__':
    app.run(debug=True)