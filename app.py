from flask import Flask, jsonify, request, render_template, redirect, session, flash
from passlib.hash import sha256_crypt
import pymysql
import smtplib
import datetime
import os
from flask_mysqldb import MySQL
from jinja2 import Environment, FileSystemLoader

file_loader = FileSystemLoader('templates')
env = Environment(loader=file_loader)

# con = pymysql.connect('localhost', 'uprisings','Ratheeshhnair', 'advay_db')

# cur = con.cursor()


TESTIMONIALS = './static/assets/img/testimonials'

SERVICES = './static/assets/img/Services'

ASKUS = './static/assets/img/ASKUS'

PROFILEPICS = './static/assets/img/profilepics'

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'

app.config['MYSQL_USER'] = 'uprisings'

app.config['MYSQL_PASSWORD'] = 'Ratheeshhnair'

app.config['MYSQL_DB'] = 'advay_db'

mysql = MySQL(app)

app.config['TESTIMONIALS'] = TESTIMONIALS

app.config['SERVICES'] = SERVICES

app.config['PROFILEPICS'] = PROFILEPICS

app.config['ASKUS'] = ASKUS

app.secret_key = "QWR2YXkgUmVzZWFyY2ggRGVzaWduZWQgYW5kIGRldmVsb3BlZCBieSBVcHJpc2luZ3M"


# General
# Home Page
@app.route('/')
def index():
    cur = mysql.connection.cursor()

    test_sql = '''select NAME,LOCATION,COMMENT from TESTIMONIALS'''

    cur.execute(test_sql)

    test = cur.fetchall()

    len_test = len(test)

    service_sql = '''select ID,NAME from SERVICES'''

    cur.execute(service_sql)

    blog = cur.fetchall()

    len_services = len(blog)

    ask_sql = '''select ID,NAME,IMAGE from ASKUS'''

    cur.execute(ask_sql)

    ask = cur.fetchall()

    len_ask = len(ask)

    qs_sql = '''select ID,NAME from QUALITYSTANDARDS'''

    cur.execute(qs_sql)

    qs = cur.fetchall()

    len_qs = len(qs)

    cr_sql = '''select ID,DESCRIPTION from CAREERS'''

    cur.execute(cr_sql)

    cr = cur.fetchall()

    len_cr = len(cr)

    fr_sql = '''select ID,NAME from FEATURES'''

    cur.execute(fr_sql)

    features = cur.fetchall()

    len_fr = len(features)

    cur.close()

    return render_template('index.html', services=blog, lenserv=len_services, testimonials=test, lentest=len_test,
                           ask=ask, asklen=len_ask, qsdata=qs, lenqs=len_qs, career=cr, careerlen=len_cr, lenfr=len_fr,
                           features=features)

#PrivacyPolicy
@app.route('/privacypolicy')
def privacypolic():
    
    return render_template('privacypolicy.html')
    
    
# Services
@app.route('/service-detail/<id>')
def service(id):
    sql = '''select NAME,IMAGE,DESCRIPTION,p1,p2,p3,p4,p5,p6,p7,p8,p9,p10 from SERVICES  where ID=%s'''

    val = [id]

    cur = mysql.connection.cursor()

    cur.execute(sql, val)

    res = cur.fetchall()

    print(res)

    cur.close()

    return render_template('servicedetail.html', result=res)


