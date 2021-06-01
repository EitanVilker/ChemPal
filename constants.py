## variable names
# arithmetic
from collections import namedtuple


EXPR = 'expression'

# general chemistry
CHEMICAL = 'chemical'
ELEMENT = 'element'
Measurement = namedtuple('Measurement', ['value', 'units'])

# air pressure
NMOLS = 'n_moles'
PRESSURE = 'pressure'
TEMPERATURE = 'temperature'
VOLUME = 'volume'

# stoichiometry
REAGENTS = 'reagents'
PRODUCTS = 'products'

## query types
ATOMIC_WEIGHT = 'atomic_weight'
ELEM_USES = 'element_uses'
MATH = 'arithmetic'
OX_STATES = 'oxidation_states'
STOICH = 'stoichiometry'

## unit conversions - if converting in opposite direction, simply divide instead of multiply
PA_TO_ATM = 1 / 101325
KPA_TO_ATM = PA_TO_ATM * 1000
PA_TO_KPA = 1 / 1000
ML_TO_L = 1 / 1000
C_TO_K = 273.15 # add instead of multiply