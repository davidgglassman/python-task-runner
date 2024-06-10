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
				"name": "Generic Question Task",
				"prompt_type": "GenericQuestion",
				"args": ["Task 1 Step 1: Generic question"],
				"kwargs": {
					"initial_value": "Some initial value"
				},
				"function": handle_generic_question
			},
			{
				"name": "Yes/No Question Task",
				"prompt_type": "YesNoQuestion",
				"args": ["Task 1 Step 2: Yes/No question"],
				"kwargs": {
					"yes_text": "Sure",
					"no_text": "Nah",
					"cursor": "*"
				},
				"function": handle_yes_no_question
			}
		]
	}

################################################################################
# TASKS
################################################################################

def handle_generic_question(result):
	return Status("Completed Generic Question Task")

def handle_yes_no_question(result):
	return Status("Failed to complete Yes/No Question Task", error=True)