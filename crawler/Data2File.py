import os
import time
from newspaper import Article
from builtins import str
import unicodedata

def normalizeFileName(input_str):
    #new_srt = normalizeStrUTF8(input_str)
    #return ''.join(c for c in new_srt if c.isalnum())
    return ''.join(c for c in input_str if c.isalnum())

def normalizeStrUTF8(input_str):
    #nkfd_form = unicodedata.normalize('NFKD', unicode(input_str))

    nkfd_form = unicodedata.normalize('NFKD', input_str)
    #str_nkfd = str(nkfd_form)
    #str_nkfd2 = eval(str_nkfd)
    #str_nkfd = str_nkfd2.decode('utf-8')

    #return "".join([c for c in str_nkfd if not unicodedata.combining(c)])
    #return "".join([c for c in nkfd_form if not unicodedata.combining(c)])
    nkfd_norm = "".join([c for c in nkfd_form if not unicodedata.combining(c)])
    nkfd_str = str(nkfd_norm)
    nkfd_str2 = eval(nkfd_str)
    return nkfd_str2.decode('utf-8')

def getDataBasePath():
    return "../../data/"

# Prints article's data into a file whichs filename consists of timestamp and title.
def article2file( aArticle, path ):
    # Extracts only the first 100 chars
    title4name = aArticle.title[:100]

    # Remove special characters (TO BE COMPLETED...)
    title4name = title4name.replace(" ", "")
    title4name = title4name.replace(",", "")
    title4name = normalizeFileName(title4name)

    try:
        date4name = aArticle.publish_date.strftime('%Y%m%d%H%M%S')
    except:
        # If cannot retrieve publish date defaults to the day it has been captured
        date4name = time.strftime('%Y%m%d%H%M%S', time.gmtime())

    # If the path does not exists, create it
    if not os.path.exists(path):
        os.makedirs(path)

    # Composing the file name enforcing backslash.
    #filename = path + "/" + date4name + '.' + title4name + '.txt'
    filename = path + "/" + date4name + title4name + '.txt'

    try:
        # Write article`s data to a file whose name follows the pattern timestamp+title.
        # Ex.: 20160829000000.TemerpreparamudancasemvitrinessociaisdoPT.txt
        text_file = open(filename, "w")

        # Output format:
        #  1. First line gives the url for the article
        #  2. Second line gives the title of the article
        #  3. The next two lines are line breaks
        #  4. Follows the article`s full content
        text_file.write("%s" % aArticle.url)
        text_file.write("\n")
        #tmp_str = normalizeStrUTF8(aArticle.title.encode('utf-8'))
        #text_file.write("%s" % tmp_str)
        text_file.write("%s" % aArticle.title.encode('utf-8').decode('utf-8'))
        text_file.write("\n\n\n")
        #tmp_str = normalizeStrUTF8(aArticle.text.encode('utf-8'))
        #text_file.write("%s" % tmp_str)
        text_file.write("%s" % aArticle.text.encode('utf-8').decode('utf-8'))

        text_file.close()
    except:
        print("WARN - Cannot save article: " + aArticle.url +". Discarded.")
        return 1

    return 0
