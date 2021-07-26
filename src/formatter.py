from chapter import Chapter


class ChapterFormatter(Chapter):
    def __init__(self, prefix, chapter):
        self.prefix = prefix
        self.chapter = chapter

    def getChapter(self, index):
        return self.chapter.getChapter(index)

    def getChapterName(self, index):
        chapter = self.getChapter(index)
        return chapter['level'] * self.prefix + ' ' + chapter['title']

    def getAncestorChapters(self, index, include=False):
        return self.chapter.getAncestorChapterNames(index, include)

    def getAncestorChapterNames(self, index, include=False):
        chapter_names = [self.getChapterName(index)
                         for chapter in self.getAncestorChapters(index, include)]
        return chapter_names
