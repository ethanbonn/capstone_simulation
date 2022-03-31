FREECAD_PATH = "C:/Program Files/FreeCAD 0.19/bin/"
import sys
sys.path.append(FREECAD_PATH) 

import FreeCAD as App
import Part

class Cell():
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
        #semi.BoundBox = [(f1, "Face1"), (f2, "Face2"), (f3, "Face3"), (f4, "Face4"), (f5, "Face5"), (f6, "Face6")]
        #semi.BoundaryList = [(lineA, "Edge1"), (lineB, "Edge1")]

        self.obj = semi

        App.ActiveDocument.recompute()

    def make_face(self,v1,v2,v3,v4):
     wire = Part.makePolygon([v1,v2,v3,v4])
     face = Part.Face(wire)
     return face

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