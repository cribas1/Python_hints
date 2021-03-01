import pdb

class Robot:
    def __init__(self, name, color, weight):
        self.name = name
        self.color = color
        self.weight = weight
    def introduce(self):
        print("My name is "+ self.name)
    def tell_weight(self):
        print("I weight "+ str(self.weight)+" Kg")

r1 = Robot("Tom","red",30)
pdb.set_trace()
r1.tell_weight()

