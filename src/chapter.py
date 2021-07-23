import epub
import json
from PyPDF2 import PdfFileReader


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

    def getSpine(self, book):
        spine = [{'idref': idref, 'linear': linear}
                 for idref, linear in book.opf.spine.itemrefs]

        return spine

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
                   toc.append(self.getToc(navPoint.nav_point, level+1, nested))
               else:
                   toc.extend(self.getToc(navPoint.nav_point, level+1, nested))

        return toc

    def getChapterName(self, chapter_id):
        book = epub.open_epub(self.path, 'r')

        chapters = self.getToc(book.toc.nav_map.nav_point, nested=False)
        itemrefs = self.getSpine(book)
        items = self.getManifest(book)

        chapter = self.getChapterById(chapter_id, itemrefs, items, chapters)

        return chapter['label']

    def getChapterById(self, chapter_id, itemrefs, items, chapters):
        '''
        itemref: idref (itemref is `itemref` label in content.opf)
        item: href, id (item is `item` label in content.opf)
        chapter: src, label (chapter is `navPoint` label in toc.ncx)
        chapter_id = itemref.idref
        itemref.idref = item.id
        item.href = chapter.src
        '''
        itemref = [itemref for itemref in itemrefs if itemref['idref'] == chapter_id][0]
        item = [item for item in items if item['id'] == itemref['idref']][0]
        chapter = [chapter for chapter in chapters if chapter['src'] == item['href']]

        if len(chapter) == 0:
            '''
            针对从 item.href 找不到 chapter.src 的情况，
            解决方案是找前一个 item 对应的 chapter。
            可能存在的问题是前一个 item 不存在。
            '''
            previous_chapter_id = itemrefs[[itemref['idref'] for itemref in itemrefs].index(chapter_id) - 1]
            return self.getChapterById(previous_chapter_id['idref'], itemrefs, items, chapters)
        else:
            return chapter[0]

    def getAncestorChapters(self, chapters, chapter):
        ancestor_chapters, level = [], chapter['level']

        idx = [chapter['id'] for chapter in chapters].index(chapter['id'])

        for cur_chapter in reversed(chapters[:idx]):
            if cur_chapter['level'] == level - 1:
                ancestor_chapters.append(cur_chapter)
                level = level - 1

        return ancestor_chapters


class PDFChapter(Chapter):
    def __init__(self, path):
        self.path = path

        with open(self.path, 'rb') as f:
            pdf = PdfFileReader(f)
            outlines = pdf.getOutlines()
            self.outlines = self.processOutlines(pdf, outlines)

    def getChapterName(self, fixed_index):
        chapter_index = self.getChapterIndex(fixed_index)

        return self.outlines[chapter_index]['title']

    def getChapterIndex(self, fixed_index):
        chapter_index = 0

        try:
            chapter_index = next(i for i,v in enumerate([outline['page']
                                                         for outline in self.outlines])
                                 if v >= fixed_index) - 1
        except StopIteration:
            chapter_index = len(self.outlines) - 1

        return chapter_index

    def processOutlines(self, pdf, outlines, level=0):
        results = []

        for outline in outlines:
            if isinstance(outline, list):
                results.extend(self.processOutlines(pdf, outline, level+1))
            else:
                results.append({
                    'title': outline.title,
                    # 多看阅读的第一页是 cover
                    # 所以会比这里得到的多一页
                    # 但是 fixed_index 里没有多页
                    'page': pdf.getDestinationPageNumber(outline),
                    'level': level,
                })

        return results


class DuoKanChapter:
    def __init__(self, path):
        self.path = path
        self.maps = self.build_maps()

    def build_maps(self):
        with open(self.path, "r") as f:
            content = f.read()

        maps = [list(map(str.strip, chapter.split('\n', 1)))
                for chapter in content.strip().split('\n\n')]

        return maps

    def getChapterName(self, annotation):
        chapter_name = ''
        note_text = json.loads(annotation[2])['note_text']
        annotation_sample = annotation[3]

        for cur_chapter_name, annotations in self.maps:
            if (note_text in annotations) and (annotation_sample in annotations):
                chapter_name = cur_chapter_name

        return chapter_name
