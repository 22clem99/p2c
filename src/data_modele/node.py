from abc import ABC, abstractmethod
from enum import Enum, auto

class Node(ABC):
    def __init__(self, inputs, outputs):
        super().__init__()
        self.inputs = inputs
        self.outputs = outputs

    @abstractmethod
    def update_node_data(self):
        ...