@app.route('/askusformsubmit', methods=['POST'])
def askusform():
    # try:

        if (request.method == 'POST'):
    
            name = request.form['name']
    
            email = request.form['email']
    
            phone = request.form['phone']
    
            service = request.form['service']
    
            urgency = request.form['urgency']
    
            pages = request.form['pages']
    
            domain = request.form['domain']
    
            reference = request.form['reference']
    
            ynRadio = request.form['ynRadio']
    
            implementation = ''
    
            if (ynRadio == 'yes'):
    
                implementation = request.form['implementation']
    
            else:
    
                implementation = "nill"
    
            current_time = datetime.datetime.now()
    
            print(name, email, phone, service, urgency, pages, domain, reference, ynRadio, implementation, current_time)
    
            cur = mysql.connection.cursor()
    
            sql = "insert into ASKUSFORM (NAME,EMAIL,PHONE,SERVICE,URGENCY,PAGES,DOMAIN,REFERENCE,IMPLEMENTATION,DESCRIPTION,CREATED_AT) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
    
            val = (name, email, phone, service, urgency, pages, domain, reference, ynRadio, implementation, current_time)
    
            cur.execute(sql, val)
    
            # con.commit()
    
            mysql.connection.commit()
    
            # gmail_user = "advayresearch@gmail.com"
    
            # gmail_password = "advayreya@1985"
            
            # sender = "info@advayresearch.com"
    
            # sent_from = gmail_user
    
            # to = email
    
            # subject = 'Thankyou for Contacting Advay'
    
            # template = env.get_template('Email.html')
    
            # msg = template.render(name=name)
    
            # body = msg
    
            # email_text = """\
            #                  From: %s
            #                  To: %s
            #                  Subject: %s
    
            #                  %s
            #                  """ % (sent_from, ", ".join(to), subject, body)
    
            # server = smtplib.SMTP('localhost')
            
            # server.sendmail(sender, email, email_text) 
    
            # server.close()
    
            cur.close()
            
            # flash('Thank you for contacting Advay.. We will contact you soon..','success')
            
            data = {'status':True,'message':"Thanks for Contacting Advay.. We will contact you soon..."}
             
            return  data
    
            return index()
        else:
    
            # error = "Failed to send message.. Please try again"
    
            # flash('Unexpected Error Occured, Please Try Again Later','error')
    
            return "error"


    # except:
    
    #     error = "Failed to send message.. Please try again"
    
    #     flash(error)
    
    #     return index()




# Contact-Form

@app.route('/submit-contact', methods=['POST'])
def contactform():
    try:

        if (request.method == 'POST'):

            name = request.form['name']

            email = request.form['email']

            subj = request.form['subject']

            msg = request.form['message']

            current_time = datetime.datetime.now()

            print([name, email, subj, msg, current_time])

            cur = mysql.connection.cursor()

            sql = "insert into CONTACT_SUBMIT (NAME,EMAIL,SUBJECT,MESSAGE,CREATED_AT) values (%s,%s,%s,%s,%s)"

            val = (name, email, subj, msg, current_time)

            cur.execute(sql, val)

            # con.commit()

            mysql.connection.commit()

            cur.close()

            return index()

        else:

            error = "Failed to send message.. Please try again"

            flash(error)

            return index()

    except:

        error = "Failed to send message.. Please try again"

        flash(error)

        return index()


# Admin

@app.route('/admin')
def admin_login():
    return render_template('login.html')


@app.route('/login-check', methods=['POST', 'GET'])
def login_chech():
    # try:

        email = request.form['email']
    
        passwd = request.form['password']
    
        cur = mysql.connection.cursor()
    
        sql = "select ID,IMAGE,NAME,EMAIL,PASSWORD,MOBILE,ROLE from USERS where EMAIL=%s"
    
        val = [email]
    
        cur.execute(sql, val)
    
        res = cur.fetchall()
    
        # return jsonify(res)
    
        if sha256_crypt.verify(passwd, res[0][4]):
    
            if (res[0][6] == 1):
    
                if res:
                    session['loggedin'] = True
    
                    session['id'] = res[0][0]
    
                    session['username'] = res[0][2]
    
                    cur.close()
    
                    return render_template('dashboard.html', profile=res)
    
            else:
    
                cur.close()
    
                return render_template('err404.html')
    
        else:
    
            cur.close()
    
            return render_template('err404.html')


    # except:
    
    #     return render_template('err404.html')


# Admin - Testimonials

