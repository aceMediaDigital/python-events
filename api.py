# =======================================================
#
#  Created by anele on 10/06/2025
#
#  @anele_ace
#
# =======================================================


from flask import Flask
from events import get_web_tickets_events

app = Flask(__name__)


@app.route('/')
def home():
    return "<p>Hello, World!</p>"


@app.get("/api/events")
def read_event():
    web_tickets_events = get_web_tickets_events()
    # howler_events = get_howler_music_events_sync()
    return {
        "web_tickets": web_tickets_events,
        "howler": []
    }


if __name__ == '__main__':
    app.run(debug=False)
