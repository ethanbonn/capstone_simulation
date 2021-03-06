import FreeCAD as App
import Part
import numpy as np
import math
from scipy.integrate import solve_ivp
import Draft


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

        L = np.sqrt((self.x2 - self.x1)**2 + (self.y1 - self.y2)**2)


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

class top():
    def __init__(self, max_z=None, max_x=None, depth=1):
        self.DELTA = 0.001
        self.max_z, self.max_x, self.depth = max_z, max_x, depth

        l1, l2 = self.lines()

        curveA = Draft.make_bspline([App.Vector(*p) for p in l1])
        curveB = Draft.make_bspline([App.Vector(*p) for p in l2])

        # doc.recompute()


        top = App.ActiveDocument.addObject('Surface::GeomFillSurface', 'Top')
        # mirror.Label = "Mirror #1"
        top.Label = "Top(Coating)"
        top.BoundaryList = [(curveA, "Edge1"), (curveB, "Edge1")]

        self.obj = top

        App.ActiveDocument.recompute()




    def lines(self):
        ## ADD DELTAS
        line_1 = np.linspace( ( 0, 0, self.max_z ), ( self.max_x, 0, self.max_z + self.DELTA), 10 )
        line_2 = np.linspace( ( 0, self.depth, self.max_z ), ( self.max_x, self.depth, self.max_z + self.DELTA), 10 )
        return line_1, line_2

        
    def getObj(self):
        return self.obj

class sillicon():
    def __init__(self, x1=0.9, y1=1/2, x2=1, y2=7/16, depth=1.0, theta=0, thickness=0.001) -> None:
        self.x1, self.y1, self.x2, self.y2, self.depth, self.thickness = x1, y1, x2, y2, depth, thickness
        DELTA = 0.001
        BACK_THICKNESS = 0.1
        
        baseLength = depth
        baseWidth = math.sqrt((x2-x1)**2 + (y2-y1)**2)

        angleOfRotation = theta # math.degrees(math.atan((y1-y2)/(x2-x1)))

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
        self.obj = object1
        self.obj.Label = "Semi_Conductor(PV)"


        #line_a, line_b = self.compute_edges()

        #lineA = Draft.make_bspline([App.Vector(*p) for p in line_a])
        #lineB = Draft.make_bspline([App.Vector(*p) for p in line_b])

        App.ActiveDocument.recompute()

        # self.obj = App.ActiveDocument.addObject('Part::Feature', 'Semi-Conductor')
        # self.obj.Shape = object1.Shape
        #semi = App.ActiveDocument.addObject('Surface::GeomFillSurface', 'Semi-Conductor')
        # self.obj.Label = "Semi_Conductor(PV)"
        #semi.BoundBox = [(f1, "Face1"), (f2, "Face2"), (f3, "Face3"), (f4, "Face4"), (f5, "Face5"), (f6, "Face6")]
        #semi.BoundaryList = [(lineA, "Edge1"), (lineB, "Edge1")]

        #BACK
        pos2 = App.Vector(x1+baseWidth*(5/7), 0, y1 + thickness)
        place2 = App.Placement(pos, App.Rotation(yaxis, angleOfRotation))
        rectangle1 = Draft.make_rectangle(baseWidth, baseLength, placement=place)
        object2 = Draft.extrude(rectangle1, App.Vector((y1-y2)*BACK_THICKNESS,0,(x2-x1)*BACK_THICKNESS))
        object2.Solid = True
        self.back = object2 #App.ActiveDocument.addObject('Part::Feature', 'Semi_ConductorBack')
        self.back.Label = "Semi_ConductorBack(semiBack)"
        # self.back.BoundaryList = [(lineA, "Edge1"), (lineB, "Edge1")]

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

    def getBack(self):
        return self.back

    def getVerticies(self):
        # z MAX
        z_max = self.obj.Shape.Vertexes[1].Z

        # X MAX 
        x_max = self.obj.Shape.Vertexes[3].X

        return z_max, x_max



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

def create(x1=0.5, y1=1.1, theta=0.01, L=0.2, thickness=0.1):
    # def create(y0=1, x1=0.9, y1=1/2, x2=1, y2=7/16, depth=1.0, theta=0, thickness=0.001):
    y0 = 1.0
    x2 = x1 + L * np.cos(theta)
    y2 = y1 - L * np.sin(theta)

    MirrorParent = mirror(y0=y0, x1=x1, y1=y1, x2=x2, y2=y2, depth=1)
    SemiParent = sillicon(x1=x1, y1=y1, x2=x2, y2=y2, depth=1, theta=theta, thickness=thickness)
    # Mirror = MirrorParent.getObj()
    # Semi = SemiParent.getObj()
    # SilliconBack = SemiParent.getBack() #silliconBack(x1=x1, y1=y1, x2=x2, y2=y2, depth=1).getObj()  
    max_z, max_x = SemiParent.getVerticies()
    Top = top(max_z=max_z, max_x=max_x)#.getObj()

