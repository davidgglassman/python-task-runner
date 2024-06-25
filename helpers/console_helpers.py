import time
import questionary
from beaupy.spinners import *
from beaupy import confirm, prompt, select, select_multiple
from prompt_toolkit.shortcuts import CompleteStyle

# ----------------------------------------------------------------------------------------

class Result:
	def __init__(self, question, value, answer=None):
		self.question = question
		self.answer = value if answer is None else answer
		self.value = value

# ----------------------------------------------------------------------------------------

class GenericQuestion:
	def __init__(self, *args, **kwargs):
		self.question 								 	= args[0]																					# Question to be asked			
		self.target_type 							 	= kwargs.get("target_type", str)									# Type to convert the answer to
		self.validator 								 	= kwargs.get("validator", lambda input: True)			# Optional function to validate the input
		self.secure  					 	 		 		= kwargs.get("secure", False)											# If True, input will be hidden
		self.raise_validation_fail 		 	= kwargs.get("raise_validation_fail", True)				# If True, invalid inputs will raise rich.internals.ValidationError, else the error will be reported onto the console
		self.raise_type_conversion_fail = kwargs.get("raise_type_conversion_fail", True)	# If True, invalid inputs will raise rich.internals.ConversionError, else the error will be reported onto the console
		self.initial_value 						 	= kwargs.get("initial_value", None)								# If present, the value is placed in the prompt as the default value

	def ask(self):
		result = prompt(f"{self.question}\n",
										target_type=self.target_type,
										validator=self.validator,
										secure=self.secure,
										raise_validation_fail=self.raise_validation_fail,
										raise_type_conversion_fail=self.raise_type_conversion_fail,
										initial_value=self.initial_value)
										
		return Result(self.question, result)

# ----------------------------------------------------------------------------------------

class YesNoQuestion:
	def __init__(self, *args, **kwargs):
		self.question 						= args[0]																		# Question to be asked						
		self.yes_text 						= kwargs.get("yes_text", "Yes")							# Text of positive response
		self.no_text 							= kwargs.get("no_text", "No")								# Text of negative response	
		self.has_to_match_case 		= kwargs.get("has_to_match_case", False)		# Check if typed response matches case
		self.enter_empty_confirms = kwargs.get("enter_empty_confirms", True)	# No response is considered as confirmation
		self.default_is_yes 			= kwargs.get("default_is_yes", False)				# Default response is positive
		self.cursor 							= kwargs.get("cursor", ">")									# Cursor to be shown
		self.cursor_style 				= kwargs.get("cursor_style", "grey82")			# Rich friendly cursor style
		self.char_prompt 					= kwargs.get("char_prompt", False)					# Print [Y/N] after the question

	def ask(self):
		result = confirm(f"[white]{self.question}[/white]\n",
										 yes_text=self.yes_text,
										 no_text=self.no_text,
										 has_to_match_case=self.has_to_match_case,
										 enter_empty_confirms=self.enter_empty_confirms,
										 default_is_yes=self.default_is_yes,
										 cursor=self.cursor,
										 cursor_style=self.cursor_style,
										 char_prompt=self.char_prompt)

		return Result(self.question, result, answer=self.yes_text if result else self.no_text)

# ----------------------------------------------------------------------------------------

class SingleChoiceQuestion:
	def __init__(self, *args, **kwargs):
		self.question 		= args[0]																			# Question to be asked		
		self.options 			= args[1]																			# A list of options to select from
		self.preprocessor = kwargs.get("preprocessor", lambda val: val)	# A callable that can be used to preprocess the list of options prior to printing
		self.cursor 			= kwargs.get("cursor", ">")										# Cursor that is going to appear in front of currently selected option
		self.cursor_style = kwargs.get("cursor_style", "grey82")					# Rich friendly style for the cursor
		self.cursor_index = kwargs.get("cursor_index", 0)								# Option can be preselected based on its list index
		self.return_index = kwargs.get("return_index", False)						# If True, select will return the index of selected element in options
		self.strict 			= kwargs.get("strict", False)									# If empty options is provided and strict is False, None will be returned, if it's True, ValueError will be thrown
		self.pagination 	= kwargs.get("pagination", False)							# If True, pagination will be used
		self.page_size 		= kwargs.get("page_size", 5)									# Number of options to show on a single page if pagination is enabled

	def ask(self):
		print(f"{self.question}\n")
		result = select(self.options, 
										preprocessor=self.preprocessor,	
										cursor=self.cursor, 
										cursor_style=self.cursor_style, 
										cursor_index=self.cursor_index, 
										return_index=self.return_index, 
										strict=self.strict, 
										pagination=self.pagination, 
										page_size=self.page_size)

		return Result(self.question, result)

# ----------------------------------------------------------------------------------------

