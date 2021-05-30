# ChemPal


### Access Information

API Key: 6QXzzjl3BI_FQEZCMArbewi7ZZEM5xrFnCBw4wkznvYP

URL: https://api.us-south.assistant.watson.cloud.ibm.com/instances/39850df7-bcfc-4ac4-b3f8-c9d39f28b4da



### Links

https://pypi.org/project/chemparse/

https://pubchempy.readthedocs.io/en/latest/

https://github.com/watson-developer-cloud/python-sdk

https://pypi.org/project/chempy/

https://pypi.org/project/mendeleev/


### Example queries
1. What is the atomic mass of calcium? 
2. I want to know how much 1 + 2 is


### Workflow
1. Get user input
2. Pass input into Watson
3. Convert input into variables
4. In Python, variables get sanitized, converting to appropriate units and order needed for calculations
5. In Python, calculations are performed
6. Python output is shown to the user based on the returned value and the type of calculation


### Units and Procedures

*Ideal Gas Law*

PV = nRT

0. "Ideal Gas Law"
1. Pressure- atm
2. Volume- liters
3. Number- moles
4. R- L·atm/(mol·K)
5. Temperature- Kelvin

Output: The missing value, float

*Atomic Weight*

0. "Atomic Weight"
1. Number- convert to int
2. Element Symbol
3. Number- convert to int
4. Element Symbol
5. Repeat as needed

Output: Total atomic weight of compound, float

*Stoichiometry*
0. "Stoichiometry"
1. Dictionary object of reactants
2. Dictionary object of products

Output: Dictionary objects of reactants and products to integers

*Multiplication*

0. "Multiplication"
1. Number
2. Number

Output: Float
