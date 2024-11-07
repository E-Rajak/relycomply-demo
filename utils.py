import base64
import hashlib
from enum import Enum
from typing import IO


def encode_image_to_base64(image: IO[bytes]) -> str:
    return base64.b64encode(image.read()).decode('utf-8')


def generate_hash(first_name: str, id_number: str) -> str:
    string_to_hash = first_name + id_number
    return hashlib.md5(string_to_hash.encode()).hexdigest()


def match_input_for_enum(input: str, enum_class: Enum) -> str:
    return next((member.name for member in enum_class if member.value == input), None)
