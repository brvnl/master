import newspaper
import re
from Data2File import getDataBasePath, article2file
from NPSpyder import NPSpyder

# Same as NPSpyder, but for brazilian websites
class NPSpyderBR(NPSpyder):

    def __init__(self, name, sourceURL, regex, firstRun=0):
        # Source`s name to create a path where data will be saved.
        self.sourceName = name

        # Building a Newspapper crawler...
        # defines the source website object from where the news are to be retrieved
        if (firstRun == 1):
            self.source = newspaper.build(sourceURL, language='pt', fetch_images=False, memoize_articles=False)
        else:
            self.source = newspaper.build(sourceURL, language='pt', fetch_images=False)

        # Define a regex to filter relevant article`s URLs
        self.filterRegex = regex
