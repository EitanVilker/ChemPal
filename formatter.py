import constants as c

# Input result is a dict
def format(result):
    new_result = {}
    variables = {}

    if result[c.INTENT] == c.ATOMIC_MASS:
        variables[c.CHEMICAL] = result[c.VARS][c.WATSON_CHEM]

    elif result[c.INTENT] == c.OX_STATES:
        variables[c.ELEMENT] = result[c.VARS][c.WATSON_ELEM]

    elif result[c.INTENT] == c.ELEM_USES:
        variables[c.ELEMENT] = result[c.VARS][c.WATSON_ELEM]

    elif result[c.INTENT] == c.INTENT:
        variables[c.PRESSURE] = c.Measurement(float(result[c.VARS][c.PRESSURE]), result[c.VARS][c.PRESSURE_UNITS])
        variables[c.VOLUME] = c.Measurement(float(result[c.VARS][c.VOLUME]), result[c.VARS][c.VOLUME_UNITS])
        variables[c.TEMPERATURE] = c.Measurement(float(result[c.VARS][c.TEMPERATURE]), result[c.VARS][c.TEMPERATURE_UNITS])
        variables[c.N_MOLS] = c.Measurement(float(result[c.VARS][c.PRESSURE]), result[c.VARS][c.PRESSURE_UNITS])
        
    elif result[c.INTENT] == "AskingStoichiometry":  # assumes that at least one reagent and one product are provided
        variables[c.REAGENTS] [result[c.VARS][c.WATSON_REAGENT0]] 
        if c.WATSON_REAGENT1 in result[c.VARS]:
            variables[c.REAGENTS].extend(result[c.VARS][c.WATSON_REAGENT1]) 
        
        variables[c.PRODUCTS] =  [result[c.VARS][c.WATSON_PRODUCT0]] 
        if c.WATSON_PRODUCT1 in result[c.VARS]:
            variables[c.PRODUCTS].extend(result[c.VARS][c.WATSON_PRODUCT1])
    
    new_result[c.INTENT] = result[c.INTENT]
    new_result[c.VARS] = variables
    
    return  new_result
