from abc import ABC, abstractmethod

class Input(ABC):
    def __init__(self, val):
        super().__init__()
        self.value = val

    def __get_val(self):
        return self.value
    
    def __set_val(self, value):
        self.value = value

class InputBool(Input):
    name = "Boolean Input"

class InputText(Input):
    name = "Text Input"

class InputInt(Input):
    name = "Int Input"

class InputImage(Input):
    name = "Image Input"

class InputFloat(Input):
    name = "Float Input"

class InputSelection(Input):
    name = "Selection Input"
