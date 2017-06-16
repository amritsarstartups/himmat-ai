import os, sys
from flask import Flask, request,  jsonify
from pymessenger import Bot
import requests
import json

app= Flask(__name__)    #initialisng app


page_access_token =" your_page_access_token"   #create a permamnent page access token
bot = Bot(page_access_token)

@app.route('/', methods=['GET'])
def verify():
    #webhook verification
	if request.args.get("hub.mode") == "subscribe" and request.args.get("hub.challenge"):
	    if not request.args.get("hub.verify_token") == "hello":
		    return "Verification token mismatch", 403
	    return request.args["hub.challenge"], 200
	return "Hello World", 200

	 
    

	
#=======================================================#	
	
	
place_api="Your_api"     #api provided by google(google placeapi)
base_url="https://maps.googleapis.com/maps/api/place/search/json?location="


def location_data(lat,lng,type):
    
    location= lat+","+lng
    final_url= base_url+location + "&rankby=distance&types=" + type+ "&key="+ place_api

    #r=requests.get("https://maps.googleapis.com/maps/api/place/search/json?location=31.6607795,74.8214579&rankby=distance&types=police&sensor=false&key="+place_api)
    r=requests.get(final_url)
    #print r.content
    #d = ast.literal_eval(r)

    result = json.loads(r.text)

    data=dict(result)

    #pprint.pprint(data)

    result=data["results"]
    final_data=dict()

    final_data["data"]=list()
    #fetching required data  

    for item in result:
        print "Name" , item["name"]
        print "Address" ,item["vicinity"]
        print "Co-ordinates", item["geometry"]["location"]["lat"], item["geometry"]["location"]["lng"] 
        
        d= {}
        d["name"]=item["name"]
        d["locations"]=item["vicinity"]
        d["lat"]=item["geometry"]["location"]["lat"]
        d["lng"]=item["geometry"]["location"]["lng"]
        final_data["data"].append(d)
    return final_data

@app.route('/api/sbcon/', methods=['GET'])     #configuring the post request to get the data
def data():
    if len(request.args.get("lats")) and len(request.args.get("lngs")) and len(request.args.get("category")):  #dynamic parameters
        lat=request.args.get("lats")
        lng=request.args.get("lngs")
        category=request.args.get("category")
        return jsonify(location_data(lat,lng,category))
   

if __name__ == "__main__":
    app.run(debug=True, port =80)		
	
