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
TEMPERATURE = 'temperature'
VOLUME = 'volume'

PRESSURE = 'pressure'
ATM = 'atm'
KPA = 'kpa'
MMHG = 'mmhg'

# stoichiometry
REAGENTS = 'reagents'
PRODUCTS = 'products'

## query types
AIR_PRESSURE - 'air_pressure'
ATOMIC_WEIGHT = 'atomic_weight'
ELEM_USES = 'element_uses'
MATH = 'arithmetic'
OX_STATES = 'oxidation_states'
STOICH = 'stoichiometry'
