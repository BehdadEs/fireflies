from dotenv import load_dotenv
import os
from asyncio import get_event_loop


def stop():
    loop = get_event_loop()
    loop.stop()


def get_config() -> dict:

    load_dotenv()
    if os.environ.get("ENVIRONMENT") == "local":

        keys = ["DATABASE_URL"]
        for key in keys:
            if os.environ.get(key) is None:
                raise ValueError(f"{key} is not set.")

        config = {
            "db_url": os.getenv("DATABASE_URL"),
        }
        return config
    elif os.environ.get("ENVIRONMENT") == "production":
        config = {
            "db_url": os.getenv("DATABASE_URL"),
        }
        return config
    else:
        raise ValueError("env is not set")


CONFIG = get_config()
