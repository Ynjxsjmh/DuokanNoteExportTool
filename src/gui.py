from PyQt5.QtCore import QDateTime, Qt, QTimer
from PyQt5.QtGui import QKeySequence
from PyQt5.QtWidgets import *


class SettingDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        timeFormatGroupBox = self.createTimeFormatGroupBox()
        outlineFormatGroupBox = self.createOutlineFormatGroupBox()
        annotationSortGroupBox = self.createAnnotationSortGroupBox()
        bottomLayout = self.createBottomLayout()

        mainLayout = QGridLayout()
        mainLayout.addWidget(timeFormatGroupBox, 0, 0)
        mainLayout.addWidget(outlineFormatGroupBox, 1, 0)
        mainLayout.addWidget(annotationSortGroupBox, 2, 0)
        mainLayout.addLayout(bottomLayout, 3, 0)

        self.setLayout(mainLayout)
        self.setWindowTitle('导出设置')

    def createTimeFormatGroupBox(self):
        timeFormatGroupBox = QGroupBox('时间格式')

        from datetime import datetime
        now = datetime.now()

        timeFormatRadioButton1 = QRadioButton(now.strftime('%Y-%m-%d'))
        timeFormatRadioButton2 = QRadioButton(now.strftime('%Y 年 %m 月 %d 日'))
        timeFormatRadioButton3 = QRadioButton(now.strftime('%Y-%m-%d %H:%M:%S'))
        timeFormatRadioButton4 = QRadioButton(now.strftime('%Y 年 %m 月 %d 日 %H 时 %M 分 %S 秒'))
        timeFormatRadioButton3.setChecked(True)

        layout = QVBoxLayout()
        layout.addWidget(timeFormatRadioButton1)
        layout.addWidget(timeFormatRadioButton2)
        layout.addWidget(timeFormatRadioButton3)
        layout.addWidget(timeFormatRadioButton4)
        timeFormatGroupBox.setLayout(layout)

        return timeFormatGroupBox

    def createOutlineFormatGroupBox(self):
        outlineFormatGroupBox = QGroupBox('目录格式')

        outlineFormatRadioButton1 = QRadioButton('无格式')
        outlineFormatRadioButton2 = QRadioButton('Markdown 格式')
        outlineFormatRadioButton3 = QRadioButton('Org 格式')

        outlineFormatRadioButton1.setChecked(True)

        layout = QVBoxLayout()
        layout.addWidget(outlineFormatRadioButton1)
        layout.addWidget(outlineFormatRadioButton2)
        layout.addWidget(outlineFormatRadioButton3)
        outlineFormatGroupBox.setLayout(layout)

        return outlineFormatGroupBox

    def createAnnotationSortGroupBox(self):
        annotationSortGroupBox = QGroupBox('想法排序方式')

        radioButton1 = QRadioButton('按章节')
        radioButton2 = QRadioButton('按时间')
        radioButton1.setChecked(True)

        layout = QVBoxLayout()
        layout.addWidget(radioButton1)
        layout.addWidget(radioButton2)
        annotationSortGroupBox.setLayout(layout)

        return annotationSortGroupBox

    def createBottomLayout(self):
        saveButton = QPushButton('保存')
        saveButton.setDefault(True)

        closeWindowButton = QPushButton('关闭')
        closeWindowButton.setDefault(True)
        closeWindowButton.clicked.connect(self.accept)

        bottomLayout = QHBoxLayout()
        bottomLayout.addWidget(saveButton)
        bottomLayout.addWidget(closeWindowButton)

        return bottomLayout


class DuoKanExportToolDialog(QDialog):
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
        topLayout.addWidget(aboutButton)
        topLayout.addWidget(closeWindowButton)

        return topLayout

    def createBookListGroupBox(self):
        bookListGroupBox = QGroupBox('书籍列表')
        bookListGroupBox.setAlignment(Qt.AlignCenter)

        tableWidget = QTableWidget(5, 5)
        tableWidget.setEditTriggers(QTableWidget.NoEditTriggers)
        tableWidget.setHorizontalHeaderLabels([
            '编号', '书名', '作者', '划线数', '想法数'
        ])

        hboxLayout = QHBoxLayout()
        hboxLayout.setContentsMargins(5, 5, 5, 5)
        hboxLayout.addWidget(tableWidget)

        bookListGroupBox.setLayout(hboxLayout)

        return bookListGroupBox

    def createSelectedBookListGroupBox(self):
        selectedBookListGroupBox = QGroupBox('已选书籍')
        selectedBookListGroupBox.setAlignment(Qt.AlignCenter)

        tableWidget = QTableWidget(0, 5)
        tableWidget.setEditTriggers(QTableWidget.NoEditTriggers)
        tableWidget.setHorizontalHeaderLabels([
            '编号', '书名', '作者', '划线数', '想法数'
        ])

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
    tool = DuoKanExportToolDialog()
    tool.show()
    sys.exit(app.exec_())
