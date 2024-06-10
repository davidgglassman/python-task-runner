# coding=utf-8

################################################################################
# IMPORTS
################################################################################

import os
import sys
import argparse
import json
import console_helpers

import importlib

from rich.console import Console

from console_helpers import GenericQuestion, YesNoQuestion, SingleChoiceQuestion, MultipleChoiceQuestion, ConsoleSpinner

from status_helpers import Status

################################################################################
# VARIABLES
################################################################################

console = Console()

modules_dict = {}

################################################################################
# FUNCTIONS
################################################################################

def clear_screen():
	os.system("cls" if os.name == "nt" else "clear")

def get_space():
	return ""

def get_line(character="-", width=75):
	return f"{character * width}"

def import_manifest():
	result = None

	try:
		parser = argparse.ArgumentParser()
		parser.add_argument("--manifest", type=str, help="Path to the manifest file")
		args = parser.parse_args()

		manifest = "manifest.json"

		if args.manifest:
			manifest = args.manifest
		
		if not os.path.exists(manifest):
			console.print(f"Manifest file not found at {manifest}")

		data = None

		with open(manifest, "r") as f:
			try:
				result = json.load(f)
			
			except json.JSONDecodeError as e:
				console.print("Invalid JSON in manifest file")
			
			except Exception as e:
				console.print(f"Error reading manifest file: {e}")

	except Exception as e:
		console.print(f"An error occurred while importing manifest: {e}")
	
	finally:
		return result

def import_tasks(path):
	result = False

	try:
		tasks_path = path and path or "tasks"

		sys.path.append(tasks_path)

		if os.path.isdir(tasks_path) and '__init__.py' in os.listdir(tasks_path):
			try:
				for module_name in os.listdir(tasks_path):
					if module_name.endswith(".py") and module_name != "__init__.py":
						module_name = module_name[:-3]
						modules_dict[module_name] = importlib.import_module(module_name)

				result = True

			except Exception as e:
				console.print(f"An error occurred while importing tasks: {e}")
		
		else:
			console.print("Tasks folder or __init__.py not found.")
		
	except Exception as e:
		console.print(f"An error occurred while importing tasks: {e}")

	finally:
		return result

def get_module(key, value):
	for module_name, module in modules_dict.items():
		if module.get_info()[key] == value:
			return module

def get_task_names():
	tasks = modules_dict.values()
	
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

		# -------- Import Manifest

		manifest_info = import_manifest()

		if not manifest_info:
			return

		app_name 	 = manifest_info.get("app_name", None)
		version  	 = manifest_info.get("version", None)
		tasks_path = manifest_info.get("tasks_path", None)

		if not app_name or not version:
			console.print("Manifest file is missing some required fields")
			return

		# -------- Import Tasks
		
		if not import_tasks(tasks_path):
			return

		# -------- Main Menu

		ApplicationHeader.print(app_name, version)
		
		# -------- Main Menu Questions Loop

		while True:
			choice = SingleChoiceQuestion("\nWhat would you like to do?", get_task_names()).ask()

			if choice.value == "Exit the application":
				clear_screen()
				break

			# -------- Selected Task

			task = get_module("prompt", choice.value)

			info = task.get_info()

			header = CommandHeader(info["header"]["title"], info["header"]["descriptions"])
			
			summarizer = TaskSummarizer(header)
			summarizer.print_header()

			# -------- Selected Task Questions Loop

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
					console.print(get_space())

					# -------- Run Task Steps

					for index, task in enumerate(summarizer.tasks):
						spinner = ConsoleSpinner(text=f"Running Task {index + 1} of {len(summarizer.tasks)}: {info['steps'][index]['name']}", time=1)

						result = info["steps"][index]["function"](task)

						if type(result) == tuple:
							status = Status(result[0], error=not result[1])
							
							print(status)

							spinner.stop()
							
							if status.error:
								console.print(f"\n{get_line()}")
								break

						else:
							print("Task step did not return a tuple")
							spinner.stop()
							break

					break

	except AttributeError:
		clear_screen()
		return

	except Exception as e:
		print(f"An error occurred: {e}")


if __name__ == "__main__":
	main()