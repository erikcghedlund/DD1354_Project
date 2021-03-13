import pygame
from pygame import display, draw, color, font

from simulation import Sim

class Screen:
    def __init__(self, sim:Sim, zoom:float, width:int, height:int, draw_ball:bool=True, draw_bat:bool=True, draw_arch_len:int=0, draw_collision:tuple=None, draw_ground:bool=False, write_cords:bool=False):
        pygame.init()
        self.sim = sim
        self.zoom = zoom
        self.canvas = display.set_mode(size=(width, height))
        self.actions = set()
        self.set_draw_bat(draw_bat)
        self.set_draw_ball(draw_ball)
        self.set_draw_arch(draw_arch_len)
        self.set_draw_ground(draw_ground)
        self.set_write_cords(write_cords)
        self.set_draw_collision(draw_collision)

    def __draw_body__(self, body):
        draw.circle(self.canvas, color.Color(0xff, 0xff, 0xff), (display.get_window_size()[0]/2+body.x*self.zoom*2, display.get_window_size()[1]/2-body.y*self.zoom*2), self.zoom)
    def __convert__(self, tup):
                    return (display.get_window_size()[0]/2+tup[0], display.get_window_size()[1]/2-tup[1])
    def __draw_arch__(self, step:int):
        for i in range(step,len(self.sim.original_arch), step*2):
            
            start_pos = self.__convert__(tuple(map(lambda x: x*self.zoom*2, self.sim.original_arch[i-step])))
            end_pos = self.__convert__(tuple(map(lambda x: x*self.zoom*2, self.sim.original_arch[i])))
            draw.line(self.canvas, color.Color(0xff, 0xff, 0xff), start_pos, end_pos, max(1,round(self.zoom/10)))
        
    def __draw_collision__(self):
        draw.line(self.canvas, color.Color(0xff, 0xff, 0xff), self.__convert__((self.sim.bat.x*self.zoom*2, self.sim.bat.y*self.zoom*2)), self.__convert__(self.collision_point), max(1,round(self.zoom/10)))

    def __draw_ground__(self):
        draw.line(self.canvas, color.Color(0xFF, 0xFF, 0xFF), (0, display.get_window_size()[1]/2),tuple(map((lambda x: x[0]/x[1]), (zip(display.get_window_size(), (1,2))))), round(self.zoom/4))

    def __write_cords__(self):
        style = font.Font('freesansbold.ttf', 16)
        text = style.render("Ball: {} {}\nBat: {} {}".format(*map(lambda x: str(round(x, 2)).ljust(10), (self.sim.ball.x, self.sim.ball.y, self.sim.bat.x, self.sim.bat.y))), True, color.Color(0xff, 0xff, 0xff), color.Color(0x00, 0x00, 0x00))
        text_rect = text.get_rect()
        self.canvas.blit(text, text_rect)

    def set_draw_ball(self, add:bool):
        [self.actions.discard,self.actions.add][int(add)](lambda: self.__draw_body__(self.sim.ball))
    def set_draw_bat(self, add:bool):
        [self.actions.discard,self.actions.add][int(add)](lambda: self.__draw_body__(self.sim.bat))
    def set_draw_arch(self, step:int):
        for i in range(10**5): #This is retarded, TODO:Fix
            try:
                self.actions.remove(lambda: self.__draw_arch__(i))
                break
            except KeyError:
                continue
        if step: self.actions.add((lambda: self.__draw_arch__(step)))
    def set_draw_collision(self, add:tuple):
        self.collision_point=tuple(map(lambda x: x*2*self.zoom, add))
        [self.actions.discard,self.actions.add][int(add is not None)](self.__draw_collision__)
    def set_draw_ground(self, add:bool):
        [self.actions.discard,self.actions.add][int(add)](self.__draw_ground__)
    def set_write_cords(self, add:bool):
        [self.actions.discard,self.actions.add][int(add)](self.__write_cords__)
    def update(self):
        self.canvas.fill(color.Color(0x00,0x00,0x00))
        for action in self.actions:
            action()
        display.update()