@app.route('/admin/testimonials')
def admin_test():
    try:

        if session['loggedin'] == True:

            sql = "select ID,NAME,LOCATION,COMMENT,DISPLAY_ON_HOME from TESTIMONIALS"

            cur = mysql.connection.cursor()

            cur.execute(sql)

            res = cur.fetchall()

            proql = "select ID,IMAGE,NAME,EMAIL,PASSWORD,MOBILE,ROLE from USERS where ID=%s"

            proval = [session['id']]

            cur.execute(proql, proval)

            prop = cur.fetchall()

            cur.close()

            return render_template('admin_testimonials.html', result=res, len=len(res), profile=prop)

        else:

            return render_template('err404.html')

    except:

        return render_template('err404.html')


@app.route('/admin/add-testimonials', methods=['POST'])
def add_test():
    try:

        if session['loggedin'] == True:
            name = request.form['name']

            cmt = request.form['comment']

            loc = request.form['Location']

            doh = request.form['displayonhome']

            current_time = datetime.datetime.now()

            sql = "insert into TESTIMONIALS (NAME,LOCATION,COMMENT,DISPLAY_ON_HOME,CREATER_AT) values (%s,%s,%s,%s,%s)"

            val = (name, loc, cmt, doh, current_time)

            cur = mysql.connection.cursor()

            cur.execute(sql, val)

            # con.commit()

            mysql.connection.commit()

            cur.close()

            return admin_test()

    except:

        return render_template('err404.html')


@app.route('/admin/del-test/<id>')
def admin_del_testimonials(id):
    try:

        if session['loggedin'] == True:

            sql = "delete from TESTIMONIALS where id=%s"

            cur = mysql.connection.cursor()

            cur.execute(sql, [id])

            # con.commit()

            mysql.connection.commit()

            cur.close()

            return admin_test()

        else:

            return render_template('err404.html')

    except:

        return render_template('err404.html')


# Admin - Serivices

@app.route('/admin/services')
def admin_services():
    try:

        if session['loggedin'] == True:

            sql = "select ID,NAME,IMAGE,DESCRIPTION,p1,p2,p3,p4,p5,p6,p7,p8,p9,p10 from SERVICES"

            cur = mysql.connection.cursor()

            cur.execute(sql)

            res = cur.fetchall()

            proql = "select ID,IMAGE,NAME,EMAIL,PASSWORD,MOBILE,ROLE from USERS where ID=%s"

            proval = [session['id']]

            cur.execute(proql, proval)

            prop = cur.fetchall()

            cur.close()

            return render_template('admin_services.html', result=res, len=len(res), profile=prop)

        else:

            return render_template('err404.html')

    except:

        return render_template('err404.html')


@app.route('/admin/add-services', methods=['POST'])
def admin_add_services():
    try:

        if session['loggedin'] == True:

            name = request.form['service_id']

            description = request.form['description'] if request.form['description']  != '' else ''

            image = request.files['image']
            
            pone = request.form['pone'] if request.form['pone']  != '' else ''
            
            ptwo = request.form['ptwo'] if request.form['ptwo']  != '' else ''
            
            pthree = request.form['pthree'] if request.form['pthree']  != '' else ''
            
            pfour = request.form['pfour'] if request.form['pfour']  != '' else ''
            
            pfive = request.form['pfive'] if request.form['pfive']  != '' else ''
            
            psix = request.form['psix'] if request.form['psix']  != '' else ''
            
            pseven = request.form['pseven'] if request.form['pseven']  != '' else ''
            
            peight = request.form['peight'] if request.form['peight']  != '' else ''
            
            pnine = request.form['pnine'] if request.form['pnine']  != '' else ''
            
            pten = request.form['pten'] if request.form['pten']  != '' else ''
            

            image.save(os.path.join(app.config['SERVICES'], image.filename))

            thumbname = image.filename

            current_time = datetime.datetime.now()

            print(name, thumbname, description, current_time)

            sql = "insert into SERVICES (NAME,IMAGE,DESCRIPTION,p1,p2,p3,p4,p5,p6,p7,p8,p9,p10,CREATED_AT) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"

            cur = mysql.connection.cursor()

            val = (name, thumbname, description, pone,ptwo,pthree,pfour,pfive,psix,pseven,peight,pnine,pten,current_time)

            cur.execute(sql, val)

            # con.commit()

            mysql.connection.commit()

            cur.close()

            return admin_services()

        else:

            return render_template('err404.html')

    except:

        return render_template('err404.html')


