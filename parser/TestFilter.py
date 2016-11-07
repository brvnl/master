from ArticlesFilter import ArticlesFilter

corpus_root = '/Volumes/REPOSITORY/Mestrado/Thesis/data/'
keywords = ['Brazil', \
            'Brasil']

aFilter = ArticlesFilter(corpus_root, keywords)
aFilter.findArticles()
#aFilter.printFileList()
aFilter.files2hash()
aFilter.printFilesDetails()