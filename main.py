from flask import Flask, render_template
import pandas as pd

CSV_BOOK_COLUMN_PUBLISHED_DATE = "publishedDate"
CSV_BOOK_COLUMN_CATEGORIES = "categories"
CSV_BOOK_COLUMN_AUTHORS = "authors"
CSV_BOOK_COLUMN_RATINGS_COUNT = "ratingsCount"

CSV_RATING_COLUMN_BOOK_TITLE = "Title"
CSV_RATING_COLUMN_USER_ID = "User_id"

# flask call
app = Flask(__name__)

# link python to front end
# temporarily prints out the top fiction books in brec.html>
@app.route('/')
def Brec():
    top_books_df = displayTopRev(getBooks(), 'Fiction')
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

def printTopRevFiction(dfBooks):
    filterCategoriesFiction = dfBooks[CSV_BOOK_COLUMN_CATEGORIES] == "['Fiction']"
    dfBooksCategoriesFiction = dfBooks[filterCategoriesFiction]
    dfBooksCategoriesFiction_sorted = dfBooksCategoriesFiction.sort_values(by=CSV_BOOK_COLUMN_RATINGS_COUNT, ascending=False)
    print(dfBooksCategoriesFiction_sorted.head(30))
    
def printTopRev(dfBooks, category : str):
    filterCategories = dfBooks[CSV_BOOK_COLUMN_CATEGORIES] == f"['{category}']"
    dfBooksCategories = dfBooks[filterCategories]
    dfBooksCategories_sorted = dfBooksCategories.sort_values(by=CSV_BOOK_COLUMN_RATINGS_COUNT, ascending=False)
    print(dfBooksCategories_sorted.head(30))

def displayTopRev(dfBooks, category : str):
    filterCategories = dfBooks['categories'] == f"['{category}']"
    dfBooksCategories = dfBooks[filterCategories]
    dfBooksCategories_sorted = dfBooksCategories.sort_values(by='ratingsCount', ascending=False)
    return dfBooksCategories_sorted.head(30)

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

  #  dfBooks = getBooks()
   # dfRatings = getRatings()

# dfAuthorBooks = getAuthorBooks(dfBooks, "")
# print(dfAuthorBooks)

# dfBookRatings = getBookRatings(dfRatings)
# print(dfBookRatings)

# printTopReadCategories(dfBooks)

 #   printTopRev(dfBooks, 'Fiction')

# printSpecificUserRatings(dfRatings)

# printBestUsersRatings(dfRatings)
