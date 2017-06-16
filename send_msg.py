import requests
import json

from bs4 import BeautifulSoup
from pygeocoder import Geocoder

from flask import Flask, request, jsonify

app = Flask(__name__)













def message_sending(lat,lng,mob):
    lat = float(lat)
    lng= float(lng)
    results = Geocoder.reverse_geocode(lat,lng)
    coord=  results.coordinates

    street = results.street_address

    state = results.administrative_area_level_1

    country = results.country


    final_add= str(coord) + " " + str(street) + " " + str(state) + " " + str(country)


     
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
		

		
    msg= final_add + "I am in Danger Situation! Help me"
    mobile_no= mob	
	
    if len(msg)>139 or len(mobile_no)!=10 :	#checks whether the given message is of length more than 139

        print "NOT VALIDs"		
    payload={'ssaction':'ss','Token':jsid,'mobile':mobile_no,'message':msg,'msgLen':'129'}
		
    
       			     	        #or the mobile_no is valid

    # payload={'ssaction':'ss',
		     # 'Token':jsid,					
		    # 'mobile':mobile_no,					
            # 'message':msg,						
	        # 'msgLen':'129'
       			     # }

    msg_url='http://site24.way2sms.com/smstoss.action'

    q=s.post(msg_url,data=payload)

    if q.status_code==200:

        print "True"

    else:
        print " False"

	

    s.get('http://site24.way2sms.com/entry?ec=0080&id=dwks')

    s.close()								# close the Session

    loggedIn=False


    


@app.route('/m/sbcon/', methods=['GET'])
def data():
    if len(request.args.get("lats")) and len(request.args.get("lngs")) and len(request.args.get("mob")):
        lat=request.args.get("lats")
        lng=request.args.get("lngs")
        mob=request.args.get("mob")
        message_sending(lat,lng,mob)
        data={"msg":["sent successfully"]}
        return jsonify(data)
        
   

if __name__ == "__main__":
    app.run(debug=True)		
    







