import math
class body:
    def __init__(self, mass, V, R, color = 'bo'):

        self.M = mass           # Mass of the object
        self.R_0 = R            # Coordinates
        self.V, self.V_0 = V , V             # Velocity
        self.R = R              # Coordinates
        self.color = color

    def Reset(self):
        self.V = self.V_0
        self.R = self.R_0

    def Update(self, force, time_step = 100):
        a = [f / self.M for f in force]
        for i in range (3):
            self.V[i] += a[i]*time_step
            self.R[i] += self.V[i]*time_step
    
    def Force(self, other):
        G = 6.67430 * 10 ** (-11)
        x = self.R[0] - other.R[0]
        y = self.R[1] - other.R[1]
        z = self.R[2] - other.R[2]
        r = math.sqrt(x ** 2 + y ** 2 + z ** 2)
        if(r == 0):
            return [0, 0, 0]
        force = - G * self.M * other.M/(r**2)
        return [force * x/r, force * y/r, force * z/r]
