from typing import List,T
from .structure import File,Dire
from .accessor import file_reader,file_writer
from .formats import read_string, write_string
import os

ENVPATH = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))