@app.route('/admin/del-services/<id>')
def admin_del_service(id):
    try:

        if session['loggedin'] == True:

            sql = "delete from SERVICES where id=%s"

            cur = mysql.connection.cursor()

            cur.execute(sql, [id])

            # con.commit()

            mysql.connection.commit()

            return admin_services()

            cur.close()

        else:

            return render_template('err404.html')

    except:

        return render_template('err404.html')


# Admin - Ask Us

@app.route('/admin/askus')
def admin_askus():
    try:

        if session['loggedin'] == True:

            sql = "select ID,NAME,IMAGE from ASKUS"

            cur = mysql.connection.cursor()

            cur.execute(sql)

            res = cur.fetchall()

            lenres = len(res)

            proql = "select ID,IMAGE,NAME,EMAIL,PASSWORD,MOBILE,ROLE from USERS where ID=%s"

            proval = [session['id']]

            cur.execute(proql, proval)

            prop = cur.fetchall()

            cur.close()

            return render_template('admin_askus.html', profile=prop, result=res, lenres=lenres)

        else:

            return render_template('err404.html')

    except:

        return render_template('err404.html')


@app.route('/admin/add-askus', methods=['POST'])
def admin_addaskus():
    try:
        if session['loggedin'] == True:

            name = request.form['title']

            image = request.files['thumbnail']

            image.save(os.path.join(app.config['ASKUS'], image.filename))

            thumbname = image.filename

            current_time = datetime.datetime.now()

            sql = "insert into ASKUS (NAME,IMAGE,CREATED_AT) values (%s,%s,%s)"

            val = (name, thumbname, current_time)

            cur = mysql.connection.cursor()

            cur.execute(sql, val)

            # con.commit()

            mysql.connection.commit()

            cur.close()

            return admin_askus()

        else:

            return render_template('err404.html')

    except:

        return render_template('err404.html')


@app.route('/admin/del-askus/<id>')
def admin_del_askus(id):
    try:

        if session['loggedin'] == True:

            sql = "delete from ASKUS where id=%s"

            cur = mysql.connection.cursor()

            cur.execute(sql, [id])

            # con.commit()

            mysql.connection.commit()

            cur.close()

            return admin_askus()

        else:

            return render_template('err404.html')

    except:

        return render_template('err404.html')


# Admin - Quality Standards

@app.route('/admin/qs')
def admin_qs():
    try:

        if session['loggedin'] == True:

            sql = "select ID,NAME from QUALITYSTANDARDS"

            cur = mysql.connection.cursor()

            cur.execute(sql)

            res = cur.fetchall()

            lenres = len(res)

            proql = "select ID,IMAGE,NAME,EMAIL,PASSWORD,MOBILE,ROLE from USERS where ID=%s"

            proval = [session['id']]

            cur.execute(proql, proval)

            prop = cur.fetchall()

            cur.close()

            return render_template('admin_Quality.html', profile=prop, result=res, lenres=lenres)

        else:

            return render_template('err404.html')

    except:

        return render_template('err404.html')


@app.route('/admin/add-qs', methods=['POST'])
def admin_addqs():
    try:

        if session['loggedin'] == True:

            name = request.form['name']

            current_time = datetime.datetime.now()

            sql = "insert into QUALITYSTANDARDS (NAME,CREATED_AT) values (%s,%s)"

            val = (name, current_time)

            cur = mysql.connection.cursor()

            cur.execute(sql, val)

            # con.commit()

            mysql.connection.commit()

            cur.close()

            return admin_qs()

        else:

            return render_template('err404.html')

    except:

        return render_template('err404.html')


