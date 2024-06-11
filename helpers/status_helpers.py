class Status:
	def __init__(self, result="", error=False):
		self.error = error
		self.result = result

	def __str__(self):
		return f"{self.error and '❌' or '✅'} {self.result}"