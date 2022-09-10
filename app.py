from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///linky.db"
db = SQLAlchemy(app)

class Link(db.Model):
    __tablename__ = 'link'
    id = db.Column(db.Integer, primary_key = True)
    link = db.Column(db.String)
    link_name = db.Column(db.String(200), nullable = False)
    link_description = db.Column(db.String(200), nullable = False)
    date_created = db.Column(db.DateTime, default = datetime.utcnow)

class Category(db.Model):
    __tablename__ = 'category'
    id = db.Column(db.Integer, primary_key = True)
    category = db.Column(db.String(200))
    

    def __init__(self, link, link_name, link_description, category):
        self.link = link 
        self.link_name = link_name
        self.link_description = link_description
        self.category = category

    #def __repr__(self):
    #    return "<Task %r>" % self.id 

@app.route("/", methods=["POST", "GET"])
def index():
    if request.method == 'POST':
      if not request.form['link'] or not request.form['link_name'] or not request.form['link_description'] or not request.form['category']:
         flash('Please enter all the fields', 'error')
      else:
         link = Link( link = request.form['link'], link_name = request.form['link_name'],
           link_description = request.form['link_description'])

         link = Category(category = request.form['category'])
         
         db.session.add(link)
         db.session.add(category)
         db.session.commit()
         #flash('Record was successfully added')
         return redirect('/')
         
    links = Link.query.order_by(Todo.date_created).all()
    categories = Category.query.order_by(Category.id).all()
    return render_template('index.html', [tasks = tasks, categories =categories])


#@app.route("/delete/<int:id>")
#def delete(id):
#    task_to_delete = Todo.query.get_or_404(id)#

#    try:
#        db.session.delete(task_to_delete)
#        db.session.commit()
#        return redirect("/")
#    except:
#        return "There was a problem deleting that task"#

#@app.route("/update/<int:id>", methods = ["GET", "POST"])
#def update(id):
#    task = Todo.query.get_or_404(id)
#    if request.method == "POST":
#        task.link_name = request.form["link_name"]
#        date_dl = datetime.strptime(request.form["date_deadline"], "%Y-%m-%d")
#        task.date_deadline = date_dl  #

#        try:
#            db.session.commit()
#            return redirect("/")
#        except:
#            return "There was an issue updating your task"#

#    else:
#         return render_template("update.html", task = task)  


if __name__ == '__main__':
   db.create_all()
   app.run(debug = True)



