from PyQt5.QtCore import QDateTime, Qt, QTimer
from PyQt5.QtGui import QKeySequence
from PyQt5.QtWidgets import *

from connector import Connector
from setting import SortType, OutlineType, ExportSetting


class MyRadioButton(QRadioButton):
    def __init__(self, text, value=''):
        super(MyRadioButton, self).__init__(text)
        self.value = value


class SettingDialog(QDialog):
    def __init__(self, exportSetting, parent=None):
        super().__init__(parent)

        self.exportSetting = exportSetting

        self.timeFormatGroupBox = self.createTimeFormatGroupBox()
        self.outlineFormatGroupBox = self.createOutlineFormatGroupBox()
        self.annotationSortGroupBox = self.createAnnotationSortGroupBox()
        self.bottomLayout = self.createBottomLayout()

        mainLayout = QGridLayout()
        mainLayout.addWidget(self.timeFormatGroupBox, 0, 0)
        mainLayout.addWidget(self.outlineFormatGroupBox, 1, 0)
        mainLayout.addWidget(self.annotationSortGroupBox, 2, 0)
        mainLayout.addLayout(self.bottomLayout, 3, 0)

        self.setLayout(mainLayout)
        self.setWindowTitle('导出设置')

    def createTimeFormatGroupBox(self):
        timeFormatGroupBox = QGroupBox('时间格式')

        from datetime import datetime
        now = datetime.now()

        timeFormatRadioButtons = [MyRadioButton(now.strftime('%Y-%m-%d'), '%Y-%m-%d'),
                                  MyRadioButton(now.strftime('%Y 年 %m 月 %d 日'), '%Y 年 %m 月 %d 日'),
                                  MyRadioButton(now.strftime('%Y-%m-%d %H:%M:%S'), '%Y-%m-%d %H:%M:%S'),
                                  MyRadioButton(now.strftime('%Y 年 %m 月 %d 日 %H 时 %M 分 %S 秒'),
                                                             '%Y 年 %m 月 %d 日 %H 时 %M 分 %S 秒')]

        layout = QVBoxLayout()

        for button in timeFormatRadioButtons:
            if button.value == self.exportSetting.time_format:
                button.setChecked(True)
            layout.addWidget(button)

        timeFormatGroupBox.setLayout(layout)

        return timeFormatGroupBox

    def createOutlineFormatGroupBox(self):
        outlineFormatGroupBox = QGroupBox('目录格式')

        outlineFormatRadioButtons = [MyRadioButton('无格式', OutlineType.ORIGIN),
                                     MyRadioButton('Markdown 格式', OutlineType.MD),
                                     MyRadioButton('Org 格式', OutlineType.ORG)]

        layout = QVBoxLayout()

        for button in outlineFormatRadioButtons:
            if button.value == self.exportSetting.outline_type:
                button.setChecked(True)
            layout.addWidget(button)

        outlineFormatGroupBox.setLayout(layout)

        return outlineFormatGroupBox

    def createAnnotationSortGroupBox(self):
        annotationSortGroupBox = QGroupBox('想法排序方式')

        radioButtons = [MyRadioButton('按章节', SortType.CHAPTER),
                        MyRadioButton('按时间', SortType.TIME)]

        layout = QVBoxLayout()

        for button in radioButtons:
            if button.value == self.exportSetting.sort_type:
                button.setChecked(True)
            layout.addWidget(button)

        annotationSortGroupBox.setLayout(layout)

        return annotationSortGroupBox

    def createBottomLayout(self):
        saveButton = QPushButton('保存')
        saveButton.setDefault(True)
        def save():
            self.saveExportSetting()
            QMessageBox.about(self, '提示', '保存成功')
        saveButton.clicked.connect(save)

        closeWindowButton = QPushButton('关闭')
        closeWindowButton.setDefault(True)
        closeWindowButton.clicked.connect(self.accept)

        bottomLayout = QHBoxLayout()
        bottomLayout.addWidget(saveButton)
        bottomLayout.addWidget(closeWindowButton)

        return bottomLayout

    def saveExportSetting(self):

        for widget in self.timeFormatGroupBox.children():
            if isinstance(widget, QRadioButton):
                if widget.isChecked():
                    self.exportSetting.time_format = widget.value

        for widget in self.outlineFormatGroupBox.children():
            if isinstance(widget, QRadioButton):
                if widget.isChecked():
                    self.exportSetting.outline_type = widget.value

        for widget in self.annotationSortGroupBox.children():
            if isinstance(widget, QRadioButton):
                if widget.isChecked():
                    self.exportSetting.sort_type = widget.value


class DuoKanExportToolDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.exportSetting = ExportSetting()

        topLayout = self.createTopLayout()
        self.bookListGroupBox = self.createBookListGroupBox()
        selectedBookListGroupBox = self.createSelectedBookListGroupBox()
        progressBar = self.createProgressBar()

        mainLayout = QGridLayout()
        mainLayout.addLayout(topLayout, 0, 0, 1, 2)
        mainLayout.addWidget(self.bookListGroupBox, 2, 0)
        mainLayout.addWidget(selectedBookListGroupBox, 3, 0)
        mainLayout.addWidget(progressBar, 4, 0, 1, 2)

        self.setLayout(mainLayout)
        self.setWindowTitle('多看导出助手')

    def createTopLayout(self):

        openFileButton = QPushButton('打开')
        openFileButton.setDefault(True)
        def openFile():
            path = QFileDialog.getOpenFileName(self, 'Open', filter='db(*.db)')[0]
            if path:
                self.exportSetting.db_path = path
                connector = Connector(path)
                bookList = connector.find_all_books()
                self.initBookListTableWidget(bookList)
        openFileButton.clicked.connect(openFile)

        settingButton = QPushButton('设置')
        settingButton.setDefault(True)
        def setPreference():
            settingDialog = SettingDialog(self.exportSetting)
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

    def initBookListTableWidget(self, bookList):
        tableWidget = self.bookListGroupBox.findChild(QTableWidget, 'bookListTableWidget')

        for (bookId, bookName, bookAuthor) in bookList:
            rowId = tableWidget.rowCount()
            tableWidget.insertRow(rowId)

            tableWidget.setItem(rowId, 0, QTableWidgetItem(str(bookId)))
            tableWidget.setItem(rowId, 1, QTableWidgetItem(str(rowId + 1)))
            tableWidget.setItem(rowId, 2, QTableWidgetItem(bookName))
            tableWidget.setItem(rowId, 3, QTableWidgetItem(bookAuthor))

            addButton = QPushButton('添加')
            addButton.clicked.connect(
                lambda checked, id=rowId+1, bookId=bookId, bookName=bookName, bookAuthor=bookAuthor:\
                self.addRowToSelectedBookListTableWidget(id, bookId, bookName, bookAuthor))

            hBox = QHBoxLayout()
            hBox.addWidget(addButton, Qt.AlignCenter)
            w = QWidget()
            w.setLayout(hBox)

            tableWidget.setCellWidget(rowId, 4, w)

        return tableWidget

    def createBookListGroupBox(self):
        bookListGroupBox = QGroupBox('书籍列表')
        bookListGroupBox.setAlignment(Qt.AlignCenter)

        tableWidget = QTableWidget(0, 5, objectName='bookListTableWidget')

        tableWidget.setColumnHidden(0, True)
        tableWidget.setEditTriggers(QTableWidget.NoEditTriggers)
        tableWidget.setHorizontalHeaderLabels([
            'ID', '编号', '书名', '作者', '操作'
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

        exportDirLabel = QLabel('导出路径：')
        exportDirText = QLineEdit()

        folderButton = QPushButton('选择')
        folderButton.setDefault(True)
        def selectFolder():
            path = str(QFileDialog.getExistingDirectory(self, 'Select Directory'))
            if path:
                exportDirText.setText(path)
                self.exportSetting.export_dir = path
        folderButton.clicked.connect(selectFolder)

        hboxLayout = QHBoxLayout()
        hboxLayout.addWidget(exportDirLabel)
        hboxLayout.addWidget(exportDirText)
        hboxLayout.addWidget(folderButton)

        exportButton = QPushButton('导出')
        exportButton.setDefault(True)

        vboxLayout = QVBoxLayout()
        vboxLayout.addWidget(tableWidget)
        vboxLayout.addLayout(hboxLayout)
        vboxLayout.addWidget(exportButton, 0, Qt.AlignCenter)

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
