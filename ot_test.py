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
from cell import mirror, sillicon, silliconBack, top
import time

WAVELENGTH_IN_NANOMETERS = 7

doc = App.newDocument()

# Need:
# - init_energy

def simulate(init_energy=1):
    # init_energy = 4.180480200259445e-13


    file_perovskite = "./sillicon_cell_refraction.txt"


    # materials
    otsun.ReflectorSpecularLayer("Mir1", 0.999)
    otsun.AbsorberSimpleLayer("semiBack", 0.95)
    otsun.PVMaterial("PV", file_perovskite)
    otsun.TransparentSimpleLayer("Coating", 0.99)
        
    phi = 0
    theta = 0 #90 #45.0
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

    x1_values = np.linspace(0.8, 1.5, 3) #[1.5]
    y1_values = np.linspace(0.6, 1.5, 3) #[0.8]
    angles = np.linspace(0, 20, 3) #[0, 5, 11, 20, 30, 40, 50, 60, 70, 80]
    lengths = np.linspace(0.5, 1.5, 2) #[1]
    thickness = [0.1, ]
    # Format: (x1, y1, theta, L, thickness)
    test_cases = [(0.5, 1.1, 30, 0.2, 0.1), (0.5, 1.1, 45, 0.3, 0.1)]


    # Create summary table for mirror statistics

    statisic_columns = ['Trial', 'Length', 'Angle', 'x1', 'y1', 'x2', 'y2', 'Width', 'Height', 'Width Ratio', 'Height Ratio', 'Thermal Energy', ' PV Energy', 'Optical Efficiency (TH)', 'Optical Efficiency (PV)']

    statistics = np.zeros((len(x1_values) * len(y1_values) * len(angles) * len(lengths), len(statisic_columns)))

    # Run iterations and record results for each one
    y0 = 1.0

    i = 1
    # for x1 in x1_values:
    #     for y1 in y1_values:
    #         for theta in angles:
    #             for L in lengths:

    for (x1, y1, theta, L, thickness) in test_cases:    
        # Input parameters
        x2 = x1 + L * np.cos(theta)
        y2 = y1 - L * np.sin(theta)
        # x_values = [x1, x2]
        # y_values = [y1, y2]    


            

        #-<>-#-<>-# BEGIN EXPERIMENT #-<>-#-<>-#

        # these are all using presets:
        MirrorParent = mirror(y0=1/2, x1=x1, y1=y1, x2=x2, y2=y2, depth=1)
        SemiParent = sillicon(x1=x1, y1=y1, x2=x2, y2=y2, depth=1, theta=theta, thickness=thickness)
        Mirror = MirrorParent.getObj()
        Semi = SemiParent.getObj()
        SilliconBack = silliconBack(x1=x1, y1=y1, x2=x2, y2=y2, depth=1).getObj()  
        max_z, max_x = SemiParent.getVerticies()
        Top = top(max_z=max_z, max_x=max_x).getObj()

        aperture_collector_Th = doc.getObject("Top").Shape.Faces[0].Area 

        DNI = 2191 / (365 * 24 * 1000)
        number_rays = 500#aperture_collector_Th * DNI / (init_energy * (1000 **2))

        print('-' * 30)

        print("Starting Trial:", i)

        print("number of rays:", number_rays)

        print("Creating:")
        print(f"mirror(y0=1, x1={x1}, y1={y1}, x2={x2}, y2={y2}, depth=1)")
        print(f"sillicon(x1={x1}, y1={y1}, x2={x2}, y2={y2}, depth=1, theta={theta})")
        print(f"silliconBack(x1={x1}, y1={y1}, x2={x2}, y2={y2}, depth=1)")
        print(f"top(max_z={max_z}, max_x={max_x})")
        print(L)

        # pass in an array of the free cad objects (i.e. the mirror and the silicon cell) to set up the scene
        # test_scene = otsun.scene.Scene([ Mirror, Semi, SilliconBack, Top])
        test_scene = otsun.scene.Scene([ Mirror, Semi, SilliconBack, Top ])

        # establish a rectangular window that the arrays will emanate from
        emitting_region = otsun.source.SunWindow(test_scene,  main_direction)

        # establish a light source based on the scene, the emitting region, as well as the strength of the rays
        light_source = otsun.source.LightSource(test_scene, emitting_region, light_spectrum, init_energy)

        start_t = time.perf_counter()


        experiment = otsun.Experiment(test_scene, light_source, number_rays)
        experiment.run()

        efficiency_from_source_Th = (experiment.captured_energy_Th / aperture_collector_Th) / (
            experiment.number_of_rays / experiment.light_source.emitting_region.aperture)

        efficiency_from_source_PV = (experiment.captured_energy_PV / aperture_collector_Th) / (
            experiment.number_of_rays / experiment.light_source.emitting_region.aperture)

        print(f"experiment.captured_energy_Th {experiment.captured_energy_Th} / aperture_collector_Th {aperture_collector_Th} / experiment.number_of_rays {experiment.number_of_rays} / experiment.light_source.emitting_region.aperture {experiment.light_source.emitting_region.aperture}")
        print("Optical Efficiency (TH):", efficiency_from_source_Th)
        print("Optical Efficiency (PV):", efficiency_from_source_PV)
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
        statistics[i - 1, 13] = efficiency_from_source_Th
        statistics[i - 1, 14] = efficiency_from_source_PV


        #-<>-#-<>-# END EXPERIMENT #-<>-#-<>-#
        i += 1
    return pd.DataFrame(statistics, columns = statisic_columns)

