
# Input result is a dict
def format(result):
    new_result = {}
    variables = []
    if result["intent"] == "AskingMass":
        new_result["intent"] = "Atomic Weight"
        if "ChemicalCompound" in result["variables"]:
            variables.append(result["variables"]["ChemicalCompound"]) 
        new_result["variables"] = variables
    elif result["intent"] == "AsingOxidationStates":
        new_result["intent"] = "Oxidation State"
        if "ChemicalElement" in result["variables"]:
            variables.append(result["variables"]["ChemicalElement"]) 
        new_result["variables"] = variables
    elif result["intent"] == "AskingElementUses":
        new_result["intent"] = "Element Uses"
        if "ChemicalElement" in result["variables"]:
            variables.append(result["variables"]["ChemicalElement"]) 
        new_result["variables"] = variables
    elif result["intent"] == "AskingGas":
        new_result["intent"] = "Ideal Gas Law"
        if "pressure" in result["variables"]:
            variables.insert(0, result["variables"]["pressure"]) 
        if "pressure_unit" in result["variables"]:
            variables.insert(1, result["variables"]["pressure_unit"]) 
        if "volume" in result["variables"]:
            variables.insert(2, result["variables"]["volume"]) 
        if "volume_unit" in result["variables"]:
            variables.insert(3, result["variables"]["volume_unit"]) 
        if "temperature" in result["variables"]:
            variables.insert(4, result["variables"]["temperature"]) 
        if "temperature_unit" in result["variables"]:
            variables.insert(5, result["variables"]["temperature_unit"]) 
        if "mole" in result["variables"]:
            variables.insert(6, result["variables"]["mole"]) 
        new_result["variables"] = variables
    elif result["intent"] == "AskingStoichiometry":
        new_result["intent"] = "Stoichiometry"
        if "Reactant0" in result["variables"]:
            variables.insert(0, result["variables"]["Reactant0"]) 
        if "Reactant1" in result["variables"]:
            variables.insert(1, result["variables"]["Reactant1"]) 
        if "Product0" in result["variables"]:
            variables.insert(2, result["variables"]["Product0"]) 
        if "Product1" in result["variables"]:
            variables.insert(3, result["variables"]["Product1"]) 
        new_result["variables"] = variables
    return  new_result
