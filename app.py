from flask import Flask, render_template, request, redirect      #used html.
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask import jsonify

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ToDo.db'    #database file location
db = SQLAlchemy(app)
app.app_context().push()

class Users(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable = False)
    desc =  db.Column(db.String(500), nullable = False)
    date_created = db.Column(db.DateTime, default = datetime.utcnow)
    
    def __repr__(self) -> str:
        return f"{self.sno} - {self.title}"
           
@app.route('/', methods=["GET", "POST"])
def hello_world():
    new_title = ""
    new_desc = ""
    if request.method=="POST":
        new_title = request.form.get('title')
        new_desc = request.form.get('desc')
        todo = Users(title = new_title, desc = new_desc)
        db.session.add(todo)
        db.session.commit()
    allTodo = Users.query.all()
    print(allTodo)
    return render_template("index.html", allTodo=allTodo)

@app.route('/shows')
def products():
    allTodo = Users.query.all()
    print(allTodo)
    return 'welcome to products page'

@app.route('/delete/<int:sno>', methods=['GET', 'DELETE'])
def delete(sno):
    todo = Users.query.filter_by(sno=sno).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect('/')

@app.route('/update/<int:sno>', methods=["GET", "POST"])
def update(sno):
    if request.method == 'POST':
        new_title = request.form.get('title')
        new_desc = request.form.get('desc')
        todo = Users.query.filter_by(sno=sno).first()
        todo.title=new_title
        todo.desc=new_desc
        db.session.add(todo)
        db.session.commit()
        return redirect('/')
    todo = Users.query.filter_by(sno=sno).first()
    return render_template("update.html", todo = todo)

# @app.errorhandler(404)
# def invalid_route(e):
#     #return "invalid route"
#     return jsonify({'errorcode': 404, 'message': 'Invalid Route'})

     