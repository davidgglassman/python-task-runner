class Status:
	def __init__(self, message="", error=False):
		self.error = error
		self.message = message

	def __str__(self):
		return f"{self.error and '❌' or '✅'} {self.message}"