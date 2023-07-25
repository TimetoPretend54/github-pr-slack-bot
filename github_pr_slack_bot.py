import os
from slack_sdk import WebClient 
from slack_sdk.errors import SlackApiError 

# We need to pass the 'Bot User OAuth Token'
slack_token = os.environ.get('SLACK_BOT_TOKEN')

# Creating an instance of the Webclient class
client = WebClient(token=slack_token)

try:
	# Posting a message in #random channel
	response = client.chat_postMessage(
    				channel="random",
    				text="Bot's first message")

	
	# Get a list of conversations
	response = client.conversations_list()

except SlackApiError as e:
	print("fail")
	print(e)
	assert e.response["error"]

else:
	for channel in response["channels"]:
  		print(channel["name"])