class MultipleChoiceQuestion:
	def __init__(self, *args, **kwargs):
		self.question 			= args[0]																			# Question to be asked		
		self.options 				= args[1]																			# A list of options to select from
		self.preprocessor   = kwargs.get("preprocessor", lambda val: val)	# A callable that can be used to preprocess the list of options prior to printing
		self.tick_character = kwargs.get("tick_character", "✓")						# Character that will be used as a tick in a checkbox
		self.tick_style 		= kwargs.get("tick_style", "grey82")					# Rich friendly style for tick character
		self.cursor_style 	= kwargs.get("cursor_style", "green")					# Rich friendly style for the option when the cursor is currently on it
		self.ticked_indices = kwargs.get("ticked_indices", None)					# Indices of options that are pre-ticked when the prompt appears
		self.cursor_index 	= kwargs.get("cursor_index", 0)								# Index of the option cursor starts at
		self.minimal_count 	= kwargs.get("minimal_count", 0)							# Minimal count of options that need to be selected
		self.maximal_count 	= kwargs.get("maximal_count", None)						# Maximal count of options that need to be selected
		self.return_indices = kwargs.get("return_indices", False)					# If True, select_multiple will return the indices of ticked elements in options
		self.strict 				= kwargs.get("strict", False)									# If empty options is provided and strict is False, None will be returned, if it's True, ValueError will be thrown
		self.pagination 		= kwargs.get("pagination", False)							# If True, pagination will be used
		self.page_size 			= kwargs.get("page_size", 5)									# Number of options to show on a single page if pagination is enabled

	def ask(self):
		print(f"{self.question}\n")
		result = select_multiple(self.options,
														 preprocessor=self.preprocessor,	
														 tick_character=self.tick_character,
														 tick_style=self.tick_style,
														 cursor_style=self.cursor_style,
														 ticked_indices=self.ticked_indices,
														 cursor_index=self.cursor_index,
														 minimal_count=self.minimal_count,
														 maximal_count=self.maximal_count,
														 return_indices=self.return_indices,
														 strict=self.strict,
														 pagination=self.pagination,
														 page_size=self.page_size)

		return Result(self.question, result)

# ----------------------------------------------------------------------------------------

class FilePathQuestion:
	def __init__(self, *args, **kwargs):
		self.question 				= args[0]																							# Question to be asked
		self.default 					= kwargs.get("default", "")														# Default return value (single value)
		self.qmark 						= kwargs.get("qmark", "")															# Question prefix displayed in front of the question
		self.complete_style 	= kwargs.get("complete_style", CompleteStyle.COLUMN)	# How autocomplete menu would be shown, it could be COLUMN MULTI_COLUMN or READLINE_LIKE from prompt_toolkit.shortcuts.CompleteStyle
		self.validate 				= kwargs.get("validate", None)												# Require the entered value to pass a validation. The value can not be submitted until the validator accepts it (e.g. to check minimum password length).
		self.completer 				= kwargs.get("completer", None)												# A custom completer to use in the prompt. For more information, see this.
		self.style 						= kwargs.get("style", None)														# A custom color and style for the question parts. You can configure colors as well as font types for different elements.
		self.only_directories = kwargs.get("only_directories", False)								# Only show directories in auto completion. This option does not do anything if a custom completer is passed.
		self.get_paths 				= kwargs.get("get_paths", None)												# Set a callable to generate paths to traverse for suggestions. This option does not do anything if a custom completer is passed.
		self.file_filter 			= kwargs.get("file_filter", None)											# Optional callable to filter suggested paths. Only paths where the passed callable evaluates to True will show up in the suggested paths. This does not validate the typed path, e.g. it is still possible for the user to enter a path manually, even though this filter evaluates to False. If in addition to filtering suggestions you also want to validate the result, use validate in combination with the file_filter.

	def ask(self):
		result = questionary.path(f"{self.question}\n\n>",
														  default=self.default,
														  qmark=self.qmark,
														  complete_style=self.complete_style,
														  validate=self.validate,
														  completer=self.completer,
														  style=self.style,
														  only_directories=self.only_directories,
														  get_paths=self.get_paths,
														  file_filter=self.file_filter).ask()

		return Result(self.question, result)

# ----------------------------------------------------------------------------------------

class ConsoleSpinner:
	def __init__(self, *args, **kwargs):
		self.spinner_characters = kwargs.get("spinner_characters", DOTS)	# List of strings that will be displayed in sequence by a spinner
		self.text 							= kwargs.get("text", "Loading...")				# Static text that will be shown after the spinner
		self.time 							= kwargs.get("time", 0)										# Time in seconds that the spinner will be shown
		self.refresh_per_second = kwargs.get("refresh_per_second", 10)		# Number of refreshes the spinner will do a second, this will affect the fluidity of the "animation"
		self.transient					= kwargs.get("transient", True)						# If True, the spinner will be shown until the program is terminated

		self.spinner = Spinner(self.spinner_characters, 
													 self.text, 
													 refresh_per_second=self.refresh_per_second, 
													 transient=self.transient)

		self.spinner.start()

		if self.time > 0:
			time.sleep(self.time)
			self.stop()

	def stop(self):
		self.spinner.stop()