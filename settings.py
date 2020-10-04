import os

from dotenv import load_dotenv
load_dotenv(dotenv_path='.env')

HOST = os.getenv('HOST')
PORT = os.getenv('PORT')

TOKEN = os.getenv('TOKEN')

REPOSITORY = 'https://github.com/jallysson/Adam'