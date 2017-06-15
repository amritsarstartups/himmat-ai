import requests

from bs4 import BeautifulSoup



api_url = "https://sheetsu.com/apis/v1.0/f40a9e99e783"



r = requests.get(api_url)

print r.text






url='http://site24.way2sms.com/Login1.action?'

cred={'username': "8427407305", 'password': "SAURABH123"}

s=requests.Session()			# Session because we want to maintain the cookies

		
s.headers['User-Agent']="Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:50.0) Gecko/20100101 Firefox/50.0"

q=s.post(url,data=cred)

loggedIn=False				# a variable of knowing whether logged in or not

if q.status_code!=200:			# http status 200 == OK

    loggedIn=False

else:

    loggedIn=True

jsid=s.cookies.get_dict()['JSESSIONID'][4:]	    # JSID is the main KEY as JSID are produced every time a session satrts

	
		

msg_left_url='http://site24.way2sms.com/sentSMS?Token='+jsid

q=s.get(msg_left_url)

soup=BeautifulSoup(q.text,'html.parser')		#we want the number of messages sent which is present in the 	

t=soup.find("div",{"class":"hed"}).h2.text		# div element with class "hed" -> h2 

sent=0

for i in t:

    if i.isdecimal():

        sent=10*sent+int(i)
		
print sent
		

		
msg= "Your Message goes here"
mobile_no= "9876099041"	
	
if len(msg)>139 or len(mobile_no)!=10 :	#checks whether the given message is of length more than 139

    print "NOT VALIDs"							#or the mobile_no is valid

payload={'ssaction':'ss',
		'Token':jsid,					#inorder to visualize how I came to these payload,
		'mobile':mobile_no,					#must see the NETWORK section in Inspect Element 
        'message':msg,						#while messagin someone from your browser
	    'msgLen':'129'
       			     }

msg_url='http://site24.way2sms.com/smstoss.action'

q=s.post(msg_url,data=payload)

if q.status_code==200:

    print "True"

else:
    print " False"

	

s.get('http://site24.way2sms.com/entry?ec=0080&id=dwks')

s.close()								# close the Session

loggedIn=False