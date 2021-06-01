import constants as c

# Input result is a dict
def format(result):
    new_result = {}
    variables = {}
    if not (c.INTENT in result and c.VARS in result):
        return None

    if result[c.INTENT] == c.ATOMIC_MASS:
        if c.WATSON_CHEM in result[c.VARS]:
            variables[c.CHEMICAL] = result[c.VARS][c.WATSON_CHEM]

    elif result[c.INTENT] == c.OX_STATES:
        if c.WATSON_ELEM in result[c.VARS]:
            variables[c.ELEMENT] = result[c.VARS][c.WATSON_ELEM]

    elif result[c.INTENT] == c.ELEM_USES:
        if c.WATSON_ELEM in result[c.VARS]:
            variables[c.ELEMENT] = result[c.VARS][c.WATSON_ELEM]

    elif result[c.INTENT] == c.IDEAL_GAS:
        if c.PRESSURE in result[c.VARS] and c.PRESSURE_UNITS in result[c.VARS]:
            variables[c.PRESSURE] = c.Measurement(float(result[c.VARS][c.PRESSURE]), result[c.VARS][c.PRESSURE_UNITS])
        if c.VOLUME in result[c.VARS] and c.VOLUME_UNITS in result[c.VARS]:
            variables[c.VOLUME] = c.Measurement(float(result[c.VARS][c.VOLUME]), result[c.VARS][c.VOLUME_UNITS])
        if c.TEMPERATURE in result[c.VARS] and c.TEMPERATURE_UNITS in result[c.VARS]:
            variables[c.TEMPERATURE] = c.Measurement(float(result[c.VARS][c.TEMPERATURE]), result[c.VARS][c.TEMPERATURE_UNITS])
        if c.NMOLS in result[c.VARS]:
            variables[c.NMOLS] = result[c.VARS][c.NMOLS]
        
    elif result[c.INTENT] == c.STOICH:  # assumes that at least one reagent and one product are provided
        if c.WATSON_REAGENT0 in result[c.VARS]:
            variables[c.REAGENTS] = []
            variables[c.REAGENTS].append(result[c.VARS][c.WATSON_REAGENT0])
        if c.WATSON_REAGENT1 in result[c.VARS] and result[c.VARS][c.WATSON_REAGENT1]!= "None":
            variables[c.REAGENTS].append(result[c.VARS][c.WATSON_REAGENT1]) 
        if c.WATSON_PRODUCT0 in result[c.VARS]:
            variables[c.PRODUCTS] = []
            variables[c.PRODUCTS].append(result[c.VARS][c.WATSON_PRODUCT0])
        if c.WATSON_PRODUCT1 in result[c.VARS] and result[c.VARS][c.WATSON_PRODUCT1] != "None":
            variables[c.PRODUCTS].append(result[c.VARS][c.WATSON_PRODUCT1])
    
    new_result[c.INTENT] = result[c.INTENT]
    new_result[c.VARS] = variables
    
    return  new_result
