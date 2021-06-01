import constants as c

from enum import Enum
from mendeleev import element
from chempy import balance_stoichiometry   
from chem_util import parse_chemical

""" 
calculate_output.py

This file contains functionality to handle user queries after they have been
received from Watson (see formatter.py for variable structure).

Currently, this file handles:
    - Atomic Weight queries for any chemical
    - Oxidation state queries for elements
    - Queries related to how an element is used
    - Air pressure calculations
    - Stoichiometric calculations

In order to add a handle, simply write a function `handle_task(variables)`, 
add necessary constants to `constants.py`, add the function and name to 
INTENTS_TO_HANDLERS. Of course, the functionality will need to be added
to both the Watson Assistant (see `assistant_skills.json`) and `formatter.py`.
"""
# handle_arithmetic removed due to compatibility issues with Watson, see our final report/challenges
# def handle_arithmetic(variables):
#     """
#     Handler for arithmetic expressions. Leverages Python's interpreter through `eval`
#     to easily calculate arithmetic in common math notation by replacing the carat used
#     for exponentiation in common notation with the double-star operator used in Python.

#     parameters:
#         variables: expected to be a dict object with the key `c.EXPR`, which 
#                 should map to a string containing an arithmetic expression
                
#     returns:
#         string containing uses for an element
#     """
#     if c.EXPR not in variables:
#             return None
#     return str(eval(variables[c.EXPR].replace('^', '**')))


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
    elem = element(variables[c.ELEMENT].title())
    return elem.oxistates


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
    elem = element(variables[c.ELEMENT].title())  # title casing (see str docs) required by mendeleev for some reason
    return elem.uses


def handle_ideal_gas(variables):
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
    temperature = variables[c.TEMPERATURE]
    n_mols = variables[c.NMOLS]

    R = 0.0821 # L·atm/(mol·K)

    # standardize the pressure unit to atmospheres
    if pressure.value != c.UNK:
        if pressure.units == c.PA:              p = pressure.value * c.PA_TO_ATM
        elif pressure.units == c.KPA:           p = pressure.value * c.KPA_TO_ATM
        elif pressure.units == c.ATM:           p = pressure.value
    
    if volume.value != c.UNK:
        if volume.units == c.MILILITERS:        v = volume.value * c.ML_TO_L
        elif volume.units == c.GALLONS:         v = volume.value * c.GAL_TO_L
        elif volume.units == c.LITERS:          v = volume.value
    
    if temperature.value != c.UNK:
        if temperature.units == c.CELSIUS:      t = temperature.value + c.C_TO_K
        elif temperature.units == c.FARENHEIT:  t = (temperature.value - 32.) * 5./9. + c.C_TO_K # Unfortunately has to be hard-coded
        elif temperature.units == c.KELVIN:     t = temperature.value

    if n_mols != c.UNK:
        n = n_mols

    if pressure.value == c.UNK:
        p = (n * R * t) / v
        if pressure.value == c.PA:              return p / c.PA_TO_ATM
        elif variables[1] == c.KPA:             return p / c.KPA_TO_ATM
        elif variables[1] == c.ATM:             return p
        else:                                   return None

    if volume.value == c.UNK:
        v = (n * R * t) / p
        if volume.units == c.MILILITERS:        return v / c.ML_TO_L
        if volume.units == c.GALLONS:           return v / c.GAL_TO_L
        elif volume.units == c.LITERS:          return v
        else:                                   return None

    if temperature.value == c.UNK:
        t = (n * R) / (p * v)
        if temperature.units == c.CELSIUS:      return t - c.C_TO_K
        elif temperature.units == c.FARENHEIT:  return (t - c.C_TO_K) * 9/5 + 32
        elif temperature.units == c.KELVIN:     return t
        else:                                   return None

    if n_mols == c.UNK:
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
    print(variables[c.REAGENTS])
    # prepare user input for use in chempy by using parse_chemical to standardize format
    reagents = set(parse_chemical(reagent, output='chempy').name
                for reagent in variables[c.REAGENTS])
    products = set(parse_chemical(product, output='chempy').name
                for product in variables[c.PRODUCTS])

    # using balance_stoichiometry from chempy
    reagents, products = balance_stoichiometry(reagents, products)
    
    # build response string from balance_stoichiometry results
    # format: 2 H2O + 1 O2 ==> 2 H2O2
    response = ''
    for reagent, count in reagents.items():
        response += f'{count} {reagent} + '

    response = response[:-2] + '==> '
    for product, count in products.items():
        response += f'{count} {product} + '

    return response[:-3] # remove trailing ' + ' from above

# helper variable to easily match intents to their handler functions
# listed in order that they appear in this file
INTENTS_TO_HANDLERS = {
    # c.MATH: handle_arithmetic, removed due to compatibility, see explanation in challenges section of report
    c.ATOMIC_WEIGHT: handle_atomic_weight,
    c.OX_STATES: handle_ox_states,
    c.ELEM_USES: handle_elem_uses,
    c.IDEAL_GAS: handle_ideal_gas,
    c.STOICH: handle_stoich
}


# Simply calls the appropriate handler for the provided intent
def handle_query(intent, variables):
    if intent not in INTENTS_TO_HANDLERS:
        raise NotImplementedError(f'Intent {intent} is not recognized')

    return INTENTS_TO_HANDLERS[intent](variables)


# input data is a dict containing keys intent and variables
def calculate_output(watson_data):
    """
    Given data from a Watson Assistant interaction represented as a Python dict,
    generate a response to the interaction.

    parameters:
        watson_data -- a dict with keys `intent` and `variables`

    returns:
        string response to the query
    """
    intent = watson_data["intent"] # string
    variables = watson_data["variables"] # format depends on intent

    return handle_query(intent, variables)


# # Examples of how to use the above functions

# user_inputs = {
#     c.INTENT: c.ATOMIC_WEIGHT,
#     c.VARS: {
#         c.CHEMICAL: 'caffeine'
#     }
# }
# print(calculate_output(user_inputs))

# user_inputs = {
#     c.INTENT: c.ELEM_USES,
#     c.VARS: {
#         c.ELEMENT: 'nickel'
#     }
# }
# print(calculate_output(user_inputs))

# user_inputs = {
#     c.INTENT: c.OX_STATES,
#     c.VARS: {
#         c.ELEMENT: 'nitrogen'
#     }
# }
# print(calculate_output(user_inputs))

# user_inputs = {
#     c.INTENT: c.IDEAL_GAS,
#     c.VARS: {
#         c.PRESSURE: c.Measurement(3.5, c.ATM),
#         c.VOLUME: c.Measurement(1, c.MILILITERS),
#         c.NMOLS: c.Measurement(12, 'unitless'),
#         c.TEMPERATURE: c.Measurement(c.UNK, c.FARENHEIT)
#     }
# }
# print(calculate_output(user_inputs))

# user_inputs = {
#     c.INTENT: c.STOICH,
#     c.VARS: {
#         c.REAGENTS: ['glucose', 'o2'],
#         c.PRODUCTS: ['h2o', 'co2']
#     }
# }
# print(calculate_output(user_inputs))