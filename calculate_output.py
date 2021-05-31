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

# helper variable to easily match intents to their handler functions
# listed in order that they appear in this file
INTENTS_TO_FNS = {
    c.MATH: handle_arithmetic,
    c.ATOMIC_WEIGHT: handle_atomic_weight,
    c.OX_STATES: handle_ox_states,
    c.ELEM_USES: handle_elem_uses,
    c.STOICH: handle_stoich
}

def handle_query(intent, variables):
    if intent not in INTENTS_TO_FNS:
        raise NotImplementedError(f'Intent {intent} is not recognized')

    return INTENTS_TO_FNS[intent](variables)

# Input result is a dict
def calculate_output(result):
    intent = result["intent"] # string
    variables = result["variables"] # format depends on intent

    return handle_query(intent, variables)
        
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