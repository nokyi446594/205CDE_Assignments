from flask import Flask, render_template, request , session ,abort
from flask_wtf import FlaskForm
from wtforms import Form ,StringField , TextAreaField , SubmitField , RadioField, SelectField, IntegerField
from wtforms.validators import DataRequired, Email
from wtforms import validators, ValidationError
from fileinput import filename
from flask import *
import os
import pymysql
import datetime
from datetime import date
app =   Flask(__name__)
app.secret_key = 'any random string'

#open database connection
db = pymysql.connect(host="localhost",user="root",password="Hny0715",database="205CDE")
db.connect()

@app.route('/')
def home():
    return render_template('main.html')
@app.route('/signup')
def signup():
    return render_template('signup.html')
@app.route('/insertDB', methods=["POST","GET"])
def result():
    if request.method == "POST":
        username = request.form['username'] 
        pwd = request.form['password']
        tel = request.form['tele']
        email = request.form['email']
        address = request.form['address']

        # prepare a cursor object using cursor() method
        db.connect()
        cursor = db.cursor()
        cursor.execute("""select (max(userNo) + 1) FROM `UserInformation`""")
        userNo = cursor.fetchall()
        cursor.execute("""insert into UserInformation(userNo,username,TelNo,email,address) values(%s,%s,%s,%s,%s)""",(userNo,username,tel,email,address))
        cursor.execute("""insert into userlogin(username,password) values(%s,%s)""",(username,pwd)) 
        
        try:
            db.commit()
            msg = "Name is successfully inserted!"
        except Exception as e:
            db.rollback()
        db.close()
        return render_template("login.html", msg = msg)
        
@app.route('/enter', methods=["POST","GET"])        
def check():
    if request.method == "POST":
        username = request.form['username']
        pwd = request.form['password']
        custName = " "
        # prepare a cursor object using cursor() method
        db.connect()
        cursor = db.cursor()
        sql = ("SELECT username , password FROM userlogin WHERE username = '"+username+"' AND password = '"+pwd+"'")
        cursor.execute(sql)
        results = cursor.fetchall()
        for row in results:
            custName = row[0]
            custPassword = row[1]
        try:
            db.commit()
        except Exception as e:
            db.rollback()
        db.close()
        if custName == ' ':
            msg = 'Incorrect usename or password'
            return render_template("login.html",msg = msg)
        elif custName == "admin":
            return render_template('adminpage.html')
        else:
            session['username'] = custName
            db.connect()
            cursor = db.cursor()
            sql = ("SELECT userNo FROM `UserInformation` WHERE username = '"+session['username']+"'")
            cursor.execute(sql)
            results = cursor.fetchall()
            for row in results:
                userNo = row[0]
            session['userNo'] = str(userNo)
            try:
                db.commit()
            except Exception as e:
                db.rollback()
            db.close()
            return render_template("welcome.html",guest = session['username'])
        
@app.route('/login')
def login():
    if 'username' in session:
        return render_template('welcome.html',guest = session['username'])
    else:
        return render_template('login.html')
@app.route('/booking')
def book():
    return render_template('bookpage.html')
@app.route('/payment',methods=["POST","GET"])
def pay():
    if request.method == "POST":
        size = str(request.form.get('size'))
        ctype = str(request.form.get('type'))
        taste = str(request.form.get('taste'))
        dec = request.form.getlist('dec')
        theme = request.form['theme']
        word = request.form['word']
        author = str(request.form.get('design'))
        if author == "user":
            dpri = 100
        else:
            dpri = 120
        price = int(size,10)*10 + 50 + len(dec)*10 + dpri
        decr = ''
        for item in dec:
            decr = decr +' '+ item
        if author == "user":
            f = request.files['df']
            f.save(os.path.join("./static/image",f.filename))
            dfile = f.filename
        else:
            dfile = " none"
        db.connect()
        cursor = db.cursor()
        cursor.execute("""select productNo FROM `product`""")
        productNO = "P" + str((len(cursor.fetchall()) + 1))
        session['product'] = productNO
        cursor.execute("""insert into `product`(`productNo`, `size`, `type`, `taste`, `decorate`, `theme`, `chocolate word`,`price`) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)""",(productNO,size,ctype,taste,decr,theme,word,str(price))) 
        cursor.execute("""insert into design(productNo,author,photoName) value(%s,%s,%s)""",(productNO,author,dfile))
        session['price'] = price
        try:
            db.commit()
        except Exception as e:
            db.rollback()
        db.close()
        if "username" in session:
            return render_template('payment.html',price = price)
        else:
            msg  = "please login first"
            return render_template('login.html',msg = msg)
        
