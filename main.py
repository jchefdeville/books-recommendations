from flask import Flask, render_template, request
import pandas as pd
from fuzzywuzzy import fuzz
import re

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
    # Get the page number from the query parameters, default to 1
    page = request.args.get('page', default=1, type=int)
    top_books_df = displayTopRev(getBooks(), 'Fiction', page)
    unique_books_df = remove_duplicates(top_books_df)
    return render_template('Brec.html', top_books_df=unique_books_df, page=page)


# detecting duplicates
def titleCompare(title1, title2):
    similarity = fuzz.ratio(title1.lower(), title2.lower())
    # Adjust threshold as needed
    return similarity > 80

# Read CSV functions #
def getBooks():
    booksCsv = "data/amazon_books.csv"
    return pd.read_csv(booksCsv, encoding='ISO-8859-1', delimiter=',')

def remove_duplicates(df):
    unique_titles = []
    unique_rows = []
    for index, row in df.iterrows():
        # Removes all special characters and everything inside parentheses for better comparison
        cleaned_title = re.sub(r'\([^()]*\)', '', row['Title']).strip()
        similar_titles = [fuzz.ratio(cleaned_title.lower(), title.lower()) for title in unique_titles]
        if not any(similarity > 60 for similarity in similar_titles):
            unique_titles.append(cleaned_title)
            unique_rows.append(row)
    # Creates a new DataFrame from the unique rows
    unique_books = pd.DataFrame(unique_rows, columns=df.columns)
    return unique_books

def getRatings():
    booksCsv = "data/amazon_ratings.csv"
    return pd.read_csv(booksCsv, encoding='ISO-8859-1', delimiter=',')

def getAuthorBooks(dfBooks, author):
    if (author == ""):
        author = "'Georgetta Jaquith Walker"
    print("Filter by author : " + author)

    filterAuthors = dfBooks[CSV_BOOK_COLUMN_AUTHORS].str.contains(author, regex=True, na=False)

    return dfBooks[filterAuthors].sort_values(by=CSV_BOOK_COLUMN_PUBLISHED_DATE)

def printPopularBooksByAuthor(dfBooks, author):
    author = 'J.K. Rowling'
    dfBooksAuthor = getAuthorBooks(dfBooks, author)
    print(dfBooksAuthor.sort_values(by=CSV_BOOK_COLUMN_RATINGS_COUNT, ascending=False).head(10))

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
    
def displayTopRev(dfBooks, category : str, page : int):
    filterCategories = dfBooks['categories'] == f"['{category}']"
    dfBooksCategories = dfBooks[filterCategories]
    pagelimit = 30
    start = (page - 1) *pagelimit
    end = start + pagelimit
    dfBooksCategories_sorted = dfBooksCategories.sort_values(by='ratingsCount', ascending=False)
    return dfBooksCategories_sorted.iloc[start:end]

def getTopReviews(dfBooks, category: str):
    filterCategories = dfBooks[CSV_BOOK_COLUMN_CATEGORIES] == f"['{category}']"
    dfBooksCategories = dfBooks[filterCategories]
    dfBooksCategories_sorted = dfBooksCategories.sort_values(by=CSV_BOOK_COLUMN_RATINGS_COUNT, ascending=False)
    return dfBooksCategories_sorted.head(30)

def getTopBooksByScore(dfBooks, category: str, dfRatings):
    filterCategories = dfBooks[CSV_BOOK_COLUMN_CATEGORIES] == f"['{category}']"
    dfBooksCategories = dfBooks[filterCategories]

    dfRatingsPerBook = dfRatings.groupby(CSV_RATING_COLUMN_BOOK_TITLE).size()
    # Filter by enough number of reviews
    dfRatingsPerBook = dfRatingsPerBook[dfRatingsPerBook > 15].index
    dfRatingsPerBook = dfRatings[dfRatings[CSV_RATING_COLUMN_BOOK_TITLE].isin(dfRatingsPerBook)]
    
    dfBooksCategoriesRatings = pd.merge(dfBooksCategories, dfRatingsPerBook, on=CSV_RATING_COLUMN_BOOK_TITLE, how='inner')

    dfBooksCategoriesRatingsGroupByTitle = dfBooksCategoriesRatings.groupby(CSV_RATING_COLUMN_BOOK_TITLE)
    dfBooksCategoriesRatingsGroupByTitleAverageScore = dfBooksCategoriesRatingsGroupByTitle[CSV_RATING_COLUMN_REVIEW_SCORE].mean()
    return dfBooksCategoriesRatingsGroupByTitleAverageScore.sort_values(ascending=False)

def printUserFavoriteCategory(dfBooks, dfRatings):
    userId = "A25HYPL2XKQPZB"
    filterUserRatings = dfRatings[CSV_RATING_COLUMN_USER_ID] == userId
    dfUserRatings = dfRatings[filterUserRatings]

    dfUserBooksRatings = pd.merge(dfBooks, dfUserRatings, on=CSV_RATING_COLUMN_BOOK_TITLE, how='inner')
    dfUserBooksRatingsGroupByCategories = dfUserBooksRatings.groupby(CSV_BOOK_COLUMN_CATEGORIES).size().sort_values(ascending=False)

    print(dfUserBooksRatingsGroupByCategories.head(5))


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

def printRecommandBooksByCategory(dfBooks, dfRatings, CATEGORY_FICTION:str):
    dfBooksScore = getTopBooksByScore(dfBooks, CATEGORY_FICTION, dfRatings)
    print("Books by score")
    print(dfBooksScore.head(10))

    print("Books by reviews")
    dfBooksReview = getTopReviews(dfBooks, CATEGORY_FICTION)
    print(dfBooksReview.head(10))


# MAIN CODE #
print('flask')
# if __name__ == '__main__':
    # app.run(debug=True)

# Unit Tests

# Retrieve CSV 
dfBooks = getBooks()
dfRatings = getRatings()


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

# print(getTopBooksByScore(dfBooks, CATEGORY_FICTION, dfRatings).head(40))

# printPopularBooksByAuthor(dfBooks, "")

# printUserFavoriteCategory(dfBooks, dfRatings)

printRecommandBooksByCategory(dfBooks, dfRatings, CATEGORY_FICTION)