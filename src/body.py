from math import sin, cos, atan, pi

class Body:
    def __init__(self, mass, x, y, angle):
        self.mass = mass
        self.x = x
        self.y = y
        self.vx = 0
        self.vy = 0
        self.angle = angle

    def apply_force(self, x, y):
        self.vx += x
        self.vy += y

    def apply_force_angle(self, scalar, angle=None):
        if angle is None: # Cause you can't have self in default parameters
            angle = self.angle
        self.apply_force(cos(angle)*scalar, -sin(angle)*scalar)        

    def move(self, timestep=1):
        self.x += self.vx*timestep
        self.y += self.vy*timestep
            

class Ball(Body):
    def __init__(self, mass, x, y, angle, gravity, velocity):
        super().__init__(mass, x, y, angle)
        self.apply_force_angle(velocity, self.angle)
        self.gravity = gravity
    
    def apply_gravity(self, timestep=1):
        self.apply_force_angle(self.gravity, pi/2)

    def air_resistance(self):
        pass

class Bat(Body):
    def __init__(self, mass, x, y, acceleration, cx, cy):
        super().__init__(mass, x, y, atan((cx-x)/(cy-y)))
        self.acceleration = acceleration

    def accelerate(self, timestep=1):
        self.apply_force_angle(self.acceleration)

    def set_angle(self, cx, cy):
        atan((cx-self.x)/(cy-self.y))