@app.route('/pay',methods=["POST","GET"])
def pay2():
    if request.method == "POST":
        productNO = request.form.get('product')
        db.connect()
        cursor = db.cursor()
        sql = ("SELECT price FROM `product` WHERE productNO = '"+productNO+"'")
        cursor.execute(sql)
        pr = cursor.fetchall()
        for row in pr:
            price = row[0]
        session['price'] = price
        session['product'] = productNO
        try:
            db.commit()
        except Exception as e:
            db.rollback()
        if "username" in session:
            db.close()
            return render_template('payment.html',price = price)
        else:
            msg  = "please login first"
            db.close()
            return render_template('login.html',msg = msg)
        
    else:
        return render_template('payment.html',price = session['price'])
@app.route('/productlist')
def prouduct():
    return render_template("product.html")
@app.route('/check')
def finpay():
    return render_template('check.html')
@app.route("/finpay",methods=["POST","GET"])
def delprodut():
    if request.method == "POST":
        session.pop('product',None) 
        session.pop('price',None)              
        return render_template('welcome.html',guest = session['username'])        
@app.route('/list')
def orderlist():
    size = " "
    ctype = " "
    taste = " "
    decorate = " "
    i = 0 
    orderlist = {} 
    olist = " "  
    unpay = 'none'
    db.connect()
    cursor = db.cursor() 
    if "product" in session:
        sql =("SELECT * FROM `product` WHERE `productNo` = '"+session['product'] +"'")
        cursor.execute(sql)
        results = cursor.fetchall()
        for row in results:
            size = str(row[1]) + " inches"
            ctype = str(row[2])
            taste = str(row[3])
            decorate = str(row[4])
        unpay = size  + ctype + taste  + decorate 
    userNo = session['userNo']
    sql =("SELECT `Date`,`productNo` FROM `order` WHERE `userNo` = '"+userNo+"'")
    cursor.execute(sql)
    results = cursor.fetchall()
    for row in results:
        gdate = str(row[0])
        product = row[1]
        sql =("SELECT * FROM `product` WHERE `productNo` = '"+ product +"'")
        cursor.execute(sql)
        results = cursor.fetchall()
        for row in results:
            size = str(row[1]) + " inches"
            ctype = row[2]
            taste = row[3]
            decorate = row[4]
        orderlist[i] = str(i + 1) + " " + gdate + " " + size + " " + ctype + " " +taste + " " + decorate 
        i += 1
    for i in range(len(orderlist)):
        olist = olist +orderlist[i] + "|"
    try:
        db.commit()
    except Exception as e:
        db.rollback()
    db.close()               
    return render_template('trolley.html',orderlist = olist,unpay = unpay)
@app.route('/order',methods=["POST","GET"])
def order():
    if request.method == "POST":
        way = str(request.form.get('way'))
        date = request.form.get("gdate")
        db.connect()
        cursor = db.cursor()
        cursor.execute("""select (max(orderNo) + 1) FROM `order`""")
        orderNo = cursor.fetchall()
        userNo = session['userNo']
        cursor.execute("""INSERT INTO `order`(`orderNo`, `WayToPay`, `Date`, `payment`, `productNo`, `userNo`) VALUES (%s,%s,%s,%s,%s,%s)""",(orderNo,way,date,session['price'],session['product'],userNo))
        try:
            db.commit()
        except Exception as e:
            db.rollback()
        db.close() 
        return render_template('check.html')
@app.route('/usepage')
def userpage():
    return render_template("welcome.html",guest = session['username'])
@app.route('/logout')
def out():
    session.pop('username',None)
    session.pop('userNo',None)
    return render_template('main.html')
@app.route('/information')
def userin():
    userNo = session['userNo']
    db.connect()
    cursor = db.cursor()
    sql = ("SELECT * FROM `UserInformation` WHERE `userNo` = '"+userNo+"'")
    cursor.execute(sql)
    results = cursor.fetchall()
    for row in results:
        tel = row[2]
        email = row[3]
        address =row[4]
    username = session['username']
    sql = ("SELECT * FROM `username` WHERE `username` = '"+username+"'")
    results = cursor.fetchall()
    pwd = row[1]
    return render_template('userin.html',username = username, tel =tel, email = email ,address = address ,pwd = pwd)
