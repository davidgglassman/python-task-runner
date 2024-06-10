# Prerequisites

- **Windows OS** (_developed and tested using `Windows 11` but other versions might work. No guarantees._)
- **Python** (_developed and tested using `v3.12.1` but other versions might work. No guarantees._)

---

# Installation

- Open a terminal
- Clone repo: `git clone https://github.com/davidgglassman/python-task-runner.git`
- `cd` to directory you just cloned repository into
- Run `.\\build.bat` (or open directory in Windows Explorer and double-click `build.bat` file)

This will create a Python virtual environment (if it does not exist), install all required packages, then build a single executable file in the directory (`app.exe`) that can be run like a regular application.

---

# Usage

## Manifest File

When the script starts up, it will be looking for a `manifest.json` file (_a sample has been provided with the repo_). It will read this file and use the information contained within during runtime. Below is a list of the key/value pairs that need to be included in the `manifest.json` file.

Note, if packaging and running the script as an .exe file, the `manifest.json` file must be placed in the same location as the .exe file. However, if running the script from the command line/terminal, a flag (`--manifest <path to manifest file>`) is provided to allow you to pass in the path of the manifest file instead.

## Manifest File Key/Value Pairs

The `manifest.json` file supports the following key/value pairs:

- `app_name` (_string_): The name you would like the application to be called **REQUIRED**
- `version` (_string_): The current version of the application **REQUIRED**
- `tasks_path` (_string_): The absolute filepath to the folder containing the Python task files to include as part of the application functionality. If this key/value pair is omitted from the file, the script will look in the directory it is currently running from for a folder named `tasks`. **OPTIONAL**

Below is an example of a manifest file:

```json
{
  "app_name": "Some App",
  "version": "v1.0.0",
  "tasks_path": "C://Users//SomeUser//Desktop//tasks"
}
```

## Tasks

Once the `manifest.json` file has been read, the script will attempt to load all the tasks from the tasks folder. The tasks folder needs to contain an empty `__init__.py` file as well as one Python file for each task you would like to be included in the application. A sample tasks folder with two tasks has been included in the repo for reference.

Each Python task file needs to include some specific information in order for the script to know how to process it. See below for specifics. Once all the tasks have been read in, the script will use this information to build a "main menu" containing a list of the available tasks. The user can choose which task they would like to perform from the menu. Once a task has been selected, the script will run through each of the questions associated with the task and gather all the responses from the user. Once all the responses have been gathered, the script will run each step in the task one by one, using the response associated with the step. Once all steps have been completed for a task, the script will return to the main menu, allowing the user to select a new task or exit the application.

## Task File

Each Python task file needs to include the following:

1. A function definition named `get_info` which takes no arguments and returns a dictionary with the following key/value pairs:

   - `prompt` (_string_): This will be the text that shows up for the task in the "main menu".
   - `header` (_dictionary_): When the task is selected from the "main menu" and starts to run, the first thing that is printed out is a header for the task. The following key/value pairs are required in this dictionary:
     - `title` (_string_): This will be the title text that shows up for the selected task.
     - `descriptions` (_list of strings_): Each item in the list will be a line of descriptive text for the task. There is no limit to how many lines of text descriptions you can have.
   - `steps` (_list of dictionaries_): Each dictionary will represent the information for a single question to be asked as well as the function to be performed once the task automation loop begins. Each dictionary in the list will need to contain the following key/value pairs:
     - `name` (_string_): This will be the name of the step to be shown to the user.
     - `prompt_type` (_string_): The app supports multiple different types of questions (prompts) that can be asked of the user. See below for a list of valid prompt types to use for this field.
     - `args` (_list of strings_): Each prompt type has a list of valid args that can be passed in to configure and customize the prompt. See below for a list of valid args to use in this field. All args listed for a particular prompt are required.
     - `kwargs` (_dictionary_): Each prompt type has a list of valid kwargs that can be passed in to configure and customize the prompt. See below for a list of valid kwargs to use in this field. Supply as many of as few kwargs as you want as a dictionary of key/value pairs.
     - `function` (_function name_): The function to call when the step is run.

2. A function definition for each step in the task to be performed when run. When the task automation is run, it will go through each step one by one and run whatever function is defined for that step. This function must include a single parameter in which to receive the response to the corresponding question that the user has answered. The function will run whatever custom logic it needs to complete the step and return a tuple. The first argument in the tuple will be either the success or error text to show to the user and the second argument in the tuple will be True if the step was successful and False if the step was not successful.

Below is an example of a Python file for a sample task:

