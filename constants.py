from collections import namedtuple

## Watson variables
VARS = 'variables'
WATSON_CHEM = 'ChemicalCompound'
WATSON_ELEM = 'ChemicalElement'
WATSON_REAGANT0 = 'Reactant0'
WATSON_REAGANT1 = 'Reactant1'
WATSON_PRODUCT0 = 'Product0'
WATSON_PRODUCT1 = 'Product1'

# intents
INTENT = 'intent'
INTENTS = 'intents'
ATOMIC_WEIGHT = 'AskingMass'
ELEM_USES = 'AskingElementUses'
IDEAL_GAS = 'AskingGas'
# MATH = 'AskingArithmetic'
OX_STATES = 'AskingOxidationStates'
STOICH = 'AskingStoichiometry'


## simple math
# MATH = 'arithmetic handle_arithmetic, removed due to compatibility, see explanation in challenges section of report'
# EXPR = 'expression'

## general chemistry
CHEMICAL = 'chemical'
ELEMENT = 'element'
Measurement = namedtuple('Measurement', ['value', 'units'])

## ideal gas law calculations
UNK = 'unknown'
NMOLS = 'mole'
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

## stoichiometry
REAGENTS = 'reagents'
PRODUCTS = 'products'

## unit conversions - if converting in opposite direction, simply divide instead of multiply
PA_TO_ATM = 1 / 101325
KPA_TO_ATM = PA_TO_ATM * 1000
PA_TO_KPA = 1 / 1000
ML_TO_L = 1 / 1000
C_TO_K = 273.15 # add instead of multiply
