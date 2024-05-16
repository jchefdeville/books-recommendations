from flask import Flask, render_template
import pandas as pd

CSV_BOOK_COLUMN_PUBLISHED_DATE = "publishedDate"
CSV_BOOK_COLUMN_CATEGORIES = "categories"
CSV_BOOK_COLUMN_AUTHORS = "authors"
CSV_BOOK_COLUMN_RATINGS_COUNT = "ratingsCount"

CSV_RATING_COLUMN_BOOK_TITLE = "Title"
CSV_RATING_COLUMN_USER_ID = "User_id"
CSV_RATING_COLUMN_REVIEW_SCORE = "review/score"

CATEGORY_FICTION = "Fiction"

# flask call
app = Flask(__name__)

# link python to front end
# temporarily prints out the top fiction books in brec.html>
@app.route('/')
def Brec():
    top_books_df = getTopReviews(getBooks(), CATEGORY_FICTION)
    return render_template('Brec.html', top_books_df=top_books_df)

# Read CSV functions #
def getBooks():
    booksCsv = "data/amazon_books.csv"
    return pd.read_csv(booksCsv, encoding='ISO-8859-1', delimiter=',')

def getRatings():
    booksCsv = "data/amazon_ratings.csv"
    return pd.read_csv(booksCsv, encoding='ISO-8859-1', delimiter=',')

def getAuthorBooks(dfBooks, author):
    authors = "['Neal Shusterman']"
    print("Filter by authors" + authors)
    filterAuthors = dfBooks[CSV_BOOK_COLUMN_AUTHORS] == authors
    return dfBooks[filterAuthors].sort_values(by=CSV_BOOK_COLUMN_PUBLISHED_DATE)

def getBookRatings(dfRatings):
    bookName = "Dark Matter"
    print("Filter by bookName" + bookName)
    filterTitle = dfRatings[CSV_RATING_COLUMN_BOOK_TITLE] == bookName
    return dfRatings[filterTitle]

def printTopReadCategories(dfBooks):
    print("Filter by categories")
    dfBookGroupByCategories = dfBooks.groupby(CSV_BOOK_COLUMN_CATEGORIES)
    # Remove small categories
    dfBookGroupByCategories = dfBookGroupByCategories.filter(lambda dfCategorie: len(dfCategorie) > 1)

    # Print top10 categories read DESC
    print(dfBookGroupByCategories[CSV_BOOK_COLUMN_CATEGORIES].value_counts().head(50))

def getTopReviews(dfBooks, category : str):
    filterCategories = dfBooks[CSV_BOOK_COLUMN_CATEGORIES] == f"['{category}']"
    dfBooksCategories = dfBooks[filterCategories]
    dfBooksCategories_sorted = dfBooksCategories.sort_values(by=CSV_BOOK_COLUMN_RATINGS_COUNT, ascending=False)
    return dfBooksCategories_sorted.head(30)

def printTopBooksByReview(dfBooks, category : str, dfRatings):
    filterCategories = dfBooks[CSV_BOOK_COLUMN_CATEGORIES] == f"['{category}']"
    dfBooksCategories = dfBooks[filterCategories]

    dfRatingsPerBook = dfRatings.groupby(CSV_RATING_COLUMN_BOOK_TITLE).size()
    # Filter by enough number of reviews
    dfRatingsPerBook = dfRatingsPerBook[dfRatingsPerBook > 15].index
    dfRatingsPerBook = dfRatings[dfRatings[CSV_RATING_COLUMN_BOOK_TITLE].isin(dfRatingsPerBook)]
    
    dfBooksCategoriesRatings = pd.merge(dfBooksCategories, dfRatingsPerBook, on=CSV_RATING_COLUMN_BOOK_TITLE, how='inner')

    dfBooksCategoriesRatingsGroupByTitle = dfBooksCategoriesRatings.groupby(CSV_RATING_COLUMN_BOOK_TITLE)
    dfBooksCategoriesRatingsGroupByTitleAverageScore = dfBooksCategoriesRatingsGroupByTitle[CSV_RATING_COLUMN_REVIEW_SCORE].mean()
    dfBooksCategoriesRatingsGroupByTitleAverageScore = dfBooksCategoriesRatingsGroupByTitleAverageScore.sort_values(ascending=False)

    print(dfBooksCategoriesRatingsGroupByTitleAverageScore.head(40))

def printSpecificUserRatings(dfRatings):
    filterUserId = dfRatings[CSV_RATING_COLUMN_USER_ID] == "A1TZ2SK0KJLLAV"
    dfRatingsUserId = dfRatings[filterUserId]

    print(dfRatingsUserId)

def printBestUsersRatings(dfRatings):
    dfRatingsGroupByUserId = dfRatings[CSV_RATING_COLUMN_USER_ID].value_counts()
    print(dfRatingsGroupByUserId.head(10))

    userIdMostRatings = dfRatingsGroupByUserId.idxmax()
    dfRatingsUserIdMostRatings = dfRatings[dfRatings[CSV_RATING_COLUMN_USER_ID] == userIdMostRatings]
    print(dfRatingsUserIdMostRatings.head(50))


# MAIN CODE #
print('flask')
if __name__ == '__main__':
    app.run(debug=True)

# Unit Tests

# Retrieve CSV 
# dfBooks = getBooks()
# dfRatings = getRatings()


# Print some basic needs

# dfAuthorBooks = getAuthorBooks(dfBooks, "")
# print(dfAuthorBooks)

# dfBookRatings = getBookRatings(dfRatings)
# print(dfBookRatings)

# printTopReadCategories(dfBooks)

# dfTopReviews = getTopReviews(dfBooks, CATEGORY_FICTION)
# print(dfTopReviews)

# printSpecificUserRatings(dfRatings)

# printBestUsersRatings(dfRatings)

# printTopBooksByReview(dfBooks, CATEGORY_FICTION, dfRatings)