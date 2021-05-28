
from mendeleev import *

def calculate_output(variables):

    if len(variables) < 2:
        return None
    calculation_type = variables[0]

    if calculation_type == "Multiplication":
        if len(variables) != 3:
            return None
        return float(variables[1]) * float(variables[2])

    elif calculation_type == "Addition":
        if len(variables) < 3:
            return None
        sum = 0
        for i in range(len(variables) - 1):
            sum += float(variables[i + 1])
        return sum
    
    elif calculation_type == "Division":
        if len(variables) != 3:
            return None
        return float(variables[1]) / float(variables[2])

    elif calculation_type == "Subtraction":
        if len(variables) < 3:
            return None
        difference = float(variables[1])
        for i in range(len(variables) - 2):
            difference -= float(variables[i + 2])
        return difference
    
    elif calculation_type == "Atomic Mass":
        if len(variables) < 3:
            return None
        sum = 0
        current_multiplier = 1
        element = "H"
        for i in range(len(variables) - 1):
            if (i + 1)%2 == 1:
                current_multiplier = int(variables[i + 1])
            else:
                element = element(variables[i + 1])
                sum += current_multiplier * element.atomic_weight
        return sum
    
    elif calculation_type == "Ideal Gas":

        if len(variables < 5):
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