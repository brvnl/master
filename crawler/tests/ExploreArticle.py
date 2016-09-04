#!/usr/bin/python
from newspaper import Article

# Prints article's data into a file whichs filename consists of timestamp and title.
def article2file( aArticle ):
	# Extracts only the first 100 chars
	title4name = aArticle.title[:100]
	title4name = title4name.replace(" ", "")
	title4name = title4name.replace(",", "")
	
	date4name = aArticle.publish_date.strftime('%Y%m%d%H%M%S')
	
	path = './'
	filename = path + date4name + '.' + title4name + '.txt' 
	text_file = open(filename, "w")
	text_file.write("%s" % a.text.encode('utf-8'))
	text_file.close()
	return 0
	

# Main program
url = 'http://www.reuters.com/article/us-mideast-crisis-bombers-idUSKCN10X25K'
a = Article(url)

a.download()
a.parse()

#title4name = a.title.replace(" ", "")
#title4name = title4name.replace(",", "")
#print('Title:')
#print(title4name)

print('First paragraph:')
print(a.text[:150])

#date4name = a.publish_date.strftime('%Y%m%d%H%M%S')
#print('Publication date:')
#print(date4name)

#path = './'
#filename = path + date4name + '.' + title4name + '.txt' 
#text_file = open(filename, "w")
#text_file.write("%s" % a.text.encode('utf-8'))
#text_file.close()

article2file(a)