@app.route('/admin/del-qs/<id>')
def admin_del_qs(id):
    try:

        if session['loggedin'] == True:

            sql = "delete from QUALITYSTANDARDS where id=%s"

            cur = mysql.connection.cursor()

            cur.execute(sql, id)

            # con.commit()

            mysql.connection.commit()

            cur.close()

            return admin_qs()

        else:

            return render_template('err404.html')

    except:

        return render_template('err404.html')


# Career Opportunity

@app.route('/admin/careers')
def careersopp():
    try:

        if session['loggedin'] == True:

            sql = "select ID,DESCRIPTION from CAREERS"

            cur = mysql.connection.cursor()

            cur.execute(sql)

            res = cur.fetchall()

            lenres = len(res)

            proql = "select ID,IMAGE,NAME,EMAIL,PASSWORD,MOBILE,ROLE from USERS where ID=%s"

            proval = [session['id']]

            cur.execute(proql, proval)

            prop = cur.fetchall()

            cur.close()

            return render_template('admin_careers.html', profile=prop, result=res, lenres=lenres)

        else:

            return render_template('err404.html')
    except:
        return render_template('err404.html')


@app.route('/admin/add-careers', methods=['POST'])
def careersadd():
    try:

        if session['loggedin'] == True:

            name = request.form['careeropps']

            current_time = datetime.datetime.now()

            sql = "insert into CAREERS (DESCRIPTION,CREATED_AT) values (%s,%s)"

            val = (name, current_time)

            cur = mysql.connection.cursor()

            cur.execute(sql, val)

            # con.commit()

            mysql.connection.commit()

            cur.close()

            return careersopp()

        else:

            return render_template('err404.html')

    except:

        return render_template('err404.html')


@app.route('/admin/del-careers/<id>')
def admin_del_careers(id):
    try:

        if session['loggedin'] == True:

            sql = "delete from CAREERS where id=%s"

            cur = mysql.connection.cursor()

            cur.execute(sql, [id])

            # con.commit()

            mysql.connection.commit()

            cur.close()

            return careersopp()

        else:

            return render_template('err404.html')

    except:

        return render_template('err404.html')


@app.route('/admin/features')
def admin_feature():
    try:

        if session['loggedin'] == True:

            sql = "SELECT ID,NAME from FEATURES;"

            cur = mysql.connection.cursor()

            cur.execute(sql)

            res = cur.fetchall()

            proql = "select ID,IMAGE,NAME,EMAIL,PASSWORD,MOBILE,ROLE from USERS where ID=%s"

            proval = [session['id']]

            cur.execute(proql, proval)

            prop = cur.fetchall()

            cur.close()

            return render_template('admin_features.html', result=res, len=len(res), profile=prop)

        else:

            return render_template('err404.html')

    except:

        return render_template('err404.html')


@app.route('/admin/add-feature', methods=['POST'])
def admin_add_feature():
    try:

        if session['loggedin'] == True:

            name = request.form['name']

            current_time = datetime.datetime.now()

            sql = "insert into FEATURES (NAME,CREATED_AT) values (%s,%s)"

            val = (name, current_time)

            cur = mysql.connection.cursor()

            cur.execute(sql, val)

            # con.commit()

            mysql.connection.commit()

            cur.close()

            return admin_feature()

        else:

            return render_template('err404.html')

    except:

        return render_template('err404.html')


@app.route('/admin/del-features/<id>')
def admin_del_features(id):
    try:

        if session['loggedin'] == True:

            sql = "delete from FEATURES where id=%s"

            cur = mysql.connection.cursor()

            cur.execute(sql, [id])

            # con.commit()

            mysql.connection.commit()

            cur.close()

            return admin_feature()

        else:

            return render_template('err404.html')

    except:

        return render_template('err404.html')


# Admin - Contact-Forms

