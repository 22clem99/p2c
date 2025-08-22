from misc.graph import Graph
from fsm.FSMProjectManager import FSMProjectManager

import uuid

class P2CProject:
    def __init__(self, name):
        self.name = name
        self.graph = Graph()
        self.list_cmd = list()
        self.fsm = FSMProjectManager()
        self.uid = str(uuid.uuid4())[0:8]
