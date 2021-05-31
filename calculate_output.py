
from mendeleev import *
from chempy import *    

# Input result is a dict
def calculate_output(result):
    calculation_type = result["intent"] # string
    variables = result["variables"] # list

    if calculation_type == "Multiplication":
        if len(variables) != 3:
            return None
        return float(variables[0]) * float(variables[1])

    elif calculation_type == "Addition":
        if len(variables) < 2:
            return None
        sum = 0
        for i in range(len(variables)):
            sum += float(variables[i])
        return sum
    
    elif calculation_type == "Division":
        if len(variables) != 2:
            return None
        return float(variables[0]) / float(variables[1])

    elif calculation_type == "Subtraction":
        if len(variables) < 2:
            return None
        difference = float(variables[0])
        for i in range(len(variables) - 1):
            difference -= float(variables[i + 1])
        return difference
    
    # Takes as input a list of alternating ints and strings
    elif calculation_type == "Atomic Weight":
        if len(variables) < 2:
            return None
        sum = 0
        current_multiplier = 1
        e = "H"
        for i in range(len(variables)):
            if i % 2 == 1:
                sum += int(variables[i]) * e.atomic_weight
            else:
                e = element(variables[i])
        return sum
    
    # Takes as input four floats (can be in string form)
    elif calculation_type == "AskingGas":

        if len(variables < 4):
            return None
        pressure = float(variables[0]) # atm
        volume = float(variables[1]) # liters
        number = float(variables[2]) # moles
        R = 0.0821 # L·atm/(mol·K)
        temperature = float(variables[3]) # Kelvin

        if variables[0] == "unknown":
            return (number * R * temperature) / volume
        if variables[1] == "unknown":
            return (number * R * temperature) / pressure
        if variables[2] == "unknown":
            return (R * temperature) / (pressure * volume)
        if variables[3] == "unknown":
            return (number * R) / (pressure * volume)

    # Takes as imput a single string, an element
    elif calculation_type == "Oxidations States":
        if len(variables) < 1:
            return None
        element = element(variables[0])
        return element.oxistates
    
    # Takes as input a single string, an element
    elif calculation_type == "Element Uses":
        if len(variables) < 1:
            return None
        element = element(variables[0])
        return element.uses

    # Takes as input two dictionaries, reactants and products. Only keys in these dicts, 
    # as values get assigned after stoichiometry is done
    elif calculation_type == "Stoichiometry":
        if len(variables) < 2:
            return None
        reactants, products = balance_stoichiometry(variables[0], variables[1])
        return reactants, products
        