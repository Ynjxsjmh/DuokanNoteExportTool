from PyQt5.QtCore import QDateTime, Qt, QTimer
from PyQt5.QtGui import QKeySequence
from PyQt5.QtWidgets import *


class WidgetGallery(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        topLayout = self.createTopLayout()
        bookListGroupBox = self.createBookListGroupBox()
        selectedBookListGroupBox = self.createSelectedBookListGroupBox()
        progressBar = self.createProgressBar()

        mainLayout = QGridLayout()
        mainLayout.addLayout(topLayout, 0, 0, 1, 2)
        mainLayout.addWidget(bookListGroupBox, 2, 0)
        mainLayout.addWidget(selectedBookListGroupBox, 3, 0)
        mainLayout.addWidget(progressBar, 4, 0, 1, 2)

        self.setLayout(mainLayout)
        self.setWindowTitle('多看导出助手')

    def createTopLayout(self):

        openFileButton = QPushButton('打开')
        openFileButton.setDefault(True)
        def openFile():
            path = QFileDialog.getOpenFileName(self, "Open")[0]
            if path:
                text.setPlainText(open(path).read())
                file_path = path
        openFileButton.clicked.connect(openFile)

        settingButton = QPushButton('设置')
        settingButton.setDefault(True)
        def setPreference():
            settingDialog = SettingDialog()
            settingDialog.exec_()
        settingButton.clicked.connect(setPreference)

        closeWindowButton = QPushButton('关闭')
        closeWindowButton.setDefault(True)
        closeWindowButton.clicked.connect(self.accept)

        aboutButton = QPushButton('关于')
        def showAboutDialog():
            text = 'Ynjxsjmh'
            QMessageBox.about(self, '关于多看导出助手', text)
        aboutButton.clicked.connect(showAboutDialog)

        topLayout = QHBoxLayout()
        topLayout.addWidget(openFileButton)
        topLayout.addWidget(settingButton)
        topLayout.addWidget(closeWindowButton)
        topLayout.addWidget(aboutButton)

        return topLayout

    def createBookListGroupBox(self):
        bookListGroupBox = QGroupBox('书籍列表')
        bookListGroupBox.setAlignment(Qt.AlignCenter)

        tableWidget = QTableWidget(10, 10)

        hboxLayout = QHBoxLayout()
        hboxLayout.setContentsMargins(5, 5, 5, 5)
        hboxLayout.addWidget(tableWidget)

        bookListGroupBox.setLayout(hboxLayout)

        return bookListGroupBox

    def createSelectedBookListGroupBox(self):
        selectedBookListGroupBox = QGroupBox('已选书籍')
        selectedBookListGroupBox.setAlignment(Qt.AlignCenter)

        tableWidget = QTableWidget(0, 0)

        defaultPushButton = QPushButton('导出')
        defaultPushButton.setDefault(True)

        vboxLayout = QVBoxLayout()
        vboxLayout.addWidget(tableWidget)
        vboxLayout.addWidget(defaultPushButton, 0, Qt.AlignCenter)

        selectedBookListGroupBox.setLayout(vboxLayout)

        return selectedBookListGroupBox

    def createProgressBar(self):
        progressBar = QProgressBar()

        progressBar.setRange(0, 10000)
        progressBar.setValue(0)

        return progressBar


if __name__ == '__main__':

    import sys

    app = QApplication(sys.argv)
    gallery = WidgetGallery()
    gallery.show()
    sys.exit(app.exec_())
