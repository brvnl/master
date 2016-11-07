from sklearn.feature_extraction.text import CountVectorizer

vectorizer = CountVectorizer(min_df=1)
X = vectorizer.fit_transform(corpus)

class Text2BoW:

	def __init__(self, manifestFile):
		self.manifest = manifestFile
	
	def transform(self):
	
		# Openning manifest file
		with open(manifestFile, 'r') as f:
			data = f.readlines()
			for line in data:
			
			
		file = open('newfile.txt', 'r')
		print file.read()