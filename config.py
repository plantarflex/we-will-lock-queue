import sys
import os
from dotenv import load_dotenv
from pathlib import Path
from datetime import timedelta, datetime


basedir = os.path.dirname(os.path.abspath(__file__))
env_path = Path(os.path.join(basedir, "..")) / '.env'
load_dotenv(dotenv_path=env_path)


class Config:
    SOCKET_MASTER_NAME = os.environ['SOCKET_MASTER_NAME']
    SOCKET_MASTER_PORT = int(os.environ['SOCKET_MASTER_PORT'])

