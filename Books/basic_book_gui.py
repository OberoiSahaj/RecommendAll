from PyQt5 import QtCore, QtGui, QtWidgets
import numpy as np
import pandas as pd
import difflib

final_df = pd.read_csv('final_df.csv')
cos_sim = np.load('cos_sim.npy')


class Ui_MainWindow(object):

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.runn = QtWidgets.QPushButton(self.centralwidget)
        self.runn.setGeometry(QtCore.QRect(140, 200, 101, 31))
        self.runn.setObjectName("runn")
        self.runn.clicked.connect(self.recommendation)

        self.query = QtWidgets.QLineEdit(self.centralwidget)
        self.query.setGeometry(QtCore.QRect(140, 130, 161, 41))
        self.query.setObjectName("query")
        self.label_1 = QtWidgets.QLabel(self.centralwidget)
        self.label_1.setGeometry(QtCore.QRect(10, 140, 131, 16))
        self.label_1.setObjectName("label_1")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(90, 270, 81, 16))
        self.label_2.setObjectName("label_2")
        self.textEdit = QtWidgets.QTextEdit(self.centralwidget)
        self.textEdit.setGeometry(QtCore.QRect(140, 260, 481, 291))
        self.textEdit.setObjectName("textEdit")
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def recommendation(self):  # ", ".join(list(self.recommendation()))
        book = str(self.query.text()).lower()
        all_per = []
        for books in final_df['book_title'].str.lower():
            seq = difflib.SequenceMatcher(isjunk=None, a=book, b=books).ratio()
            per = round(seq * 100, 2)
            all_per.append(per)

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

        self.textEdit.append(" \n ".join(list(final_recomm)))  # ", ".join(list(self.final_recomm))

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.runn.setText(_translate("MainWindow", "RUN"))
        self.label_1.setText(_translate("MainWindow", "Recommendation for:"))
        self.label_2.setText(_translate("MainWindow", "Result:"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
