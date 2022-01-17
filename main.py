from flask import Flask, render_template,request,url_for
from flask_mysqldb import MySQL
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy 
from datetime import datetime
from flask import send_from_directory
import MySQLdb.cursors
app=Flask(__name__)
@app.route('/')
def hello_world():
    return render_template("index.html")   
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER']='root'
app.config['MYSQL_PASSWORD']=''
app.config['MYSQL_DB']='login'
mysql=MySQL(app)
@app.route('/py') 
def python():
    return render_template("python.html")
@app.route('/c') 
def c():
    return render_template("ds.html")
@app.route('/dsa') 
def dsa():
    return render_template("dsa.html")
@app.route('/dbms')    
def dbms():
    return render_template("dbms.html")  
@app.route('/se')
def se():
    return render_template("SE.html")  
@app.route('/signup')
def signup():
    return render_template("signup.html")       
@app.route('/login', methods =['GET', 'POST'])
def login():
    msg = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        # cursor.execute('INSERT INTO login VALUES ( % s, % s)', (username, password))
        # mysql.connection.commit()
        cursor.execute('SELECT * FROM signin WHERE username = % s AND password = % s',(username, password,))
        fetchdata=cursor.fetchall()
        count=cursor.rowcount
        if (count==1):
                 return render_template("index.html",data=username)
        else:
            return(render_template("index.html",data="frist signup"))         
@app.route('/register', methods =['GET', 'POST'])
def register():
    msg=''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form :
        username = request.form['username']
        password = request.form['password']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('INSERT INTO signin VALUES (% s,% s)', (username, password))
        mysql.connection.commit()
        msg = username
        return render_template('index.html',data=msg) 
    elif request.method == 'POST':
        return render_template('index.html') 
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///C:/Users/chint/OneDrive/Desktop/projects/Blogging-Website-using-Flask-main/blog.db'
db = SQLAlchemy(app)
class Blogpost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50))
    subtitle = db.Column(db.String(50))
    author = db.Column(db.String(20))
    date_posted = db.Column(db.DateTime)
    content = db.Column(db.Text)            
@app.route('/b')
def index():
    posts = Blogpost.query.order_by(Blogpost.date_posted.desc()).all()
    return render_template('index2.html', posts=posts)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/post/<int:post_id>')
def post(post_id):
    post = Blogpost.query.filter_by(id=post_id).one()
    return render_template('post.html', post=post)

@app.route('/add')
def add():
    return render_template('add.html')

@app.route('/delete')
def delete():
    posts = Blogpost.query.order_by(Blogpost.date_posted.desc()).all()
    return render_template('delete.html', posts=posts)

@app.route('/addpost', methods=['POST'])
def addpost():
    title = request.form['title']
    subtitle = request.form['subtitle']
    author = request.form['author']
    content = request.form['content']

    post = Blogpost(title=title, subtitle=subtitle, author=author, content=content, date_posted=datetime.now())

    db.session.add(post)
    db.session.commit()

    return redirect(url_for('index'))

@app.route('/deletepost', methods=['DELETE','POST'])
def deletepost():
    post_id = request.form.get("post_id")

    post = Blogpost.query.filter_by(id=post_id).first()

    db.session.delete(post)
    db.session.commit()
    return redirect(url_for('index'))
if __name__ == '__main__':
    app.run(debug=True)       
               



