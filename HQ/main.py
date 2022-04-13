from gui.Screen import  Screen
from network.Network import Network


def main():
    n = Network()

    s = Screen(1280, 720, "Head-Quarters", n)
    s.display()


if __name__ == "__main__":
    main()
