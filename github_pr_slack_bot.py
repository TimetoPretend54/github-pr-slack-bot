import os
import requests
from json import JSONEncoder
from slack_sdk import WebClient 
from slack_sdk.errors import SlackApiError 


class Pull_Request_Info:
	def __init__(self, title, url, number, repo, created, updated, channels):
		self.title = title
		self.url = url
		self.number = number
		self.repo = repo
		self.created = created
		self.updated = updated
		self.channels = channels

class Pull_Request_Info_Encoder(JSONEncoder):
        def default(self, o):
            return o.__dict__


#
# Slack Channel - GitHub Repo Mapping
#
channel_repo_dict = {
	"devops": ['go-chatgpt-copilot', 'technical-docs', 'MyPortfolio', 'web-go-k8', 'github-pr-slack-bot' ],		# Could default to fetching "all" repos with a keyword instead, depends on need/fine-grain control
	"team-a": ['go-chatgpt-copilot']
}

#
# Setup
#
GITHUB_API_BASE_URL="https://api.github.com"

slack_token = os.environ.get('SLACK_BOT_TOKEN')
github_token = os.environ.get('API_TOKEN_GITHUB')
owner = os.environ.get('OWNER_NAME_GITHUB')


# 
# GitHub API Request Logic
#
headers = {'Authorization':"Token "+str(github_token)}


repos=[]
try:
	# to find all the repos' names (use https://api.github.com/orgs/{orgName}/repos for organizations)
	url=f"{GITHUB_API_BASE_URL}/users/{owner}/repos" 
	resp=requests.get(url,headers=headers).json()
	repos = resp

except Exception as e:
	print(e)
	repos.append(None)


all_repo_names=[]
for repo in repos:
	try:
		all_repo_names.append(repo['full_name'].split("/")[1]) # {owner}/{repo_name}

	except Exception as e:
		print(e)
		pass
# # Debug
# print(all_repo_names)


pull_requests=[]
for repo_name in all_repo_names:
	try:
		url=f"{GITHUB_API_BASE_URL}/repos/{owner}/{repo_name}/pulls?state=open" 
		prs_resp=requests.get(url,headers=headers).json()
		if len(prs_resp) != 0:
			for pr in prs_resp:
				pull_requests.append(pr)

	except Exception as e:
		print(e)
		pass


pull_requests_info=[]
for pull_request in pull_requests:
	try:
		title=pull_request['title']
		url=pull_request['html_url']
		number=pull_request['number']
		repo=pull_request['base']['repo']['full_name'].split("/")[1]
		created=pull_request['created_at']
		updated=pull_request['updated_at']
		channels=[]

		for k_channel, v_repos in channel_repo_dict.items():
			if repo in v_repos:
				channels.append(k_channel)

		pull_requests_info.append(Pull_Request_Info(title,url,number,repo,created,updated,channels))
		
	except Exception as e:
		print(e)
		pass
# # Debug
# for pr in pull_requests_info:
# 	json_data = json.dumps(pr, indent=4, cls=Pull_Request_Info_Encoder)
# 	print(json_data)


# 
# Slack SDK Logic
#
client = WebClient(token=slack_token)

for k_channel in channel_repo_dict.keys():
	bot_msg = "Here are the following outstanding Pull Requests:"

	for pull_request_info in pull_requests_info:
		if k_channel in pull_request_info.channels:
			pr_msg_list = [
				f"	URL: {pull_request_info.url}",
			]

			pr_msg_list = [
				f"> <{pull_request_info.url}|*#{pull_request_info.number} {pull_request_info.title}*>",
				f">		*Created:* {pull_request_info.created}",
				f">		*Updated:* {pull_request_info.updated}",
				f">		{pull_request_info.url}",
			]

			pr_msg = "\n".join(pr_msg_list)
			bot_msg = bot_msg + "\n\n\n" + pr_msg

	try:
		response = client.chat_postMessage(
						channel=k_channel,
						text=bot_msg)

		response = client.conversations_list()

	except SlackApiError as e:
		print(e)
		assert e.response["error"]

	# # Debug
	# else:
	# 	for channel in response["channels"]:
	# 		print(channel["name"])

