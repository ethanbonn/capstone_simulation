import FreeCAD as App
import Part
import numpy as np
from scipy.integrate import solve_ivp
import Draft


class mirror():
    def __init__(self, x0=1, y0=1/2, x1=0.9, y1=1/2, x2=1, y2=7/16, width=1 ):
        self.x0, self.y0, self.x1, self.y1, self.x2, self.y2, self.width = x0, y0, x1, y1, x2, y2, width

        curve_a, curve_b = self.curve_solver()

        curveA = Draft.make_bspline([App.Vector(*p) for p in curve_a])
        curveB = Draft.make_bspline([App.Vector(*p) for p in curve_b])

        App.ActiveDocument.recompute()

        mirror = App.ActiveDocument.addObject('Surface::GeomFillSurface', 'Mirror')
        mirror.BoundaryList = [(curveA, "Edge1"), (curveB, "Edge1")]

        mirror.Label = "Mirror(Mir1)"

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
        p3 = App.Vector(1, 1, 0)
        place3 = App.Placement(p3, App.Rotation(yaxis, 45))
        rectangle1 = Draft.make_rectangle(1, 2, placement=place3)
        object1 = Draft.extrude(rectangle1, App.Vector(1,0,1))
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
        return np.vstack((x, np.zeros(num_sim_points), y)).T.tolist(), np.vstack((x, np.ones(num_sim_points) * self.width, y)).T.tolist()


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


# class sillicon():
#     def __init__(self, x1=0.9, y1=1/2, x2=1, y2=7/16, width=1.0) -> None:
#         thickness = 0.25
#         self.x1, self.y1, self.x2, self.y2, self.width, self.thickness = x1, y1, x2, y2, width, thickness
        
#         v1 = App.Vector(x1,0,y1)
#         v2 = App.Vector(x2,0,y2)
#         v3 = App.Vector(x1+thickness,0,y1+thickness)
#         v4 = App.Vector(x2+thickness,0,y2+thickness)
        
#         v5 = App.Vector(x1,width,y1)
#         v6 = App.Vector(x2,width,y2)
#         v7 = App.Vector(x1+thickness,width,y1+thickness)
#         v8 = App.Vector(x2+thickness,width,y2+thickness)
        
#         # f1 = self.make_face(v1,v2,v4,v3)
#         # f2 = self.make_face(v5,v6,v8,v7)
#         # f3 = self.make_face(v1,v3,v7,v5)
#         # f4 = self.make_face(v2,v4,v8,v6)
#         # f5 = self.make_face(v1,v5,v6,v2)
#         # f6 = self.make_face(v3,v7,v8,v4)
    
#         # shell=Draft.makeShell([f1,f2,f3,f4,f5,f6])
#         # solid=Draft.makeSolid(shell)
#         # self.Shape = solid
#         yaxis = App.Vector(0, 1, 0)
#         p3 = App.Vector(1, 1, 0)
#         place3 = App.Placement(p3, App.Rotation(yaxis, 45))
#         rectangle1 = Draft.make_rectangle(1, 2, placement=place3)
#         object1 = Draft.extrude(rectangle1, App.Vector(1,0,1))
#         object1.Solid = True

#         #line_a, line_b = self.compute_edges()

#         #lineA = Draft.make_bspline([App.Vector(*p) for p in line_a])
#         #lineB = Draft.make_bspline([App.Vector(*p) for p in line_b])

#         # App.ActiveDocument.recompute()

#         # semi = App.ActiveDocument.addObject('Surface::GeomFillSurface', 'Semi-Conductor')
#         # semi.BoundaryList = [(lineA, "Edge1"), (lineB, "Edge1")]

#         zaxis = App.Vector(0, 0, 1)
#         p3 = App.Vector(1, 1, 0)
#         place3 = App.Placement(p3, App.Rotation(zaxis, 45))

#         rec = Draft.make_rectangle(2, 1, placement=place3)
#         object1 = Draft.extrude(rec, App.Vector(1,0,1))
#         # self.Shape.Solid = True
#         # semi = App.ActiveDocument.addObject('PartDesign::Body', 'Semi-Conductor')

#         # print("Type: ", type(semi))

#         # semi.addObject(self.Shape.getObj())

#         # semi.Label = "Semi_Conductor(PV)"

#         self.obj = App.ActiveDocument.addObject('Part::Feature', 'Semi-Conductor')
#         self.obj.Shape = object1.Shape
#         #semi = App.ActiveDocument.addObject('Surface::GeomFillSurface', 'Semi-Conductor')
#         self.obj.Label = "Semi_Conductor(PV)"
#         #semi.BoundBox = [(f1, "Face1"), (f2, "Face2"), (f3, "Face3"), (f4, "Face4"), (f5, "Face5"), (f6, "Face6")]
#         #semi.BoundaryList = [(lineA, "Edge1"), (lineB, "Edge1")]

#         #self.obj = semi

#         App.ActiveDocument.recompute()

#     # def make_face(self,v1,v2,v3,v4):
#     #  wire = Draft.make_polygon([v1,v2,v3,v4])
#     #  face = Draft.Face(wire)
#     #  return face

#     def compute_edges(self, num_sim_points=100):
#         m = (self.y2 - self.y1) / (self.x2 - self.x1)
#         b = self.y1 - (m*self.x1)
#         # eq: y = mx + b
#         x = np.linspace(self.x1, self.x2, num_sim_points)
#         y = (m * x) + b

#         # return np.vstack((x, y, np.zeros(num_sim_points))).T.tolist(), np.vstack((x, y, np.ones(num_sim_points) * self.width)).T.tolist()
#         return np.vstack((x, np.zeros(num_sim_points), y)).T.tolist(), np.vstack((x, np.ones(num_sim_points) * self.width, y)).T.tolist()


#     def compute_edges(self, num_sim_points=100):
#         m = (self.y2 - self.y1) / (self.x2 - self.x1)
#         b = self.y1 - (m*self.x1)
#         # eq: y = mx + b
#         x = np.linspace(self.x1, self.x2, num_sim_points)
#         y = (m * x) + b

#         # return np.vstack((x, y, np.zeros(num_sim_points))).T.tolist(), np.vstack((x, y, np.ones(num_sim_points) * self.width)).T.tolist()
#         return np.vstack((x, np.zeros(num_sim_points), y)).T.tolist(), np.vstack((x, np.ones(num_sim_points) * self.width, y)).T.tolist()

#     def getObj(self):
#         return self.obj




