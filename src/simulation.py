from math import sqrt
from copy import deepcopy
from body import Ball, Bat

class Sim:

    def __init__(self, timestep, ball:Ball, bat:Bat):
        self.ball = ball
        self.bat = bat
        self.timestep = timestep
        self.original_arch = self.__original_arch__()
        self.elasticity = 0.95

    def turn_init(self, cp_index):
        # Init bat
        self.bat.set_angle(*self.original_arch[cp_index]) 
        localbat = deepcopy(self.bat)
        old = (self.bat.x, self.bat.y)
        iterations = 0
        localbat.accelerate(self.timestep)
        localbat.move(self.timestep)
        def distance_from_collisionpoint(point):
            return sqrt((point[0]-self.original_arch[cp_index][0])**2 + (point[1]-self.original_arch[cp_index][1])**2)
        while distance_from_collisionpoint(next := (localbat.x, localbat.y)) < distance_from_collisionpoint(old): # Run until we have found collision point by checking for sign-change
            localbat.accelerate(self.timestep)
            localbat.move(self.timestep)
            old = next
            iterations += 1
        if iterations > cp_index:
            raise ValueError("Bat can't reach this point if starting at the same time or later as ball")
        self.bat_start_travel_timepoint = cp_index-iterations

        # Init state-trackers
        self.state_index = 0
        self.turn_index = 0
        self.collision_point = cp_index
        
        

    def turn(self):
        def bat_deacceleration_check():
            old_vx = abs(self.bat.vx) # Not must efficient way to do it, but it just works
            for i in range(2):
                self.bat.accelerate()
                self.bat.acceleration *= -1
                if not i: new_vx = abs(self.bat.vx) # Only write first time
            return old_vx < new_vx

        states = [self.__ball_moving__, self.__both_moving__, self.__collide__, self.__both_moving__, self.__ball_moving__, self.__bounce__]
        exit_conditions = [lambda: (self.turn_index >= self.bat_start_travel_timepoint), lambda:  (self.turn_index >= self.collision_point), lambda: True, bat_deacceleration_check, lambda: self.ball.y < 0, lambda: True]
        states[self.state_index]()
        self.turn_index += 1
        self.state_index += int(exit_conditions[self.state_index]())
        return len(exit_conditions) <= self.state_index



    # Where only moving ball
    def __ball_moving__(self):
        self.ball.air_resistance(self.timestep)
        self.ball.apply_gravity(self.timestep)
        self.ball.move(self.timestep)

    # Ball and bat moving
    def __both_moving__(self):
        self.__ball_moving__()
        self.bat.accelerate(self.timestep)
        self.bat.move(self.timestep)

    # Post collision
    def __post_collision__(self):
        pass

    def __collide__(self):
        ball_force = self.ball.mass*self.ball.vx*self.elasticity, self.ball.mass*self.ball.vy*self.elasticity
        bat_force = self.bat.mass*self.bat.vx*self.elasticity, self.bat.mass*self.bat.vy*self.elasticity
        self.bat.apply_force(*tuple(map(lambda x: x/self.bat.mass, ball_force))) #Action
        self.ball.apply_force(*tuple(map(lambda x: x/self.ball.mass, bat_force)))
        self.ball.apply_force(*tuple(map(lambda x: -x/self.ball.mass, ball_force))) #Reaction
        self.bat.apply_force(*tuple(map(lambda x: -x/self.bat.mass, bat_force)))
        self.bat.set_angle(self.bat.x - self.bat.vx, self.bat.y - self.bat.vy)

    def __bounce__(self):
        self.ball.vy *= -self.elasticity
        if round(self.ball.vy, 2) > 0.0: # Can't really justify this constant
            self.state_index -= 2 # This is a fucking dirty hack
    
    def __original_arch__(self):
        #prepare
        lst = []
        temp_velx = self.ball.vx
        temp_vely = self.ball.vy
        #simulate
        while self.ball.y>0:
            lst.append((self.ball.x, self.ball.y))
            self.__ball_moving__()
        #reset
        self.ball.x = lst[0][0]
        self.ball.y = lst[0][1]
        self.ball.vx = temp_velx
        self.ball.vy = temp_vely
        return lst

            