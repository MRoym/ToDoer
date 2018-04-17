from flask_wtf import Form
from wtforms import TextField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length
from models import User

class LoginForm(Form):
  username = TextField('username', validators=[DataRequired()])
  password = PasswordField('password', validators=[DataRequired()])

  def __init__(self, *args, **kwargs):
    Form.__init__(self, *args, **kwargs)
    self.user = None

  def validate(self):
    rv = Form.validate(self)
    if not rv:
      return False

    user = User.query.filter_by(username=self.username.data).first()
    if user is None:
      self.username.errors.append('Unknown username')
      return False

    if not user.check_password(self.password.data):
      self.password.errors.append('Invalid password')
      return False

    self.user = user
    return True

class SignupForm(Form):
  username = TextField('username', validators=[DataRequired()])
  password = PasswordField('password', validators=[DataRequired()])

  def __init__(self, *args, **kwargs):
    Form.__init__(self, *args, **kwargs)

  def validate(self):
    rv = Form.validate(self)
    if not rv:
      return False

    user = User.query.filter_by(username=self.username.data).first()
    if not user is None:
      self.username.errors.append('User already exists')
      return False

    return True
