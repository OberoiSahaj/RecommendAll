from PyQt5 import QtCore, QtGui, QtWidgets
import numpy as np
import pandas as pd
from fuzzywuzzy import fuzz

final_df_songs = pd.read_csv('final_df_songs.csv')
cos_sim_songs = np.load('cos_sim_songs.npy')
final_df = pd.read_csv('final_df_books.csv')
cos_sim = np.load('cos_sim_books.npy')
final_df_movies = pd.read_csv('final_df_movies.csv')
cos_sim_movies = np.load('cos_sim_movies2.npz') #Trying compressed cosine numpy file
cos_sim_movies= cos_sim_movies.f.arr_0

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(804, 667)
        MainWindow.setWindowOpacity(1.0)
        MainWindow.setAutoFillBackground(False)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.runn = QtWidgets.QPushButton(self.centralwidget)
        self.runn.setGeometry(QtCore.QRect(140, 290, 101, 31))
        self.runn.setObjectName("runn")
        self.runn.clicked.connect(self.recommendation)

        self.query = QtWidgets.QLineEdit(self.centralwidget)
        self.query.setGeometry(QtCore.QRect(140, 220, 161, 41))
        self.query.setObjectName("query")
        self.label_1 = QtWidgets.QLabel(self.centralwidget)
        self.label_1.setGeometry(QtCore.QRect(10, 230, 131, 16))
        self.label_1.setObjectName("label_1")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(10, 350, 81, 16))
        self.label_2.setObjectName("label_2")
        self.textEdit = QtWidgets.QTextEdit(self.centralwidget)
        self.textEdit.setGeometry(QtCore.QRect(140, 350, 481, 291))
        self.textEdit.setReadOnly(True)
        self.textEdit.setObjectName("textEdit")
        self.headingg = QtWidgets.QTextEdit(self.centralwidget)
        self.headingg.setGeometry(QtCore.QRect(230, 10, 361, 71))
        self.headingg.setAutoFillBackground(False)
        self.headingg.setStyleSheet("background-color: rgb(240, 240, 240);")
        self.headingg.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.headingg.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.headingg.setLineWidth(0)
        self.headingg.setReadOnly(True)
        self.headingg.setObjectName("headingg")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(10, 150, 101, 16))
        self.label_3.setObjectName("label_3")
        self.category = QtWidgets.QComboBox(self.centralwidget)
        self.category.setGeometry(QtCore.QRect(140, 150, 73, 22))
        self.category.setObjectName("category")
        self.category.addItem("Movies")
        self.category.addItem("Books")
        self.category.addItem("Songs")

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def recommendation_movies(self):

        movie = str(self.query.text()).lower()
        all_per = []
        for movies in final_df_movies['original_title'].str.lower():
            all_per.append(fuzz.token_set_ratio(movie, movies))

        final_query = final_df_movies['original_title'].iloc[(pd.Series(all_per).sort_values(ascending=False)[:2].index)]
        idx = []
        for movie in final_query:
            i = final_df_movies[final_df_movies['original_title'] == movie].index
            idx.append(i)
        final_recomm = []

        for i in idx:
            text_10 = pd.Series(cos_sim_movies[i][0]).sort_values(ascending=False)[1:11]
            text_idx = text_10.index
            text_recom_idx = (text_10 + final_df_movies['numerical'].loc[text_idx]).index
            final_recomm.append(final_df_movies['numerical'].loc[text_recom_idx])

        final_idx = pd.concat([final_recomm[0], final_recomm[1]]).sort_values(ascending=False).index
        final_recomm = final_df_movies.iloc[final_idx]
        final_recomm = final_recomm[~final_recomm['original_title'].duplicated()]['original_title']

        final = ""
        for word in list(final_recomm):
            final = final + "\n" + word

        self.textEdit.clear()
        self.textEdit.append(" \n ".join(list(final_recomm[:15])))

    def recommendation_books(self):
        book = str(self.query.text()).lower()
        all_per = []
        for books in final_df['book_title'].str.lower():
            all_per.append(fuzz.token_set_ratio(book, books))

        final_query = final_df['book_title'].iloc[(pd.Series(all_per).sort_values(ascending=False)[:2].index)]
        idx = []
        for book in final_query:
            i = final_df[final_df['book_title'] == book].index
            idx.append(i)
        final_recomm = []

        for i in idx:
            text_10 = pd.Series(cos_sim[i][0]).sort_values(ascending=False)[1:11]
            text_idx = text_10.index
            text_recom_idx = (text_10 + final_df['numerical'].loc[text_idx]).index
            final_recomm.append(final_df['numerical'].loc[text_recom_idx])

        final_idx = pd.concat([final_recomm[0], final_recomm[1]]).sort_values(ascending=False).index
        final_recomm = final_df.iloc[final_idx]
        final_recomm = final_recomm[~final_recomm['book_title'].duplicated()]['book_title']

        final = ""
        for word in list(final_recomm):
            final = final + "\n" + word

        self.textEdit.clear()
        self.textEdit.append(" \n ".join(list(final_recomm[:15])))


    def recommendation_songs(self):  # ", ".join(list(self.recommendation()))
        song = str(self.query.text()).lower()
        all_per = []
        for songs in final_df_songs['track_name'].str.lower():
            all_per.append(fuzz.token_set_ratio(song, songs))

        final_query = final_df_songs['track_name'].iloc[(pd.Series(all_per).sort_values(ascending=False)[:2].index)]
        idx = []
        for song in final_query:
            i = final_df_songs[final_df_songs['track_name'] == song].index
            idx.append(i)
        final_recomm = []

        for i in idx:
            text_10 = pd.Series(cos_sim_songs[i][0]).sort_values(ascending=False)[1:11]
            text_idx = text_10.index
            text_recom_idx = (text_10 + final_df_songs['numerical'].loc[text_idx]).index
            final_recomm.append(final_df_songs['numerical'].loc[text_recom_idx])

        final_idx = pd.concat([final_recomm[0], final_recomm[1]]).sort_values(ascending=False).index
        final_recomm = final_df_songs.iloc[final_idx]
        final_recomm = final_recomm[~final_recomm['track_name'].duplicated()]['track_name']

        final = ""
        for word in list(final_recomm):
            final = final + "\n" + word

        self.textEdit.clear()
        self.textEdit.append(" \n ".join(list(final_recomm[:15])))


    def recommendation(self):
        category = str(self.category.currentText())

        if category == 'Movies':
            self.recommendation_movies()
        elif category == 'Books':
            self.recommendation_books()
        elif category == 'Songs':
            self.recommendation_songs()

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "RecommendAll"))
        self.runn.setText(_translate("MainWindow", "RUN"))
        self.label_1.setText(_translate("MainWindow", "Recommendation for:"))
        self.label_2.setText(_translate("MainWindow", "Result:"))
        self.headingg.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:7.8pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:26pt; font-weight:600;\">RecommendAll</span></p></body></html>"))
        self.label_3.setText(_translate("MainWindow", "Select Category:"))



if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
