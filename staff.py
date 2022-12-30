import datetime
from flask import Flask,Blueprint,render_template,request,redirect,url_for,flash,session
from database import *
import uuid

staff=Blueprint('staff',__name__)

@staff.route('/staffhome')
def staffhome():
    return render_template("staffhome.html")
    

@staff.route('/stafviewprofile',methods=['get','post']) 
def stafviewprofile():
    data={}  
    qry="select * from staff where id='%s'"%(session['sid'])
    res=select(qry)
    data['r']=res
    if 'action' in request.args:
        action=request.args['action']
        id=request.args['id']
         
    else:
        action=None

    if action=='update':
        qry="select * from staff where id='%s'"%(id)
        res=select(qry)
        data['re']=res

    if 'Submit' in request.form:
        name=request.form['textfield']
        gender=request.form['textfield2']
        phone=request.form['textfield3']
        email=request.form['textfield4']
        dob=request.form['textfield5']
        qry="update staff set firstname='%s',gender='%s',phone='%s',email='%s',dob='%s'where id='%s'"%(name,gender,phone,email,dob,id)
        update(qry)
        return redirect(url_for('staff.stafviewprofile'))
    return render_template("stafprofile.html",data=data)         

@staff.route('/changepass',methods=['get','post']) 
def changepass():
    if 'Submit' in request.form:
        old=request.form['textfield']
        new=request.form['textfield2']
        con=request.form['textfield3']
        if old:
            qry="select * from login where id='%s'"%(session['lid'])
            val=select(qry)
            if val[0]['password']==old:
                if new==con:
                    q="update login set password='%s' where id='%s'"%(new,session['lid'])
                    update(q)
                else:
                    flash("not matching")  
                    return redirect(url_for('staff.changepass'))  




        else:
            flash("incorrect password")
    # flash(" password reset successfully")

    return render_template("changepass.html")


 
     

@staff.route('/viewnoti',methods=['get','post'])
def viewnoti():
    data={}
    
    qry="select * from notification"
    res=select(qry)
    data['res']=res
    return render_template("view notification.html",data=data)   

@staff.route('/sendcomplaint',methods=['get','post'])
def sendcomplaint():
    if 'Submit' in request.form:
        comp=request.form['textfield']

        qry="insert into complaints values(null,'%s','%s','pending',now())"%(session['sid'],comp)
        insert(qry)
        flash("send complaint")
        return redirect(url_for('staff.staffhome'))
    return render_template("sendcomplaint.html")  

@staff.route('/makeappoinment',methods=['get','post'])
def makeappoinment(): 
    data={}
    
    qry="select * from healthteam"
    res=select(qry)
    data['app']=res
    
    if 'action' in request.args:
        htid=request.args['hid']
        q="insert into appointment values(null,'%s','%s',now(),'pending')"%(htid,session['sid'])
        insert(q)
        flash("successful appoinment")
    
    return render_template("makeappointment.html",data=data) 

@staff.route('/viewappoinments',methods=['get','post'])
def viewappoinments():
    data={}
    
    qry="select * from appointment"
    res=select(qry)
    data['ap']=res
    
    
    return render_template("viewappoinment.html",data=data)

@staff.route('/viewmeditation',methods=['get','post'])
def viewmeditation():
     data={}
     id=request.args['id']
     q="select * from meditation where id='%s'"%(id)
     res=select(q)
     data['v']=res
     return render_template("viewmeditation.html",data=data) 
       
