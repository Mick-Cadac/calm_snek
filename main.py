import logging
import os

from flask import Flask
from flask import request
from flask_cors import CORS

from move_process import move_it

app = Flask(__name__)
CORS(app)

@app.get("/")
def index():
  return {
      "apiversion": "1",
      "author": "Mick",  # TODO: Your Battlesnake Username
      "color": "#7F47C9",  # TODO: Personalize
      "head": "smile",  # TODO: Personalize
      "tail": "curled",  # TODO: Personalize
  }

@app.post("/start")
def start():
  return{"ok"}
  
@app.post("/move")
def move():
  data = request.get_json()
  print(f"BOARD: {data}")
  move = move_it(data)
  return{"move": move}
  
@app.post("/end")
def end():
  data = request.get_json()

  print(f"{data['game']['id']} END")
  return "ok"

if __name__ == "__main__":
    logging.getLogger("werkzeug").setLevel(logging.ERROR)

    print("Starting Calm Snek Server...")
    port = int(os.environ.get("PORT", "8080"))
    app.run(host="0.0.0.0", port=port, debug=True)