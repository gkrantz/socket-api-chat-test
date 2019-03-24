import socket
import sys
import threading
import json
from api import APIServer

server = APIServer(('localhost', 10000), ('localhost', 5000))