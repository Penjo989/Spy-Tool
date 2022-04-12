from Communicator import *

class ProgramManager:
    def __init__(self, ip, port = 4096):
        self.communicator = Communicator(ip, port)

    def main(self):
        self.communicator.main()