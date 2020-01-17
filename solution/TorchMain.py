# bin/sh/python3
""" This Module contains the server and main class of our informaticup 2020 project.
    Agent Type is a Q-Learning-Agent.
"""
import argparse
import json
import logging
import logging.config
import time

from flask import (Flask, Blueprint, render_template)
from flask_cors import CORS
from flask import request

import common.data_processing.utils
from common.d3t_agent.TorchAgent import TorchAgent
from common.data_processing.state_extractor import GameState

app = Flask(__name__)  # pylint: disable=C0103
# This makes AJAX to work properly
CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

bp = Blueprint('map', __name__, url_prefix='/map')

# Disable flask default logging
log = logging.getLogger('werkzeug')
log.disabled = True

arg_parser = argparse.ArgumentParser(
    description="Twin (Delayed) Deep Deterministic Policy Gradient Actor to play Pandemie using PyTorch. "
                "This program is to be handed in at the 'Gesellschaft für Informatik' InformatiCup 2020. "
                "Developed at University of Oldenburg."
)

arg_parser.add_argument("-l", "--logging",
                        help="Generates a csv of counter,win/loss,round.",
                        action="store_true")

arg_parser.add_argument("-p", "--port",
                        help="Sets port.",
                        action="store",
                        )
arg_parser.add_argument("-vi", "--visualisation",
                        help="Generates visualisations if set.",
                        action="store_true")
startup_args = arg_parser.parse_args()
visuals = startup_args.visualisation

# Loading agent
agent: TorchAgent = TorchAgent()
model_dir = "pytorch_models"
dirs = f"./{model_dir}"
agent.load(dirs)
print("Loaded max")
# Loading Logger
csv_logger = startup_args.logging
game_counter = 0

@app.route('/', methods=['GET', 'POST'])
def process_request():
    """This function provides the server for our project. Also main class.
    When we get the Game.json receive over 'POST' we get am instance of class state.
    In this class we parse the json in a structure we need for the neuronal network and further processing.
    We check every round if we win or loss the game. In case the game is over we train the neuronal network.
    Deterministic tells if the agent should always take the greedy function, or explore further.
    Training tells if the agent should learn after playing a game.
    """
    global agent, game_counter, visuals  # pylint: disable=C0103, global-statement

    logging.basicConfig(filename='example.log', level=logging.DEBUG)

    game = request
    reward = 0
    response_ = {"type": "endRound"}

    if game.method == 'POST':

        state = GameState(request.json)
        if visuals:
            global game_json
            game_json = game.json
            time.sleep(2)
        rounds = game.json["round"]

        if state.move_done() or "error" in game.json.keys():
            if "error" in game.json.keys():
                logging.error("Error in json. Ending Round %s" % state.get_errors())
            return {"type": "endRound"}

        logging.info("Round: %s" % rounds)

        if game.json['outcome'] == 'pending':
            response_ = agent.act(state)
        else:
            game_counter = game_counter + 1
            print(f"Spiel: {game_counter} ist vorbei - Runden: {game.json['round']} - Status: {game.json['outcome']}")
            if game.json['outcome'] == 'loss':
                reward = -1500 / rounds
                logging.info("Loss: %s" % reward)

            elif game.json['outcome'] == 'win':
                reward = 1500 / rounds
                logging.info("Win: %s" % reward)

                logging.info("Reward would have been: %s" % reward)

            if csv_logger:
                with open("log.csv", "a+") as f:
                    f.write(f"{game_counter},{game.json['outcome']},{rounds},{reward}\n")

        if game.json['outcome'] == 'pending':
            if isinstance(response_, list):
                choice_counter = 0
                while common.data_processing.utils.valid_response(json.loads(response_[choice_counter][0]), game.json):
                    choice_counter += 1
                return response_[choice_counter][0]
        else:
            logging.info("====================")
            return "end"


@app.route('/get_game_json', methods=['GET'])
def get_game_json():
    return json.dumps(game_json)


@app.route('/map', methods=['GET'])
def get_map():
    return render_template('map.html')


if __name__ == '__main__':
    app.register_blueprint(bp)
    app.run(debug=False, host='0.0.0.0', port=startup_args.port if startup_args.port else 50123, threaded=True)
