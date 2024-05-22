import re
from flask import Flask, render_template, request
import pandas as pd
from fuzzywuzzy import fuzz
from collections import Counter

CSV_BOOK_COLUMN_TITLE = "Title"
CSV_BOOK_COLUMN_PUBLISHED_DATE = "publishedDate"
CSV_BOOK_COLUMN_CATEGORIES = "categories"
CSV_BOOK_COLUMN_AUTHORS = "authors"
CSV_BOOK_COLUMN_RATINGS_COUNT = "ratingsCount"

CSV_RATING_COLUMN_BOOK_TITLE = CSV_BOOK_COLUMN_TITLE
CSV_RATING_COLUMN_USER_ID = "User_id"
CSV_RATING_COLUMN_REVIEW_SCORE = "review/score"

CATEGORY_FICTION = "Fiction"

ENCODING_CSV = 'UTF-8'

# Read CSV functions #
def getBooks():
    booksCsv = "data/amazon_books_v2.csv"
    return pd.read_csv(booksCsv, encoding=ENCODING_CSV, delimiter=',')

def getRatings():
    booksCsv = "data/amazon_ratings_v2.csv"
    return pd.read_csv(booksCsv, encoding=ENCODING_CSV, delimiter=',')

# Retrieve CSV
dfBooks = getBooks()
dfRatings = getRatings()

# flask call
app = Flask(__name__)

# link python to front end
# temporarily prints out the top fiction books in Home.html>
@app.route('/')
def Home():
    # Get the page number from the query parameters, default to 1
    page = request.args.get('page', default=1, type=int)
    print(f"page={page}")
    top_books_df = displayTopRev(CATEGORY_FICTION, page)
    unique_books_df = remove_duplicates(top_books_df)
    return render_template('Home.html', top_books_df=unique_books_df, category=CATEGORY_FICTION, page=page)

@app.route('/categories/<string:category>/books')
def BooksCategory(category:str):
    # Get the page number from the query parameters, default to 1
    page = request.args.get('page', default=1, type=int)
    print(f"page={page}")
    top_books_df = displayTopRev(category, page)
    unique_books_df = remove_duplicates(top_books_df)
    return render_template('Home.html', top_books_df=unique_books_df, category=category, page=page)

@app.route('/authors/')
def Authors():
    authors = getAuthors()
    return render_template('Authors.html', authors=authors)

@app.route('/authors/<string:author>/books')
def AuthorBooks(author:str):
    top_books_df = getAuthorBooks(author)
    print(top_books_df)
    unique_books_df = remove_duplicates(top_books_df)
    print(unique_books_df)
    return render_template('Home.html', top_books_df=unique_books_df, page=1)

@app.route('/books/<int:index_book>/ratings')
def Ratings(index_book):
    dfBook = getBook(index_book)
    dfRatingsBook = getRatingsBook(dfBook[CSV_BOOK_COLUMN_TITLE])
    print(dfRatingsBook)

    return render_template("Ratings.html", dfRatingsBook=dfRatingsBook)

@app.route('/users/')
def Users():
    page = request.args.get('page', default=1, type=int)
    users = getUsers(page)
    return render_template('Users.html', users=users, page=page)

@app.route('/users/<string:id_user>/recommendations')
def BooksRecommendations(id_user):
    recommendedBooks = getRecommandedBooksForUser(id_user)
    return render_template('BooksRecommendations.html', recommendedBooks=recommendedBooks)

@app.route('/users/<string:id_user>/ratings')
def userRatings(id_user):
    ratings = getSpecificUserRatings(id_user)
    ratings_list = list(ratings.to_records(index=False))
    return render_template('UserRatings.html', ratings_list=ratings_list)

@app.route('/categories/')
def Categories():
    df_books_top_read_categories = getTopReadCategories()
    return render_template('Categories.html', df_books_top_read_categories=df_books_top_read_categories)



