################################################################################
# IMPORTS
################################################################################

from helpers.status_helpers import Status

################################################################################
# INFO
################################################################################

def get_info():
	return {
		"title": "Second task",
		"descriptions": [
			"This is line 1 for task 2",
			"This is line 2 for task 2"
		],
		"questions": [
			{
				"prompt_type": "SingleChoiceQuestion",
				"args": [
					"Task 2 Step 1: Single choice question",
					["Option 1", "Option 2", "Option 3"]
				],
				"kwargs": {
					"cursor": "x"
				}
			},
			{
				"prompt_type": "MultipleChoiceQuestion",
				"args": [
					"Task 2 Step 2: Multiple choice question",
					["Option 1a", "Option 2a", "Option 3a"]
				],
				"kwargs": {
					"tick_character": "x"
				}
			}
		]
	}

################################################################################
# TASKS
################################################################################

def run_task(results):
	return Status("Completed Second Task")