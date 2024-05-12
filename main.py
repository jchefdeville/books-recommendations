import pandas as pd

def readBookInformations():
    booksCsv = "source/books.csv"
    cols_to_read = ["ISBN", "Book-Title"]
    return pd.read_csv(booksCsv, usecols=cols_to_read, encoding='ISO-8859-1', delimiter=';')

def readRatings(isbn):
    path_ratings = "source/ratings.csv"
    ratings = pd.read_csv(path_ratings, encoding='ISO-8859-1', delimiter=';')
    filterISBN = ratings["ISBN"] == isbn
    filteredRatings = ratings[filterISBN]
    filterNoVote = filteredRatings["Book-Rating"] > 0
    return filteredRatings[filterNoVote]

bookHarryPotter1 = '059035342X'

# Read books
dfBooks = readBookInformations()

filterISBN = dfBooks["ISBN"] == bookHarryPotter1
dfBooks = dfBooks[filterISBN]
print(dfBooks)

# Ratings > 0 from book
dfRatings = readRatings(bookHarryPotter1)

print("Average rating =", + dfRatings["Book-Rating"].mean(), "for", len(dfRatings), "users")
