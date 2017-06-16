import requests
import pprint
from flask import Flask, request, jsonify

import json

app = Flask(__name__)
place_api="AIzaSyDT0P7r0ezcoeNvotC_J2AwviQnCCfj0Oo"


def location_data():
    type="police"

    r=requests.get("https://maps.googleapis.com/maps/api/place/search/json?location=31.6607795,74.8214579&rankby=distance&types=police&sensor=false&key="+place_api)
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
        print "********************************"
        d= {}
        d["name"]=item["name"]
        d["address"]=item["vicinity"]
        d["lat"]=item["geometry"]["location"]["lat"]
        d["lng"]=item["geometry"]["location"]["lng"]
        final_data["data"].append(d)
    return final_data

@app.route('/')
def data():
    return jsonify(location_data())
   

if __name__ == "__main__":
    app.run(debug=True, port =80)		




    
    








