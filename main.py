import pandas as pd

# Read CSV functions #
def getBookInformations(isbn):
    booksCsv = "source/books.csv"
    cols_to_read = ["ISBN", "Book-Title"]
    dfBooks = pd.read_csv(booksCsv, usecols=cols_to_read, encoding='ISO-8859-1', delimiter=';')
    filterISBN = dfBooks["ISBN"] == isbn
    return dfBooks[filterISBN]

def getBooks(author):
    booksCsv = "source/books.csv"
    cols_to_read = ["ISBN", "Book-Title", "Book-Author", "Year-Of-Publication"]
    dfBooks = pd.read_csv(booksCsv, usecols=cols_to_read, encoding='ISO-8859-1', delimiter=';')
    filterISBN = dfBooks["Book-Author"] == author
    return dfBooks[filterISBN].sort_values(by='Year-Of-Publication')

def getRatings(isbn):
    path_ratings = "source/ratings.csv"
    ratings = pd.read_csv(path_ratings, encoding='ISO-8859-1', delimiter=';')
    filterISBN = ratings["ISBN"] == isbn
    filteredRatings = ratings[filterISBN]
    filterNoVote = filteredRatings["Book-Rating"] > 0
    return filteredRatings[filterNoVote]


# Prints functions #
def printBookRatings(isbn):
    dfBook = getBookInformations(isbn)
    print(dfBook["Book-Title"].values)

    dfRatings = getRatings(isbn)
    print("Average rating =", + dfRatings["Book-Rating"].mean(), "for", len(dfRatings), "users")


# Execution main code #
author = "Neal Shusterman"
dfBooks = getBooks(author)
print(dfBooks)

print("******")

isbnHarryPotter1 = '059035342X'
printBookRatings(isbnHarryPotter1)

print("******")

isbnHarryPotter2 = '0439064872'
printBookRatings(isbnHarryPotter2)
