from dotenv import load_dotenv
import os
from asyncio import get_event_loop


def stop():
    loop = get_event_loop()
    loop.stop()


def get_config() -> dict:
    if os.environ.get("ENVIRONMENT") == "production":
        host = os.getenv("HOST")
        user = os.getenv("USER")
        password = os.getenv("PASSWORD")
        db_name = os.getenv("DATABASE_NAME")
        config = {
            "db_url": f"postgresql://{user}:{password}@{host}/{db_name}",
        }
        return config
    elif os.environ.get("ENVIRONMENT", "local") == "local":
        load_dotenv()
        keys = ["DATABASE_URL"]
        for key in keys:
            if os.environ.get(key) is None:
                raise ValueError(f"{key} is not set.")

        config = {
            "db_url": os.getenv("DATABASE_URL"),
        }
        return config
    else:
        raise ValueError("env is not set")


CONFIG = get_config()
