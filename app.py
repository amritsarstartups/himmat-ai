import os, sys
from flask import Flask, request,  jsonify
from pymessenger import Bot
import requests
import json

app= Flask(__name__)

page_access_token = "EAATZAU8XCjkcBAI12BNwPrB5RZCZC4poPsJlmTJZAHLbSqtR4GPZC6b2fG5onlNCxYZA8ysMxErMD366dKNmW4pFq6jU0zx55ZAbjvlMfm0uN0GEkbU2GrpyZABdIVlsvdDdWcjvqooYfUNA3iWw4UJb4psevtqGCsQu9lFW9tH8zwZDZD"
bot = Bot(page_access_token)

@app.route('/', methods=['GET'])
def verify():
    #webhook verification
	if request.args.get("hub.mode") == "subscribe" and request.args.get("hub.challenge"):
	    if not request.args.get("hub.verify_token") == "hello":
		    return "Verification token mismatch", 403
	    return request.args["hub.challenge"], 200
	return "Hello World", 200

	 
    
@app.route('/', methods=['POST'])
def webhook():
    data= request.get_json()
    log(data)	
	
    if data['object'] == 'page':
	    for entry in data['entry']:
		    for messaging_event in entry['messaging']:
			    
				#ids
				sender_id= messaging_event['sender']['id']
				recipient_id = messaging_event['recipient']['id']
				
				if messaging_event.get('message'):
				    if 'text' in messaging_event['message']:
					    messaging_text=messaging_event['message']['text']
				    else:
					    messaging_text = 'no_text'
					
				    response =response_msg(messaging_text)
				    bot.send_text_message(sender_id, response)
	
    return "ok", 200
	  

#Main task is to genrate responses for the CESS MANIA 
# 3 main resonses based on the query
# 1) Answer to the event: Particular format needed ->
# format :  Cess Mania , Name , Task , Answer
# response: "Wassup! I am Cess-istant" /n Welcome to CESS Mania /n Your answer is successfully submitted/n Points will be rewared accorind to correctness of your answer/ Keep playing in CESS MANIA

# 2)  Answer to event but wrong format : "Wassup! I am Cess-istant"/n Oops! look like you entered the answer in wrong format! /n "Format details" /n Please send your response again in given format/n Keep playing in CESS MANIA 
# 3)   Any other answer response ->  "Wassup! I am Cess-istant"/n Thankyou for connecting with CESS /n We will get back to you soonest! /n Cess mania details..


def response_msg(savaal):
    
    savaal=savaal.lower()
    if (savaal.startswith("cess mania") and len(savaal.split(",")) == 4) :
	    
        text_list= savaal.split(",")
        student_name= text_list[1]
        task=text_list[2]
        task_answer=text_list[3]        
        output = "Wassup! I am Cess-istant. Welcome to CESS Mania. Your answer is successfully submitted. Points will be rewarded according to correctness of your answer. Keep playing in CESS MANIA"
    
    elif (savaal.startswith("cess mania") or len(savaal.split(",")) == 4) :
        output = "Wassup! I am Cess-istant. Oops! looks like you entered the answer in wrong format! Format -> Cess Mania , Name , Task , Answer. Please send your response again in given format. Keep playing in CESS MANIA"	
        
		      
            	
    else :
        output =  "Wassup! I am Cess-istant. Thankyou for connecting with CESS. We will get back to you soonest! (In case you submitted answer for CESS MANIA TASK, please send the answer in given format). Till then go check out CESS MANIA, its awesome. CESS MANIA FAQs : Q) How to register for CESS MANIA A)There is no registration for CESS MANIA, just like and share CESS PAGE and you are good to go"
		
    		
    return output	
		
 
def log(msg):
    print msg
    sys.stdout.flush()	
	  
if __name__ == "__main__":
    app.run(debug=True, port =80)

	
#=======================================================#	
	
	
place_api="AIzaSyDT0P7r0ezcoeNvotC_J2AwviQnCCfj0Oo"
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


    for item in result:
        print "Name" , item["name"]
        print "Address" ,item["vicinity"]
        print "Co-ordinates", item["geometry"]["location"]["lat"], item["geometry"]["location"]["lng"] 
        
        d= {}
        d["name"]=item["name"]
        d["address"]=item["vicinity"]
        d["lat"]=item["geometry"]["location"]["lat"]
        d["lng"]=item["geometry"]["location"]["lng"]
        final_data["data"].append(d)
    return final_data

@app.route('/api/sbcon/', methods=['GET'])
def data():
    if len(request.args.get("lats")) and len(request.args.get("lngs")) and len(request.args.get("category")):
        lat=request.args.get("lats")
        lng=request.args.get("lngs")
        category=request.args.get("category")
        return jsonify(location_data(lat,lng,category))
   

if __name__ == "__main__":
    app.run(debug=True, port =80)		
	
