import chempy  # allows us to calculate basic chemical formulae https://pypi.org/project/chempy/
from pubchempy import get_compounds  # for searching chemical names https://pubchempy.readthedocs.io/en/latest/guide/gettingstarted.html#searching

"""
Chemical format utility for CS89 final project. Provides functions which
take strings representing chemicals (either by name or by chemical formula),
and return Python objects representing those chemicals.

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

def parse_chemical_name(name, format='chempy'):
    """
    Parses a chemical name provided as a string into the chosen format.

    parameters:
        name -- string containing the name of the chemical
        format -- string stating the output type (currently either chempy or pubchempy)

    returns:
        Python object in chosen format representing the chemical
    """
    compound = get_compounds(name, 'name')[0]

    if format == 'pubchempy':
        return compound

    elif format == 'chempy':
        print(compound.molecular_formula)
        substance = chempy.Substance.from_formula(compound.molecular_formula)
        return substance

    elif format == 'mendeleev':
        # I believe the pubchempy functionality provides as much information
        # as Mendeleev while also supporting compounds
        pass


def parse_chemical_formula(formula, format='chempy'):
    """
    Parses a string containing a chemical formula into the chosen format.

    parameters:
        formula -- string representing a chemical formula, such as H2O
        format -- string stating the output type (currently either chempy or pubchempy)
    
    returns:
        Python object in chosen format representing the chemical
    """
    if format == 'chempy':
        return chempy.Substance.from_formula(formula)

    elif format == 'pubchempy':
        return get_compounds(formula, 'formula')[0]

    elif format == 'mendeleev':
        # I believe the pubchempy functionality provides as much information
        # as Mendeleev while also supporting compounds
        pass
