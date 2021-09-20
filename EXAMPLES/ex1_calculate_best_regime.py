import os
from os import getcwd
from pathlib import Path
import sys

from numpy.lib.utils import info

path = getcwd()
sys.path.append(path)

from get_cogen_saving import get_cogen_saving
from get_best_regime import get_best_regime
import pandas as pd

file_path = os.path.join(path, "EXAMPLES", "ex1_input_data.csv")

#print(file_path)

requested_power = pd.read_csv(file_path)

requested_power["Best_Regime"] = requested_power.apply(lambda row: get_best_regime(row["Requested_Electric_Power"], row["Requested_Thermal_Power"]), axis=1)

#Now requested_energy["Best_Regime"] contains the best regime to use the cogenerator
#with the given "Requested_Electric_Power" and "Requested_Thermal_Power"

print(requested_power.head(30))
print(requested_power.info())
