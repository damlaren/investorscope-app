from wtforms import Form, StringField, PasswordField, validators

class LoginForm(Form):
    username = StringField("username", validators=[validators.DataRequired()])
    password = PasswordField("password", validators=[validators.DataRequired()])
