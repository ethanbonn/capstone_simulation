FREECAD_PATH = "C:/Program Files/FreeCAD 0.19/bin/"
import sys
sys.path.append(FREECAD_PATH) 

import FreeCAD as App
import Part
import numpy as np
import math
from scipy.integrate import solve_ivp
import Draft
from FreeCAD import Base
import otsun
import pandas as pd
WAVELENGTH_IN_NANOMETERS = 7

doc = App.newDocument()


class mirror():
    def __init__(self, y0=1/2, x1=0.9, y1=1/2, x2=1, y2=7/16, depth=1):
        self.y0, self.x1, self.y1, self.x2, self.y2, self.depth, self.width, self.height = y0, x1, y1, x2, y2, depth, x2, 1

        curve_a, curve_b= self.curve_solver()

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

        F = lambda x, y: - 1 / np.tan(np.pi/4 + 1/2 * np.arctan(((self.x1 * L - x * L) * self.y1 + x * L * self.y2 - self.x1 * L * y) / ((self.x1 * L - x * L) * self.x1 + x * L * self.x2 - self.x1 * L * x)))

        # Numerically solve the ODE corresponding to the 

        dt = 0.01

        t_eval = np.arange(0, self.x1, dt)
        sol = solve_ivp(F, [0, self.x1 - dt], [self.y0], t_eval=t_eval) 
        self.height = max(self.y0, self.y1) - min(sol.y[0])

        # # make points 3D along Z-axis
        # l = []
        # for i in np.linspace(0, width, num_w_points):
        #     l.append(np.vstack((sol.t, sol.y[0], np.ones(len(sol.t)) * i)).T)

        # return np.array(l).reshape(-1, 3).tolist()
        # return np.vstack((sol.t, sol.y[0], np.zeros(len(sol.t)))).T.tolist(), np.vstack((sol.t, sol.y[0], np.ones(len(sol.t)) * self.width)).T.tolist()
        return np.vstack((sol.t, np.zeros(len(sol.t)), sol.y[0])).T.tolist(), np.vstack((sol.t, np.ones(len(sol.t)) * self.depth, sol.y[0])).T.tolist()

    def getObj(self):
        return self.obj


class sillicon():
    def __init__(self, x1=0.9, y1=1/2, x2=1, y2=7/16, depth=1.0) -> None:
        thickness = 0.5
        self.x1, self.y1, self.x2, self.y2, self.depth, self.thickness = x1, y1, x2, y2, depth, thickness
        
        baseLength = depth
        baseWidth = math.sqrt((x2-x1)**2 + (y2-y1)**2)

        angleOfRotation = math.degrees(math.atan((y1-y2)/(x2-x1)))

        # extrudeRotate = math.degrees(math.atan((x2-x1)/(y2-y1)))
        # extrudeRotate = 90-extrudeRotate
        # x_extrudeRotate = math.tan(extrudeRotate)
        # v1 = App.Vector(x1,0,y1)
        # v2 = App.Vector(x2,0,y2)
        # v3 = App.Vector(x1+thickness,0,y1+thickness)
        # v4 = App.Vector(x2+thickness,0,y2+thickness)
        
        # v5 = App.Vector(x1,width,y1)
        # v6 = App.Vector(x2,width,y2)
        # v7 = App.Vector(x1+thickness,width,y1+thickness)
        # v8 = App.Vector(x2+thickness,width,y2+thickness)
        
        # f1 = self.make_face(v1,v2,v4,v3)
        # f2 = self.make_face(v5,v6,v8,v7)
        # f3 = self.make_face(v1,v3,v7,v5)
        # f4 = self.make_face(v2,v4,v8,v6)
        # f5 = self.make_face(v1,v5,v6,v2)
        # f6 = self.make_face(v3,v7,v8,v4)
    
        # shell=Draft.makeShell([f1,f2,f3,f4,f5,f6])
        # solid=Draft.makeSolid(shell)
        # self.Shape = solid
        yaxis = App.Vector(0, 1, 0)
        pos = App.Vector(x1+baseWidth*(5/7), 0, y1)
        place = App.Placement(pos, App.Rotation(yaxis, angleOfRotation))
        rectangle1 = Draft.make_rectangle(baseWidth, baseLength, placement=place)
        object1 = Draft.extrude(rectangle1, App.Vector((y1-y2)*thickness,0,(x2-x1)*thickness))
        object1.Solid = True

        #line_a, line_b = self.compute_edges()

        #lineA = Draft.make_bspline([App.Vector(*p) for p in line_a])
        #lineB = Draft.make_bspline([App.Vector(*p) for p in line_b])

        App.ActiveDocument.recompute()

        self.obj = App.ActiveDocument.addObject('Part::Feature', 'Semi-Conductor')
        self.obj.Shape = object1.Shape
        #semi = App.ActiveDocument.addObject('Surface::GeomFillSurface', 'Semi-Conductor')
        self.obj.Label = "Semi_Conductor(PV)"
        #semi.BoundBox = [(f1, "Face1"), (f2, "Face2"), (f3, "Face3"), (f4, "Face4"), (f5, "Face5"), (f6, "Face6")]
        #semi.BoundaryList = [(lineA, "Edge1"), (lineB, "Edge1")]

        #self.obj = semi

        App.ActiveDocument.recompute()

    # def make_face(self,v1,v2,v3,v4):
    #  wire = Draft.make_polygon([v1,v2,v3,v4])
    #  face = Draft.Face(wire)
    #  return face

    def compute_edges(self, num_sim_points=100):
        m = (self.y2 - self.y1) / (self.x2 - self.x1)
        b = self.y1 - (m*self.x1)
        # eq: y = mx + b
        x = np.linspace(self.x1, self.x2, num_sim_points)
        y = (m * x) + b

        # return np.vstack((x, y, np.zeros(num_sim_points))).T.tolist(), np.vstack((x, y, np.ones(num_sim_points) * self.width)).T.tolist()
        return np.vstack((x, np.zeros(num_sim_points), y)).T.tolist(), np.vstack((x, np.ones(num_sim_points) * self.depth, y)).T.tolist()


    def getObj(self):
        return self.obj

