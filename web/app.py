from flask import Flask, render_template, request, jsonify
from datetime import datetime, date
import json, os, time, sys, threading, signal

dir_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(dir_path)

app = Flask(__name__)

def shutdown_server():
    time.sleep(5)
    print("Shutting down...")
    os.kill(os.getpid(), signal.SIGINT)

@app.route('/')
def index():
    with open(r'web\data.json', 'r', encoding="utf-8") as file:
        data = json.load(file)

    # Sort events by date
    data['events'].sort(key=lambda x: datetime.strptime(x['date'], '%d.%m.%Y'))

    non_world = [x.split(" : ")[2] for x in open("DailyStatusInfo.txt", "r", encoding="utf-8").read().split("\n")]
    print(non_world)
    # Calculate the number of days until each event
    for event in data['events']:
        event_date = datetime.strptime(event['date'], '%d.%m.%Y').date()
        today = date.today()
        event['days_until'] = min((event_date - today).days, 11)
        event["is_birthday"] = str("har bursdag" in event["name"])
        event["is_self_event"] = event["name"] in non_world

    return render_template('index.html', data=data)

@app.after_request
def add_header(response):
    response.headers['Cache-Control'] = 'no-store, must-revalidate'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response

if __name__ == '__main__':
    threading.Thread(target=shutdown_server).start()
    app.run(debug=False, port=1290)