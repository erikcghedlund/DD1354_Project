from math import sqrt
from body import Ball, Bat

class Sim:

    def __init__(self, timestep, ball:Ball, bat:Bat):
        self.ball = ball
        self.bat = bat
        self.timestep = timestep
        self.original_arch = self.__original_arch__()

    def turn_init(self, cp_index):
        # Init bat
        self.bat.set_angle(*self.original_arch[cp_index]) 
        localbat = self.bat
        pos_vector = [(localbat.x, localbat.y)]
        localbat.accelerate(self.timestep)
        localbat.move(self.timestep)
        pos_vector.append((localbat.x, localbat.y))
        def distance_from_collisionpoint(point):
            sqrt((point[0]-self.original_arch[cp_index][0])**2 + (point[1]-self.original_arch[cp_index][1])**2)
        while distance_from_collisionpoint(pos_vector[-1])>=0 == distance_from_collisionpoint(pos_vector[-2])>=0: # Run until we have found collision point by checking for sign-change
            localbat.accelerate(self.timestep)
            localbat.move(self.timestep)
            pos_vector.append((localbat.x, localbat.y))
        index = int(abs(distance_from_collisionpoint(pos_vector[-1])) >= abs(distance_from_collisionpoint(pos_vector[-2]))) # Get closest approximation
        self.bat_start_travel_timepoint = cp_index-len(pos_vector)-index

        # Init state-trackers
        self.state_index = 0
        self.turn_index = 0
        self.collision_point = cp_index
        
        

    def turn(self):
        states = [self.__ball_moving__, self.__bat_moving__, self.__post_collision__]
        exit_conditions = [(self.turn_index != self.bat_start_travel_timepoint), (self.turn_index != self.collision_point), self.ball.y < 0]
        states[self.state_index]()
        self.state_index += int(exit_conditions[self.state_index])
        return len(exit_conditions) < self.state_index



    # Where only moving ball
    def __ball_moving__(self):
        self.ball.air_resistance()
        self.ball.apply_gravity(self.timestep)
        self.ball.move(self.timestep)

    # Ball and bat moving
    def __bat_moving__(self):
        pass

    # Post collision
    def __post_collision__(self):
        pass

    def __collide__(self):
        pass
    
    def __original_arch__(self):
        lst = []
        while self.ball.y>0:
            lst.append((self.ball.x, self.ball.y))
            self.__ball_moving__()
        self.ball.x = lst[0][0] #reset
        self.ball.y = lst[0][1]
        return lst

            