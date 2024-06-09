################################################################################
# IMPORTS
################################################################################

from status_helpers import Status

################################################################################
# INFO
################################################################################

def get_info():
	return {
		"prompt": "Second task",
		"header": {
			"title": "Task 2 Header",
			"descriptions": [
				"This is line 1 for task 2",
				"This is line 2 for task 2"
			]
		},
		"steps": [
			{
				"prompt_type": "SingleChoiceQuestion",
				"args": [
					"Task 2 Step 1: Single choice question",
					["Option 1", "Option 2", "Option 3"]
				],
				"kwargs": {
					"cursor": "**"
				},
				"function": handle_single_choice_question
			},
			{
				"prompt_type": "MultipleChoiceQuestion",
				"args": [
					"Task 2 Step 2: Multiple choice question",
					["Option 1a", "Option 2a", "Option 3a"]
				],
				"kwargs": {
					"tick_character": "x"
				},
				"function": handle_multiple_choice_question
			}
		]
	}

################################################################################
# TASKS
################################################################################

def handle_single_choice_question(result):
	return Status("single choice question result: success")

def handle_multiple_choice_question(result):
	return Status("multiple choice question result: failure", error=True)