@app.route('/admin/askus-forms')
def admin_askusforms():
    try:

        if session['loggedin'] == True:

            sql = "SELECT ID,NAME,EMAIL,PHONE,SERVICE,URGENCY,PAGES,DOMAIN,REFERENCE,IMPLEMENTATION,DESCRIPTION,CREATED_AT from ASKUSFORM;"

            cur = mysql.connection.cursor()

            cur.execute(sql)

            res = cur.fetchall()

            proql = "select ID,IMAGE,NAME,EMAIL,PASSWORD,MOBILE,ROLE from USERS where ID=%s"

            proval = [session['id']]

            cur.execute(proql, proval)

            prop = cur.fetchall()

            cur.close()

            return render_template('admin_askusforms.html', result=res, len=len(res), profile=prop)

        else:

            return render_template('err404.html')

    except:

        return render_template('err404.html')


@app.route('/admin/del-contactform/<id>')
def admin_del_contactform(id):
    try:

        if session['loggedin'] == True:

            sql = "delete from ASKUSFORM where id=%s"

            cur = mysql.connection.cursor()

            cur.execute(sql, [id])

            # con.commit()

            mysql.connection.commit()

            cur.close()

            return admin_askusforms()

        else:

            return render_template('err404.html')

    except:

        return render_template('err404.html')


# Admin - Add

@app.route('/admin/list-admin')
def admin_listadmin():
    try:

        if session['loggedin'] == True:

            sql = "SELECT ID,IMAGE,NAME,EMAIL,MOBILE,ROLE from USERS;"

            cur = mysql.connection.cursor()

            cur.execute(sql)

            res = cur.fetchall()

            proql = "select ID,IMAGE,NAME,EMAIL,PASSWORD,MOBILE,ROLE from USERS where ID=%s"

            proval = [session['id']]

            cur.execute(proql, proval)

            prop = cur.fetchall()

            cur.close()

            return render_template('admin_administrator.html', result=res, len=len(res), profile=prop)

        else:

            return render_template('err404.html')

    except:

        return render_template('err404.html')


@app.route('/admin/add-user', methods=['POST'])
def admin_add_user():
    try:

        if session['loggedin'] == True:

            name = request.form['name']

            email = request.form['email']

            password = request.form['password']

            mobile = request.form['mobile']

            role = request.form['adminoruser']

            pwd = sha256_crypt.encrypt(password)

            image = request.files['image']

            image.save(os.path.join(app.config['PROFILEPICS'], image.filename))

            imagename = image.filename

            current_time = datetime.datetime.now()

            sql = "insert into USERS (IMAGE,NAME,EMAIL,PASSWORD,MOBILE,ROLE,CREATED_AT) values (%s,%s,%s,%s,%s,%s,%s)"

            val = (imagename, name, email, pwd, mobile, role, current_time)

            cur = mysql.connection.cursor()

            cur.execute(sql, val)

            # con.commit()

            mysql.connection.commit()

            cur.close()

            return admin_listadmin()

        else:

            return render_template('err404.html')

    except:

        return render_template('err404.html')


@app.route('/admin/up-user', methods=['POST'])
def admin_update():
    try:

        if session['loggedin'] == True:

            id = request.form['userid']

            email = request.form['email']

            password = request.form['password']

            role = request.form['adminoruser']

            cur = mysql.connection.cursor()

            if (email != ''):

                if (password != ''):

                    pwd = sha256_crypt.encrypt(password)

                    if (role != ''):

                        sql = '''UPDATE USERS SET EMAIL = %s, PASSWORD= %s,ROLE=%s WHERE ID = %s;'''

                        val = (email, pwd, role, id)

                        cur.execute(sql, val)

                        # con.commit()

                        mysql.connection.commit()

                        cur.close()

                        return admin_listadmin()

                    else:

                        sql = '''UPDATE USERS SET EMAIL = %s, PASSWORD= %s WHERE ID = %s;'''

                        val = (email, pwd, id)

                        cur.execute(sql, val)

                        # con.commit()

                        mysql.connection.commit()

                        cur.close()

                        return admin_listadmin()

                else:

                    sql = '''UPDATE USERS SET EMAIL = %s WHERE ID = %s;'''

                    val = (email, id)

                    cur.execute(sql, val)

                    # con.commit()

                    mysql.connection.commit()

                    cur.close()

                    return admin_listadmin()

            elif (password != ''):

                pwd = sha256_crypt.encrypt(password)

                sql = '''UPDATE USERS SET PASSWORD= %s WHERE ID = %s;'''

                val = (pwd, id)

                cur.execute(sql, val)

                # con.commit()

                mysql.connection.commit()

                cur.close()

                return admin_listadmin()

            elif (role != ''):

                sql = '''UPDATE USERS SET ROLE=%s WHERE ID = %s;'''

                val = (role, id)

                cur.execute(sql, val)

                # con.commit()

                mysql.connection.commit()

                cur.close()

                return admin_listadmin()

            else:

                return render_template('err404.html')

        else:

            return render_template('err404.html')

    except:

        return render_template('err404.html')