```python
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

def handle_generic_question(result):
	# do some logic associated with this step
	return ("Completed Generic Question Task", True)

def handle_yes_no_question(result):
	# do some logic associated with this step
	return ("Failed to complete Yes/No Question Task", False)
```

## Prompt Types

There are 4 available prompt types available to use.

### Generic Question

**Usage**
Use this when you want to ask a question that has a single typed response from the user.

**Prompt Type**
`GenericQuestion`

**Available Args**
_(args are not named but instead must be added to the list in the order shown below)_

- `arg1` (_string_): The question to be asked of the user **REQUIRED**

**Available Kwargs**

- `target_type` (_any valid Python type_): Type to convert the answer to
- `validator` (_function_): Optional function to validate the input
- `secure` (_bool_): If True, input will be hidden
- `raise_validation_fail` (_bool_): If True, invalid inputs will raise rich.internals.ValidationError, else the error will be reported onto the console
- `raise_type_conversion_fail` (_bool_): If True, invalid inputs will raise rich.internals.ConversionError, else the error will be reported onto the console
- `initial_value` (_string_): If present, the value is placed in the prompt as the default value

### Yes/No Question

**Usage**
Use this when you want to ask a question where the answer can be one of two options. The answer to this question will be converted to a boolean (True for the Yes response, False for the No response).

**Prompt Type**
`YesNoQuestion`

**Available Args**
_(args are not named but instead must be added to the list in the order shown below)_

- `arg1` (_string_): The question to be asked of the user **REQUIRED**

**Available Kwargs**

- `yes_text` (_string_): Text of positive response
- `no_text` (_string_): Text of negative response
- `has_to_match_case` (_bool_): Check if typed response matches case
- `enter_empty_confirms` (_bool_): No response is considered as confirmation
- `default_is_yes` (_bool_): Default response is positive
- `cursor` (_string_): Cursor to be shown
- `cursor_style` (_string_): Rich friendly cursor style
- `char_prompt` (_bool_): Print [Y/N] after the question

### Single Choice Question

**Usage**
Use this when you want to ask a question where the user is presented with a list of options to choose from and can only select one of the items in the list.

**Prompt Type**
`SingleChoiceQuestion`

**Available Args**
_(args are not named but instead must be added to the list in the order shown below)_

- `arg1` (_string_): The question to be asked of the user **REQUIRED**
- `arg2` (_list of strings_): Options to select from **REQUIRED**

**Available Kwargs**

- `preprocessor` (_function_): A callable that can be used to preprocess the list of options prior to printing
- `cursor` (_string_): Cursor that is going to appear in front of currently selected option
- `cursor_style` (_string_): Rich friendly style for the cursor
- `cursor_index` (_number_): Option can be preselected based on its list index
- `return_index` (_bool_): If True, select will return the index of selected element in options
- `strict` (_bool_): If empty options is provided and strict is False, None will be returned, if it's True, ValueError will be thrown
- `pagination` (_bool_): If True, pagination will be used
- `page_size` (_number_): Number of options to show on a single page if pagination is enabled

### Multiple Choice Question

**Usage**
Use this when you want to ask a question where the user is presented with a list of options to choose from and can select as many items from the list as they want.

**Prompt Type**
`MultipleChoiceQuestion`

**Available Args**
_(args are not named but instead must be added to the list in the order shown below)_

- `arg1` (_string_): The question to be asked of the user **REQUIRED**
- `arg2` (_list of strings_): Options to select from **REQUIRED**

**Available Kwargs**

- `preprocessor` (_function_): A callable that can be used to preprocess the list of options prior to printing
- `tick_character` (_string_): Character that will be used as a tick in a checkbox
- `tick_style` (_string_): Rich friendly style for tick character
- `cursor_style` (_string_): Rich friendly style for the option when the cursor is currently on it
- `ticked_indices` (_number_): Indices of options that are pre-ticked when the prompt appears
- `cursor_index` (_number_): Index of the option cursor starts at
- `minimal_count` (_number_): Minimal count of options that need to be selected
- `maximal_count` (_number_): Maximal count of options that need to be selected
- `return_indices` (_bool_): If True, select_multiple will return the indices of ticked elements in options
- `strict` (_bool_): If empty options is provided and strict is False, None will be returned, if it's True, ValueError will be thrown
- `pagination` (_bool_): If True, pagination will be used
- `page_size` (_number_): Number of options to show on a single page if pagination is enabled

---

# Credits

This repo makes use of the following awesome projects behind-the-scenes:

- [BeauPy](https://github.com/petereon/beaupy "BeauPy")
- [Rich](https://github.com/Textualize/rich "Rich")
