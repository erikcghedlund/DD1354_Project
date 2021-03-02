from body import Ball, Bat
from simulation import Sim
from math import pi

def main():
    sim = Sim(1/6, Ball(5, 1, 1, -pi/4, 9.82, 250))
    sim.bat = Bat(15, -3, -3, 3, *sim.original_arch[15])
    for entry in sim.original_arch:
        print("{}, {}".format(*entry))

if __name__ == "__main__":
    main()