class Memory:
    def __init__(self):
        self.ins_start_addr = 0
        self.current_ins_addr = 0
        self.last_ins_addr = 511
        self.data_start_addr = 512
        self.current_data_addr = 512
        self.last_data_addr = 1024
        self.base_pointer = 512

    def occupyMemory(self, number):
        self.current_data_addr += number
        return self.current_data_addr
    
    def getLastInstructionAddress(self):
        return self.current_ins_addr
    
    def setInstructionAddress(self,number):
        self.current_ins_addr += number
        return self.current_ins_addr
    

    def checkIfWithinMemory(self,current_data_addr):
        return current_data_addr < self.last_data_addr 
        