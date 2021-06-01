import chempy  # allows us to calculate basic chemical formulae https://pypi.org/project/chempy/
from pubchempy import get_compounds  # for searching chemical names https://pubchempy.readthedocs.io/en/latest/guide/gettingstarted.html#searching
from pyparsing import ParseException
from sympy.core.function import BadArgumentsError

"""
Chemical format utility for CS89 final project. Provides both parsing functions
and conversion functions. 

PARSING FUNCTIONS
The parsing functions take strings representing chemicals (either by name or 
by chemical formula), and return Python objects representing those chemicals.

PubChemPy format:
- Provides API for searching compounds by name in a large, publicly available
    dataset. This allows us to accept a wider range of inputs and still convert
    to consistent formats.
- Provides many more attributes than needed, but also charge, mass, isotope
    information, molecular formula, and structure.

ChemPy format:
- Provides API for initialization from chemical formula only.
- Can perform various calculations if inputs are given in ChemPy format.
"""

## PARSING FUNCTIONS
def parse_chemical_name(name, output):
    """
    Parses a chemical name provided as a string into the chosen output.

    parameters:
        name -- string containing the name of the chemical
        output -- string stating the output type (currently either chempy or pubchempy)

    returns:
        Python object in chosen format representing the chemical
    """
    compounds = get_compounds(name, 'name')
    if compounds:
        compound = compounds[0]
    else:
        raise BadArgumentsError(f'Failed to find a compound with name {name}')

    if output == 'pubchempy':
        return compound

    elif output == 'chempy':
        substance = chempy.Substance.from_formula(compound.molecular_formula)
        return substance

    elif output == 'mendeleev':
        # I believe the pubchempy functionality provides as much information
        # as Mendeleev while also supporting compounds
        pass

    elif output == 'atomic_weight':
        substance = chempy.Substance.from_formula(compound.molecular_formula)
        return substance.molar_mass()


def parse_chemical_formula(formula, output):
    """
    Parses a string containing a chemical formula into the chosen format.

    parameters:
        formula -- string representing a chemical formula, such as H2O
        output -- string stating the output type
    
    returns:
        Python object in chosen format representing the chemical
    """
    if output == 'chempy':
        return chempy.Substance.from_formula(formula)

    elif output == 'pubchempy':
        return get_compounds(formula, 'formula')[0]

    elif output == 'mendeleev':
        # I believe the pubchempy functionality provides as much information
        # as Mendeleev while also supporting compounds
        pass

    elif output == 'atomic_weight':
        substance = chempy.Substance.from_formula(formula)
        return substance.molar_mass()


def parse_chemical(chemical, output='chempy'):
    """
    Parses a string representing a chemical. The chemical string must be either
    a chemical formula or a common name for a chemical.

    parameters:
        chemical -- string representing a chemical
        output -- string stating the output datatype (currently either chempy, 
                    pubchempy, or atomic weight)

    returns:
        chemical represented as a Python object in the chosen format
    
    throws:
        pyparsing.ParseException (following chempy here) if we fail to parse the chemical string
    """
    try: 
        return parse_chemical_formula(chemical, output)
    
    except ParseException:  # thrown by chempy if it fails to parse a chemical formula
        try:
            return parse_chemical_name(chemical, output)
        except BadArgumentsError:  # thrown by our code if searching for the compound name in pubchempy fails
            raise ParseException(f'Unable to parse string {chemical}')
