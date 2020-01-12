# bin/sh/python3
""" This Module contains the server and main class of our informaticup 2020 project.
    Agent Type is a Q-Learning-Agent.
"""
import argparse
import gc
import io
import json
import logging
import logging.config
import os
import tarfile
import time

import requests
from flask import (Flask, Blueprint, render_template, request)
from flask_cors import CORS
from requests import post

from common.d3t_agent.TorchAgent import TorchAgent
from common.data_processing.state_extractor import GameState

app = Flask(__name__)  # pylint: disable=C0103
CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

bp = Blueprint('map', __name__, url_prefix='/map')

# Disable flask default logging
log = logging.getLogger('werkzeug')
log.disabled = True
agent: TorchAgent

arg_parser = argparse.ArgumentParser(
    description="Twin (Delayed) Deep Deterministic Policy Gradient Actor to play Pandemie using PyTorch. "
                "This program is to be handed in at the 'Gesellschaft für Informatik' InformatiCup 2020. "
                "Developed at University of Oldenburg."
)
arg_parser.add_argument("-nt", "--no_training",
                        help="Weather or not the agent should learn after playing a game.",
                        action="store_false")
arg_parser.add_argument("-l", "--logging",
                        help="Generates a csv of counter,win/loss,round.",
                        action="store_true")
arg_parser.add_argument("-vi", "--visualisation",
                        help="Generates visualisations if set.",
                        action="store_true")
arg_parser.add_argument("-p", "--port",
                        help="Sets port.",
                        action="store",
                        )
arg_parser.add_argument("-ip", "--ip_out",
                        help="Sets ip to send models to.",
                        action="store",
                        )


@app.route('/', methods=['GET', 'POST'])
def process_request():
    """This function provides the server for our project. Also main class.
    When we get the Game.json receive over 'POST' we get am instance of class state.
    In this class we parse the json in a structure we need for the neuronal network and further processing.
    We check every round if we win or loss the game. In case the game is over we train the neuronal network.
    Deterministic tells if the agent should always take the greedy function, or explore further.
    Training tells if the agent should learn after playing a game.
    """
    global agent, iteration_counter, game_counter, visuals  # pylint: disable=C0103, global-statement

    logging.basicConfig(filename='example.log', level=logging.DEBUG)

    game = request
    reward = 0

    if game.method == 'POST':

        state = GameState(game.json)
        if visuals:
            global game_json
            game_json = game.json
            time.sleep(2)
            # Visualization(game.json)
        rounds = game.json["round"]

        if state.move_done() or "error" in game.json.keys():
            if "error" in game.json.keys():
                logging.error("Error in json. Ending Round %s" % state.get_errors())
            return {"type": "endRound"}

        logging.info("Round: %s" % rounds)

        if game.json['outcome'] == 'pending':
            response_ = agent.act(state)
            return response_
        else:
            game_counter = game_counter + 1
            print(f"Spiel: {game_counter} ist vorbei - Runden: {game.json['round']} - Status: {game.json['outcome']}")
            if game.json['outcome'] == 'loss':
                reward = -1 / rounds
                logging.info("Loss: %s" % reward)

            elif game.json['outcome'] == 'win':
                reward = 1 / rounds
                logging.info("Win: %s" % reward)

            agent.update_reward(reward)
            logging.info("Reward: %s" % reward)

            if iteration_counter % 10 == 0:
                logging.info("Training Model")
                agent.train()
                logging.info("Model Trained")

            # Save all 10 iterations hours
            iteration_counter += 1
            if csv_logger:
                with open("log.csv", "a+") as f:
                    f.write(f"{iteration_counter},{game.json['outcome']},{rounds},{reward}\n")
            gc.collect()
            # TODO: ITERATIONEN!
            if iteration_counter % 30 == 0:
                logging.info("Saving Model")
                tar = agent.get_models_as_tar_bin()
                files = {'models': ("models.tar", tar, "multipart/form-data")}
                post(url=f"{target_ip}/models",
                     files=files,
                     headers={"Authorization": f"Basic {id_}", }
                     )
                logging.info("Model saved")
                logging.warning(f"Exiting after: {iteration_counter} iterations")

                os._exit(0)  # only way to avoid flasks auto-restart
            return "Over"


@app.route('/get_game_json', methods=['GET'])
def get_game_json():
    return json.dumps(game_json)


@app.route('/map', methods=['GET'])
def get_map():
    return render_template('map.html')


if __name__ == '__main__':
    global game_counter, iteration_counter

    startup_args = arg_parser.parse_args()
    training = startup_args.no_training
    visuals = startup_args.visualisation
    iteration_counter = 0

    target_ip = startup_args.ip_out if startup_args.ip_out else "http://0.0.0.0:8087"

    id_ = requests.get(url=f"{target_ip}/get-id").content

    # Loading agent
    agent = TorchAgent()
    agent.exploration_rate = float(requests
                                   .get(url=f"{target_ip}/get-exploration")
                                   .content
                                   )
    try:
        ref_models_stream = requests.get(url=f"{target_ip}/get-model").content
        bin_ref_models = io.BytesIO(ref_models_stream)
        models = tarfile.open(fileobj=bin_ref_models, mode="r")
        agent.load_bin(models)
    except Exception:
        raise

    # Loading Logger
    csv_logger = startup_args.logging

    game_counter = 0
    game_json = None
    app.run(debug=True, host='localhost', port=startup_args.port if startup_args.port else 50123, threaded=True)
    app.register_blueprint(bp)
    app.run(host='localhost', port=startup_args.port if startup_args.port else 5000, threaded=True)
