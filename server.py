
import yaml
with open("config.yaml", 'r') as ymlfile:
    cfg = yaml.safe_load(ymlfile)

MERGE_FOLDER = cfg["MERGE_FOLDER"]
MODEL_CLASSES = cfg["MODEL_CLASSES"]
MODEL_TYPES = cfg["MODEL_TYPES"]
DATABASE_PATH = cfg["DATABASE_PATH"]


from merger.ModelMerger import ModelMerger

if __name__ == "__main__":
    file_reciever = FileReciever()
    model_merger = ModelMerger(DATABASE_PATH, MODEL_CLASSES, MODEL_TYPES)
    model_merger.start()


