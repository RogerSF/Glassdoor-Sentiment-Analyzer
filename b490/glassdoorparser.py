import BeautifulSoup

class GlassdoorParser:
    """Uses BeautifulSoup to parse the Glassdoor HTML files."""

    def parseAndStoreGlassdoorReview(self, glassdoorHTML):
        """Parses and stores a single Glassdoor review page HTML file into the database."""
        pass

    def divideFile(self, glassdoorHTML):
        """Parses the HTML file into 10 different segments, with each segment
        representing an unparsed Glassdoor review."""

        pass

    def parseReview(self, review):
        """Parses the HTML of a single Glassdoor review and compiles them into
        a dictionary containing title, rating, pros, cons, and advice to management."""

        pass

    def storeReview(self, contentDictionary):
        """Stores the dictionary containing the 5 fields of a glassdoor review."""

        pass

