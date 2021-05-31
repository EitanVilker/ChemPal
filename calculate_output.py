import constants as c

from enum import Enum
from mendeleev import *
from chempy import *    
from chem_util import parse_chemical_name, parse_chemical_formula, parse_chemical


# Input result is a dict
def calculate_output(result):
    calculation_type = result["intent"] # string
    variables = result["variables"] # list

    if calculation_type == c.MATH:
        if c.EXPR not in variables:
            return None
        return eval(variables[c.EXPR])

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
    elif calculation_type == c.ATOMIC_WEIGHT:
        if c.CHEMICAL not in variables:
            return None
        
        return parse_chemical(variables[c.CHEMICAL], output='atomic_weight')
        
        # sum = 0
        # current_multiplier = 1
        #
        # for i in range(len(variables)):
        #     if i % 2 == 0:
        #         current_multiplier = int(variables[i])
        #     else:
        #         e = element(variables[i])
        #         sum += current_multiplier * e.atomic_weight
        # return sum
    
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

    # Takes as input a single string, an element
    elif calculation_type == c.OX_STATES:
        if len(variables) < 1:
            return None
        element = element(variables[0])
        return element.oxistates
    
    # Takes as input a single string, an element
    elif calculation_type == c.ELEM_USES:
        if len(variables) < 1:
            return None
        element = element(variables[0])
        return element.uses

    # Takes as input two dictionaries, reactants and products. Only keys in these dicts, 
    # as values get assigned after stoichiometry is done
    elif calculation_type == c.STOICH:
        if len(variables) < 2:
            return None
        reactants, products = balance_stoichiometry(variables[0], variables[1])
        return reactants, products
        
user_inputs = {
    'intent': c.ATOMIC_WEIGHT,
    'variables': {
        'chemical': 'glucose'
    }
}
user_inputs = {
    'intent': c.MATH,
    'variables': {
        'expression': '4 * 7 - 13 ^ 2'.replace('^', '**') # TODO Convert ^ to ** in expressions
    }
}

print(calculate_output(user_inputs))