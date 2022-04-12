from gui.Screen import  Screen
from network.Network import Network

n = Network()

s = Screen(1280, 720, "Head-Quarters", n)
s.display()