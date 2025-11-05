from flask import Flask, render_template, request,redirect
import requests as req
import uuid
from data_manager import add_entry,get_data,delete_entry
from datetime import datetime


 
app = Flask(__name__)


def show_data(arg_list):
    
    print(arg_list)
    paste_id, title, content, expiry, is_password_protected,password, language, is_one_view = arg_list 

    current_time = datetime.now().timestamp()
            
    if current_time > expiry:
        delete_entry(paste_id)
        return render_template("404.html")

    else:

        if is_one_view == 'on':
            if paste_id:

                delete_entry(paste_id)

                return render_template("view_paste.html",
                paste_id=paste_id , title=title, content=content)

        elif is_one_view == 'off':

            if paste_id:

                return render_template("view_paste.html",
                paste_id=paste_id , title=title, content=content)
        
 
def generate_uid():
    new_uuid = uuid.uuid4()
    final_id = str(new_uuid)[0:4]
    return final_id


#  <.....HOME PAGE.....>
@app.route('/',methods=['GET','POST'])
 
def home():
     return render_template('home.html')


#  <.....CREATE PAGE.....>
@app.route('/drop',methods=['GET','POST'])
 
def drop():
    if request.method == "POST":
        title = request.form.get('Title')
        content = request.form.get('Content')
        language = request.form.get('language')
        expiry = request.form.get('expiry')
        is_password_protected = request.form.get('is_password_protected')
        password = request.form.get('password')
        burn_after_read = request.form.get('burn_after_read')

        uid = generate_uid()

        if not is_password_protected:
            is_password_protected = "off"

        if not burn_after_read:
            burn_after_read = "off" 

        
        current_datetime = datetime.now()

        current_epoch = current_datetime.timestamp()

        print(current_epoch)
        
        expiry_mapping = {'never':3318809528,'1h':current_epoch+3600 ,'1d':current_epoch+86400 ,
        '1w':current_epoch+604800 ,'1m': current_epoch+267800,'10s':current_epoch+10}
        
        expiry = expiry_mapping[expiry]



        add_entry(uid, title, content, expiry, is_password_protected,
        password,language, burn_after_read)

        return redirect(f'/{uid}')

    else:
        return render_template('drop.html')



#  <.....ABOUT PAGE.....>
@app.route('/about',methods=['GET','POST'])
 
def about():
    return render_template('about.html')


#  <....RENDER PAGE....>
@app.route('/<uid>',methods=['GET','POST'] )
 
def view_paste(uid):
    paste_data = get_data(uid)

    if len(paste_data) != 0:
        paste_id, title, content, expiry, is_password, password, language, is_one_view = paste_data[0]
        
        
        if is_password == "on":
            
            if request.method == 'GET':
                return render_template('password.html')
            
            elif request.method == 'POST':
            
                user_provided_password = request.form.get('password')
                   
                if user_provided_password == str(password):
                    return show_data(paste_data[0])
                    
                else:
                    return render_template('password.html')
            
        else:
            
            return show_data(paste_data[0])
       
        
    else:
        return render_template("404.html")

            # current_time = datetime.now().timestamp()
            
            # if current_time >expiry:
            #     delete_entry(paste_id)
            #     return render_template("404.html")

            # else:

            #     if is_one_view == 'on':
            #         if paste_id:

            #             delete_entry(paste_id)

            #             return render_template("view_paste.html",
            #             paste_id=uid , title=title, content=content)

            #     elif is_one_view == 'off':

            #         if paste_id:

            #             return render_template("view_paste.html",
            #             paste_id=uid , title=title, content=content)
            


            # if is_one_view == 'on':
            #     if paste_id:

            #         delete_entry(paste_id)

            #         return render_template("view_paste.html",
            #         paste_id=uid , title=title, content=content)

            # elif is_one_view == 'off':

            #     if paste_id:

            #         return render_template("view_paste.html",
            #         paste_id=uid , title=title, content=content)

    # else:
    #     return render_template('404.html')


app.run(debug=True)