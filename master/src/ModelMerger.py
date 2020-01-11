import io
import sqlite3
from copy import deepcopy
from threading import Thread
from time import sleep

import torch
from torch import nn

from common.d3t_agent import TorchAgent
from common.d3t_agent.Actor import Actor
from common.d3t_agent.Critic import Critic
from common.data_processing import state_actions

sql_select_models = """SELECT model FROM models WHERE model_type LIKE ?;"""
sql_replace_max_model = """REPLACE INTO max_model VALUES (?,?);"""
sql_get_model_count_indicator = """SELECT model_type FROM models;"""
sql_delete_models = """DELETE FROM models;"""


class ModelMerger(Thread):
    """
    Merges all recieved models to one single reference model.
    """

    def __init__(self, database, model_classes, model_types):
        Thread.__init__(self)
        self.database = database
        self.model_classes = model_classes
        self.model_types = model_types

    def run(self) -> None:
        """
        Run method for multi threading.
        Updates the models all 20 minutes if update was successful. Otherwise updates all 2 Minutes.
        :return: None
        """
        while True:
            successful_update = self.update()
            if successful_update:
                # update each 30 min if models were merged
                print("Update successful")
                sleep(60 * 20)
            else:
                # try updating again after 2 min
                print("Update not successful")
                sleep(60 * 2)

    def update(self) -> bool:
        """ merges models in sqlite db
        Merges models in SQLite3 db if enough models were available.

        :return: weather or not it was possible to merge models
        """
        try:
            print("Updating models")
            conn = sqlite3.connect(self.database, timeout=10)
            c = conn.cursor()
            conn.commit()
            for type_name in self.model_types:
                c.execute(sql_select_models, [type_name])
                models = c.fetchall()
                if len(models) < 1:
                    conn.rollback()
                    return False
                merged_model = self.merge(models, type_name)
                buffer = io.BytesIO()
                torch.save({'state_dict': merged_model.state_dict()}, buffer)
                data = buffer.getvalue()
                c.execute(sql_replace_max_model, [type_name, data])
            conn.commit()
            c.execute(sql_delete_models)
            conn.close()
            return True
        except Exception:
            print("Error during updating")
            raise Exception

    def get_model(self, model_type: str, ) -> nn.Module:
        """
        Creates a neural network of given type.

        :param model_type: Network type .
        :param input_size: Input size of NN.
        :param output_size: Output size of NN.
        :param max_activation: Maximum activation of NN.
        :return: Neural network.
        """
        input_size = TorchAgent.INPUT_SIZE
        output_size = state_actions.get_number_of_actions()

        if model_type == "actor" or model_type == "actor_target":
            model = Actor(input_size, output_size)
        else:
            model = Critic(input_size, output_size)
        return model

    def merge_models(self, model_list: list, model_type: str, ):
        """
        Merges multiple model weights into one.

        :param model_list: List of multiple models.
        :param model_type: Type of recieved models.
        :param output_size: Output size of NN.
        :param max_activation: Maximum activation of NN.
        :return: Neural network.
        """
        beta = 1 / len(model_list)  # The interpolation parameter
        params = model_list[0].named_parameters()
        dict_params = deepcopy(dict(params))

        for name1, param1 in model_list[0].named_parameters():
            dict_params[name1].data.copy_(beta * param1.data)

        for model_ in model_list[1:]:
            params1 = model_.named_parameters()
            for name1, param1 in params1:
                if name1 in dict_params:
                    dict_params[name1].data += beta * param1.data

        # Creating and loading model
        model = self.get_model(model_type)
        model.load_state_dict(dict_params)
        return model

    def load_model(self, pth: bytearray, model_type):
        """
        Loads model weights from bytearray.

        :param pth: Bytearray containing a *.pth.tar file.
        :param model_type: Network type .
        :param input_size: Input size of NN.
        :param output_size: Output size of NN.
        :param max_activation: Maximum activation of NN.
        :return: Neural network.
        """
        model = self.get_model(model_type, )
        checkpoint = torch.load(io.BytesIO(pth[0]))["state_dict"]
        model.load_state_dict(checkpoint)
        return model

    def merge(self, models_bin: list, model_type) -> list:
        """
        Updates merge parameters for the models.

        :param models_bin: List of bytearrays containing *.pth.tar files.
        :param model_type: Type of model to load.
        :return: List with merged models.
        """
        loaded_models = []
        for bin_model in models_bin:
            loaded_models.append(self.load_model(bin_model, model_type))
        model_merged = self.merge_models(loaded_models, model_type)
        return model_merged
