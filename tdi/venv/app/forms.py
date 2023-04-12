from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, IntegerField, DateField, SelectField, TextAreaField
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo
from app.models import User
from flask_login import current_user

class RegistrationForm(FlaskForm):
    ashoka_email = StringField('Ashoka Email ID', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_email(self, ashoka_email):
        user = User.query.filter_by(email=ashoka_email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address')
        
class UserDetailsForm(FlaskForm):
    name=StringField('Name', validators=[DataRequired()])
    ashoka_id=IntegerField('Ashoka ID', validators=[DataRequired()])    
    flat=IntegerField('Flat Number', validators=[DataRequired()])
    #floor=SelectField('Floor', choices=[('GF','GF'),('FF','FF'),('SF','SF'),('TF','TF'),('Duplex','Duplex')],validators=[DataRequired()])
    room=IntegerField('Room Number', validators=[DataRequired()])
    submit=SubmitField('Continue')  
        
class LogInForm(FlaskForm):
    ashoka_email=StringField('Ashoka Email ID', validators=[DataRequired()])
    password=PasswordField('Password', validators=[DataRequired()])
    remember_me=BooleanField('Remember Me')
    submit=SubmitField('Sign In')
    register=SubmitField('Register Here')

class MealForm(FlaskForm):
    meal_date=DateField('Date')
    book=SubmitField('Book')

#class HouseForm(FlaskForm):
    #house_time=SelectField('Time Slot', choices=[('8 - 9'), ('9 - 10'), ('10 - 11'), ('11 - 12'), ('12 - 1'), ('2 - 3'), ('3 - 4'), ('4 - 5')])
    #remarks=TextAreaField('Remarks')
    #submit=SubmitField('Submit')



                         