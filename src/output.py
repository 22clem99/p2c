from abc import ABC, abstractmethod

class Output(ABC):
    def __init__(self, val):
        super().__init__()
        self.value = None

    def __get_val(self):
        return self.value
    
    def __set_val(self, value):
        self.value = value

class OutputBool(Output):
    name = "Boolean Output"

class OutputText(Output):
    name = "Text Output"

class OutputInt(Output):
    name = "Int Output"

class OutputImage(Output):
    name = "Image Output"

class OutputFloat(Output):
    name = "Float Output"

class OutputSelection(Output):
    name = "Selection Output"
