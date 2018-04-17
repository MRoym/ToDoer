from app import db
import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import event

class Task(db.Model):
  __tablename__ = 'task'

  id = db.Column(db.Integer, primary_key=True)
  user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
  task = db.Column(db.String(), nullable=False)
  date_created = db.Column(db.DateTime)
  group = db.Column(db.String(20))
  completed = db.Column(db.Boolean())


  def __init__(self, user_id, task, group):
    self.user_id = user_id
    self.task = task
    self.date_created = datetime.datetime.now()
    self.group = group
    self.completed = False

  def __repr__(self):
    return '<id {}>'.format(self.id)


class User(db.Model):
  __tablename__ = 'user'

  id = db.Column(db.Integer, primary_key=True)
  username = db.Column(db.String(15), nullable=False)
  password = db.Column(db.String(), nullable=False)
  tasks = db.relationship("Task", backref="user", lazy=True)

  def __init__(self, username, password):
    self.username = username
    self.password = generate_password_hash(password)

  def check_password(self, pswd):
    return check_password_hash(self.password, pswd)



class Achievement(db.Model):
    __tablename__ = 'achievements'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime)

    def __init__(self, name, description, date_created):
        self.name = name
        self.description = description
        self.date_created = datetime.datetime.now()

class UserStatistics(db.Model):
    __tablename__ = 'user_statistics'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    num_tasks = db.Column(db.Integer, nullable=False, server_default="0")
    num_deleted = db.Column(db.Integer, nullable=False, server_default="0")
    num_completed = db.Column(db.Integer, nullable=False, server_default="0")
    max_completed_one_day = db.Column(db.Integer, nullable=False, server_default="0")
    num_completed_consecutive_days = db.Column(db.Integer, nullable=False, server_default="0")
    max_completed_consecutive_days = db.Column(db.Integer, nullable=False, server_default="0")

    def __init__(self, user_id):
        self.user_id = user_id
        """
        self.num_tasks = num_tasks
        self.num_deleted = num_del
        self.num_completed = num_comp
        self.num_completed_one_day = num_one_day
        self.max_completed_one_day = max_one_day
        self.num_completed_consecutive_days = num_cons_days
        self.max_completed_consecutive_days = max_cons_days
"""

def add_statistics_for_user(mapper, connection, target):
    session = db.create_scoped_session()
    stat = UserStatistics(target.username)
    session.add(stat)
    session.commit()

event.listen(User, 'after_insert', add_statistics_for_user)
