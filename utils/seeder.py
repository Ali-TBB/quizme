import os
import json


from utils import list_dir
from utils.collection import Collection
from utils.env import Env
from models.quizzes import Quizzes
from models.questions import Questions
from models.options import Options
from models.attachment import Attachment
from models.dataset import Dataset 
from models.dataset_item import DatasetItem

tables: dict[str, Collection] = {
    "datasets": Dataset,
    "dataset_items": DatasetItem,
    "quizzes": Quizzes,
    "questions": Questions,
    "options": Options,
    "attachments": Attachment,
}

def seed():
    [table.truncate() for table in tables.values()]

    path = os.path.join(Env.base_path, "database/seeders")
    pathFiles = list_dir(path, only_files=True)

    for filePath in pathFiles:
        if filePath.endswith(".json"):
            content = open(filePath, "r").read()
            seeder = json.loads(content)
            if not ("table" in seeder or "items" in seeder):
                raise Exception("Invalid seeder, missing table or items key")
            elif not seeder["table"] in tables:
                raise Exception(
                    f"Invalid table, table '{seeder['table']}' doesn't exists"
                )
            for item in seeder["items"]:
                collector = tables[seeder["table"]]
                collector.create(**item)
