from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, IntegerField
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo
from app.models import User
from flask_login import current_user

class RegistrationForm(FlaskForm):
    login_mail = StringField('Ashoka Email ID', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_email(self, ashoka_email):
        user = User.query.filter_by(email=ashoka_email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address')
        
class UserDetailsForm(FlaskForm):
    name=StringField('Name', validators=[DataRequired()])
    ashoka_id=StringField('Ashoka ID', validators=[DataRequired()])    
    flat_number=StringField('Flat Number', validators=[DataRequired()])
    room_number=IntegerField('Room Number', validators=[DataRequired()])
    submit=SubmitField('Continue')       
        
class LogInForm(FlaskForm):
    login_mail=StringField('Ashoka Email ID', validators=[DataRequired()])
    password=PasswordField('Password', validators=[DataRequired()])
    remember_me=BooleanField('Remember Me')
    submit=SubmitField('Sign In')
    register=SubmitField('Register Here')


                         