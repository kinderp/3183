from abc import ABC

class View(ABC):

    def __init__(self, child):
        self.child = child
        self.model = child.model
        self.fields = child.fields

    def render(self):
        objects = []
        for elem in dir(self.model):
            if elem in self.fields:
                print(elem)
                cuurent_field = getattr(self.model,elem)
                objects.insert(0,cuurent_field.render())

