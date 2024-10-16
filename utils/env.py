import os
from dotenv import load_dotenv, set_key, find_dotenv


class Env:
    """
    A utility class for managing environment variables.

    Methods:
    - get(key): Retrieves the value of the specified environment variable.
    - set(key, value): Sets the value of the specified environment variable.
    - unset(key): Removes the specified environment variable.
    - has(key): Checks if the specified environment variable exists.
    
    Properties:
    - base_path: Returns the base path of the current file.
    - all: Returns a dictionary containing all environment variables.
    """

    @classmethod
    @property
    def base_path(cls):
        return "\\".join(os.path.dirname(__file__).split("\\")[0:-1])

    @staticmethod
    def get(key) -> str:
        return os.environ.get(key)

    def set(key, value):
        os.environ[key] = value
        set_key(find_dotenv(), key, value)

    def unset(key):
        del os.environ[key]

    @classmethod
    @property
    def all(cls) -> dict:
        return os.environ

    @staticmethod
    def has(key) -> bool:
        return key in os.environ
