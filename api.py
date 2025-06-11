# =======================================================
#
#  Created by anele on 10/06/2025
#
#  @anele_ace
#
# =======================================================


from flask import Flask
from flask_restx import Api
from events import get_web_tickets_events

app = Flask(__name__)


@app.route('/')
def home():
    return "<h1>Hello, World!</h1>"


@app.get("/api/events")
def read_event():
    # itemid = "1184163"
    itemid = "1529499628"
    web_tickets_events = get_web_tickets_events(itemid=itemid)
    return {
        "web_tickets": web_tickets_events,
    }


if __name__ == '__main__':
    app.run(debug=True)
