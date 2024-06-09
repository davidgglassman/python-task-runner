import importlib
import os
import sys

def import_all_modules():
	directory = os.path.dirname(__file__)
	module_names = []
	for filename in os.listdir(directory):
		if filename.endswith(".py") and filename != "__init__.py":
			module_name = filename[:-3]
			module_path = f"{__name__}.{module_name}"
			importlib.import_module(module_path)
			module_names.append(module_path)
	return module_names

# Import all modules when the package is imported
imported_modules = import_all_modules()

# Create a dictionary to store the references to the modules
modules_dict = {module_name.split('.')[-1]: sys.modules[module_name] for module_name in imported_modules}