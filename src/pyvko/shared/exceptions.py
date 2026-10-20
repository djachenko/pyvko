from dataclasses import dataclass


@dataclass
class MethodWasDeleted(Exception):
    method_name: str