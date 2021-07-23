

class Chapter:
    def __init__(self):
        raise NotImplementedError

    def getChapterName(self, index):
        raise NotImplementedError


class TXTChapter(Chapter):
    def __init__(self):
        pass

    def getChapterName(self, index):
        pass


class EPUBChapter(Chapter):
    def __init__(self):
        pass

    def getChapterName(self, index):
        pass


class PDFChapter(Chapter):
    def __init__(self):
        pass

    def getChapterName(self, index):
        pass


class DuoKanChapter:
    def __init__(self, annotations):
        pass

    def getChapterName(self, annotation):
        pass
