from misc.graph import Graph
from fsm.FSMProjectManager import FSMProjectManager

class P2CProject:
    def __init__(self, name):
        self.name = name
        self.graph = Graph()
        self.list_cmd = list()
        self.fsm = FSMProjectManager()
