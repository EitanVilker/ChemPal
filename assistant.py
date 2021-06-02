import constants as c
import json
import sys

from ibm_watson import AssistantV2
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from calculate_output import calculate_output
from formatter import format
from time import sleep


API_KEY = "eV6IqpY5KaKIWRgw5XRk94hR6DC5fYCxaDX1nNIJz3iT"
ASSISTANT_ID = "eb2dc57e-dc4d-475e-95bc-c7b646dbe09c" 

authenticator = IAMAuthenticator(API_KEY)
assistant = AssistantV2(
    version='2020-09-24',
    authenticator=authenticator)
assistant.set_service_url('https://api.us-south.assistant.watson.cloud.ibm.com')


#########################
# Sessions
#########################

session = assistant.create_session(ASSISTANT_ID).get_result()

# assistant.delete_session(ASSISTANT_ID, session["session_id"]).get_result()

#########################
# Message
#########################
message = assistant.message(
            ASSISTANT_ID,
            session["session_id"],
            input={'text': ""},
            context={
                'metadata': {
                    'deployment': 'myDeployment'
                }
            }).get_result()
    
print(message["output"]["generic"][0]["text"])
 
try:
    result = {}
    result[c.INTENT] = ""
    result[c.VARS] = {}
    should_raise = False

    while True:
        ### user input
        sys.stdout.write('>> ')
        input_text = input()

        ### get response from Watson assistant
        message = assistant.message(
            ASSISTANT_ID,
            session["session_id"],
            input={
            'text': input_text,
            'options': {
                'return_context': True
            }},
            context={
                'metadata': {
                    'deployment': 'myDeployment'
                }
            }).get_result()

        ### print the response
        # print(json.dumps(message, indent=2))

        ### retrieve the information from the response
        output = message["output"]
        if output:
            if c.INTENTS in output and len(output[c.INTENTS]) > 0:
                result[c.INTENT] = output[c.INTENTS][0][c.INTENT]
        if "context" in message:
            if "skills" in message["context"] and "main skill" in message["context"]["skills"] and "user_defined" in message["context"]["skills"]["main skill"]:
                result[c.VARS] = message["context"]["skills"]["main skill"]["user_defined"]
        
        ### format the information
        formatted_result = format(result)

        #### Parse the result here

        ### Calculate output
        if formatted_result:
            try:
                print(formatted_result)
                calculation_output = calculate_output(formatted_result)
            
                if calculation_output:
                    print(calculation_output)
                else:
                    intent = formatted_result[c.INTENT]
                    if intent in [c.ATOMIC_MASS, c.OX_STATES, c.ELEM_USES]:
                        inputs = formatted_result['variables']
                        if len(formatted_result['variables']):
                            print(f'Unable to handle {intent} with inputs {formatted_result}')
                        else:
                            print(f'Watson Assistant was unable to parse your inputs for chemicals for {intent}, please try another query.')

            except ValueError as e:
                if formatted_result[c.INTENT] == c.STOICH:
                    if len(formatted_result[c.PRODUCTS] > 1):
                        print(f'Unable to handle stoichiometry with reagents {formatted_result[c.REAGENTS]} and products {formatted_result[c.PRODUCTS]}')
                else:
                    raise e
        
        ### clear variables if the calculation is completed
        if calculation_output:
            if "generic" in output and len(output["generic"]) > 0:
                print(output['generic'])
                if "response_type" in output["generic"][0] and output["generic"][0]["response_type"] == "text":
                    if "calculating" in output["generic"][0]["text"].lower():
                        result = {}
                        result[c.INTENT] = ""
                        result[c.VARS] = {}
                        # print(output['generic'][0]['text'])
                        # print('\nIs there anything else I can help you with?')
                    else:
                        print(output["generic"][0]["text"])

        
except KeyboardInterrupt:
    print("")
    print("Quit")