import numpy as np
from scipy.integrate import solve_ivp


def curve_solver( x0, y0, x1, y1, x2, y2, width=1, num_w_points=20 ):
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

    num_length_points = int(1 / dt)

    upper_border = np.ones((num_length_points,3)) * (0, y0, 1)
    upper_border[:,2] = np.linspace(0,1,num_length_points)
    lower_border = np.ones((num_length_points,3)) * (x0, 0, 1)
    lower_border[:,2] = np.linspace(0,1,num_length_points)


    


    # make points 3D along Z-axis
    l = [np.vstack((sol.t, sol.y[0], np.ones(len(sol.t)) * 0)).T , np.vstack((sol.t, sol.y[0], np.ones(len(sol.t)) * 1)).T, upper_border, lower_border ]

    # l = []
    # for i in np.linspace(0, width, num_w_points):
    #     l.append(np.vstack((sol.t, sol.y[0], np.ones(len(sol.t)) * i)).T)

    return np.array(l).reshape(-1, 3).tolist()

points = curve_solver(x0 = 1, y0 = 1/2, x1 = 0.9, y1 = 1/2, x2 = 1, y2 = 7/16)

points_asc = str(points).replace(" [", "").replace("[", "").replace(",", "").replace("]", "\n")


with open('points.asc', 'w') as f:
    f.write(points_asc)


