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
    return str(eval(variables[c.EXPR].replace('^', '**')))


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


def handle_air_pressure(variables):
    """
    Handler for `pv=nrt` calculations. 

    parameters:
        variables: expected to be a dict object with the keys `c.PRESSURE`, `c.VOLUME`,
                `c.NMOLS`, and `c.TEMPERATURE`, which should each be of type c.Measurement
                to facilitate calculations
    returns:
        string containing air presure calculation output
    """
    # TODO Add code to convert units
    if c.PRESSURE not in variables \
            or c.VOLUME not in variables \
            or c.NMOLS not in variables \
            or c.TEMPERATURE not in variables:
        return None

    pressure = variables[c.PRESSURE]
    volume = variables[c.VOLUME]
    temperature = variables[c.NMOLS]
    n_mols = variables[c.TEMPERATURE]

    volume = 0
    number = 0
    temperature = 0
    R = 0.0821 # L·atm/(mol·K)

    # standardize the pressure unit to atmospheres
    if pressure.value != c.UNK:
        if pressure.units == c.PA:              p = pressure.value * c.PA_TO_ATM
        elif pressure.units == c.KPA:           p = pressure.value * c.KPA_TO_ATM
        elif pressure.units == c.ATM:           p = pressure.value
    
    if volume.value != c.UNK:
        if volume.units == c.MILILITERS:        v = volume.value * c.ML_TO_L
        elif volume.units == c.LITERS:          v = volume.value
    
    if temperature.value != c.UNK:
        if temperature.units == c.CELSIUS:      t = temperature.value + c.C_TO_K
        elif temperature.units == c.FARENHEIT:  t = (temperature.value - 32.) * 5./9. + c.C_TO_K # Unfortunately has to be hard-coded
        elif temperature.units == c.KELVIN:     t = temperature.value

    if n_mols.value != c.UNK:
        number = n_mols.value

    if pressure.value == c.UNK:
        p = (n * R * t) / v
        if pressure.value == c.PA:              return p * 1/c.PA_TO_ATM
        elif variables[1] == c.KPA:             return p * 1/c.KPA_TO_ATM
        elif variables[1] == c.ATM:             return p
        else:                                   return None

    if volume.value == c.UNK:
        v = (n * R * t) / p
        if volume.units == c.MILILITERS:        return v * 1 / c.ML_TO_L
        elif volume.units == c.LITERS:          return v
        else:                                   return None

    if temperature.value == c.UNK:
        t = (n * R) / (p * v)
        if temperature.units == c.CELSIUS:      return t - c.C_TO_K
        elif temperature.units == c.FARENHEIT:  return (t - c.C_TO_K) * 9/5 + 32
        elif temperature.units == c.KELVIN:     return t
        else:                                   return None
    if n_mols.value == c.UNK:
        return (R * t) / (p * v)
    return None


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
    c.AIR_PRESSURE: handle_air_pressure,
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


# # Examples of how to use the above functions

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