@app.route('/change',methods=["POST","GET"])
def change():
    if request.method == "POST":
        userNo = session['userNo']
        username = request.form['username'] 
        pwd = request.form['password']
        tel = request.form['tele']
        email = request.form['email']
        address = request.form['address']
        db.connect()
        cursor = db.cursor()
        if username != '':
            sql = ("UPDATE `UserInformation` SET `username`= '"+username+"' WHERE `userNo` = '"+userNo+"'")
            cursor.execute(sql)
            sql = ("UPDATE `userlogin` SET `username`= '"+username+"' WHERE `username` = '"+session['username']+"'")
            cursor.execute(sql)
            session.pop('username',None)
            session['username'] = username 
        else:
            username = session['username']
        if pwd != '':
            sql = ("UPDATE `userlogin` SET `password`= '"+pwd+"' WHERE `username` = '"+username+"'")
            cursor.execute(sql)
        if tel != '':
            sql = ("UPDATE `UserInformation` SET `TelNo`= '"+tel+"' WHERE `userNo` = '"+userNo+"'")
            cursor.execute(sql)
        if email != '':
            sql = ("UPDATE `UserInformation` SET `email`= '"+email+"' WHERE `userNo` = '"+userNo+"'")
            cursor.execute(sql)
        if address != '':
            sql = ("UPDATE `UserInformation` SET `address`= '"+address+"' WHERE `userNo` = '"+userNo+"'")
            cursor.execute(sql)
        try:
            db.commit()
        except Exception as e:
            db.rollback()
        db.close()   
        return render_template('welcome.html',guest=session['username'])
@app.route('/admin')
def adminpage():
    return render_template("adminpage.html")
@app.route('/newprod')
def addnew():
    return render_template("newproduct.html")
@app.route('/newProduct',methods={"POST","GET"})
def newprod():
        if request.method == "POST":
            size = str(request.form.get('size'))
            ctype = str(request.form.get('type'))
            taste = str(request.form.get('taste'))
            dec = request.form.getlist('dec')
            author = str(request.form.get('design'))
            dpri = 120
            price = int(size,10)*10 + 50 + len(dec)*10 + dpri
            decr = ''
            for item in dec:
                decr = decr +' '+ item
            f = request.files['df']
            f.save(os.path.join("./static/image",f.filename))
            dfile = f.filename
            theme = "none"
            word = "none"
            db.connect()
            cursor = db.cursor()
            cursor.execute("""select productNo FROM `product`""")
            productNO = "P" + str((len(cursor.fetchall()) + 1))
            cursor.execute("""insert into `product`(`productNo`, `size`, `type`, `taste`, `decorate`, `theme`, `chocolate word`,`price`) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)""",(productNO,size,ctype,taste,decr,theme,word,str(price))) 
            cursor.execute("""insert into design(productNo,author,photoName) value(%s,%s,%s)""",(productNO,author,dfile))
            try:
                db.commit()
            except Exception as e:
                db.rollback()
            db.close()
            return render_template("adminpage.html")
@app.route('/adddesign')
def adddesign():
    size = " "
    ctype = " "
    taste = " "
    decorate = " "
    theme = " "
    word = " "
    productNo = " "
    i = 0 
    orderlist = {} 
    olist = " "  
    db.connect()
    cursor = db.cursor()
    cursor.execute("""select * FROM `design` WHERE photoname = ' none'""")
    results = cursor.fetchall()
    for row in results:
        productNo = row[0]
        sql = ("SELECT * FROM `product` WHERE `productNo` = '"+productNo+"'")
        cursor.execute(sql)
        prouduct = cursor.fetchall()
        for row in prouduct:
            size = str(row[1])
            ctype = row[2]
            taste = row[3]
            decorate = row[4]
            theme = row[5]
            word = row[6]
        orderlist[i] = "productNO:"+productNo + "  size:" + size + "  type" + ctype+ "  taste" + taste +"  decorate"+decorate + "  theme"+ theme + "  word" + word
        i += 1    
    for i in range(len(orderlist)):
        olist = olist +orderlist[i] + "|"
    try:
        db.commit()
    except Exception as e:
        db.rollback()
    db.close()
    return render_template("adddesign.html",orderlist = olist)

