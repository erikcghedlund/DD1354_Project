from math import sin, cos, atan, pi

class Body:
    def __init__(self, mass, x, y, angle, alghoritm="euler"):
        self.mass = mass
        self.x = x
        self.y = y
        self.vx = 0
        self.vy = 0
        self.angle = angle
        if alghoritm=="euler":
            self.alghoritm = self.euler
        if alghoritm=="rk4":
            raise RuntimeError("Runge-Kutta4 not implemented (yet)!")

    def apply_force(self, x, y):
        self.vx += x
        self.vy += y

    def apply_force_angle(self, scalar, angle=None):
        if angle is None: # Cause you can't have self in default parameters
            angle = self.angle
        self.apply_force(cos(angle)*scalar, -sin(angle)*scalar)        

    def move(self, timestep=1):
        self.alghoritm(timestep)

    def euler(self, timestep):
        self.x += self.vx*timestep
        self.y += self.vy*timestep

    def runge_kutta4(self, timestep):
        def f(x, y):
            return y+timestep*x
        xf1 = timestep*f(self.vx,self.vx)
        xf2 = timestep*f(self.vx+timestep/2, self.x+xf1/2)
        xf3 = timestep*f(self.vx+timestep/2, self.x+xf2/2)
        xf4 = timestep*f(self.vx+timestep, self.x+xf3)
        self.x += 6**-1*(xf1+xf2+xf3+xf4)
        yf1 = timestep*f(self.vy,self.vy)
        yf2 = timestep*f(self.vy+timestep/2, self.y+yf1/2)
        yf3 = timestep*f(self.vy+timestep/2, self.y+yf2/2)
        yf4 = timestep*f(self.vy+timestep, self.y+yf3)
        self.y += 6**-1*(yf1+yf2+yf3+yf4)
            

            

class Ball(Body):
    def __init__(self, mass, x, y, angle, gravity, velocity, air_resistance=0, alghoritm="euler"):
        super().__init__(mass, x, y, angle, alghoritm)
        self.apply_force_angle(velocity, self.angle)
        self.gravity = gravity
        self.air_resistance_factor = air_resistance
    
    def apply_gravity(self, timestep=1):
        self.apply_force_angle(self.gravity*timestep, pi/2)

    def air_resistance(self, timestep=1):
        self.apply_force(-self.vx*self.air_resistance_factor*timestep, -self.vy*self.air_resistance_factor*timestep)

class Bat(Body):
    def __init__(self, mass, x, y, acceleration, alghoritm="euler", cx=0, cy=0):
        super().__init__(mass, x, y, 0, alghoritm)
        self.set_angle(cx, cy)
        self.acceleration = acceleration
    def __sign__(self, val):
        try:
            return val/abs(val)
        except ZeroDivisionError:
            return 0

    def accelerate(self, timestep=1):
        self.apply_force_angle(self.acceleration*timestep)

    def set_angle(self, cx, cy):
        try:
            self.angle = pi*int((cx-self.x)<0)-atan((cy-self.y)/(cx-self.x))
        except ZeroDivisionError:
            self.angle = -self.__sign__(cy-self.y)*(pi/2)