class silliconBack():
    def __init__(self, x1=0.9, y1=1/2, x2=1, y2=7/16, depth=1.0) -> None:
        thickness = 0.5
        baseWidth = math.sqrt((x2-x1)**2 + (y2-y1)**2)
        self.x1, self.y1, self.x2, self.y2, self.depth, self.thickness = x1 + baseWidth*(5/7)+ (y1 - y2) * thickness, y1 + (x2 - x1) * thickness, x2 + baseWidth*(5/7)+(y1 - y2) * thickness, y2 + (x2 - x1) * thickness, depth, 0
        

        line_a, line_b = self.compute_edges()

        lineA = Draft.make_bspline([App.Vector(*p) for p in line_a])
        lineB = Draft.make_bspline([App.Vector(*p) for p in line_b])

        App.ActiveDocument.recompute()

        semi = App.ActiveDocument.addObject('Surface::GeomFillSurface', 'Semi_ConductorBack')
        semi.Label = "Semi_ConductorBack(semiBack)"
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
        return np.vstack((x, np.zeros(num_sim_points), y)).T.tolist(), np.vstack((x, np.ones(num_sim_points) * self.depth, y)).T.tolist()


    def getObj(self):
        return self.obj

phi = 0
theta = 45.0
init_energy = 1

# establish the direction of the rays
emitting_region_mainDirection = [1.0, 0.0, 0.0]
main_direction = otsun.polar_to_cartesian(phi, theta) * -1.0  # Sun direction vector

light_spectrum = WAVELENGTH_IN_NANOMETERS
number_rays = 100000

# file containing the index of refraction for a perovskite solar cell
file_perovskite = "C:/Users/kates/AppData/Roaming/FreeCAD/Macro/capstone_simulation/sillicon_cell_refraction.txt"

# Specify parameter lists for iterations
# x1_values = [1.5, 1.75, 2.0, 2.25]
# y1_values = [0.6, 0.8, 1.0, 1.2]
# angles = [0, np.pi / 6, np.pi / 5, np.pi / 4, np. pi / 3, np.pi / 2]
# lengths = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6]

x1_values = [1.5]
y1_values = [0.8]
angles = [0, np.pi / 6]
lengths = [0.1, 0.2]


# Create summary table for mirror statistics

statisic_columns = ['Trial', 'Length', 'Angle', 'x1', 'y1', 'x2', 'y2', 'Width', 'Height', 'Width Ratio', 'Height Ratio', 'Thermal Energy', ' PV Energy']

