# For pythonanywhere's scheduled task 
# see https://help.pythonanywhere.com/pages/ScheduledTasks
#     https://www.pythonanywhere.com/forums/topic/1113/ 
#     https://www.pythonanywhere.com/forums/topic/12398/
export SLACK_BOT_TOKEN=INSERT_HERE
export API_TOKEN_GITHUB=INSERT_HERE
export OWNER_NAME_GITHUB=INSERT_HERE
python /home/{pythonanywhere_user}/github_pr_slack_bot.py
