import epub


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
    def __init__(self, path):
        self.path = path

    def getManifest(self, book):
        manifest = []

        for key in book.opf.manifest.keys():
            manifest_item = book.opf.manifest[key]
            manifest.append({
                'id': manifest_item.identifier,
                'href': manifest_item.href,
                'media_type': manifest_item.media_type,
            })

        return manifest

    def getToc(self, navPoints, level=0, nested=True):
        toc = []

        for navPoint in navPoints:
           toc.append({
               'class': navPoint.class_name,
               'id': navPoint.identifier,
               'play_order': navPoint.play_order,
               'src': navPoint.src,
               'level': level,
               'label': navPoint.labels[0][0],
           })

           if len(navPoint.nav_point):
               if nested:
                   toc.append(self.getToc(navPoint.nav_point, level+1))
               else:
                   toc.extend(self.getToc(navPoint.nav_point, level+1))

        return toc

    def getChapterName(self, chapter_id):
        book = epub.open_epub(self.path, 'r')

        self.getToc(book.toc.nav_map.nav_point)
        self.getManifest(book)
    def getChapterById(self, chapter_id, chapters, items):
        item = [item for item in items if item['id'] == chapter_id][0]
        chapter = [chapter for chapter in chapters if chapter['src'] == item['href']][0]
        return chapter

    def getAncestorChapters(self, chapters, chapter_id):
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
