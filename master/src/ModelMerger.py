import io
import sqlite3
import torch

from copy import deepcopy
from threading import Thread
from time import sleep

from common.d3t_agent.Actor import Actor
from common.d3t_agent.Critic import Critic

sql_select_models = """SELECT model FROM models WHERE model_class LIKE ? AND model_type LIKE ?;"""
sql_replace_max_model = """REPLACE INTO max_model VALUES (?,?,?);"""
sql_get_model_count_indicator = """SELECT model_class FROM models;"""
sql_delete_models = """DELETE FROM models;"""


class ModelMerger(Thread):

    def __init__(self, database, model_classes, model_types):
        Thread.__init__(self)
        self.database = database
        self.model_classes = model_classes
        self.model_types = model_types

    def run(self) -> None:
        while True:
            successful_update = self.update()
            if successful_update:
                # update each 30 min if models were merged
                sleep(60 * 30)
            else:
                # try updating again after 2 min
                sleep(60 * 2)

    def update(self) -> bool:
        """ merges models in sqlite db
        Merges models in SQLite3 db if enough models were available.

        :return: weather or not it was possible to merge models
        """
        print("Updating models")
        conn = sqlite3.connect(self.database, timeout=10)
        c = conn.cursor()
        conn.commit()
        for class_name in self.model_classes:
            for type_name in self.model_types:
                c.execute(sql_select_models, (class_name, type_name))
                models = c.fetchall()
                if len(models) < 1:
                    conn.rollback()
                    print("Updating models failed.")
                    return False
                merged_model = self.merge(models, class_name, type_name)
                buffer = io.BytesIO()
                torch.save({'state_dict': merged_model.state_dict()}, buffer)
                data = buffer.getvalue()
                c.execute(sql_replace_max_model, (class_name, type_name, data))
        conn.commit()
        c.execute(sql_delete_models)
        conn.close()
        print("Updating models successful.")
        return True

    def get_model(self, model_type, input_size, output_size, max_size):
        if model_type == "actor" or model_type == "actor_target":
            model = Actor(input_size, output_size, max_size)
        else:
            model = Critic(input_size, output_size)
        return model

    def merge_models(self, model_list: list, model_type, input_size, output_size, max_size):
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
        model = self.get_model(model_type, input_size, output_size, max_size)
        model.load_state_dict(dict_params)
        return model

    def load_model(self, pth: bytearray, model_type, input_size: int, output_size: int, max_size: int):
        model = self.get_model(model_type, input_size, output_size, max_size)
        checkpoint = torch.load(io.BytesIO(pth[0]))["state_dict"]
        model.load_state_dict(checkpoint)
        return model

    def merge(self, models_bin: list, model_class: str, model_type) -> list:
        if model_class == "city":
            input_size, output_size, max_size = 10, 9, 1
        elif model_class == "disease":
            input_size, output_size, max_size = 7, 2, 1
        loaded_models = []
        for bin_model in models_bin:
            loaded_models.append(self.load_model(bin_model, model_type, input_size, output_size, max_size))
        model_merged = self.merge_models(loaded_models, model_type, input_size, output_size, max_size)
        return model_merged
