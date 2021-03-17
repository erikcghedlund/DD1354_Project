from time import time
from sys import argv
from os.path import realpath
from json import load

import pygame
from pygame import event

from body import Ball, Bat
from simulation import Sim
from screen import Screen

class VisualSim:
    def __init__(self, sim:Sim, zoom:float=1.0, width:int=1920, height:int=1080):
        pygame.init()
        self.sim = sim
        self.zoom = zoom
        self.width = width
        self.height = height
        self.ready_to_run = False
    def slct_col(self, index:int):
        if not (0 <= index and index < len(self.sim.original_arch)):
            print("index must be between 0 and "+str(len(self.sim.original_arch)-1))
        else:
            try:
                self.sim.turn_init(index)
                self.screen = Screen(self.sim, self.zoom, self.width, self.height, True, True, max(round(1e-2/self.sim.timestep), 1), (0,0), True, True)
                self.ready_to_run = True
                self.screen.set_draw_collision(self.sim.original_arch[index])
            except ValueError as e:
                print(e)
                

    def run(self):
        startTime = time()
        frame_rate = 240
        last_frame = time()
        i = 0
        running = self.ready_to_run
        while running and not self.sim.turn():
            for ev in event.get():
                    if ev.type == pygame.QUIT: 
                        running = False
                        break
            while time() - startTime < self.sim.timestep*i:
                pass
            i += 1
            if time() - last_frame > frame_rate**-1: # Drawing frames are expensive, ok?
                self.screen.update()
                last_frame = time()
        if not self.ready_to_run:
            print("You must set collision point with slct_col()")

if __name__ == "__main__":
    if len(argv) >= 4:
        cached = load(open(realpath(__file__)[:-len("src/test_run.py")]+"stored.json", "r"))
        s = Sim(float(argv[1]), Ball(*cached["balls"][int(argv[2])].values()), Bat(*cached["bats"][int(argv[3])].values()))
        
    def print_collision_points(sim:Sim, steps:int=1):
        for i in range(0, len(sim.original_arch), steps): print("{}: {} {}".format(i, *sim.original_arch[i]))

    try:
        vs = VisualSim(s, *cached["visualsettings"][int(argv[4])].values())
    except IndexError:
        vs = VisualSim(s)
    try:
        vs.slct_col(int(argv[5]))
    except IndexError:
        print_collision_points(s, len(s.original_arch)//10)
        vs.slct_col(int(input("Collision point: ")))
    finally:
        vs.run()