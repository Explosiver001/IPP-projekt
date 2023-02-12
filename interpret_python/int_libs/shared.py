
class Token:
    def __init__(self, identif, type, data_type, data):
        self.identif = identif
        self.type = type
        self.data_type = data_type
        self.data = data
    
    def changeDataType(self, data_type):
        self.data_type = data_type
        
    def changeData(self, data):
        self.data = data
