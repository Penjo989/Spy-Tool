import os
import sys


class Shell:
    def __init__(self, outputFile = "shellOutput.txt"):
        self.outputFile = outputFile
        self.tmuxWindowName = "shell"
        self.setup()

    def setup(self):
        try:
            print("Setting up Shell...")
            f = open(self.outputFile, "w")
            f.close()

            os.system('tmux kill-server')
            os.system(f'sudo tmux new -d -s {self.tmuxWindowName}')
            os.system(f'sudo tmux send-keys -t {self.tmuxWindowName} "script -a -q -f {self.outputFile}" ENTER')
        except Exception as e:
            print(e)
            sys.exit(1)

    def shutDown(self):
        try:
            os.system('tmux kill-server')
        except Exception as e:
            print(e)
            sys.exit(1)

    def enterCommand(self, command):
        try:
            os.system(f'sudo tmux send-keys -t shell "{command}" ENTER')
        except Exception as e:
            print(e)
            sys.exit(1)

    def getShellOutput(self):
        try:
            fullMsg = ""
            f = open(self.outputFile, "r")
            lines = f.readlines()
            for line in lines[5:]:
                fullMsg += line
            f.close()
            return fullMsg
        except Exception as e:
            print(e)
            sys.exit(1)