@app.route('/add',methods={"POST","GET"})
def adddes():
    if request.method == "POST":
        productNo = request.form.get('product')
        f = request.files['df']
        f.save(os.path.join("./static/image",f.filename))
        dfile = f.filename
        db.connect()
        cursor = db.cursor()
        sql = ("UPDATE `design` SET `photoName`= '"+dfile+"' WHERE `productNo` = '"+productNo+"'")
        cursor.execute(sql)
        try:
            db.commit()
        except Exception as e:
            db.rollback()
        db.close()   
        return render_template('adminpage.html')
@app.route('/todaylist')
def todaylist():
    size = " "
    ctype = " "
    taste = " "
    decorate = " "
    theme = " "
    word = " "
    productNo = " "
    design = " "
    i = 0 
    orderlist = {} 
    olist = ""  
    db.connect()
    cursor = db.cursor() 
    today = str(date.today())
    sql =("SELECT `productNo` FROM `order` WHERE `Date` = '"+today+"'")
    cursor.execute(sql)
    results = cursor.fetchall()
    for row in results:
        productNo = row[0]
        sql = ("SELECT * FROM `product` WHERE `productNo` = '"+productNo+"'")
        cursor.execute(sql)
        prouduct = cursor.fetchall()
        for row in prouduct:
            size = str(row[1])
            ctype = row[2]
            taste = row[3]
            decorate = row[4]
            theme = row[5]
            word = row[6]
        sql = ("SELECT photoName FROM `design` WHERE `productNo` = '"+productNo+"'")
        cursor.execute(sql)
        pro = cursor.fetchall()
        for row in pro:
            design = row[0]
        orderlist[i] = str(i + 1) +"  size:" + size + "  type" + ctype+ "  taste" + taste +"  decorate"+decorate + "  theme"+ theme + "  word" + word +"  design:"+design
        i += 1
    for i in range(len(orderlist)):
        olist = olist +orderlist[i] + "|"
    try:
        db.commit()
    except Exception as e:
        db.rollback()
    db.close()               
    return render_template('admintorder.html',orderlist = olist, today =today)
@app.route('/search')
def search():
    return render_template('search.html')
