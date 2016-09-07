import newspaper
import re
from Data2File import getDataBasePath, article2file
from NPSpyder import NPSpyder

# Same as NPSpyder, but for brazilian websites
class NPSpyderBR(NPSpyder):

    def __init__(self, name, sourceURL, regex):
        # Source`s name to create a path where data will be saved.
        self.sourceName = name

        # Building a Newspapper crawler...
        # defines the source website object from where the news are to be retrieved
        self.source = newspaper.build(sourceURL, memoize_articles=False, language='pt', fetch_images=False)

        # Define a regex to filter relevant article`s URLs
        self.filterRegex = regex