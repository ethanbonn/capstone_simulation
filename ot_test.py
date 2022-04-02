FREECAD_PATH = "C:/Program Files/FreeCAD 0.19/bin/"
import sys
sys.path.append(FREECAD_PATH) 

import FreeCAD as App
import Part
import numpy as np
from scipy.integrate import solve_ivp
import Draft
from FreeCAD import Base
import otsun
from cell import mirror, sillicon
WAVELENGTH_IN_NANOMETERS = 7

doc = App.newDocument()

Mirror = mirror(x0=1, y0=1/2, x1=0.9, y1=1/2, x2=1, y2=7/16, width=1 ).getObj()
Semi = sillicon(x1=0.9, y1=1/2, x2=1, y2=7/16, width=1).getObj()

print("boundbox:", Semi.Shape.BoundBox.DiagonalLength)

# print(Mirror.label, Semi.label)

# pass in an array of the free cad objects (i.e. the mirror and the silicon cell) to set up the scene
# Calculating the bounding box of the two objects.

test = Semi.Shape.BoundBox
test.add(Mirror.Shape.BoundBox)
print("full bb:", test, test.DiagonalLength)

# file containing the index of refraction for a perovskite solar cell
file_perovskite = "./sillicon_cell_refraction.txt"

# materials
otsun.ReflectorSpecularLayer("Mir1", 0.95)
otsun.PVMaterial("PV", file_perovskite)



test_scene = otsun.scene.Scene([  Mirror, Semi])
# test_scene = otsun.scene.Scene([ Mirror ])

phi = 0 # 0
theta = 0 #45.0
init_energy = 1 # CHANGE THIS

# establish the direction of the rays
# emitting_region_mainDirection = [1.0, 0.0, 0.0]
main_direction = otsun.polar_to_cartesian(phi, theta) #* -1.0  # Sun direction vector

# establish a rectangular window that the arrays will emanate from
# emitting_region = otsun.source.SunWindow(test_scene,  emitting_region_mainDirection)
emitting_region = otsun.source.SunWindow(test_scene,  main_direction)


light_spectrum = WAVELENGTH_IN_NANOMETERS
number_rays = 100 # need a researched number here

# establish a light source based on the scene, the emitting region, as well as the strength of the rays
light_source = otsun.source.LightSource(test_scene, emitting_region, light_spectrum, init_energy)

experiment = otsun.Experiment(test_scene, light_source, number_rays)

experiment.run()
thermal_energy = experiment.captured_energy_Th
PV_energy = experiment.captured_energy_PV

print('\nThermal energy: ' + str(thermal_energy) + '\nPhotovoltaic energy: ' + str(PV_energy))

