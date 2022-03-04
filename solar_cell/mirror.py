import FreeCAD as App
import Part
import numpy as np
from scipy.integrate import solve_ivp

def create(obj_name):
    """
    Object creation method
    """

    obj = App.ActiveDocument.addObject('Part::FeaturePython', obj_name)

    mirror(obj)

    ViewProviderBox(obj.ViewObject)

    App.ActiveDocument.recompute()

    return obj

class mirror():

    def __init__(self, obj):
        """
        Default constructor
        """

        self.Type = 'mirror'

        obj.Proxy = self

        # points for bsplines
        self.points = self.curve_solver(x0 = 1, y0 = 1/2, x1 = 0.9, y1 = 1/2, x2 = 1, y2 = 7/16)


        vec_list = [App.Vector(*p) for p in self.points[0]]

        bs = Part.BSplineCurve()
        bs.interpolate(Points=vec_list)
        Part.show(bs.toShape())

        vec_list_2 = [App.Vector(*p) for p in self.points[1]]

        bs_2 = Part.BSplineCurve()
        bs_2.interpolate(Points=vec_list_2)
        Part.show(bs_2.toShape())

        # obj.addProperty('App::PropertyString', 'Description', 'Base', 'Box description').Description = ""
        # obj.addProperty('App::PropertyLength', 'Length', 'Dimensions', 'Box length').Length = 10.0
        # obj.addProperty('App::PropertyLength', 'Width', 'Dimensions', 'Box width').Width = '10 mm'
        # obj.addProperty('App::PropertyLength', 'Height', 'Dimensions', 'Box height').Height = '1 cm'

    def curve_solver(self, x0, y0, x1, y1, x2, y2, width=1, num_w_points=20):
        '''
        the solution will be a curved surface travelling from (0, y0, 0) to (x0, 0, width)
        '''

        # Calculate CPV cell length from coordiantes of the mirror endpoints

        L = np.sqrt((x2 - x1)**2 + (y2 - y1)**2)


        # In[7]:


        # Define ODE

        F = lambda x, y: - 1 / np.tan(np.pi/4 + 1/2 * np.arctan(((x0 * L - x * L) * y1 + x * L * y2 - x0 * L * y) / ((x0 * L - x * L) * x1 + x * L * x2 - x0 * L * x)))

        # Numerically solve the ODE corresponding to the 

        dt = 0.01

        t_eval = np.arange(0, 1, dt)
        sol = solve_ivp(F, [0, x0 - dt], [y0], t_eval=t_eval)

        # # make points 3D along Z-axis
        # l = []
        # for i in np.linspace(0, width, num_w_points):
        #     l.append(np.vstack((sol.t, sol.y[0], np.ones(len(sol.t)) * i)).T)

        # return np.array(l).reshape(-1, 3).tolist()
        return np.vstack((sol.t, sol.y[0], np.zeros(len(sol.t)))).T.tolist(), np.vstack((sol.t, sol.y[0], np.ones(len(sol.t)))).T.tolist()

    def execute(self, obj):
        """
        Called on document recompute
        """

        # obj.Shape = Part.makeBox(obj.Length, obj.Width, obj.Height)

class ViewProviderBox:

    def __init__(self, obj):
        """
        Set this object to the proxy object of the actual view provider
        """

        obj.Proxy = self

    def attach(self, obj):
        """
        Setup the scene sub-graph of the view provider, this method is mandatory
        """
        return

    def updateData(self, fp, prop):
        """
        If a property of the handled feature has changed we have the chance to handle this here
        """
        return

    def getDisplayModes(self,obj):
        """
        Return a list of display modes.
        """
        return []

    def getDefaultDisplayMode(self):
        """
        Return the name of the default display mode. It must be defined in getDisplayModes.
        """
        return "Shaded"

    def setDisplayMode(self,mode):
        """
        Map the display mode defined in attach with those defined in getDisplayModes.
        Since they have the same names nothing needs to be done.
        This method is optional.
        """
        return mode

    def onChanged(self, vp, prop):
        """
        Print the name of the property that has changed
        """

        App.Console.PrintMessage("Change property: " + str(prop) + "\n")

    def getIcon(self):
        """
        Return the icon in XMP format which will appear in the tree view. This method is optional and if not defined a default icon is shown.
        """

        return """
            /* XPM */
            static const char * ViewProviderBox_xpm[] = {
            "16 16 6 1",
            "    c None",
            ".   c #141010",
            "+   c #615BD2",
            "@   c #C39D55",
            "#   c #000000",
            "$   c #57C355",
            "        ........",
            "   ......++..+..",
            "   .@@@@.++..++.",
            "   .@@@@.++..++.",
            "   .@@  .++++++.",
            "  ..@@  .++..++.",
            "###@@@@ .++..++.",
            "##$.@@$#.++++++.",
            "#$#$.$$$........",
            "#$$#######      ",
            "#$$#$$$$$#      ",
            "#$$#$$$$$#      ",
            "#$$#$$$$$#      ",
            " #$#$$$$$#      ",
            "  ##$$$$$#      ",
            "   #######      "};
            """

    def __getstate__(self):
        """
        Called during document saving.
        """
        return None

    def __setstate__(self,state):
        """
        Called during document restore.
        """
        return None