import constants as c

from enum import Enum
from mendeleev import *
from chempy import *    
from chem_util import parse_chemical_name, parse_chemical_formula, parse_chemical


def handle_arithmetic(variables):
    if c.EXPR not in variables:
            return None
    return eval(variables[c.EXPR])

def handle_atomic_weight(variables):
    if c.CHEMICAL not in variables:
        return None
    
    return parse_chemical(variables[c.CHEMICAL], output='atomic_weight')

def handle_ox_states(variables):
    if len(variables) < 1:
        return None
    element = element(variables[0])
    return element.oxistates

def handle_elem_uses(variables):
    if len(variables) < 1:
        return None
    element = element(variables[0])
    return element.uses

def handle_asking_gas(variables):
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

def handle_stoich(variables):
    if len(variables) < 2:
        return None
    reactants, products = balance_stoichiometry(variables[0], variables[1])
    return reactants, products

# Input result is a dict
def calculate_output(result):
    calculation_type = result["intent"] # string
    variables = result["variables"] # list

    if calculation_type == c.MATH:
        return handle_arithmetic(variables)
    
    # Takes as input a name or formula of a chemical
    elif calculation_type == c.ATOMIC_WEIGHT:
        return handle_atomic_weight(variables)

    # Takes as input a single string, an element
    elif calculation_type == c.OX_STATES:
        return handle_ox_states(variables)
    
    # Takes as input a single string, an element
    elif calculation_type == c.ELEM_USES:
        return handle_elem_uses(variables)
    
    # Takes as input four floats (can be in string form)
    elif calculation_type == "AskingGas":
        return handle_asking_gas(variables)

    # Takes as input two dictionaries, reactants and products. Only keys in these dicts, 
    # as values get assigned after stoichiometry is done
    elif calculation_type == c.STOICH:
        return handle_stoich(variables)
        
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