import methods as methods
import json as json
from matplotlib import pyplot as plt
import numpy as np
import scipy as scipy
from scipy.integrate import cumulative_trapezoid
from pvd_class import*
import math
import my_plotter_methods as myPlotter


## INPUT DATA
#relativePath =  "19_01_2023_sirius_internal_V20_f1190_velocity.pvd"
fullPath=  "C:\\Users\\leys40\\OneDrive - imec\\Gargamel 2.0\\TOOLS\\MSA-600\\Measurements\\analysis\\19_01_2023_sirius_internal_V20_f1190_velocity.pvd"
myPVD = Pvd(filePath = fullPath)
measurementFrequency = 625000            # TODO get from settingsFile!! or pvd file
voltageFrequency = 1090                  # TODO get from settingsFile
voltageAmplification = 50                # TODO: measure this, to check impedance matching 
displacementAmplification = 125000*100

## DATA ANALYSIS
velocity = displacementAmplification* myPVD.get_velocity()
voltage = voltageAmplification * myPVD.get_voltage()

# SHIFTING: start from 0 voltage in time domain
zero_crossings = np.where(np.diff(np.sign(voltage)))[0]
firstZeroCrossing = zero_crossings[0]
voltageShifted = voltage[firstZeroCrossing:]
velocityShifted = velocity[firstZeroCrossing:]

# CUTTING: keep only an integer number of periods
amountOfVoltageDataPoints = voltageShifted.size
dataPointsInOneVoltagePeriod = measurementFrequency/voltageFrequency
fullVoltagePeriodsInMeasurement = math.floor(amountOfVoltageDataPoints/dataPointsInOneVoltagePeriod)
totalDatapointsNeeded = math.floor(dataPointsInOneVoltagePeriod*fullVoltagePeriodsInMeasurement)
print("fullVoltagePeriodsInMeasurement: " + str(fullVoltagePeriodsInMeasurement))
print("totalDatapointsNeeded: " + str(totalDatapointsNeeded))
voltageShiftedCutted = voltageShifted[:totalDatapointsNeeded]
velocityShiftedCutted = velocityShifted[:totalDatapointsNeeded]

# FLATTING: remove constant noice term
zeroDrift = np.average(velocityShiftedCutted)
velocityShiftedCuttedFlattended = velocityShiftedCutted-zeroDrift

# DISPLACEMENT (two methods)
timeStep = 1/measurementFrequency
displacementCumsum = np.cumsum(velocityShiftedCuttedFlattended)*timeStep
displacementScipy = cumulative_trapezoid(velocityShiftedCuttedFlattended, dx = timeStep)



## PLOTS

# # DV PLOT
# filename = "first_msa600_DV"
# myPlotter.DV_plot(displacementCumsum , voltageShiftedCutted, filename) # times two for voltage is probably because of impedance matching // can be avoided

# Time Domain
plt.plot(2*velocityShiftedCuttedFlattended) 
plt.plot(15000*displacementCumsum)
plt.plot(voltageShiftedCutted)
plt.axhline(y=0, color='r', linestyle='-')
plt.xlabel('Index')
plt.ylabel('Value')
plt.title('1D Vector Data')
plt.show()


#TODO
# - absolute values (understand)
# - measurementfrequency and other data from settings
# - leren werken met pandas, docker, ...
# - expand my_plotter_methods
# - clean up code

# meting: - starten voor exitatie ?
# meting: - meer periodes 
# meting: - always trigger (we already do that for the averaging)
# meting: - always picture with measurement position on beam