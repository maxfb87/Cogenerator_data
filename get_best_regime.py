from get_cogen_saving import get_cogen_saving
from decimal import *
import numpy as np

getcontext().prec = 2

def get_best_regime(requested_electric_power, requested_thermal_power, optional_args = []):
    """ This function returns the regimes that has the highest saving value.
    Regimes to compare are fixed and they start from 0.5 to 1 with step of 0.05
    Input values (the order must be respected):
    - requested_electric_power: int number from 1 to 1.000 in kW 
    - requested_thermal_power: int number from 1 to 1.000 in kW
    - [optional args list]
        "-verbose" (Verbose mode) if specified, the function prints the saving value for every regime
    Output value:
    - best_regime: float number from 0.5 to 1 with step of 0.05

    example: get_best_regime(200, 300)
    returns 0.75 that means that the best regime with those input values is 0.75

    """
    if "-verbose" in optional_args:
        verbose_mode = True
    else:
        verbose_mode = False
    
    first_regime_value = 0.5
    last_regime_value = 1.05
    step_regime_value = 0.05

    regimes = list(np.arange(Decimal(first_regime_value), Decimal(last_regime_value), Decimal(step_regime_value)))
    #print(regimes)
    best_regime = regimes[0]
    best_saving = 0

    separation_string = "*"*10

    for regime in regimes:
        saving = get_cogen_saving(regime, requested_electric_power, requested_thermal_power)
        if verbose_mode:
            if regime == first_regime_value:
                print(separation_string)
                print(f"REGIME:  {regime}  SAVING: {saving}")
            if regime == regimes[-1]:
                print(f"REGIME:  {regime}  SAVING: {saving}")
                print(separation_string)
                print("\n")
            else:
                print(f"REGIME:  {regime}  SAVING: {saving}")
                
        #print(f"REGIME:  {regime}  SAVING: {saving}")
        if saving > best_saving:
            best_regime = regime
            best_saving = saving
    
    return best_regime

# If this program was run (instead of imported), run the script:
if __name__ == "__main__":
    import sys
    optional_args = sys.argv[3:]
    best_regime = get_best_regime(int(sys.argv[1]), int(sys.argv[2]), optional_args)
    print(f"BEST REGIME: {str(best_regime)}")