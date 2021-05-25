import json
from ibm_watson import AssistantV2
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

API_KEY = "eV6IqpY5KaKIWRgw5XRk94hR6DC5fYCxaDX1nNIJz3iT"
ASSISTANT_ID = "a1ceb56d-4515-40b2-896e-6033078034ea" 
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
    while True:

        input_text = input()
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
        print(json.dumps(message, indent=2))
        print(message["output"]["generic"][0]["text"])

except KeyboardInterrupt:
    print("")
    print("Quit")