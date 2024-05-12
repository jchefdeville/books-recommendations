import pandas as pd

def readBookInformations():
    booksCsv = "source/books.csv"
    cols_to_read = ["ISBN", "Book-Title"]
    donnees = pd.read_csv(booksCsv, usecols=cols_to_read, encoding='ISO-8859-1', delimiter=';')
    return donnees

books = readBookInformations()

filtre = books["ISBN"] == '0002005018'
donnees_filtrees = books[filtre]

print(donnees_filtrees)
