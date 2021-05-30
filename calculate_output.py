
from mendeleev import *

def calculate_output(result):
    calculation_type = result["intent"]
    variables = result["variables"]
    if calculation_type == "AskingMath":
        if len(variables) != 3:
            return None
        return eval(str(variables["number"]) + variables["Operator"] + str(variables["number_2"]))
    elif calculation_type == "AskingMass":
        if len(variables) < 2:
            return None
        # sum = 0
        current_multiplier = variables["number"]
        e = element(variables["ChemicalElement"])
        # for i in range(len(variables) - 1):
        #     if (i + 1)%2 == 1:
        #         current_multiplier = int(variables[i + 1])
        #     else:
        #         element = element(variables[i + 1])
        #         sum += current_multiplier * element.atomic_weight
        return current_multiplier * e.atomic_weight
    
    elif calculation_type == "AskingGas":

        if len(variables < 4):
            return None
        pressure = float(variables[1]) # atm
        volume = float(variables[2]) # liters
        number = float(variables[3]) # moles
        R = 0.0821 # L·atm/(mol·K)
        temperature = float(variables[4]) # Kelvin
        
        if variables[1] == "Unknown":
            return (number * R * temperature) / volume
        if variables[2] == "Unknown":
            return (number * R * temperature) / pressure
        if variables[3] == "Unknown":
            return (R * temperature) / (pressure * volume)
        if variables[4] == "Unknown":
            return (number * R) / (pressure * volume)