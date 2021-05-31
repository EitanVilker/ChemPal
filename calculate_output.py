import constants as c

from enum import Enum
from mendeleev import *
from chempy import *    
from chem_util import parse_chemical_name, parse_chemical_formula, parse_chemical


def handle_arithmetic(variables):
    """
    Handler for arithmetic expressions. Leverages Python's interpreter through `eval`
    to easily calculate arithmetic in common math notation by replacing the carat used
    for exponentiation in common notation with the double-star operator used in Python.

    parameters:
        variables: expected to be a dict object with the key `c.EXPR`, which 
                should map to a string containing an arithmetic expression
                
    returns:
        string containing uses for an element
    """
    if c.EXPR not in variables:
            return None
    return eval(variables[c.EXPR].replace('^', '**')) 


def handle_atomic_weight(variables):
    """
    Handler for atomic weight lookup for a chemical. 

    parameters:
        variables: expected to be a dict object with the key constants.CHEMICAL, 
                which should be a string containing a chemical name or formula
                
    returns:
        string containing atomic weight of the chemical
    """
    if c.CHEMICAL not in variables:
        return None
    
    return parse_chemical(variables[c.CHEMICAL], output='atomic_weight')


def handle_ox_states(variables):
    """
    Handler for lookups for element oxidation states. 

    parameters:
        variables: expected to be a dict object with the key constants.ELEMENT, 
                which should be a string containing an element name or symbol
                
    returns:
        string containing oxidation states for an element
    """
    if len(variables) < 1:
        return None
    element = element(variables[0])
    return element.oxistates


def handle_elem_uses(variables):
    """
    Handler for lookups for element uses. 

    parameters:
        variables: expected to be a dict object with the key constants.ELEMENT, 
                which should be a string containing an element name or symbol
                
    returns:
        string containing uses for an element
    """
    if len(variables) < 1:
        return None
    element = element(variables[0])
    return element.uses


def handle_asking_gas(variables):
    """
    Handler for `pv=nrt` calculations. 

    parameters:
        variables: expected to be a dict object with the keys `c.PRESSURE`, `c.VOLUME`,
                `c.NMOLS`, and `c.TEMPERATURE`, which should each be of type c.Measurement
                to facilitate calculations
    returns:
        string containing air presure calculation output
    """
    # TODO Update to use dict of labelled variables with units
    # TODO Add code to convert units
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
    """
    Handler for stoichiometry calculations. Uses ChemPy's  `balance_stoichiometry` to 
    calculate the resulting ratios to balance a chemical equation.

    parameters:
        variables: expected to be a dict object with the keys `reagents` and `products`
                which should each contain a list of strings representing chemicals in a
                stoichiometry problem
    returns:
        string containing stoichiometry output
    """
    if c.REAGENTS not in variables or c.PRODUCTS not in variables:
        return None
    
    reagants = [parse_chemical(reagant, format='chempy') 
                for reagant in variables[c.REAGANTS]]
    products = [parse_chemical(product, format='chempy')
                for product in variables[c.PRODUCTS]]

    return balance_stoichiometry(reagents, products)
    

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


## Examples of how to use the above functions

# user_inputs = {
#     'intent': c.ATOMIC_WEIGHT,
#     'variables': {
#         'chemical': 'glucose'
#     }
# }
# user_inputs = {
#     'intent': c.MATH,
#     'variables': {
#         'expression': '4 * 7 - 13 ^ 2'.replace('^', '**') # TODO Convert ^ to ** in expressions
#     }
# }

# print(calculate_output(user_inputs))