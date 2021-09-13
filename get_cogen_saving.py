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
    
    #Costs
    ch4_purchase_cost = input_power * CH4_PRICE / HEATING_CH4_POWER
    maintenance_cost = electric_power * MAINTENANCE_COGENERATOR_PRICE
    tax_cost = electric_power * TAX_PRICE
    distribution_pump_cost = DISTRIBUTION_PUMP_POWER * ELECTRIC_ENERGY_PRICE

    #Revenues and savings
    if requested_electric_power < electric_power:
        electric_energy_revenue = (electric_power - requested_electric_power) * ELECTRIC_ENERGY_SOLD_PRICE
        electric_energy_saving = requested_electric_power * ELECTRIC_ENERGY_PRICE
    else:
        electric_energy_revenue = 0
        electric_energy_saving = electric_power * ELECTRIC_ENERGY_PRICE

    if requested_thermal_power < thermal_power:
        thermal_energy_saving = requested_thermal_power * EFFECTIVE_KWH_COST
    else:
        thermal_energy_saving = thermal_power * EFFECTIVE_KWH_COST
    
    classic_heating_water_electric_saving = thermal_power / classic_water_heater_thermal_power * classic_water_heater_electric_power * ELECTRIC_ENERGY_PRICE
    government_revenue = GOVERNMENT_BENEFIT * electric_power
    

    total_costs = ch4_purchase_cost + maintenance_cost + tax_cost + distribution_pump_cost
    total_savings = electric_energy_saving + thermal_energy_saving + classic_heating_water_electric_saving
    total_revenues = electric_energy_revenue + government_revenue

    print(f"{total_costs} - {total_savings} - {total_revenues}")

    print(f"{total_costs} - {total_savings+total_revenues}")

    print(f"BALANCE: {total_savings+total_revenues-total_costs} \n")

# If this program was run (instead of imported), run the script:
if __name__ == "__main__":
    import sys
    get_cogen_saving(float(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]))