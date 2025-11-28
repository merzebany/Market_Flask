from flask_wtf import FlaskForm
from wtforms import StringField , PasswordField , SubmitField , IntegerField , BooleanField
from wtforms.validators import Length ,EqualTo, Email ,DataRequired ,ValidationError
from My_App.models import User
import config

class RegisterForm(FlaskForm):

    def validate_username (self, username_to_check):
        user = User.query.filter_by(username=username_to_check.data).first()
        if user:
            raise ValidationError("Username already exist Please try a different username")
        
    def validate_email_address (self, email_address_to_check):
        email_address_01 = User.query.filter_by(email_address=email_address_to_check.data).first()
        if email_address_01:
            raise ValidationError("email_address already exist Please try a different email_address")


    username = StringField(label='User Name:', validators=[Length(min=2, max=30), DataRequired()])
    email_address = StringField(label='Email Address:', validators=[Email(), DataRequired()])
    password1 = PasswordField(label='Password:', validators=[Length(min=6), DataRequired()])
    password2 = PasswordField(label='Confirm Password:', validators=[EqualTo('password1'), DataRequired()])
    submit = SubmitField(label='Create Account')


class LoginForm(FlaskForm):
   
    username = StringField(label='User Name:', validators=[DataRequired()])
    password = PasswordField(label='Password:', validators=[DataRequired()])
    submit = SubmitField(label='Sign In')


class PurchaseItemForm(FlaskForm):
    submit = SubmitField(label='Purchase Item!')


class SellItemForm(FlaskForm):
    submit = SubmitField(label='Sell Item!')


class DeleteUserForm(FlaskForm):
    submit = SubmitField(label='Delete User!')


class ItemForm(FlaskForm):

    Item_name = StringField(label='Item Name:', validators=[Length(min=3, max=50), DataRequired()])
    Item_price = IntegerField (label='Item price:', validators=[DataRequired()])
    Item_barcode =StringField(label='Item barcode:', validators=[Length(min=5, max=12), DataRequired()])
    Item_description = StringField(label='Item description:', validators=[Length(min=5, max=1024), DataRequired()]) 
    submit = SubmitField(label='Create Item')


class EditItemForm(FlaskForm):

    Item_name = StringField(label='Item Name:', validators=[Length(min=3, max=50), DataRequired()])
    Item_price = IntegerField (label='Item price:', validators=[DataRequired()])
    Item_barcode =StringField(label='Item barcode:', validators=[Length(min=5, max=12), DataRequired()])
    Item_description = StringField(label='Item description:', validators=[Length(min=5, max=1024), DataRequired()]) 
    submit = SubmitField(label='Edit Item')


class Edit_UserForm(FlaskForm):

#    if config.Validation_on_email_V  == 'username' :
     
     def validate_username (self, username_to_check):
      
      if config.Validation_on_email_V  == 'username' :
        config.Validation_on_email_V == ''

        user = User.query.filter_by(username=username_to_check.data).first()
        if user:
            raise ValidationError("Username already exist Please try a different username")
        
#    if config.Validation_on_email_V  == 'email' :
     
     def validate_email_address (self, email_address_to_check):
       
       if config.Validation_on_email_V  == 'email':
        config.Validation_on_email_V  == ''

        email_address_01 = User.query.filter_by(email_address=email_address_to_check.data).first()
        if email_address_01:
            raise ValidationError("email_address already exist Please try a different email_address")


     username = StringField(label='User Name:', validators=[Length(min=2, max=30), DataRequired()])
     email_address = StringField(label='Email Address:', validators=[Email(), DataRequired()])
     budget = IntegerField (label='User Budget:', validators=[DataRequired()])
     admin = BooleanField (label='Admin User:', render_kw={'class': 'my-checkbox large-checkbox'} )
     submit = SubmitField(label='Edit User Data')


class ChangeUserPassword_Form(FlaskForm):
   
    password_Old = PasswordField(label='Old Password:', validators=[DataRequired()])
    New_password1 = PasswordField(label='New Password:', validators=[Length(min=6), DataRequired()])
    New_password2 = PasswordField(label='Confirm New Password:', validators=[EqualTo('New_password1'), DataRequired()])
    submit = SubmitField(label='Confirm New Password')
