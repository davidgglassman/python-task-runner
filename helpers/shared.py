################################################################################
# IMPORTS
################################################################################

from enum import StrEnum

################################################################################
# ENUMS
################################################################################

class PromptType(StrEnum):
	GENERIC 				= "GenericQuestion"
	YES_NO 					= "YesNoQuestion"
	SINGLE_CHOICE 	= "SingleChoiceQuestion"
	MULTIPLE_CHOICE = "MultipleChoiceQuestion"
	FILE_PATH				= "FilePathQuestion"

################################################################################
# CLASSES
################################################################################

class Status:
	def __init__(self, result="", error=False):
		self.error = error
		self.result = result

	def __str__(self):
		return f"{self.error and '❌' or '✅'} {self.result}"