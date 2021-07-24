from PyQt5.QtCore import QDateTime, Qt, QTimer
from PyQt5.QtWidgets import (QApplication, QCheckBox, QComboBox, QDateTimeEdit,
        QDial, QDialog, QGridLayout, QGroupBox, QHBoxLayout, QLabel, QLineEdit,
        QProgressBar, QPushButton, QRadioButton, QScrollBar, QSizePolicy,
        QSlider, QSpinBox, QStyleFactory, QTableWidget, QTabWidget, QTextEdit,
        QVBoxLayout, QWidget)


class WidgetGallery(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        bookListGroupBox = self.createBookListGroupBox()
        selectedBookListGroupBox = self.createSelectedBookListGroupBox()
        progressBar = self.createProgressBar()

        mainLayout = QGridLayout()
        mainLayout.addWidget(bookListGroupBox, 1, 0)
        mainLayout.addWidget(selectedBookListGroupBox, 2, 0)
        mainLayout.addWidget(progressBar, 4, 0, 1, 2)

        self.setLayout(mainLayout)
        self.setWindowTitle('多看导出助手')

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
