from wtforms import Form, StringField, PasswordField, validators

class LoginForm(Form):
    username = StringField("username",
                           validators=[validators.DataRequired(message="Username must be provided.")])
    password = PasswordField("password",
                             validators=[validators.DataRequired(message="Password must be provided.")])
