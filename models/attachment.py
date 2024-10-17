import os
import google.generativeai as genai

from utils.collection import Collection
from utils.storage import get_storage


class Attachment(Collection):

    table = "attachments"

    def __init__(self, id, mime_type, path, created_at=None, updated_at=None):
        super().__init__(
            {
                "id": id,
                "mime_type": mime_type,
                "path": path,
                "created_at": created_at,
                "updated_at": updated_at,
            },
        )

    @property
    def mime_type(self) -> str:
        return self.get("mime_type")

    @mime_type.setter
    def mime_type(self, value):
        self.set("mime_type", value)

    @property
    def path(self) -> str:
        return self.get("path")

    @path.setter
    def path(self, value):
        self.set("path", value)

    __url: str = None

    @property
    def url(self) -> str:
        if not self.__url:
            self.__url = genai.upload_file(
                self.path, mime_type=self.mime_type
            )
        return self.__url
