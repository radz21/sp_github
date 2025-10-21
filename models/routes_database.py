from flask import session, redirect, url_for, render_template, request
import mysql.connector
from mysql.connector import Error
import os, sys, json
import pymysql.cursors
from flask_cors import CORS
from os.path import exists
# import simplejson as json

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from smtplib import SMTPAuthenticationError
from smtplib import SMTPRecipientsRefused
from smtplib import SMTPSenderRefused
from smtplib import SMTPDataError


if sys.platform.lower() == "win32":
    os.system('color')

class style():
    BLACK = lambda x: '\033[30m' + str(x)
    RED = lambda x: '\033[31m' + str(x)
    GREEN = lambda x: '\033[32m' + str(x)
    YELLOW = lambda x: '\033[33m' + str(x)
    BLUE = lambda x: '\033[36m' + str(x)
    MAGENTA = lambda x: '\033[35m' + str(x)
    WHITE = lambda x: '\033[37m' + str(x)
    UNDERLINE = lambda x: '\033[4m' + str(x)
    RESET = lambda x: '\033[0m' + str(x)

def prnt_Y(msg):
	clr=print(style.YELLOW(msg),style.RESET(''))
	return clr

def prnt_R(msg):
	clr=print(style.RED(msg),style.RESET(''))
	return clr

def prnt_W(msg):
	clr=print(style.MAGENTA(msg),style.RESET(''))
	return clr

def prnt_B(msg):
	clr=print(style.BLUE(msg),style.RESET(''))
	return clr

def prnt_G(msg):
	clr=print(style.GREEN(msg),style.RESET(''))
	return clr

# host = "192.168.254.104"
# user = "carlo"
# password = "password"


host = "localhost"
user = "root"

password = "sp_bislig"
database1 = "sangunian_db"


host = "localhost"
user = "root"
password = "sp_bislig"

# password = "bislig"
# database1 = "sangs"

#<-----------------------Connection database------------------------------->

try:
	db =  mysql.connector.connect(host=host, user=user, password =password, database=database1,auth_plugin='mysql_native_password')
	print(style.WHITE("Successfuly Connected to Database") + style.RESET(""))
except Exception as e:
	ers="Failed to connect database try to restart server"
	print(style.RED(ers) + style.RESET(""))

#<---------------------------Crud-------------------------------->

def cud(sql):
	try:
		db = mysql.connector.connect(host=host, user=user, password =password, database=database1, charset='utf8',use_unicode=True);
		con = db.cursor()
		con.execute(sql)
		db.commit()

		if(db.is_connected()):
			db.close()
			con.close()
			print(style.GREEN("Successfuly queried") + style.RESET(""))
		return "200"
	except Exception as e:
		print(style.RED("MYSQL error in loading: '"+str(e)+"' '"+str(sql)+"'") + style.RESET(""))
		sys.exit("Error message")
		return "400"

#<---------------------crud closed -------------------------------->

def cud_callbackid(sql):
	try:
		db = mysql.connector.connect(host=host, user=user, password =password, database=database1, charset='utf8',use_unicode=True);
		con = db.cursor()
		con.execute(sql)
		db.commit()

		if(db.is_connected()):
			db.close()
			con.close()
			ids = con.lastrowid
			print(style.GREEN(ids) + style.RESET(""))
		return ids
	except Exception as e:
		print(style.RED("MYSQL error in loading: '"+str(e)+"'") + style.RESET(""))
		sys.exit("Error message")


def read(sql):
#---------3.7v and upper version of py connection -------#
	try:
		# prnt_G(sql)
		db =  mysql.connector.connect(host=host, user=user, password =password, database=database1)
		con = db.cursor()
		for result in con.execute(sql, multi=True):
			return result.fetchall()
		if(db.is_connected()):
			db.close()
			con.close()
	except Exception as e:
		print(style.RED("MYSQL error in loading: '"+str(e)+"'") + style.RESET(""))


