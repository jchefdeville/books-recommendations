import pandas as pd
from main import *

# Unit Tests

def test_getAuthorBooks():
    dfAuthorBooks = getAuthorBooks("Cornelia Cornelissen")
    assert len(dfAuthorBooks) > 0

def test_getRatingsBook():
    dfRatingsBook = getRatingsBook("")
    assert len(dfRatingsBook) > 0

def test_getTopReadCategories():
    dfCategories = getTopReadCategories()
    assert len(dfCategories) > 0

def test_getTopReviews():
    dfTopReviews = getTopReviews(CATEGORY_FICTION)
    assert 1

def test_getSpecificUserRatings():
    userId = "A25HYPL2XKQPZB"
    ratings = getSpecificUserRatings(userId)
    assert len(ratings) > 0

def test_getBestUsersRatings():
    dfUsersRatings = getBestUsersRatings()
    assert len(dfUsersRatings) > 0

def test_getTopBooksByScoreCategoryFiction():
    df = getTopBooksByScore(CATEGORY_FICTION)
    assert 1

def test_getPopularBooksByAuthor():
    df = getPopularBooksByAuthor("")
    assert 1

def test_getUserFavoriteCategory():
    userId = "A25HYPL2XKQPZB"
    df = getUserFavoriteCategory(userId)
    assert len(df) > 0

def test_getRecommandedBooksForUser():
    userId = "A25HYPL2XKQPZB"
    df = getRecommandedBooksForUser(userId)
    assert len(df) > 0

def test_getAutors():
    df = getAuthors()
    assert len(df) > 0