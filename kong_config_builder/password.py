import string
import random


class PasswordManager:
    @staticmethod
    def generate(size: int) -> str:
        password = f"{string.ascii_letters}{string.digits}"
        return "".join(random.choice(password) for i in range(int(size)))