# detecting duplicates
def titleCompare(title1, title2):
    similarity = fuzz.ratio(title1.lower(), title2.lower())
    # Adjust threshold as needed
    return similarity > 80

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


# get all authors
def getAuthors():
    authors = dfBooks[CSV_BOOK_COLUMN_AUTHORS]
    author_counts = Counter(authors)
    sorted_author_counts = sorted(author_counts.items(), key=lambda x:x[1], reverse=True)
    return sorted_author_counts

def getAuthorBooks(author):
    print("Filter by author : " + author)

    filterAuthors = dfBooks[CSV_BOOK_COLUMN_AUTHORS].str.contains(author, regex=False, na=False)

    return dfBooks[filterAuthors].sort_values(by=CSV_BOOK_COLUMN_RATINGS_COUNT, ascending=False)

def getPopularBooksByAuthor(author):
    if author == "":
        author = 'J.K. Rowling'
    dfBooksAuthor = getAuthorBooks(author)
    return dfBooksAuthor.sort_values(by=CSV_BOOK_COLUMN_RATINGS_COUNT, ascending=False)

def getBook(index:int):
    return dfBooks.iloc[index]

def getRatingsBook(bookTitle: str):
    if bookTitle == "":
        bookTitle = "Dark Matter"
    print("Get ratings for bookTitle=" + bookTitle)
    filterTitle = dfRatings[CSV_RATING_COLUMN_BOOK_TITLE] == bookTitle
    return dfRatings[filterTitle]

def getTopReadCategories():
    print("Group by categories")
    dfBookGroupByCategories = dfBooks.groupby(CSV_BOOK_COLUMN_CATEGORIES)
    # Remove small categories
    dfBookGroupByCategories = dfBookGroupByCategories.filter(lambda dfCategorie: len(dfCategorie) > 1)

    return dfBookGroupByCategories[CSV_BOOK_COLUMN_CATEGORIES].value_counts()

def displayTopRev(category: str, page: int):
    filterCategories = dfBooks[CSV_BOOK_COLUMN_CATEGORIES] == category
    dfBooksCategories = dfBooks[filterCategories]
    pagelimit = 30
    start = (page - 1) *pagelimit
    end = start + pagelimit
    dfBooksCategories_sorted = dfBooksCategories.sort_values(by=CSV_BOOK_COLUMN_RATINGS_COUNT, ascending=False)
    return dfBooksCategories_sorted.iloc[start:end]

def getTopReviews(category: str):
    filterCategories = dfBooks[CSV_BOOK_COLUMN_CATEGORIES] == category
    dfBooksCategories = dfBooks[filterCategories]
    dfBooksCategories_sorted = dfBooksCategories.sort_values(by=CSV_BOOK_COLUMN_RATINGS_COUNT, ascending=False)
    return dfBooksCategories_sorted

def getTopBooksByScore(category: str):
    filterCategories = dfBooks[CSV_BOOK_COLUMN_CATEGORIES] == category
    dfBooksCategories = dfBooks[filterCategories]

    dfRatingsPerBook = dfRatings.groupby(CSV_RATING_COLUMN_BOOK_TITLE).size()
    # Filter by enough number of reviews
    dfRatingsPerBook = dfRatingsPerBook[dfRatingsPerBook > 15].index
    dfRatingsPerBook = dfRatings[dfRatings[CSV_RATING_COLUMN_BOOK_TITLE].isin(dfRatingsPerBook)]
    
    dfBooksCategoriesRatings = pd.merge(dfBooksCategories, dfRatingsPerBook, on=CSV_RATING_COLUMN_BOOK_TITLE, how='inner')

    dfBooksCategoriesRatingsGroupByTitle = dfBooksCategoriesRatings.groupby(CSV_RATING_COLUMN_BOOK_TITLE)
    dfBooksCategoriesRatingsGroupByTitleAverageScore = dfBooksCategoriesRatingsGroupByTitle[CSV_RATING_COLUMN_REVIEW_SCORE].mean()
    return dfBooksCategoriesRatingsGroupByTitleAverageScore.sort_values(ascending=False)