@app.route('/alllist',methods={"POST","GET"})
def allist():
    if request.method == "POST":
        orderlist = {} 
        olist = " " 
        i = 0
        cursor = db.cursor()
        db.connect()
        searchtype = request.form.get("searchtype")
        if searchtype == "userin":
            usertype = request.form.get("usertype")
            if usertype == "userNo":
                userNo = request.form.get("usearchKey")
                sql = ("SELECT * FROM `UserInformation` WHERE `userNo` = '"+userNo+"'")
                cursor.execute(sql)
                results = cursor.fetchall()
                for row in results:
                    username = row[1]
                    tel = str(row[2])
                    email = row[3]
                    address =row[4]
                    orderlist[i] = "userNO:"+userNo+"  username:"+username+"  tel:"+tel+"  email"+email+"  address"+address
                    i += 1 
            else:
                username = request.form.get("usearchKey")
                sql = ("SELECT * FROM `UserInformation` WHERE `username` = '"+username+"'")
                cursor.execute(sql)
                results = cursor.fetchall()
                for row in results:
                    userNo = str(row[0])
                    tel = str(row[2])
                    email = row[3]
                    address =row[4]
                    orderlist[i] = "userNO:"+userNo+"  username:"+username+"  tel:"+tel+"  email"+email+"  address"+address
                    i += 1   
        elif searchtype == "orderlist":
            ordertype = request.form.get("ordertype")
            size = " "
            ctype = " "
            taste = " "
            decorate = " "
            theme = " "
            word = " "
            productNo = " "
            design = " "
            orderNo = " " 
            if ordertype == "date":
                gdate = request.form.get('dayKey')
                sql =("SELECT `Date`,`productNo`,`orderNo` FROM `order` where Date = '"+ gdate +"'")
                cursor.execute(sql)
                results = cursor.fetchall()
                for row in results:
                    productNo = row[1]
                    date = str(row[0])
                    orderNo = str(row[2])
                    sql = ("SELECT * FROM `product` WHERE `productNo` = '"+productNo+"'")
                    cursor.execute(sql)
                    prouduct = cursor.fetchall()
                    for row in prouduct:
                        size = str(row[1])
                        ctype = row[2]
                        taste = row[3]
                        decorate = row[4]
                        theme = row[5]
                        word = row[6]
                    sql = ("SELECT photoName FROM `design` WHERE `productNo` = '"+productNo+"'")
                    cursor.execute(sql)
                    pro = cursor.fetchall()
                    for row in pro:
                        design = row[0]
                    orderlist[i] = orderNo+"  date:"+date+"  size:" + size + "  type" + ctype+ "  taste" + taste +"  decorate"+decorate + "  theme"+ theme + "  word" + word +"  design:"+design
                    i += 1   
            else:
                userNO = request.form.get("searchKey")
                sql =("SELECT `Date`,`productNo`,`orderNo` FROM `order` where userNo = '"+userNO+"'")
                cursor.execute(sql)
                results = cursor.fetchall()
                for row in results:
                    productNo = row[1]
                    date = str(row[0])
                    orderNo = str(row[2])
                    sql = ("SELECT * FROM `product` WHERE `productNo` = '"+productNo+"'")
                    cursor.execute(sql)
                    prouduct = cursor.fetchall()
                    for row in prouduct:
                        size = str(row[1])
                        ctype = row[2]
                        taste = row[3]
                        decorate = row[4]
                        theme = row[5]
                        word = row[6]
                    sql = ("SELECT photoName FROM `design` WHERE `productNo` = '"+productNo+"'")
                    cursor.execute(sql)
                    pro = cursor.fetchall()
                    for row in pro:
                        design = row[0]
                    orderlist[i] = orderNo+"  date:"+date+"  size:" + size + "  type" + ctype+ "  taste" + taste +"  decorate"+decorate + "  theme"+ theme + "  word" + word +"  design:"+design
                    i += 1   
        else:
            producttype = request.form.get("producttype")
            size = " "
            ctype = " "
            taste = " "
            decorate = " "
            theme = " "
            word = " "
            productNo = " "
            design = " "
            if producttype == "productNo":
                productNo = request.form.get("psearchKey")
                sql = ("SELECT * FROM `product` WHERE `productNo` = '"+productNo+"'")
                cursor.execute(sql)
                prouduct = cursor.fetchall()
                for row in prouduct:
                    size = str(row[1])
                    ctype = row[2]
                    taste = row[3]
                    decorate = row[4]
                    theme = row[5]
                    word = row[6]
                    sql = ("SELECT photoName FROM `design` WHERE `productNo` = '"+productNo+"'")
                    cursor.execute(sql)
                    pro = cursor.fetchall()
                    for row in pro:
                        design = row[0]
                    orderlist[i] = productNo+"  size:" + size + "  type" + ctype+ "  taste" + taste +"  decorate"+decorate + "  theme"+ theme + "  word" + word +"  design:"+design
                    i += 1   
            elif producttype == "ctype":
                ctype = request.form.get("psearchKey")
                sql = ("SELECT * FROM `product` WHERE `type` = '"+ctype+"'")
                cursor.execute(sql)
                prouduct = cursor.fetchall()
                for row in prouduct:
                    size =str(row[1])
                    productNo = row[0]
                    taste = row[3]
                    decorate = row[4]
                    theme = row[5]
                    word = row[6]
                    sql = ("SELECT photoName FROM `design` WHERE `productNo` = '"+productNo+"'")
                    cursor.execute(sql)
                    pro = cursor.fetchall()
                    for row in pro:
                        design = row[0]
                    orderlist[i] = productNo+"  size:" + size + "  type" + ctype+ "  taste" + taste +"  decorate"+decorate + "  theme"+ theme + "  word" + word +"  design:"+design
                    i += 1   
            else :
                taste = request.form.get("psearchKey")
                sql = ("SELECT * FROM `product` WHERE `taste` = '"+taste+"'")
                cursor.execute(sql)
                prouduct = cursor.fetchall()
                for row in prouduct:
                    size =str(row[1])
                    ctype = row[2]
                    productNo = row[0]
                    decorate = row[4]
                    theme = row[5]
                    word = row[6]
                    sql = ("SELECT photoName FROM `design` WHERE `productNo` = '"+productNo+"'")
                    cursor.execute(sql)
                    pro = cursor.fetchall()
                    for row in pro:
                        design = row[0]
                    orderlist[i] = productNo+"  size:" + size + "  type" + ctype+ "  taste" + taste +"  decorate"+decorate + "  theme"+ theme + "  word" + word +"  design:"+design
                    i += 1   
        for i in range(len(orderlist)):
            olist = olist +orderlist[i] + "|"
        try:
            db.commit()
        except Exception as e:
            db.rollback()
        db.close()               
        return render_template('adminalorder.html',orderlist = olist)
if __name__=='__main__':
    app.debug   =   True
    app.run(host="0.0.0.0",port=8000)