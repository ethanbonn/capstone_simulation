FREECAD_PATH = "C:/Program Files/FreeCAD 0.19/bin/"
import sys
sys.path.append(FREECAD_PATH) 

import FreeCAD as App
import Part
import numpy as np
from scipy.integrate import solve_ivp
import Draft
<<<<<<< HEAD
from FreeCAD import Base
import otsun

WAVELENGTH_IN_NANOMETERS = 7
=======
import otsun

WAVELENGTH_IN_NANOMETERS = 10
>>>>>>> ed142a833625fc1faeb79fe1b4c4f2e6c9e86ef8

doc = App.newDocument()


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
<<<<<<< HEAD
    def __init__(self, x1=0.9, y1=1/2, x2=1, y2=7/16, width=1.0) -> None:
        thickness = 0.25
        self.x1, self.y1, self.x2, self.y2, self.width, self.thickness = x1, y1, x2, y2, width, thickness
        
        v1 = App.Vector(x1,0,y1)
        v2 = App.Vector(x2,0,y2)
        v3 = App.Vector(x1+thickness,0,y1+thickness)
        v4 = App.Vector(x2+thickness,0,y2+thickness)
        
        v5 = App.Vector(x1,width,y1)
        v6 = App.Vector(x2,width,y2)
        v7 = App.Vector(x1+thickness,width,y1+thickness)
        v8 = App.Vector(x2+thickness,width,y2+thickness)
        
        f1 = self.make_face(v1,v2,v4,v3)
        f2 = self.make_face(v5,v6,v8,v7)
        f3 = self.make_face(v1,v3,v7,v5)
        f4 = self.make_face(v2,v4,v8,v6)
        f5 = self.make_face(v1,v5,v6,v2)
        f6 = self.make_face(v3,v7,v8,v4)
        semi.BoundBox = BoundBox()
        shell=Part.makeShell([f1,f2,f3,f4,f5,f6])
        solid=Part.makeSolid(shell)
        self.Shape = solid

        #line_a, line_b = self.compute_edges()

        #lineA = Draft.make_bspline([App.Vector(*p) for p in line_a])
        #lineB = Draft.make_bspline([App.Vector(*p) for p in line_b])

        App.ActiveDocument.recompute()

        semi = App.ActiveDocument.addObject('PartDesign::FeaturePython', 'Semi-Conductor')
        #semi = App.ActiveDocument.addObject('Surface::GeomFillSurface', 'Semi-Conductor')
        semi.Label = "Semi_Conductor(PV)"
        semi.BoundBox = [(f1, "Face1"), (f2, "Face2"), (f3, "Face3"), (f4, "Face4"), (f5, "Face5"), (f6, "Face6")]
        #semi.BoundaryList = [(lineA, "Edge1"), (lineB, "Edge1")]
=======
    def __init__(self, x1=0.9, y1=1/2, x2=1, y2=7/16, width=1) -> None:
        self.x1, self.y1, self.x2, self.y2, self.width = x1, y1, x2, y2, width
        
        line_a, line_b = self.compute_edges()

        lineA = Draft.make_bspline([App.Vector(*p) for p in line_a])
        lineB = Draft.make_bspline([App.Vector(*p) for p in line_b])

        App.ActiveDocument.recompute()

        semi = App.ActiveDocument.addObject('Surface::GeomFillSurface', 'Semi-Conductor')
        semi.Label = "Semi_Conductor(Mat2)"
        semi.BoundaryList = [(lineA, "Edge1"), (lineB, "Edge1")]
>>>>>>> ed142a833625fc1faeb79fe1b4c4f2e6c9e86ef8

        self.obj = semi

        App.ActiveDocument.recompute()

<<<<<<< HEAD
    def make_face(self,v1,v2,v3,v4):
     wire = Part.makePolygon([v1,v2,v3,v4])
     face = Part.Face(wire)
     return face
=======

>>>>>>> ed142a833625fc1faeb79fe1b4c4f2e6c9e86ef8

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

test = Semi.Shape.BoundBox
test.add(Mirror.Shape.BoundBox)
print("full bb:", test, test.DiagonalLength)

<<<<<<< HEAD
# file containing the index of refraction for a perovskite solar cell
file_perovskite = "C:/Users/kates/AppData/Roaming/FreeCAD/Macro/capstone_simulation/sillicon_cell_refraction.txt"

# materials
otsun.ReflectorSpecularLayer("Mir1", 0.95)
otsun.PVMaterial("PV", file_perovskite)
=======

# materials
otsun.ReflectorSpecularLayer("Mir1", 0.95)
otsun.AbsorberSimpleLayer("Mat2", 0.9)
>>>>>>> ed142a833625fc1faeb79fe1b4c4f2e6c9e86ef8



test_scene = otsun.scene.Scene([  Mirror, Semi])
# test_scene = otsun.scene.Scene([Semi])

<<<<<<< HEAD
phi = 0
theta = 45.0
init_energy = 1
=======
phi = 0.0
theta = 45.0
init_energy = 100
>>>>>>> ed142a833625fc1faeb79fe1b4c4f2e6c9e86ef8

# establish the direction of the rays
emitting_region_mainDirection = [1.0, 0.0, 0.0]
main_direction = otsun.polar_to_cartesian(phi, theta) * -1.0  # Sun direction vector

# establish a rectangular window that the arrays will emanate from
# emitting_region = otsun.source.SunWindow(test_scene,  emitting_region_mainDirection)
emitting_region = otsun.source.SunWindow(test_scene,  main_direction)


light_spectrum = WAVELENGTH_IN_NANOMETERS
<<<<<<< HEAD
number_rays = 100
# establish a light source based on the scene, the emitting region, as well as the strength of the rays
light_source = otsun.source.LightSource(test_scene, emitting_region, light_spectrum, init_energy)

experiment = otsun.Experiment(test_scene, light_source, number_rays)
=======

# establish a light source based on the scene, the emitting region, as well as the strength of the rays
light_source = otsun.source.LightSource(test_scene, emitting_region, light_spectrum, init_energy)

experiment = otsun.Experiment(test_scene, None, None)
>>>>>>> ed142a833625fc1faeb79fe1b4c4f2e6c9e86ef8

experiment.run()
thermal_energy = experiment.captured_energy_Th
PV_energy = experiment.captured_energy_PV

<<<<<<< HEAD
print('\nThermal energy: ' + str(thermal_energy) + '\nPhotovoltaic energy: ' + str(PV_energy))

=======
print('\nThermal energy: ' + str(thermal_energy) + '\nPhotovoltaic energy: ' + str(PV_energy))
>>>>>>> ed142a833625fc1faeb79fe1b4c4f2e6c9e86ef8
