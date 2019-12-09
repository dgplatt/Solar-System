import numpy as np
from matplotlib import pyplot as plt
from matplotlib import animation
import Body

class Solar_System:
    def __init__(self, Bodies, total_time, dt, dt_skip):
        self.Bodies = Bodies                        # List of bodies in the solar system
        self.dt = dt                                # Time that acceleration is regarded as constant
        self.dt_skip = dt_skip                      # Number of dt to skip while graphing/animating
        self.frames = total_time//(dt*dt_skip)      # Total number of frames/points in graphing/animating
        self.fig, self.ax = plt.subplots()
        self.point, = plt.plot([],[],'ko')
        self.for_plot = [([0]*self.frames, [0]*self.frames, self.Bodies[i].color) for i in range(len(self.Bodies))]

    def Total_Force_On(self, Obj):  #Calculate the total force on an object
        total = [0, 0, 0]
        for other in self.Bodies:
            f = Obj.Force(other)
            for i in range(3):
                total[i] += f[i]
        return total

    def Reset_All(self):
        for Obj in self.Bodies:
            Obj.Reset()

    def Step(self):  # One step of size dt
        Forces = []
        for Obj in self.Bodies:
            Forces.append(self.Total_Force_On(Obj))
        for i in range(len(self.Bodies)):
            self.Bodies[i].Update(Forces[i], self.dt)
        

    def init(self):
        self.point.set_data([], [])
        return self.point,

    def animate(self, i):
        """perform animation step"""
        if(i < self.frames):
            self.point.set_data([Obj[0][i] for Obj in self.for_plot], [Obj[1][i]  for Obj in self.for_plot])
        return self.point,

    def Plot_x_y (self):
        plt.axis('equal')
        M_total = 0                          # Total Mass of Bodies for center of Mass Caculations
        for Obj in self.Bodies:
            M_total += Obj.M

        for j in range(self.frames):        # Coordianates of the points in each frame 
            print(j)
            x_cm = 0                        # Calculate Center of Mass 
            y_cm = 0
            for Obj in self.Bodies:
                x_cm += Obj.R[0]*Obj.M
                y_cm += Obj.R[1]*Obj.M
            x_cm = x_cm/M_total
            y_cm = y_cm/M_total
            for i in range(len(self.Bodies)):
                self.for_plot[i][0][j] = self.Bodies[i].R[0] - x_cm
                self.for_plot[i][1][j] = self.Bodies[i].R[1] - y_cm

            for i in range(self.dt_skip):   # Do dt_skip steps of size dt
                self.Step()
        # Plot the tragectories
        for i in range(len(self.Bodies)):
            self.ax.plot(self.for_plot[i][0],self.for_plot[i][1],self.for_plot[i][2])
        self.Reset_All()
        # Animation fuction
        anim = animation.FuncAnimation(self.fig, self.animate, init_func=self.init, frames=self.frames, interval=1)
        plt.show()

M_sun = 1.989 * 10 ** 30 #kg
M_earth = 5.972 * 10 ** 24 #kg
M_moon = 7.34767309 * 10**22 #kg

V_earth = 29788.6 #m/s 
V_moon = 1022 #m/s +/- V_earth

D_earth = 1.4959787 * 10 ** 11 #m
D_moon = 3.844 * 10 ** 8 #m +/- D_earth

t_year = 31540000 #s
t_day = 86400 #s

if __name__ == "__main__":
    Earth = Body.body(M_earth, [V_earth, 0.0, 0.0], [0.0, D_earth, 0.0], 'b')
    Moon = Body.body(M_moon, [V_earth + V_moon, 0.0, 0.0], [0.0, D_earth + D_moon, 0.0], 'r')

    Rogue_planet = Body.body(M_sun * (1/1000), [-26330, 0.0, 0.0], [5.9*10**12, 1*10**11, 0.0], 'g')
    Sun_1 = Body.body(M_sun, [0.0, 0.0, 0.0], [0.0, 0.0, 0.0], 'y')
    Sun_2 = Body.body(M_sun * 3, [8400, 0.0, 0.0], [0.0, 5*10**11, 0.0], 'k')

    #S = Solar_System([Sun_1, Earth, Rogue_planet , Moon], 10*t_year, 100, 100)
    #S = Solar_System([Sun_1, Earth, Sun_2 , Moon], 10*t_year, 100, 100)

    Star_1 = Body.body(M_sun * 4.0, [600, 2000, 0.0], [-2*10**13, 0.0, 0.0], 'b')
    Star_2 = Body.body(M_sun * 0.55, [2000, -1500, 0.0], [0.0, 10**13, 0.0], 'y')
    Star_3 = Body.body(M_sun * 2.5, [-1900, -2000, 0.0], [10**13, 0.0, 0.0], 'r')

    S = Solar_System([Star_1, Star_2, Star_3], 5000*t_year, 1000, 1000)

    S.Plot_x_y()