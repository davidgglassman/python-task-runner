# coding=utf-8

app_name = "CCI Tool"
version  = "v1.0.0"

################################################################################
# IMPORTS
################################################################################

import os
import console_helpers
import tasks as task_modules

from rich.console import Console

from console_helpers import GenericQuestion, YesNoQuestion, SingleChoiceQuestion, MultipleChoiceQuestion, ConsoleSpinner

from status_helpers import Status

################################################################################
# VARIABLES
################################################################################

console = Console()

################################################################################
# FUNCTIONS
################################################################################

def clear_screen():
	os.system("cls" if os.name == "nt" else "clear")

def get_space():
	return ""

def get_line(character="-", width=75):
	return f"{character * width}"

def get_module(key, value):
	for module_name, module in task_modules.modules_dict.items():
		if module.get_info()[key] == value:
			return module

def get_task_names():
	tasks = task_modules.modules_dict.values()
	
	task_names = [task.get_info()["prompt"] for task in tasks]
	task_names.append("Exit the application")
	
	return task_names

################################################################################
# CLASSES
################################################################################

class ApplicationHeader:
	@classmethod
	def print(cls, title, version):
		console.print(get_line(character="#"))
		console.print(get_space())
		console.print(f"{title} {version}")
		console.print(get_space())
		console.print(get_line(character="#"))

# ----------------------------------------------------------------------------------------

class CommandHeader:
	def __init__(self, title="", descriptions=[]):
		self.buffer = []
		
		self.buffer.append(get_line())
		self.buffer.append(get_space())
		self.buffer.append(title.upper())
		self.buffer.append(get_space())

		for description in descriptions:
			self.buffer.append(description)

		self.buffer.append(get_space())
		self.buffer.append(get_line())
		self.buffer.append(get_space())

	def print(self):
		for item in self.buffer:
			console.print(item)

	def clear(self):
		self.buffer = []

# ----------------------------------------------------------------------------------------

class TaskSummarizer:
	def __init__(self, header):
		self.header = header
		self.tasks = []

	def add(self, task):
		self.tasks.append(task)

	def print_header(self):
		clear_screen()
		self.header.print()

	def print_summary(self):
		self.print_header()

		for task in self.tasks:
			console.print(task)

	def clear(self):
		self.tasks = []
		self.print_header()

################################################################################
# MAIN
################################################################################

def main():
	try:
		clear_screen()

		ApplicationHeader.print(app_name, version)

		while True:
			choice = SingleChoiceQuestion("\nWhat would you like to do?", get_task_names()).ask()

			if choice.value == "Exit the application":
				clear_screen()
				break

			task = get_module("prompt", choice.value)

			info = task.get_info()

			header = CommandHeader(info["header"]["title"], info["header"]["descriptions"])
			
			summarizer = TaskSummarizer(header)
			summarizer.print_header()

			while True:
				summarizer.clear()

				for step in info["steps"]:
					cls = getattr(console_helpers, step["prompt_type"])
					instance = cls(*step["args"], **step["kwargs"])
					
					summarizer.add(instance.ask())
					summarizer.print_header()
				
				summarizer.print_summary()

				choice = YesNoQuestion("\nAre you satisfied with your answers?", default_is_yes=True).ask()
				
				if choice.value == "Yes":
					for index, task in enumerate(summarizer.tasks):
						result = info["steps"][index]["function"](task)
						print(result)
						
						if result.error:
							print("Task failed")
							break

					break

	except Exception as e:
		print(f"Exception: {e}")


if __name__ == "__main__":
	main()