import numpy as np
import collections

def get_cogen_saving(cogen_functioning_regime, requested_electric_power, requested_thermal_power):
    """Get the saving in % using the cogenerator giving the
    - cogen_functioning_regime float number from 0 to 1
    - requested_electric_power int number from 1 to 1.000 in kW 
    - requested_thermal_power int number from 1 to 1.000 in kW
    
    example: get_cogen_saving(0.7, 294, 350)
    returns 0.50 that means 50% of saving using the cogenerator instead of not using it """

    if cogen_functioning_regime <= 0 or cogen_functioning_regime > 1:
        raise ValueError("Cogeneratore regime value must be between 0 and 1")
    
    if requested_electric_power < 0:
        raise ValueError("Requested electtric energy must be a positive number")
    
    if requested_thermal_power < 0:
        raise ValueError("Requested thermal energy must be a positive number")

    #MEP system constants
    MAX_ELECTRIC_COGENERATOR_POWER = 294  #kW
    CLASSIC_WATER_HEATER_EFFICIENCY = 0.85
    HOT_WATER_DISTRIBUTION_EFFICIENCY = 0.9
    HEATING_CH4_POWER = 9.6  #
    DISTRIBUTION_PUMP_POWER = 7.5 #kw (electric)
    
    #MONEY-RELATED CONSTANTS
    EFFECTIVE_KWH_COST = 0.05  #€/kwh (thermal)
    ELECTRIC_ENERGY_SOLD_PRICE = 0.05  #€/kwh (electric)
    ELECTRIC_ENERGY_PRICE = 0.185   #€/kwh (electric)
    CH4_PRICE = 0.27  #€/SMc
    MAINTENANCE_COGENERATOR_PRICE = 0.03  #€/kwh (electric)
    TAX_PRICE = 0.0125  #€/kwh (electric)
    GOVERNMENT_BENEFIT = 39/339011 * 250  #€/kwh (electric)
    
    #Derived constants
    auxiliary_cogenerator_electric_power = 0.005 * MAX_ELECTRIC_COGENERATOR_POWER  #kw (electric)
    classic_water_heater_electric_power = 1  #kw (electric)
    classic_water_heater_thermal_power = 700  #kw (thermal)

    functioning_regimes_list = [0.5, 0.625, 0.75, 1]
    electric_power_list = [147, 183.75, 220.5, 294]
    global_efficiency_list = [0.871, 0.8635, 0.856, 0.832]
    electric_efficiency_list = [0.339, 0.351, 0.363, 0.3764]
    thermal_efficiency_list = [0.533, 0.513, 0.493, 0.456]

    electric_power = np.interp(cogen_functioning_regime, functioning_regimes_list, electric_power_list)
    global_efficiency = np.interp(cogen_functioning_regime, functioning_regimes_list, global_efficiency_list)
    electric_efficiency = np.interp(cogen_functioning_regime, functioning_regimes_list, electric_efficiency_list)
    thermal_efficiency = np.interp(cogen_functioning_regime, functioning_regimes_list, thermal_efficiency_list)

    input_power = electric_power / electric_efficiency

    thermal_power = input_power * thermal_efficiency
        
    costs = collections.defaultdict(dict)
    revenues = collections.defaultdict(dict)

    costs["no cogen"]["ch4"] = requested_thermal_power * EFFECTIVE_KWH_COST
    costs["no cogen"]["electric energy"] = requested_electric_power * ELECTRIC_ENERGY_PRICE
    costs["no cogen"]["classic water heater electric energy"] = classic_water_heater_electric_power * ELECTRIC_ENERGY_PRICE

    costs["cogen"]["ch4"] = input_power * CH4_PRICE / HEATING_CH4_POWER

    if requested_thermal_power > thermal_power:
        costs["cogen"]["ch4"] += (requested_thermal_power-thermal_power) * EFFECTIVE_KWH_COST
    
    costs["cogen"]["maintainance"] = electric_power * MAINTENANCE_COGENERATOR_PRICE
    costs["cogen"]["tax"] = electric_power * TAX_PRICE
    costs["cogen"]["distribution pump"] = DISTRIBUTION_PUMP_POWER * ELECTRIC_ENERGY_PRICE
    costs["cogen"]["classic water heater electric energy"] = (1 - thermal_power / classic_water_heater_thermal_power) * classic_water_heater_electric_power * ELECTRIC_ENERGY_PRICE

    if requested_electric_power > electric_power:
        costs["cogen"]["electric energy"] = (requested_electric_power-electric_power) * ELECTRIC_ENERGY_PRICE
    
    if requested_electric_power < electric_power:
        revenues["cogen"]["electric energy"] = (electric_power - requested_electric_power) * ELECTRIC_ENERGY_SOLD_PRICE
    else:
        revenues["cogen"]["electric energy"] = 0

    revenues["cogen"]["government"] = GOVERNMENT_BENEFIT * electric_power

    no_cogen_total_costs = sum(costs["no cogen"].values())
    cogen_total_costs = sum(costs["cogen"].values())
    cogen_total_revenues = sum(revenues["cogen"].values())

    print(f"TOTAL NO COGEN COSTS: {no_cogen_total_costs} €")
    print(f"++ TOTAL COGEN COSTS: {cogen_total_costs} €")
    print(f"TOTAL COGEN REVENUE: {cogen_total_revenues} €")
    print(f"++ TOTAL COGEN COSTS-REVENUES: {cogen_total_costs - cogen_total_revenues} €")
    print(f"BALANCE:  {no_cogen_total_costs+cogen_total_revenues-cogen_total_costs}")

# If this program was run (instead of imported), run the script:
if __name__ == "__main__":
    import sys
    get_cogen_saving(float(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]))
