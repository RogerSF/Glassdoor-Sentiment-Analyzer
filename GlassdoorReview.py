import MySQLdb

class GlassdoorReview:
    """Contains the five fields of each Glassdoor review: rating, title, pros
    cons, and advice. This class also provides static methods for retrieving
    glassdoor reviews from the reviews table."""

    def __init__(self, id, rating, title, pros, cons, advice):
        """Creates a Glassdoor Review object with all five fields populated."""
        self.id = id
        self.rating = rating
        self.title = title
        self.pros = pros
        self.cons = cons
        self.advice = advice

    @staticmethod
    def get_training_set():
        """Returns the training set for this project."""
        return GlassdoorReview.get_review_list(101, 895)

    @staticmethod
    def get_test_set():
        """Returns the test set for the NLP project."""
        return GlassdoorReview.get_review_list(1, 100)

    @staticmethod
    def get_review_list(start_id=1, number_of_reviews=1):
        """Returns a list of GlassdoorReview objects, starting from the start_id
        and the subsequent reviews based on number_of_reviews."""

        # Establish connection.
        con = MySQLdb.connect(
            host='silo.cs.indiana.edu',
            user='harry',
            passwd='rutabega',
            db='glassdoor',
            port=14272
        )
        cursor = con.cursor()

        # Retrieve reviews based on input parameters.
        try:
            if number_of_reviews is 1:
                query = """SELECT * FROM reviews WHERE id = %s"""
                cursor.execute(query, (start_id))
            else:
                query = """SELECT * FROM reviews WHERE id >= %s AND id <= %s"""
                cursor.execute(query, (start_id, start_id + number_of_reviews))
        except:
            print "There was an error in trying to retrieve reviews."
            con.rollback()

        # Pack the retrieved reviews into a a list.
        reviews = []
        row = cursor.fetchone()
        while row is not None:
            review = GlassdoorReview(row[0], row[1], row[2], row[3], row[4], row[5])
            reviews.append(review)
            row = cursor.fetchone()

        con.close()
        return reviews
