import os
import sys
import re
from typing import Dict, List
import dotenv
dotenv.load_dotenv()


def get_env(name: str) -> str:
    e = os.environ.get(name)
    if not e:
        print(f"Please set the environment variable {name}")
        exit(1)
    return e
