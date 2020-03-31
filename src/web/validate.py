
def validate_add_to_dataset(obj):
	def validate_emotion():
		if 'emotion' in obj:
			print('si hay emotion')
		else:
			return False
		
	
	return validate_emotion()
