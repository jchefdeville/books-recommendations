import pandas as pd

CSV_BOOK_COLUMN_PUBLISHED_DATE = "publishedDate"
CSV_BOOK_COLUMN_CATEGORIES = "categories"
CSV_BOOK_COLUMN_AUTHORS = "authors"
CSV_BOOK_COLUMN_RATINGS_COUNT = "ratingsCount"

CSV_RATING_COLUMN_BOOK_TITLE = "Title"

# Read CSV functions #
def getBooks():
    booksCsv = "datas/amazon_books.csv"
    return pd.read_csv(booksCsv, encoding='ISO-8859-1', delimiter=',')

def getRatings():
    booksCsv = "datas/amazon_ratings.csv"
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

def printTop10ReadCategories(dfBooks):
    print("Filter by categories")
    dfBookGroupByCategories = dfBooks.groupby(CSV_BOOK_COLUMN_CATEGORIES)
    # Remove small categories
    dfBookGroupByCategories = dfBookGroupByCategories.filter(lambda dfCategorie: len(dfCategorie) > 1)

    # Print top10 categories read DESC
    print(dfBookGroupByCategories[CSV_BOOK_COLUMN_CATEGORIES].value_counts().head(50))

def printTop30ReadFiction(dfBooks):
    filterCategoriesFiction = dfBooks[CSV_BOOK_COLUMN_CATEGORIES] == "['Technology']"
    dfBooksCategoriesFiction = dfBooks[filterCategoriesFiction]
    dfBooksCategoriesFiction_sorted = dfBooksCategoriesFiction.sort_values(by=CSV_BOOK_COLUMN_RATINGS_COUNT, ascending=False)

    print(dfBooksCategoriesFiction_sorted.head(30))



# MAIN CODE #
dfBooks = getBooks()
# print(dfBooks.iloc[-1])

# dfAuthorBooks = getAuthorBooks(dfBooks, "")
# print(dfAuthorBooks)

# dfRatings = getRatings()
# print(dfRatings.iloc[-1])

# dfBookRatings = getBookRatings(dfRatings)
# print(dfBookRatings)

printTop10ReadCategories(dfBooks)

printTop30ReadFiction(dfBooks)
