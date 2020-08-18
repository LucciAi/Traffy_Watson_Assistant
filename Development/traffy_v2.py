import requests,json,re
from ibm_watson import AssistantV2,ApiException
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
from datetime import datetime,timedelta
from PIL import Image
from weather_v2 import weather
from state import state
from zip import zip

#Obtained From Watson Assistant
API_Key='8dwm6jdHdEghcGIc6SULg6BOOkfGGA12ovPOC8hd5gvK'
Version='2020-08-09'
URL='https://api.us-south.assistant.watson.cloud.ibm.com'
Assistant_ID='23c7e3a3-b5b3-4357-b2f8-d5cd002c316b'

#Authentication
authenticator=IAMAuthenticator(API_Key)
assistant=AssistantV2(
    version=Version,
    authenticator=authenticator
)

#Set URL
assistant.set_service_url(URL)

#Create Session ID
session_response=assistant.create_session(
    assistant_id=Assistant_ID
).get_result()

Session_ID=session_response['session_id'] #Store Session ID

#Start Conversation
message_input='start_session' #Initial Message Input

while message_input!='quit': #Exit Conversation
    try:
        message_input=input('Message: ') #Input Message

        #Recieve Response
        message_response=assistant.message(
            assistant_id=Assistant_ID,
            session_id=Session_ID,
            input={
                'message_type': 'text',
                'text': str(message_input)
                }
        ).get_result()

        #print(json.dumps(message_response,indent=2))
        if len(message_response['output']['generic'])!=0:
            message_return=message_response['output']['generic'][0]['text'] #Return Message
            print(message_return) #Print Message
        if len(message_response['output']['intents'])!=0:
            if message_response['output']['intents'][0]['intent']=='Weather':
                weather(message_response)
    except ApiException as ex:
        print('Method failed with status code ' + str(ex.code) + ': ' + ex.message) #Print Error Code
        continue
