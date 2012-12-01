from BeautifulSoup import BeautifulSoup as Soup
import soupselect; soupselect.monkeypatch()
import urllib2
import MySQLdb

class Fortune100Scraper:
    """A convenient way to get the 100 companies into a database."""
    def __init__(self):
        pass

    def scrapeFortune100(self):
        """Scrapes off 100 companies from CNN's Fortune 500 companies list."""
        url = 'http://money.cnn.com/magazines/fortune/global500/2012/full_list/index.html'
        soup = Soup(urllib2.urlopen(url))
        companies = soup.findSelect('td.cnncol2 a')
        
        con = MySQLdb.connect(
            host='silo.cs.indiana.edu',
            user='harry',
            passwd='rutabega',
            db='glassdoor',
            port=14272
        )

        x = con.cursor()
        
        for company in companies:
            try:
                query = """INSERT INTO companies (name) VALUES (%s)"""
                x.execute(query, (company.string))
                con.commit()
            except:
                con.rollback()

        con.close()

def getCompanyList():
    """Retrieves 100 companies in the companies table."""
    con = MySQLdb.connect(
        host='silo.cs.indiana.edu',
        user='harry',
        passwd='rutabega',
        db='glassdoor',
        port=14272
    )
    x = con.cursor()

    companiesList = []
    try:
        x.execute("""SELECT name FROM companies""")
        company = x.fetchone()
        while company is not None:
            companiesList.append(company[0])
            company = x.fetchone()
    except:
        con.rollback()
    con.close()

    return companiesList