@app.route('/admin/del-admin/<id>')
def admin_del(id):
    try:

        if session['loggedin'] == True:

            sql = "delete from USERS where id=%s"

            cur = mysql.connection.cursor()

            cur.execute(sql, [id])

            # con.commit()

            mysql.connection.commit()

            cur.close()

            return admin_listadmin()

        else:

            return render_template('err404.html')

    except:

        return render_template('err404.html')


# Admin - Dashboard

@app.route('/admin/dashboard')
def dashboard():
    try:

        if session['loggedin'] == True:

            sql = "select ID,IMAGE,NAME,EMAIL,PASSWORD,MOBILE,ROLE from USERS where ID=%s"

            val = [session['id']]

            cur = mysql.connection.cursor()

            cur.execute(sql, val)

            res = cur.fetchall()

            cur.close()

            return render_template('dashboard.html', profile=res)

        else:

            return render_template('err404.html')

    except:

        return render_template('err404.html')


@app.route('/admin/update-data', methods=['POST'])
def updatedata():
    try:
        if session['loggedin'] == True:
    
            id = session['id']
    
            npwd = request.form['npwd']
    
            cpwd = request.form['cpwd']
    
            image = request.files['profilepic']
    
            image.save(os.path.join(app.config['PROFILEPICS'], image.filename))
    
            imagename = image.filename
    
            cur = mysql.connection.cursor()
    
            if (imagename != ''):
    
                if (npwd == cpwd):
    
                    sql = '''UPDATE USERS SET PASSWORD = %s, IMAGE= %s WHERE ID = %s;'''
    
                    pwd = sha256_crypt.encrypt(npwd)
    
                    val = (pwd, imagename, id)
    
                    cur.execute(sql, val)
    
                    # con.commit()
    
                    mysql.connection.commit()
    
                    cur.close()
    
                    return setting()
    
                else:
    
                    flash("Confirm Password and Password is mismatch")
    
                    return setting()
    
            elif (npwd == cpwd):
    
                sql = '''UPDATE USERS SET PASSWORD = %s WHERE ID = %s;'''
    
                pwd = sha256_crypt.encrypt(npwd)
    
                val = (pwd, id)
    
                cur.execute(sql, val)
    
                # con.commit()
    
                mysql.connection.commit()
    
                cur.close()
    
                return setting()
    
            else:
    
                flash("Error No Updation Requested")
    
                return setting()
    
        else:
    
            return render_template('err404.html')
    except:
        
        return render_template('err404.html')
        


@app.route('/settings')
def setting():
    try:

        if session['loggedin'] == True:

            sql = "select ID,IMAGE,NAME,EMAIL,PASSWORD,MOBILE,ROLE,CREATED_AT from USERS where ID=%s"

            val = [session['id']]

            cur = mysql.connection.cursor()

            cur.execute(sql, val)

            res = cur.fetchall()

            cur.close()

            return render_template('admin_settings.html', profile=res)


        else:

            return render_template('err404.html')

    except:

        return render_template('err404.html')


# Admin - logout

@app.route('/admin/logout')
def logout():
    session.pop('loggedin', None)

    session.pop('id', None)

    session.pop('username', None)

    return redirect('/admin')

if __name__ == '__main__':
    app.run(debug=True)
