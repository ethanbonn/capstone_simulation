FREECAD_PATH = "C:/Program Files/FreeCAD 0.19/bin/"
import sys
sys.path.append(FREECAD_PATH) 

import FreeCAD as App
import Part
import numpy as np
from scipy.integrate import solve_ivp
import Draft
import otsun

WAVELENGTH_IN_NANOMETERS = 10

doc = App.newDocument()


# It creates a mirror object.
class mirror():
    def __init__(self, x0=1, y0=1/2, x1=0.9, y1=1/2, x2=1, y2=7/16, width=1 ):
        self.x0, self.y0, self.x1, self.y1, self.x2, self.y2, self.width = x0, y0, x1, y1, x2, y2, width

        curve_a, curve_b = self.curve_solver()

        curveA = Draft.make_bspline([App.Vector(*p) for p in curve_a])
        curveB = Draft.make_bspline([App.Vector(*p) for p in curve_b])

        # doc.recompute()


        mirror = App.ActiveDocument.addObject('Surface::GeomFillSurface', 'Mirror')
        # mirror.Label = "Mirror #1"
        mirror.Label = "Mirror(Mir1)"
        mirror.BoundaryList = [(curveA, "Edge1"), (curveB, "Edge1")]

        self.obj = mirror

        App.ActiveDocument.recompute()




    def curve_solver(self):
        '''
        the solution will be a curved surface travelling from (0, self.y0, 0) to (self.x0, 0, width)
        '''

        # Calculate CPV cell length from coordiantes of the mirror endpoints

        L = np.sqrt((self.x2 - self.x1)**2 + (self.y2 - self.y1)**2)


        # In[7]:


        # Define ODE

        F = lambda x, y: - 1 / np.tan(np.pi/4 + 1/2 * np.arctan(((self.x0 * L - x * L) * self.y1 + x * L * self.y2 - self.x0 * L * y) / ((self.x0 * L - x * L) * self.x1 + x * L * self.x2 - self.x0 * L * x)))

        # Numerically solve the ODE corresponding to the 

        dt = 0.01

        t_eval = np.arange(0, 1, dt)
        sol = solve_ivp(F, [0, self.x0 - dt], [self.y0], t_eval=t_eval)

        # # make points 3D along Z-axis
        # l = []
        # for i in np.linspace(0, width, num_w_points):
        #     l.append(np.vstack((sol.t, sol.y[0], np.ones(len(sol.t)) * i)).T)

        # return np.array(l).reshape(-1, 3).tolist()
        # return np.vstack((sol.t, sol.y[0], np.zeros(len(sol.t)))).T.tolist(), np.vstack((sol.t, sol.y[0], np.ones(len(sol.t)) * self.width)).T.tolist()
        return np.vstack((sol.t, np.zeros(len(sol.t)), sol.y[0])).T.tolist(), np.vstack((sol.t, np.ones(len(sol.t)) * self.width, sol.y[0])).T.tolist()

    def getObj(self):
        return self.obj


class sillicon():
    def __init__(self, x1=0.9, y1=1/2, x2=1, y2=7/16, width=1) -> None:
        self.x1, self.y1, self.x2, self.y2, self.width = x1, y1, x2, y2, width
        
        line_a, line_b = self.compute_edges()

        lineA = Draft.make_bspline([App.Vector(*p) for p in line_a])
        lineB = Draft.make_bspline([App.Vector(*p) for p in line_b])

        App.ActiveDocument.recompute()

        semi = App.ActiveDocument.addObject('Surface::GeomFillSurface', 'Semi-Conductor')
        semi.Label = "Semi_Conductor(Mat2)"
        semi.BoundaryList = [(lineA, "Edge1"), (lineB, "Edge1")]

        self.obj = semi

        App.ActiveDocument.recompute()



    def compute_edges(self, num_sim_points=100):
        m = (self.y2 - self.y1) / (self.x2 - self.x1)
        b = self.y1 - (m*self.x1)
        # eq: y = mx + b
        x = np.linspace(self.x1, self.x2, num_sim_points)
        y = (m * x) + b

        # return np.vstack((x, y, np.zeros(num_sim_points))).T.tolist(), np.vstack((x, y, np.ones(num_sim_points) * self.width)).T.tolist()
        return np.vstack((x, np.zeros(num_sim_points), y)).T.tolist(), np.vstack((x, np.ones(num_sim_points) * self.width, y)).T.tolist()

    def getObj(self):
        return self.obj


Mirror = mirror(x0=1, y0=1/2, x1=0.9, y1=1/2, x2=1, y2=7/16, width=1 ).getObj()
Semi = sillicon(x1=0.9, y1=1/2, x2=1, y2=7/16, width=1).getObj()

print("boundbox:", Semi.Shape.BoundBox.DiagonalLength)

# print(Mirror.label, Semi.label)

# pass in an array of the free cad objects (i.e. the mirror and the silicon cell) to set up the scene
# Calculating the bounding box of the two objects.

test = Semi.Shape.BoundBox
test.add(Mirror.Shape.BoundBox)
print("full bb:", test, test.DiagonalLength)


# materials
otsun.ReflectorSpecularLayer("Mir1", 0.95)
otsun.AbsorberSimpleLayer("Mat2", 0.9)



test_scene = otsun.scene.Scene([  Mirror, Semi])
# test_scene = otsun.scene.Scene([Semi])

phi = 0.0
theta = 45.0
init_energy = 100

# establish the direction of the rays
emitting_region_mainDirection = [1.0, 0.0, 0.0]
main_direction = otsun.polar_to_cartesian(phi, theta) * -1.0  # Sun direction vector

# establish a rectangular window that the arrays will emanate from
# emitting_region = otsun.source.SunWindow(test_scene,  emitting_region_mainDirection)
emitting_region = otsun.source.SunWindow(test_scene,  main_direction)



light_spectrum = WAVELENGTH_IN_NANOMETERS

# establish a light source based on the scene, the emitting region, as well as the strength of the rays
light_source = otsun.source.LightSource(test_scene, emitting_region, light_spectrum, init_energy)

experiment = otsun.Experiment(test_scene, None, None)

experiment.run()
thermal_energy = experiment.captured_energy_Th
PV_energy = experiment.captured_energy_PV

print('\nThermal energy: ' + str(thermal_energy) + '\nPhotovoltaic energy: ' + str(PV_energy))