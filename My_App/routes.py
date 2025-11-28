from My_App import app ,db
from flask import render_template,redirect ,url_for,flash,request
from My_App.models import Item,User

from My_App.forms import RegisterForm ,LoginForm, PurchaseItemForm,SellItemForm,ItemForm
from My_App.forms import Edit_UserForm,ChangeUserPassword_Form,EditItemForm,DeleteUserForm

from flask_login import login_user ,logout_user, login_required, current_user
import config
from sqlalchemy import func
from sqlalchemy import delete

from sqlalchemy import create_engine, text 



EditItemId_V = None
NoOfItemForUser= None
total = None

@app.route('/')
@app.route('/home')
def home_page():
    return render_template('home.html')



@app.route('/market' , methods= ["POST" , "GET"] )
@login_required
def market_page():
    purchase_form = PurchaseItemForm()
    selling_form = SellItemForm()

    if request.method == "POST":

        #Purchase Item Logic
 
        purchased_item = request.form.get('purchased_item')
        p_item_object = Item.query.filter_by(name=purchased_item).first()
        if p_item_object:
            if current_user.can_purchase(p_item_object):
                p_item_object.buy(current_user)
                flash(f"Congratulations! You purchased {p_item_object.name} for {p_item_object.price}$", category='success')
            else:
                flash(f"Unfortunately, you don't have enough money to purchase {p_item_object.name}!", category='danger')

        #Sell Item Logic

        sold_item = request.form.get('sold_item')
        s_item_object = Item.query.filter_by(name=sold_item).first()

        if s_item_object:
            if current_user.can_sell(s_item_object):
                s_item_object.sell(current_user)
                flash(f"Congratulations! You sold {s_item_object.name} back to market!", category='success')
            else:
                flash(f"Something went wrong with selling {s_item_object.name}", category='danger')


        return redirect(url_for('market_page'))

    if request.method == "GET":
        items = Item.query.filter_by(owner=None)
        owned_items = Item.query.filter_by(owner=current_user.id)

        NoOfItemForUser = Item.query.filter_by(owner=current_user.id).count()
        total = db.session.query(db.func.sum(Item.price)).filter_by(owner=current_user.id).scalar()
       

        return render_template('market.html', items_V=items, purchase_form=purchase_form, owned_items=owned_items, selling_form=selling_form 
                                , NoOfItemForUser_V=NoOfItemForUser ,total_v=total)
       
@app.route('/Users' , methods= ["POST" , "GET"] )
@login_required
def users_page():
   
   DeleteUser_form = DeleteUserForm()

   if request.method == "POST": 
       
      
      DeleteIUser_V = request.form.get('deleted_user')
      Item_by_User =  Item.query.filter_by(owner = DeleteIUser_V)

      for item_v in  Item_by_User :
         item_v.owner = None   
      
        
      stmt = delete(User).where(User.id == DeleteIUser_V)
      db.session.execute(stmt)
      db.session.commit()
      flash('User deleted successfully', 'success')

   Users = User.query.all()

   for user in Users:
        user.item_count = Item.query.filter_by(owner=user.id).count()
        user.total_value = db.session.query(db.func.sum(Item.price)).filter_by(owner=user.id).scalar() or 0

   return render_template('Users.html', Users_v=Users ,DeleteUser_form = DeleteUser_form)



@app.route('/EditUser' , methods= ["POST" , "GET"])
@login_required
def EditUser_page():

    config.Validation_on_email_V  == ''
    form = Edit_UserForm() 
    form_Change_password = ChangeUserPassword_Form() 
    
    user_V = request.args.get('user_id')
    index_V = request.args.get('index_V')
    
    if  index_V == '1' :
       Edit_user = User.query.filter_by(id=user_V).first()
    else :
       Edit_user = User.query.filter_by(username=current_user.username).first()
    

    Old_username = Edit_user.username
    Old_email_address =  Edit_user.email_address
    Old_budget = Edit_user.budget
    Old_admin = Edit_user.admin

    if request.method == "GET":
     
      form.username.data = Edit_user.username
      form.email_address.data = Edit_user.email_address
      form.budget.data = Edit_user.budget
      form.admin.data = Edit_user.admin

      User_name = Edit_user.username
      User_id =Edit_user.id

      return render_template("UserEdit.html" ,form=form, User_name_V = User_name ,User_id_V = User_id , form_Change_password_V = form_Change_password )

    if request.method == "POST": 
      
      form = Edit_UserForm() 
      form_Change_password = ChangeUserPassword_Form() 
      User_name = Edit_user.id

      # -----------------------------------------------------------------------------------------------------
      # -----------------------------------------------------------------------------------------------------
      if form_Change_password.password_Old.data != None or form_Change_password.New_password1.data != None  or form_Change_password.New_password2.data != None  :
          
          if form_Change_password.validate_on_submit():
                
                if  Edit_user.check_password_correction(
                    attempted_password=form_Change_password.password_Old.data
                ):

                    Edit_user.password=form_Change_password.New_password1.data
                    db.session.commit() 
                    flash(f"User Password successfully changed ! " ,category="success")
                    # return render_template("UserEdit.html" ,form=form, owned_User_name_V = User_name ,form_Change_password_V = form_Change_password )
                    return redirect(url_for("market_page"))
                else:
                   flash('User password are not match! Please try again', category='danger')
                   return render_template("UserEdit.html" ,form=form, owned_User_name_V = User_name ,form_Change_password_V = form_Change_password )

          elif form_Change_password.errors != {}: #If there are not errors from the validations
             for err_msg in form_Change_password.errors.values():
               flash(f'There was an error with creating a user : {err_msg}', category='danger')
             return render_template("UserEdit.html" ,form=form, owned_User_name_V = User_name ,form_Change_password_V = form_Change_password )
      # -----------------------------------------------------------------------------------------------------
      # -----------------------------------------------------------------------------------------------------
      if  Old_username != form.username.data :
          config.Validation_on_email_V = 'username'

          if form.validate_on_submit():
             
             Edit_user.username=form.username.data 

          elif form.errors != {}: #If there are not errors from the validations
             for err_msg in form.errors.values():
               flash(f'There was an error with creating a user..: {err_msg}', category='danger')
             return render_template("UserEdit.html" ,form=form, owned_User_name_V = User_name ,form_Change_password_V = form_Change_password )
      # -----------------------------------------------------------------------------------------------------
      # -----------------------------------------------------------------------------------------------------
      if  Old_email_address != form.email_address.data :
          config.Validation_on_email_V = 'email'
          if form.validate_on_submit():
             
             Edit_user.email_address=form.email_address.data 

          elif form.errors != {}: #If there are not errors from the validations
             for err_msg in form.errors.values():
               flash(f'There was an error with creating a user...: {err_msg}', category='danger')
             return render_template("UserEdit.html" ,form=form, owned_User_name_V = User_name ,form_Change_password_V = form_Change_password )
      # -----------------------------------------------------------------------------------------------------
      # -----------------------------------------------------------------------------------------------------
      if Old_budget != form.budget.data :
              
              Edit_user.budget=form.budget.data 
      # -----------------------------------------------------------------------------------------------------
      # -----------------------------------------------------------------------------------------------------
      if Old_admin != form.admin.data :
              
              Edit_user.admin=form.admin.data 
      # -----------------------------------------------------------------------------------------------------
      # -----------------------------------------------------------------------------------------------------

      db.session.commit() 

      flash(f"User {Edit_user.username} Updated successfully ! " ,category="success")
      # save Data to table user
      return redirect(url_for("market_page"))


