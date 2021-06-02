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
assistant = AssistantV2(version='2020-09-24', authenticator=authenticator)
assistant.set_service_url('https://api.us-south.assistant.watson.cloud.ibm.com')

# create session and start context dictionary
session = assistant.create_session(ASSISTANT_ID).get_result()
context = {'metadata': { 'deployment': 'myDeployment'}}
result = {}

# assistant.delete_session(ASSISTANT_ID, session["session_id"]).get_result()

# Wake assistant with first message and print response
message = assistant.message_stateless(ASSISTANT_ID,input={'text': ""},context=context).get_result()
print(message["output"]["generic"][0]["text"])
 
try:
    while True:
        # user input
        sys.stdout.write('>> ')
        input_text = input()

        # get response from Watson assistant
        message = assistant.message_stateless(
            ASSISTANT_ID,
            # session["session_id"],
            input={
            'text': input_text,
            'options': {
                'return_context': True
            }},
            context=context).get_result()

        ### retrieve the information from the response
        output = message["output"]
        context = message['context']

        if output:
            if c.INTENTS in output and len(output[c.INTENTS]) > 0:
                result[c.INTENT] = output[c.INTENTS][0][c.INTENT]
        
        if "skills" in context and "user_defined" in context["skills"]["main skill"]:
            result[c.VARS] = context["skills"]["main skill"]["user_defined"]
        
        ### format the information
        formatted_result = format(result)

        ### Calculate output
        if formatted_result is not None:
            try:
                calculation_output = calculate_output(formatted_result)
            
                if calculation_output:
                    ### clear variables if the calculation is completed

                    del context['skills']
                    result = {}
                    print(calculation_output)
                    print('\nIs there anything else I can help you with?')
                    continue

                else:
                    intent = formatted_result[c.INTENT]
                    if intent in [c.ATOMIC_MASS, c.OX_STATES, c.ELEM_USES]:
                        inputs = formatted_result[c.VARS]
                        if len(inputs):
                            print(f'Unable to handle {intent} with inputs {inputs}')
                        else:
                            print(f'Watson Assistant was unable to parse your inputs for chemicals for {intent}, please try another query.')

            except ValueError as e:
                if formatted_result[c.INTENT] == c.STOICH:
                    inputs = formatted_result[c.VARS]
                    if len(inputs[c.PRODUCTS]) > 1:
                        print(f'Unable to handle stoichiometry with reagents {inputs[c.REAGENTS]} and products {inputs[c.PRODUCTS]}')
                else:
                    raise e
            
        if output:
            if "generic" in output and len(output["generic"]) > 0:
                if "response_type" in output["generic"][0] and output["generic"][0]["response_type"] == "text":
                    if "calculating" not in output["generic"][0]["text"].lower():
                        print(output["generic"][0]["text"].capitalize())
       
except KeyboardInterrupt:
    print("")
    print("Quit")