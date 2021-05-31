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
