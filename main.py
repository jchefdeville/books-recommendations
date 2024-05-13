import pandas as pd

CSV_BOOK_COLUMN_PUBLISHED_DATE = "publishedDate"
CSV_BOOK_COLUMN_CATEGORIES = "categories"

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
    filterAuthors = dfBooks["authors"] == authors
    return dfBooks[filterAuthors].sort_values(by=CSV_BOOK_COLUMN_PUBLISHED_DATE)

def getBookRatings(dfRatings):
    bookName = "Dark Matter"
    print("Filter by bookName" + bookName)
    filterTitle = dfRatings["Title"] == bookName
    return dfRatings[filterTitle]

def printTop10ReadCategories(dfBooks):
    print("Filter by categories")
    dfBookGroupByCategories = dfBooks.groupby(CSV_BOOK_COLUMN_CATEGORIES)
    # Remove small categories
    dfBookGroupByCategories = dfBookGroupByCategories.filter(lambda dfCategorie: len(dfCategorie) > 1)

    # Print top10 categories read DESC
    print(dfBookGroupByCategories[CSV_BOOK_COLUMN_CATEGORIES].value_counts().head(10))



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