def getUsers(page:int):
    users = dfRatings[CSV_RATING_COLUMN_USER_ID]
    users_counts = Counter(users)
    sorted_users_counts = sorted(users_counts.items(), key=lambda x:x[1], reverse=True)

    pagelimit = 30
    start = (page - 1) *pagelimit
    end = start + pagelimit

    return sorted_users_counts[start:end]

def getUserFavoriteCategory(userId):
    filterUserRatings = dfRatings[CSV_RATING_COLUMN_USER_ID] == userId
    dfUserRatings = dfRatings[filterUserRatings]

    dfUserBooksRatings = pd.merge(dfBooks, dfUserRatings, on=CSV_RATING_COLUMN_BOOK_TITLE, how='inner')
    dfUserBooksRatingsGroupByCategories = dfUserBooksRatings.groupby(CSV_BOOK_COLUMN_CATEGORIES).size().sort_values(ascending=False)

    return dfUserBooksRatingsGroupByCategories

def getSpecificUserRatings(userId):
    filterUserId = dfRatings[CSV_RATING_COLUMN_USER_ID] == userId
    dfRatingsUserId = dfRatings[filterUserId]
    return dfRatingsUserId

def getBestUsersRatings():
    dfRatingsGroupByUserId = dfRatings[CSV_RATING_COLUMN_USER_ID].value_counts()
    print(dfRatingsGroupByUserId.head(10))

    userIdMostRatings = dfRatingsGroupByUserId.idxmax()
    return dfRatings[dfRatings[CSV_RATING_COLUMN_USER_ID] == userIdMostRatings]



# Nice Function
def getRecommandedBooksForUser(userId):

    if userId == "":
        userId = "A25HYPL2XKQPZB"

    favoriteCategories = getUserFavoriteCategory(userId)
    favoriteCategory = favoriteCategories.idxmax()
    print(f"Favorite category for user {userId} : {favoriteCategory}")

    booksRead = getSpecificUserRatings(userId)

    dfBooksScore = getTopBooksByScore(favoriteCategory)
    dfBooksReview = getTopReviews(favoriteCategory)

    print(f"Recommanded {favoriteCategory} books")
    recommandedBooks = addRecommendedBooks(booksRead, dfBooksScore, dfBooksReview)
    return recommandedBooks

def addRecommendedBooks(booksRead, dfBooksScore, dfBooksReview):
    recommandedBooks = []
    nbRecommandedBooks = len(recommandedBooks)

    nbDuplicateBooks = 0

    # TO REFACTO
    while nbRecommandedBooks < 5:
        recommandedBook = dfBooksScore.index[nbRecommandedBooks + nbDuplicateBooks]

        # if might not be working
        if (recommandedBook in booksRead):
            print(f"already read {recommandedBook}")
            nbDuplicateBooks += 1
        else:
            recommandedBooks.append(recommandedBook)

        nbRecommandedBooks = len(recommandedBooks) #usefull ?
        
    while nbRecommandedBooks < 10:
        index_recommended = dfBooksReview.index[nbRecommandedBooks - 5]
        recommandedBook = dfBooksReview.loc[index_recommended, CSV_BOOK_COLUMN_TITLE]

        # if might not be working
        if recommandedBook in booksRead:
            print(f"already read {recommandedBook}")
            nbDuplicateBooks += 1
        if recommandedBook in recommandedBooks:
            print(f"already recommanded {recommandedBook}")
            nbDuplicateBooks += 1
        else:
            recommandedBooks.append(recommandedBook)

        nbRecommandedBooks = len(recommandedBooks) #usefull ?
        
    print(recommandedBooks)
    return recommandedBooks
        


    



# MAIN CODE #
if __name__ == '__main__':
     app.run(debug=True, use_debugger=False)