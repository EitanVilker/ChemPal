import json
from ibm_watson import AssistantV2
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from calculate_output import calculate_output
from handler import handle

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
    result["intent"] = ""
    result["variables"] = {}
    while True:
        ### user input
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
            if "intents" in output and len(output["intents"]) > 0:
                result["intent"] = output["intents"][0]["intent"]
        if "context" in message:
            if "skills" in message["context"] and "main skill" in message["context"]["skills"] and "user_defined" in message["context"]["skills"]["main skill"]:
                result["variables"] = message["context"]["skills"]["main skill"]["user_defined"]
        
        ### post-process the information to make the format consistent with our calculator
        post_processed_result = handle(result)
        # print(result)
        # print(post_processed_result)

        #### Parse the result here

        ### Calculate output
        # calculation_output = calculate_output(new_result)
        # if output:
        #     print(output)

        ### clear variables if the calculation is completed
        if output:
            if "generic" in output and len(output["generic"]) > 0:
                if output["generic"][0]["response_type"] and output["generic"][0]["response_type"] == "text":
                    print(output["generic"][0]["text"])
                    if "calculating" in output["generic"][0]["text"]:
                        result = {}
                        result["intent"] = ""
                        result["variables"] = {}

        
except KeyboardInterrupt:
    print("")
    print("Quit")