def single_sim(init_energy=1):
    # init_energy = 4.180480200259445e-13


    file_perovskite = "./sillicon_cell_refraction.txt"


    # materials
    otsun.ReflectorSpecularLayer("Mir1", 0.999)
    otsun.AbsorberSimpleLayer("semiBack", 0.95)
    otsun.PVMaterial("PV", file_perovskite)
    otsun.TransparentSimpleLayer("Coating", 0.99)
        
    phi = 0
    theta = 0 #90 #45.0
    #init_energy = 1 ####### NEED

    # establish the direction of the rays
    main_direction = otsun.polar_to_cartesian(phi, theta) #* -1.0  # Sun direction vector

    light_spectrum = WAVELENGTH_IN_NANOMETERS

    # file containing the index of refraction for a perovskite solar cell


 
    y1 = 1/2
    x1 = 0/8
    y1 = 0.6
    x2 = 2.279591836734694
    y2 = 0.6
    theta = 0.0
    L = 1.2

    # Create summary table for mirror statistics

    # Input parameters
    x2 = x1 + L * np.cos(theta)
    y2 = y1 - L * np.sin(theta)
    # x_values = [x1, x2]
    # y_values = [y1, y2]    


        

    #-<>-#-<>-# BEGIN EXPERIMENT #-<>-#-<>-#

    # these are all using presets:
    MirrorParent = mirror(y0=1/2, x1=x1, y1=y1, x2=x2, y2=y2, depth=1)
    SemiParent = sillicon(x1=x1, y1=y1, x2=x2, y2=y2, depth=1, theta=theta)
    Mirror = MirrorParent.getObj()
    Semi = SemiParent.getObj()
    SilliconBack = SemiParent.getBack() #silliconBack(x1=x1, y1=y1, x2=x2, y2=y2, depth=1).getObj()  
    max_z, max_x = SemiParent.getVerticies()
    Top = top(max_z=max_z, max_x=max_x).getObj()

    aperture_collector_Th = doc.getObject("Top").Shape.Faces[0].Area 

    DNI = 2191 / (365 * 24 * 1000)
    number_rays = 500 #aperture_collector_Th * DNI / (init_energy * (1000 **2))

    print("number of rays:", number_rays)

    print("Creating:")
    print(f"mirror(y0=1/2, x1={x1}, y1={y1}, x2={x2}, y2={y2}, depth=1)")
    print(f"sillicon(x1={x1}, y1={y1}, x2={x2}, y2={y2}, depth=1, theta={theta})")
    print(f"silliconBack(x1={x1}, y1={y1}, x2={x2}, y2={y2}, depth=1)")
    print(f"top(max_z={max_z}, max_x={max_x})")

    # pass in an array of the free cad objects (i.e. the mirror and the silicon cell) to set up the scene
    test_scene = otsun.scene.Scene([Mirror, Semi, SilliconBack, Top])

    # establish a rectangular window that the arrays will emanate from
    emitting_region = otsun.source.SunWindow(test_scene,  main_direction)

    # establish a light source based on the scene, the emitting region, as well as the strength of the rays
    light_source = otsun.source.LightSource(test_scene, emitting_region, light_spectrum, init_energy)

    start_t = time.perf_counter()
    print("Starting Trial:", i)

    experiment = otsun.Experiment(test_scene, light_source, number_rays)
    experiment.run()

    efficiency_from_source_Th = (experiment.captured_energy_Th / aperture_collector_Th) / (
        experiment.number_of_rays / experiment.light_source.emitting_region.aperture)

    print(f"experiment.captured_energy_Th {experiment.captured_energy_Th} / aperture_collector_Th {aperture_collector_Th} / experiment.number_of_rays {experiment.number_of_rays} / experiment.light_source.emitting_region.aperture {experiment.light_source.emitting_region.aperture}")
    print("Optical Efficiency:", efficiency_from_source_Th)
    print("Experiment Took:", time.perf_counter() - start_t)


    #-<>-#-<>-# END EXPERIMENT #-<>-#-<>-#
# single_sim()
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

