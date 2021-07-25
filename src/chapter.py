import cchardet as chardet
import epub
import json

from outline import PyPDF2Outline, PdfminerOutline,\
                    TXTOutline, EPUBOutline


class Chapter:
    '''用于从原文件或多看笔记中得到笔记所在章节
    '''
    def __init__(self):
        raise NotImplementedError

    def getChapter(self, index):
        '''获取 chapter 字典
        一般来说 chapter 字典有 title, page, level 这三个键
        '''
        raise NotImplementedError

    def getChapterName(self, index):
        raise NotImplementedError

    def getAncestorChapters(self, index, include):
        '''获取当前 chapter 的所有父 chapter
        一般来说 chapter 字典有 title, page, level 这三个键
        include: boolean
          是否包含当前 chapter
        '''
        raise NotImplementedError

    def getAncestorChapterNames(self, index, include):
        raise NotImplementedError


class TXTChapter(Chapter):
    def __init__(self, path):
        self.encoding = self._detectEncoding(path)

        with open(path, 'r', encoding=self.encoding) as f:
            self.content = f.read()

        self.outlines = TXTOutline.getOutlines(path, self.encoding, self.content)

    def _detectEncoding(self, path):
        with open(path, "rb") as f:
            content = f.read()
            result = chardet.detect(content)
            encoding = result['encoding']
        return encoding

    def getChapterName(self, annotation_sample):
        chapter_name = ''
        start = self.content.find(annotation_sample)

        for outline in reversed(self.outlines):
            if start >= outline['start_byte_offset']:
                chapter_name = outline['title']
                break

        return chapter_name


class EPUBChapter(Chapter):
    def __init__(self, path):
        book = epub.open_epub(path, 'r')

        self.outlines = EPUBOutline.getOutlines(book)
        self.itemrefs = self.getSpine(book)
        self.items = self.getManifest(book)

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

    def getChapterName(self, chapter_id):
        chapter = self.getChapterById(chapter_id, self.itemrefs, self.items, self.outlines)

        return chapter['title']

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
        self.outlines = PdfminerOutline.getOutlines(path)

    def getChapterName(self, fixed_index):
        chapter_index = self.getChapterIndex(fixed_index)

        return self.outlines[chapter_index]['title']

    def getChapterIndex(self, fixed_index):
        chapter_index = 0

        try:
            chapter_index = next(i for i, chapter_index in enumerate([outline['page']
                                                                      for outline in self.outlines])
                                 if chapter_index > fixed_index) - 1
        except StopIteration:
            chapter_index = len(self.outlines) - 1

        return chapter_index


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