@app.route('/register' , methods= ["POST" , "GET"])
def register_page():
  
  form = RegisterForm()  
  if form.validate_on_submit():
     user_to_create = User(username=form.username.data , 
                           email_address=form.email_address.data ,
                           password=form.password1.data,
                           admin=False)
     
     
     db.session.add(user_to_create)
     db.session.commit() 

     login_user(user_to_create)
     flash(f"Account created successfully ! You are now logged in as {user_to_create.username}" ,category="success")
      # save Data to table user
     return redirect(url_for("market_page"))


  if form.errors != {}: #If there are not errors from the validations
        for err_msg in form.errors.values():
            flash(f'There was an error with creating a user: {err_msg}', category='danger')

  return render_template( "register.html" ,form=form )


@app.route('/login', methods=['GET', 'POST'])
def login_page():
    form = LoginForm()
    if form.validate_on_submit():
        attempted_user = User.query.filter_by(username=form.username.data).first()
        if attempted_user and attempted_user.check_password_correction(
                attempted_password=form.password.data
        ):
            login_user(attempted_user)
            flash(f'Success! You are logged in as: {attempted_user.username} ', category='success')
            return redirect(url_for('market_page'))
        else:
            flash('Username and password are not match! Please try again', category='danger')

    return render_template('login.html', form=form)


@app.route('/logout')
def logout_page():

    logout_user()
    flash("You have been logged out!", category='info')
    return redirect(url_for("home_page"))


@app.route('/Item' , methods= ["POST" , "GET"])
@login_required
def Item_page():

    form = ItemForm() 
    Tital_V_Form ="Please Create New Item"

    if form.validate_on_submit():
      Item_to_create = Item(name=form.Item_name.data , 
                           price=form.Item_price.data ,
                           barcode=form.Item_barcode.data,
                           description=form.Item_description.data )
     
     
      db.session.add(Item_to_create)
      db.session.commit() 

      flash(f"Item {Item_to_create.name} created successfully ! " ,category="success")
      # save Data to table user
      return redirect(url_for("market_page"))
    
    return render_template("Item.html" ,form=form ,Tital_V_Form=Tital_V_Form )


@app.route('/EditItem' , methods= ["POST" , "GET"])
@login_required
def EditItem_page():

    
    EditItemId_V = request.args.get('item_id')
    form = EditItemForm() 
    Edit_item = Item.query.filter_by(id=EditItemId_V).first()
    Tital_V_Form ="Please Edit Item"

    Old_itemname = Edit_item.name
    Old_itemnprice =  Edit_item.price
    Old_itemnbarcode = Edit_item.barcode
    Old_itemdescription = Edit_item.description

    if request.method == "GET":
 

      form.Item_name.data = Edit_item.name
      form.Item_price.data = Edit_item.price
      form.Item_barcode.data = Edit_item.barcode
      form.Item_description.data = Edit_item.description

      return render_template("Item.html" ,form=form , Tital_V_Form=Tital_V_Form )


    if request.method == "POST": 
       
       Edit_item.name = form.Item_name.data
       Edit_item.price = form.Item_price.data
       Edit_item.barcode = form.Item_barcode.data
       Edit_item.description = form.Item_description.data

    db.session.commit() 
    flash(f"Item {Edit_item.name} Updated successfully ! " ,category="success")
      # save Data to table user
    return redirect(url_for("market_page"))


@app.route('/DeleteItem' , methods= ["POST" , "GET"])
@login_required
def DeleteItem_page():
   
   DeleteItemId_V = request.args.get('item_id')

   stmt = delete(Item).where(Item.id == DeleteItemId_V)
   db.session.execute(stmt)
   db.session.commit()

   return redirect(url_for('market_page'))



