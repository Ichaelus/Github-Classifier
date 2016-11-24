
def ConvertClassifierCollectionToJSON(ClassifierCollection):
    # Return a list of classificator objects, containing the following attributes:
		# id: int, 
		# name: string, 
		# description: 
		# string, 
		# accuracy: int [0-100], 
		# active: boolean,
		# result: []
	print "Testkommeichhierhin"
	return '[{"id":1,"name":"Neural network","description":"A neuronal network with 3x2000 fully connected neurons. Only Readme, Description and Filenames are being used as input.","accuracy":"81","active":true,"result":[{"class":"DEV","val":0.0},{"class":"HW","val":0.0},{"class":"EDU","val":0.0},{"class":"DOCS","val":0.0},{"class":"WEB","val":0.0},{"class":"DATA","val":0.0},{"class":"OTHER","val":0.0}]},{"id":2,"name":"Neural network","description":"A neuronal network with 3x2000 fully connected neurons. Only Readme, Description and Filenames are being used as input.","accuracy":"55","active":false,"result":[{"class":"DEV","val":0.0},{"class":"HW","val":0.0},{"class":"EDU","val":0.0},{"class":"DOCS","val":0.0},{"class":"WEB","val":0.0},{"class":"DATA","val":0.0},{"class":"OTHER","val":0.0}]},{"id":2,"name":"Neural network","description":"A neuronal network with 3x2000 fully connected neurons. Only Readme, Description and Filenames are being used as input.","accuracy":"90","active":true,"result":[{"class":"DEV","val":0.0},{"class":"HW","val":0.0},{"class":"EDU","val":0.0},{"class":"DOCS","val":0.0},{"class":"WEB","val":0.0},{"class":"DATA","val":0.0},{"class":"OTHER","val":0.0}]}]'
			# EXAMPLE
			# [{
			#	id: 1,
			#	name: "Neural network",
			#	description: "A neuronal network with 3x2000 fully connected neurons. Only Readme, Description and Filenames are being used as input.",
			#	accuracy: "81",
			#	active: true,
			#	result: [
			#		{class: "DEV", val : 0.04},
			#		{class: "HW", val : 0.13},
			#		{class: "EDU", val : 0.11},
			#		{class: "DOCS", val : 0.24},
			#		{class: "WEB", val : 0.59},
			#		{class: "DATA", val : 0.02},
			#		{class: "OTHER", val : 0.04}
			#	]
			#}]

def getFormulas():
	return '["e=mc²", "Abra kadabra"]'