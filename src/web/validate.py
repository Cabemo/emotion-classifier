
def validate_add_to_dataset(obj):

	def validate_emotion():
		if 'emotion' in obj.keys():
			return obj['emotion'] in range(7)
		return False
		
	def validate_pixel():
		if 'pixels' in obj.keys() and type(obj['pixels']) is list:
			#print(len(obj['pixels']))
			return len(obj['pixels']) == 2034
		return False

	return validate_pixel() and validate_emotion()
