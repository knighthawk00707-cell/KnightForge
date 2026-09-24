import json
from pathlib import Path


class ProfileController:

    PROFILE_DIR = Path("profiles")

    @classmethod
    def list_profiles(cls):
        return sorted(
            p.stem for p in cls.PROFILE_DIR.glob("*.json")
        )

    @classmethod
    def load_profile(cls, name):

        file = cls.PROFILE_DIR / f"{name}.json"

        with open(file, "r", encoding="utf-8") as f:
            return json.load(f)