statistics = np.zeros((len(x1_values) * len(y1_values) * len(angles) * len(lengths), len(statisic_columns)))

# Run iterations and record results for each one
y0 = 1.0

i = 1
for x1 in x1_values:
    for y1 in y1_values:
        for theta in angles:
            for L in lengths:
                
                # Input parameters
                x2 = x1 + L * np.cos(theta)
                y2 = y1 - L * np.sin(theta)
                x_values = [x1, x2]
                y_values = [y1, y2]
                      
                statistics[i - 1, 0] = i
                statistics[i - 1, 1] = L
                statistics[i - 1, 2] = theta
                statistics[i - 1, 3] = x1
                statistics[i - 1, 4] = y1
                statistics[i - 1, 5] = x2
                statistics[i - 1, 6] = y2    

                      

                #-<>-#-<>-# BEGIN EXPERIMENT #-<>-#-<>-#
                MirrorParent = mirror(y0=1/2, x1=0.9, y1=1/2, x2=1, y2=7/16, depth=1)
                SemiParent = sillicon(x1=0.9, y1=1/2, x2=1, y2=7/16, depth=1)     
                Mirror = MirrorParent.getObj()
                Semi = SemiParent.getObj()
                SilliconBack = silliconBack(x1=0.9, y1=1/2, x2=1, y2=7/16, depth=1).getObj()  

                      
                statistics[i - 1, 7] = MirrorParent.width
                statistics[i - 1, 9] = statistics[i - 1, 7] / L
                statistics[i - 1, 8] = MirrorParent.height
                statistics[i - 1, 10] = statistics[i - 1, 8] / L

                # materials
                otsun.ReflectorSpecularLayer("Mir1", 0.95)
                otsun.AbsorberSimpleLayer("semiBack", 0.95)
                otsun.PVMaterial("PV", file_perovskite)

    
                # pass in an array of the free cad objects (i.e. the mirror and the silicon cell) to set up the scene
                test_scene = otsun.scene.Scene([Mirror, Semi, SilliconBack])

                # establish a rectangular window that the arrays will emanate from
                emitting_region = otsun.source.SunWindow(test_scene,  main_direction)

                # establish a light source based on the scene, the emitting region, as well as the strength of the rays
                light_source = otsun.source.LightSource(test_scene, emitting_region, light_spectrum, init_energy)

                experiment = otsun.Experiment(test_scene, light_source, number_rays)

                experiment.run()
                      
                #-<>-#-<>-# END EXPERIMENT #-<>-#-<>-#
                  
                      
                      
                statistics[i - 1, 11] = experiment.captured_energy_Th
                statistics[i - 1, 12] = experiment.captured_energy_PV      
                
                i += 1

df_statistics = pd.DataFrame(statistics, columns = statisic_columns)

df_statistics.to_csv('test_results.csv', index = False)
#path_or_buf= "C:/Users/kates/Downloads/capstone2"

#print("boundbox:", Semi.Shape.BoundBox.DiagonalLength)

# print(Mirror.label, Semi.label)

# pass in an array of the free cad objects (i.e. the mirror and the silicon cell) to set up the scene

# test = Semi.Shape.BoundBox
# test.add(Mirror.Shape.BoundBox)
# print("full bb:", test, test.DiagonalLength)

# materials
# otsun.ReflectorSpecularLayer("Mir1", 0.95)
# otsun.PVMaterial("PV", file_perovskite)



# test_scene = otsun.scene.Scene([Mirror, Semi])
# # test_scene = otsun.scene.Scene([Semi])



# # establish a rectangular window that the arrays will emanate from
# # emitting_region = otsun.source.SunWindow(test_scene,  emitting_region_mainDirection)
# emitting_region = otsun.source.SunWindow(test_scene,  main_direction)


# # establish a light source based on the scene, the emitting region, as well as the strength of the rays
# light_source = otsun.source.LightSource(test_scene, emitting_region, light_spectrum, init_energy)

# experiment = otsun.Experiment(test_scene, light_source, number_rays)

# experiment.run()
# thermal_energy = experiment.captured_energy_Th
# PV_energy = experiment.captured_energy_PV

# print('\nThermal energy: ' + str(thermal_energy) + '\nPhotovoltaic energy: ' + str(PV_energy))