def pyread(sql):
	try:
		connection = pymysql.connect(host=host, user=user, password =password, database=database1,charset='utf8',cursorclass=pymysql.cursors.DictCursor)
		# connection = pymysql.connect(host="localhost", user="root", password ="", database="hrmis_v3", charset='utf8',cursorclass=pymysql.cursors.DictCursor)
		with connection.cursor() as cursor:
			# Read a single record
			cursor.execute(sql)
			result = cursor.fetchall()
			connection.close();	
			return result
	except Exception as e:
		print(style.RED("MYSQL error in pyMSQL: '"+str(e)+"' '"+str(sql)+"'") + style.RESET(""))

#<------>-----------------end read database------------------->



class EmailSender():
    from_address = ""
    password = ""

    msg = MIMEMultipart()
    files=[]
    def set_sender_credentials(self, email_add, password):
        self.from_address = email_add
        self.password = password
        print("Successfully setted sender credentials")
    def set_email_data(self, subject, body, attachment, emailed_to, sender_email, sender_password):
    	prnt_R(os.path.abspath(os.getcwd()))
    	self.msg=""
    	self.msg = MIMEMultipart()
    	self.msg['Subject'] = subject
    	# selg.msg.clear()
    	self.msg.attach(MIMEText(body, 'html'))
    	self.files = attachment
    	self.email_to=emailed_to
    	self.sender_from=sender_email
    	self.sender_pass=sender_password

    	for f in self.files:
    		fl =  exists(f)
    		if fl:
    			attachment = open(f, "rb")
    			f_name = os.path.basename(f)
    			p = MIMEBase('application', 'octe-stream')
    			p.set_payload((attachment).read())
    			encoders.encode_base64(p)
    			p.add_header('Content-Disposition', "attachment; filename=%s" % f_name)
    			self.msg.attach(p)
    			print("Successfully attached file: ", f)
    		else:
    			prnt_G("file not exists")
    			
    def send_email(self, to):
    	self.msg['From'] = self.sender_from
    	self.msg['To'] = self.email_to
    	self.msg['pass'] = self.sender_pass
    	s = smtplib.SMTP("smtp.gmail.com", 587)
    	s.set_debuglevel(1)
    	s.verify(self.sender_from)
    	s.ehlo()
    	s.starttls()
    	s.ehlo()
    	text = self.msg.as_string()
    	try:
    		print("Logging in credentials")
    		s.login(self.sender_from, self.sender_pass)
    		print("Successfully logged in")
    	except SMTPAuthenticationError:
    		print("Sending error: Athentication invalid")
    		return False
    	try:
    		print("Sending email")
    		s.sendmail(self.sender_from, self.email_to, text)
    		s.quit()
    		return True
    	except SMTPRecipientsRefused as e:
    		print("Sending error: Recipient Refused", e)
    		s.quit()
    		return False
    	except SMTPSenderRefused as e:
    		print("Sending error: Sender Refused", type(e))
    		s.quit()
    		return False
    	except SMTPDataError:
    		print("Sending error: Incorrect or invalid data passed")
    		return False



def rd_query(sql, val, one=False):
	try:
		connection = pymysql.connect(host=host, user=user, password =password, database=database1,charset='utf8')
		cur = connection.cursor() 
		cur.execute(sql,val) 
		r = [dict((cur.description[i][0], value) \
               for i, value in enumerate(row)) for row in cur.fetchall()]
		cur.connection.close()
		return (r[0] if r else None) if one else r
	except Exception as e:
		print(style.RED("MYSQL error in pyMSQL: '"+str(e)+"'") + style.RESET(""))



#<---------------------------Crud-------------------------------->
def crud(sql, ar):
    try:
        db = mysql.connector.connect(
            host=host, user=user, password=password, database=database1,
            charset='utf8', use_unicode=True
        )
        con = db.cursor()
        con.execute(sql, ar)
        db.commit()

        if db.is_connected():
            con.close()
            db.close()
            print("Successfully queried")
            return "200" # Fixed indentation here
    except Exception as e:
        print("MYSQL error:", str(e))
        return "1062"
