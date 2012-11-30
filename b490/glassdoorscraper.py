import MySQLdb
import urllib2
from BeautifulSoup import BeautifulSoup

class GlassdoorScraper:
    """Use to scrape review pages of a company."""

    def __init__(self, reviewURL):
        """Creates a list of URLs that contain review #20-69."""

        # Contains the five URLs for getting reviews #20 to #69.
        self.reviewPages = [reviewURL]

        # Chop off the last five characters of the original URL to replace
        # page number.
        offset = len(reviewURL) - 5
        baseURL = reviewURL[0:offset]

        # Add the URLs to the list.
        for i in [3, 4, 5, 6]:
            reviewPage = baseURL + str(i) + '.htm'
            self.reviewPages.append(reviewPage)

    def scrapeAllPages(self):
        """Scrapes and stores the contents of all 5 review pages and stores
        them into the database."""

        for reviewPage in self.reviewPages:
            reviewPageHTML = self.scrapePage(reviewPage)
            self.saveReview(reviewPageHTML)

    def scrapePage(self, reviewPageURL):
        """Scrapes a single page based on the given URL and returns a string."""

        request = urllib2.Request(reviewPageURL)
        response = urllib2.urlopen(request)
        soup = BeautifulSoup(''.join(response.read()))
        return soup.prettify()

    def saveReview(self, reviewPage):
        """Stores the HTML of a review page into the database."""

        con = MySQLdb.connect(host='silo.cs.indiana.edu', user='harry',
                              passwd='rutabega', db='glassdoor', port=14272)
        cursor = con.cursor()

        try:
            query = """INSERT INTO raw_reviews (content) VALUES (%s)"""
            cursor.execute(query, (reviewPage))
            con.commit()
        except:
            print 'Failed to save review into database.'
            con.rollback()
        con.close()
