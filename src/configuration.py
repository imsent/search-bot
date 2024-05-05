"""This file represents configurations from files and environment."""
import logging
from dataclasses import dataclass
from environs import Env

env = Env()
env.read_env(".env")


@dataclass
class Configuration:
    """All in one configuration's class."""
    debug = bool(env('DEBUG',0))
    logging_level = int(env('LOGGING_LEVEL', logging.INFO))
    token: str = env('BOT_TOKEN')

    host: str = env('HOST')
    ps_user: str = env('POSTGRES_USER')
    ps_pass: str = env('POSTGRES_PASSWORD')
    ps_port: str = env('POSTGRES_PORT')
    ps_db: str = env('POSTGRES_DATABASE')
    ps_cname: str = env('POSTGRES_COLECCTION_NAME')


conf = Configuration()
