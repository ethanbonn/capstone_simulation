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
from cell import mirror, sillicon, silliconBack
import time

WAVELENGTH_IN_NANOMETERS = 7

doc = App.newDocument()

# Need:
# - init_energy

def simulate(init_energy=1, number_rays=1000):

    file_perovskite = "./sillicon_cell_refraction.txt"


    # materials
    otsun.ReflectorSpecularLayer("Mir1", 0.95)
    otsun.AbsorberSimpleLayer("semiBack", 0.95)
    otsun.PVMaterial("PV", file_perovskite)
        
    phi = 0
    theta = 45.0
    #init_energy = 1 ####### NEED

    # establish the direction of the rays
    main_direction = otsun.polar_to_cartesian(phi, theta) * -1.0  # Sun direction vector

    light_spectrum = WAVELENGTH_IN_NANOMETERS

    # file containing the index of refraction for a perovskite solar cell


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
                    # x_values = [x1, x2]
                    # y_values = [y1, y2]       

                    #-<>-#-<>-# BEGIN EXPERIMENT #-<>-#-<>-#

                    # these are all using presets:
                    MirrorParent = mirror(y0=1/2, x1=x1, y1=y1, x2=x2, y2=y2, depth=1)
                    SemiParent = sillicon(x1=x1, y1=y1, x2=x2, y2=y2, depth=1)
                    Mirror = MirrorParent.getObj()
                    Semi = SemiParent.getObj()
                    SilliconBack = silliconBack(x1=x1, y1=y1, x2=x2, y2=y2, depth=1).getObj()  

                    # pass in an array of the free cad objects (i.e. the mirror and the silicon cell) to set up the scene
                    test_scene = otsun.scene.Scene([Mirror, Semi, SilliconBack])

                    # establish a rectangular window that the arrays will emanate from
                    emitting_region = otsun.source.SunWindow(test_scene,  main_direction)

                    # establish a light source based on the scene, the emitting region, as well as the strength of the rays
                    light_source = otsun.source.LightSource(test_scene, emitting_region, light_spectrum, init_energy)

                    start_t = time.perf_counter()
                    print("Starting Trial:", i)

                    experiment = otsun.Experiment(test_scene, light_source, number_rays)
                    experiment.run()

                    print("Experiment Took:", time.perf_counter() - start_t)

                    # Record inputs:
                    statistics[i - 1, 0] = i
                    statistics[i - 1, 1] = L
                    statistics[i - 1, 2] = theta
                    statistics[i - 1, 3] = x1
                    statistics[i - 1, 4] = y1
                    statistics[i - 1, 5] = x2
                    statistics[i - 1, 6] = y2    
                    statistics[i - 1, 7] = MirrorParent.width
                    statistics[i - 1, 9] = statistics[i - 1, 7] / L
                    statistics[i - 1, 8] = MirrorParent.height
                    statistics[i - 1, 10] = statistics[i - 1, 8] / L
                    statistics[i - 1, 11] = experiment.captured_energy_Th
                    statistics[i - 1, 12] = experiment.captured_energy_PV   

                    #-<>-#-<>-# END EXPERIMENT #-<>-#-<>-#
                    i += 1
    return pd.DataFrame(statistics, columns = statisic_columns)

df_statistics = simulate()
df_statistics.to_csv('test_results.csv', index = False)


#path_or_buf= "C:/Users/kates/Downloads/capstone2"

#print("boundbox:", Semi.Shape.BoundBox.DiagonalLength)

# print(Mirror.label, Semi.label)

# pass in an array of the free cad objects (i.e. the mirror and the silicon cell) to set up the scene
# Calculating the bounding box of the two objects.

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

