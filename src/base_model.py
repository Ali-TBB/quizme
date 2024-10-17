import json

import google.generativeai as genai

from models.attachment import Attachment
from models.dataset import Dataset
from models.dataset_item import DatasetItem
from utils.env import Env


def create_model(mim_type, model_type, data_type, **kwargs):
    """
    Creates and configures the generative model.

    Args:
        mim_type (str): The MIME type of the response.
        model_type (str): The type of the generative model.

    Returns:
        genai.GenerativeModel: The configured generative model.
    """
    # Configure the model with the API key
    genai.configure(api_key=Env.get("API_KEY"))

    generation_config = {
        "temperature": 1,
        "top_p": 1,
        "top_k": 1,
        "max_output_tokens": 2048,
        "response_mime_type": mim_type,
        "response_schema": data_type,
    }
    safety_settings = [
        {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
        {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
        {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
        {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"},
    ]

    model = genai.GenerativeModel(
        model_name=model_type,
        generation_config=generation_config,
        safety_settings=safety_settings,
        **kwargs,
    )

    return model


class BaseModel:
    """
    Represents a base model for executing commands and managing chat history.

    Attributes:
        model (genai.GenerativeModel): The generative model to use.
        convo (genai.Conversation): The conversation object for chat history.
    """

    data_type = None

    backup_name: str = None

    def __init__(self, dataset: Dataset):
        """
        Initializes a new instance of the BaseModel class.

        Args:
            dataset (Dataset): The dataset used for training the model.
        """
        self.dataset = dataset
        self.create_model()

    @property
    def backup(self) -> Dataset:
        """
        Backs up the chat history.
        """
        if self.backup_name:
            return Dataset.findWhere("`name` = ?", (self.backup_name,))

    def create_model(self):
        self.model = create_model(
            "application/json", "gemini-1.5-pro-002", self.data_type
        )

        history = []
        backup_dataset = self.backup
        # all_items = (
        #     backup_dataset.all_items if backup_dataset else []
        # ) + self.dataset.all_items
        all_items = backup_dataset.all_items if backup_dataset else []

        for dataset_item in all_items:
            history_item = {
                "role": dataset_item.role,
                "parts": dataset_item.parts,
            }

            i = 0
            for part in dataset_item.parts:
                if part.startswith("<-attachment->: "):
                    attachment_id = int(part.split("<-attachment->: ")[-1].strip())
                    attachment: Attachment = Attachment.find(attachment_id)
                    if attachment:
                        history_item["parts"][i] = attachment.url
                i += 1

            history.append(history_item)

        self.convo = self.model.start_chat(history=history)

    def update_history(self, input_msg, output_msg, attachments: list[Attachment] = []):
        """
        Updates the chat history with the input and output messages.

        Args:
            input_msg (str): The input message.
            output_msg (str): The output message.
            path (str): The path associated with the message.
            type (str): The type of the message.
        """

        inputParts = [input_msg]
        for attachment in attachments:
            inputParts.append(f"<-attachment->: {attachment.id}")

        datasets_ids = [str(self.dataset.id)]
        if self.backup:
            datasets_ids.append(str(self.backup.id))

        exists = (
            DatasetItem.findWhere(
                f"`parts` = ? AND dataset_id IN ({', '.join([str(id) for id in datasets_ids])})",
                (json.dumps(inputParts),),
            )
            != None
        )

        if not exists:
            self.dataset.addItem("user", inputParts)

            self.dataset.addItem("model", [output_msg])

    def send_message(self, input_msg, attachments: list[Attachment] = []):
        if attachments:
            self.convo.send_message(
                [input_msg] + [attachment.url for attachment in attachments]
            )
        else:
            self.convo.send_message(input_msg)

        return self.convo.last.text
