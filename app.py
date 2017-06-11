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
	  
	  
def log(msg):
    print msg
    sys.stdout.flush()	
	  
if __name__ == "__main__":
    app.run(debug=True, port =80)		
