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
				"name": "Single Choice Question Task",
				"prompt_type": "SingleChoiceQuestion",
				"args": [
					"Task 2 Step 1: Single choice question",
					["Option 1", "Option 2", "Option 3"]
				],
				"kwargs": {
					"cursor": "x"
				},
				"function": handle_single_choice_question
			},
			{
				"name": "Multiple Choice Question Task",
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
	return ("Completed Single Choice Question Task", True)

def handle_multiple_choice_question(result):
	return ("Failed to complete Multiple Choice Question Task", False)