################################################################################
# IMPORTS
################################################################################

from status_helpers import Status

################################################################################
# INFO
################################################################################

def get_info():
	return {
		"prompt": "First task",
		"header": {
			"title": "Task 1 Header",
			"descriptions": [
				"This is line 1 for task 1",
				"This is line 2 for task 1"
			]
		},
		"steps": [
			{
				"prompt_type": "GenericQuestion",
				"args": ["Task 1 Step 1: Generic question"],
				"kwargs": {},
				"function": handle_generic_question
			},
			{
				"prompt_type": "YesNoQuestion",
				"args": ["Task 1 Step 2: Yes/No question"],
				"kwargs": {
					"yes_text": "Sure",
					"no_text": "Nah"
				},
				"function": handle_yes_no_question
			}
		]
	}

################################################################################
# TASKS
################################################################################

def handle_generic_question(result):
	return Status("generic question result: success")

def handle_yes_no_question(result):
	return Status("yes/no question result: failure", error=True)