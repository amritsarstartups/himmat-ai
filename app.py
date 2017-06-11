import os, sys

from flask import Flask, request
from pymessenger import Bot


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
					
				    response ="how may i help u?"
				    bot.send_text_message(sender_id, response)
	
    return "ok", 200
	  

#Main task is to genrate responses for the CESS MANIA 
# 3 main resonses based on the query
# 1) Answer to the event: Particular format needed ->
# format :  Cess Mania ,Name abc , Task XYZ, Answer ans
# response: "Wassup! I am Cess-istant" /n Welcome to CESS Mania /n Your answer is successfully submitted/n Points will be rewared accorind to correctness of your answer/ Keep playing in CESS MANIA

# 2)  Answer to event but wrong format : "Wassup! I am Cess-istant"/n Oops! look like you entered the answer in wrong format! /n "Format details" /n Please send your response again in given format/n Keep playing in CESS MANIA 
# 3)   Any other answer response ->  "Wassup! I am Cess-istant"/n Thankyou for connecting with CESS /n We will get back to you soonest! /n Cess mania details..


def response_msg(savaal):
    savaal=savaal.lower()
    if savaal.startswith("CESS MANIA") :
	    if(savaal.split(",")[1].split()[0] == "name" and savaal.split(",")[2].split()[0] == "task" and savaal.split(",")[3].split()[0] == "answer"):
	        text_list= savaal.split(",")
	        student_name= text_list[1].split()[1]
	        task=text_list[2].split()[1]
	        task_answer=text_list[3].split()[1]
	        output = "Wassup! I am Cess-istant /n Welcome to CESS Mania /n Your answer is successfully submitted/n Points will be rewared accorind to correctness of your answer/n Keep playing in CESS MANIA"
        #else :
		      
            #output = "Wassup! I am Cess-istant/n Oops! look like you entered the answer in wrong format! /n Format -> CESS MANIA , Name abc, Task XYZ , Answer your_answer /n Please send your response again in given format/n Keep playing in CESS MANIA"		
    else:
        output =  "Wassup! I am Cess-istant /n Thankyou for connecting with CESS /n We will get back to you soonest! /n Till then go check out CESS MANIA, its awesome"
    return output	
		
 
def log(msg):
    print msg
    sys.stdout.flush()	
	  
if __name__ == "__main__":
    app.run(debug=True, port =80)		
