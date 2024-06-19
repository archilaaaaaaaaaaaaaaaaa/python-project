from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50))
    password = db.Column(db.String(100))

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.Text)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

@app.route('/')
def index():
    return render_template('index1.html')

@app.route('/shop')
def ship():
    return render_template('shop.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User(username=username, password=password)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('register1.html')

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    user_id = session['user_id']
    user = User.query.get(user_id)
    posts = Post.query.filter_by(user_id=user_id).all()
    return render_template('dashboard.html', user=user, posts=posts)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username, password=password).first()
        if user:
            session['user_id'] = user.id
            return redirect(url_for('dashboard'))
        else:
            return "Invalid username or password"
    return render_template('login.html')

@app.route('/logout')
def logout():
    del session['user_id']
    session.modified = True
    return redirect(url_for('index'))

@app.route('/add_post', methods=['GET', 'POST'])
def add_post():
    if 'user_id' not in session:
        return redirect(url_for('login'))
    if request.method == 'POST':
        description = request.form['description']
        user_id = session['user_id']
        post = Post(description=description, user_id=user_id)
        db.session.add(post)
        db.session.commit()
        return redirect(url_for('dashboard'))
    return render_template('add_post.html')

class Nigger(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(100))
    price = db.Column(db.Integer)
    owner_id = db.Column(db.Integer, db.ForeignKey('owner.id'))

    def __repr__(self):
        return f"<Nigger: {self.id}, {self.name}, {self.price}>"

class Owner(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(100))
    niggers = db.relationship('Nigger', backref='owner', lazy=True)

    def __repr__(self):
        return f"{self.name}"


@app.route("/")
def main():
    # ვირჩევთ ყველა ზანგს ჩვენი მონაცემთა ბაზიდან
    # ეს იგივეა რაც "SELECT * FROM Nigger"
    niggers = Nigger.query.all()
    return render_template("main.html", niggers = niggers)


@app.route("/add_nigger", methods=["GET", "POST"])
def add_nigger():
    if request.method == "POST":
        # ვქმნით ჯერ Owner'ს
        owner_name = request.form["owner"]
        nigger_owner = Owner(name=owner_name)
       
        db.session.add(nigger_owner)  
        db.session.commit()    
        
        nigger_name = request.form["name"]
        nigger_price = request.form["price"]
        nigger = Nigger(name=nigger_name, owner=nigger_owner, price=nigger_price)
        # ვამატებთ ცვლილებებს
        db.session.add(nigger) 
        db.session.commit()    
        return redirect(url_for("main")) 
    return render_template("add_course.html")

@app.route("/buy_nigger/<int:pk>", methods=["POST"])
def buy_nigger(pk):
    # ვქმნით ჯერ Owner'ს
    owner_name = request.form["owner"]
    nigger_owner = Owner(name=owner_name)
    # ვამატებთ ცვლილებებს
    db.session.add(nigger_owner)
    db.session.commit()
    # ვირჩევთ Nigger 'ს, ეს იგივეა რაც "SELECT * FROM Nigger WHERE id = pk"
    nigger = Nigger.query.get(pk)
    # ვანიჭებთ ზანგ ბიჭუნას ახალ პატრონს
    nigger.owner = nigger_owner
    # ვადასტურებთ ცვლილებებს
    db.session.commit()
    return redirect(url_for("main"))     

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
