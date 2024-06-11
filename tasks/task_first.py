################################################################################
# IMPORTS
################################################################################

from helpers.status_helpers import Status

################################################################################
# INFO
################################################################################

def get_info():
	return {
		"title": "First task",
		"descriptions": [
			"This is line 1 for task 1",
			"This is line 2 for task 1"
		],
		"questions": [
			{
				"prompt_type": "GenericQuestion",
				"args": ["Task 1 Step 1: Generic question"],
				"kwargs": {
					"initial_value": "Some initial value"
				}
			},
			{
				"prompt_type": "YesNoQuestion",
				"args": ["Task 1 Step 2: Yes/No question"],
				"kwargs": {
					"yes_text": "Sure",
					"no_text": "Nah",
					"cursor": "*"
				}
			}
		]
	}

################################################################################
# TASKS
################################################################################

def run_task(results):
	return Status("Completed First Task")