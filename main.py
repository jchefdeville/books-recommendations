import pandas as pd

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
    return dfBooks[filterAuthors].sort_values(by='publishedDate')

def getBookRatings(dfRatings):
    bookName = "Dark Matter"
    print("Filter by bookName" + bookName)
    filterTitle = dfRatings["Title"] == bookName
    return dfRatings[filterTitle]


# MAIN CODE #
dfBooks = getBooks()
# print(dfBooks.iloc[-1])

dfAuthorBooks = getAuthorBooks(dfBooks, "")
print(dfAuthorBooks)

dfRatings = getRatings()
print(dfRatings.iloc[-1])

dfBookRatings = getBookRatings(dfRatings)
print(dfBookRatings)
