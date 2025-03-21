from dataclasses import dataclass, asdict
from datetime import datetime

@dataclass
class UserPreferences:
    timezone: str

@dataclass
class User:
    username: str
    password: str
    roles: list
    preferences: UserPreferences
    active: bool
    created_ts: float

    def to_dict(self):
        # Converte a dataclass para dict de forma que fique adequada para o MongoDB
        data = asdict(self)
        # Converter o objeto UserPreferences para dict
        data["preferences"] = asdict(self.preferences)
        return data