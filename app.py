from flask import Flask, request, render_template, redirect, url_for, session, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
import os
from datetime import datetime

app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

from forms import *
from models import *


@app.route('/')
def index():

  if "username" in session:

    user = User.query.filter_by(username=session["username"]).first()
    tasks = user.tasks
    groups = get_groups()
    task_data = {}
    for g in groups:
      if not g in task_data:
        task_data[g] = []

    for t in tasks:
      if not t.completed:
        task_data[t.group].append(t)
    return render_template("/index.html", tasks=tasks, groups=task_data)

  else:
    flash("You need to login to see or edit your to dos", "Error")
    return render_template("/index.html")


  return render_template("/index.html")




@app.route('/login', methods=['GET', 'POST'])
def login():

  form = LoginForm()

  if request.method == 'POST':

    if form.validate():
      session["username"] = form.user.username
      return redirect(url_for("index"))

    else:
      flash("Invalid login credentials", "Error")
      return render_template("/login.html", form=form)

  if request.method == "GET":

    if 'username' in session:
      return render_template("/index.html", form=form)

    return render_template("/login.html", form=form)


@app.route('/signup', methods=['GET', 'POST'])
def signup():

  form = SignupForm()

  if request.method == 'GET':
    return render_template("/signup.html", form=form)
  else:

    if not 'username' in session:
      if form.validate():
        user = User(form.username.data, form.password.data)
        db.session.add(user)
        db.session.commit()
        session["username"] = user.username
        flash("Awesome! Thanks for joining", "Success")
        flash("You can add new tasks by clicking the Add button", "Info")
        return redirect(url_for("index"))
      else:
        flash("That username is already taken", "Error")
        return render_template("/signup.html", form=form)
    else:
      flash("You're already logged in.")
      return render_template("/index.html")


@app.route('/logout', methods=["GET"])
def logout():

  if "username" in session:
    session.pop("username", None)
    flash("You're logged out", "Success")
    return render_template("/index.html")

  else:
    flash("You're not logged in", "Error")
    return render_template("/index.html")



@app.route("/add", methods=["POST"])
def add_task():
  if request.method == "POST":

    if "username" in session:
      t_descr = request.form['task']
      try:
        group = t_descr.split("#")[1].strip()
        t_descr = t_descr.split("#")[0].strip()
      except IndexError:
        group = ""

      user = User.query.filter_by(username=session["username"]).first()

      new_task = Task(user.id, t_descr, group)
      db.session.add(new_task)
      db.session.commit()
      flash("Cool, you added a new task", "Success")
      return redirect(url_for("index"))

    else:
      return redirect(url_for("index"))

  return redirect(url_for("index"))


@app.route("/delete/<task_id>", methods=["GET"])
def delete_task(task_id):
  if "username" in session:

    user = User.query.filter_by(username=session["username"]).first()
    tasks = [i for i in user.tasks if i.id==int(task_id)]

    if tasks:

      task_to_delete = tasks[0]
      db.session.delete(task_to_delete)
      db.session.commit()
      flash("Task deleted", "Success")
      return redirect(url_for("index"))
    else:
      flash("We couldn't delete that task.", "Error")
      return redirect(url_for("index"))

  else:
    flash("You're not logged in.", "Error")
    return redirect(url_for("index"))


@app.route("/complete/<task_id>", methods=["GET"])
def mark_complete(task_id):

  if "username" in session:
    user = User.query.filter_by(username=session["username"]).first()
    tasks = [i for i in user.tasks if i.id==int(task_id)]

    if tasks:
      task = tasks[0]
      task.completed = True
      db.session.commit()
      flash("Nice job!", "Success")
      return redirect(url_for("index"))


    else:
      flash("Oops, something went wrong.", "Error")
      return redirect(url_for("index"))

  else:
    flash("You're not logged in.", "Error")
    return redirect(url_for("index"))


@app.route("/groups", methods=["GET"])
def group_json():
  return jsonify(get_groups())

def get_groups():
  if "username" in session:
    user = User.query.filter_by(username=session["username"]).first()

    tasks = Task.query.filter_by(user_id=user.id, completed=False)
    groups = [g.group for g in tasks]
    groups = list(set(groups))
    return groups
  else:
    return {"Error":"Error"}


@app.template_filter()
def timesince(dt, default="just now"):

    now = datetime.datetime.now()
    diff = now - dt
    seconds = diff.seconds
    interval = round(seconds/31536000)

    if interval > 1:
        return "%d years ago" % interval
    interval = round(seconds / 2592000);
    if interval > 1:
        return "%d months ago" % interval
    interval = round(seconds / 86400);
    if interval > 1:
        return "%d days ago" % interval
    interval = round(seconds / 3600);
    if interval > 1:
        return "%d hours ago" % interval
    interval = round(seconds / 60);
    if interval > 1:
        return "%d minutes ago" % interval
    interval = round(seconds / 2592000);

    return "%d seconds ago" % interval


if __name__ == '__main__':
    app.run()
