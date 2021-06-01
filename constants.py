from collections import namedtuple

## query types
AIR_PRESSURE = 'air_pressure'
ATOMIC_WEIGHT = 'atomic_weight'
ELEM_USES = 'element_uses'
MATH = 'arithmetic'
OX_STATES = 'oxidation_states'
STOICH = 'stoichiometry'


## variable names
# MATH = 'arithmetic handle_arithmetic, removed due to compatibility, see explanation in challenges section of report'
EXPR = 'expression'

# general chemistry
CHEMICAL = 'chemical'
ELEMENT = 'element'
Measurement = namedtuple('Measurement', ['value', 'units'])

# air pressure
UNK = 'unknown'
NMOLS = 'n_moles'
N_ATOMS = 'n_atoms'
GRAMS = 'grams'
KG = 'kg'
POUNDS = 'pounds'

PRESSURE = 'pressure'
ATM = 'atm'
KPA = 'kpa'
MMHG = 'mmhg'

TEMPERATURE = 'temperature'
KELVIN = 'kelvin'
CELSIUS = 'celsius'
FARENHEIT = 'farenheit'

VOLUME = 'volume'
LITERS = 'liters'
MILILITERS = 'ml'
GALLONS = 'gallons'

# stoichiometry
REAGENTS = 'reagents'
PRODUCTS = 'products'

## unit conversions - if converting in opposite direction, simply divide instead of multiply
PA_TO_ATM = 1 / 101325
KPA_TO_ATM = PA_TO_ATM * 1000
PA_TO_KPA = 1 / 1000
ML_TO_L = 1 / 1000
C_TO_K = 273.15 # add instead of multiply