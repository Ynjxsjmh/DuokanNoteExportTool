import re

from pdfminer.pdfdocument import PDFDocument, PDFNoOutlines
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfparser import PDFParser
from pdfminer.pdftypes import PDFObjRef, resolve1
from pdfminer.psparser import PSLiteral

from PyPDF2 import PdfFileReader


class EPUBOutline:

    @staticmethod
    def getOutlines(book):
        outlines = EPUBOutline._processOutlines(book.toc.nav_map.nav_point)
        return outlines

    @staticmethod
    def _processOutlines(navPoints, level=1):
        outlines = []

        for navPoint in navPoints:
           outlines.append({
               'class': navPoint.class_name,
               'id': navPoint.identifier,
               'play_order': navPoint.play_order,
               'src': navPoint.src,
               'level': level,
               'title': navPoint.labels[0][0],
           })

           if len(navPoint.nav_point):
               outlines.extend(EPUBOutline._processOutlines(navPoint.nav_point, level+1))

        return outlines


class PyPDF2Outline:
    @staticmethod
    def getOutlines(path):
        with open(path, 'rb') as f:
            pdf = PdfFileReader(f)
            outlines = pdf.getOutlines()
            outlines = PyPDF2Outline._processOutlines(pdf, outlines)

        return outlines

    @staticmethod
    def _processOutlines(pdf, outlines, level=1):
        results = []

        for outline in outlines:
            if isinstance(outline, list):
                results.extend(PyPDF2Outline._processOutlines(pdf, outline, level+1))
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


class PdfminerOutline:

    @staticmethod
    def getOutlines(path):
        with open(path, 'rb') as f:
            parser = PDFParser(f)
            doc = PDFDocument(parser)
            outlines = PdfminerOutline._processOutlines(doc)

        return outlines

    @staticmethod
    def _processOutlines(doc):
        def resolve_dest(dest):
            if isinstance(dest, str):
                dest = resolve1(doc.get_dest(dest))
            elif isinstance(dest, PSLiteral):
                dest = resolve1(doc.get_dest(dest.name))
            if isinstance(dest, dict):
                dest = dest['D']
            if isinstance(dest, PDFObjRef):
                dest = dest.resolve()
            return dest

        pages = {page.pageid: pageno for (pageno, page)
                 in enumerate(PDFPage.create_pages(doc), 1)}

        results = []

        try:
            outlines = doc.get_outlines()

            for (level, title, dest, a, se) in outlines:
                pageno = None
                if dest:
                    dest = resolve_dest(dest)
                    pageno = pages[dest[0].objid]
                elif a:
                    action = a
                    if isinstance(action, dict):
                        subtype = action.get('S')
                        if subtype and repr(subtype) == '/\'GoTo\'' and action.get(
                                'D'):
                            dest = resolve_dest(action['D'])
                            pageno = pages[dest[0].objid]

                results.append({
                    'title': title,
                    'page': pageno,
                    'level': level,
                })

        except PDFNoOutlines:
            pass

        return results


class TXTOutline:

    @staticmethod
    def getOutlines(path, encoding, content):
        outlines = TXTOutline._guessOutlines(path, encoding, content)

        return outlines

    @staticmethod
    def _guessOutlines(path, encoding, content):
        chapters = []

        with open(path, 'r', encoding=encoding) as f:
            while True:
                line = f.readline()

                # readline() returns an empty string when EOF is encountered
                if not line: break

                if re.match(r'(^第.+[卷|章|节|篇].*)', line):
                    start = content.find(line)
                    chapters.append({
                        'title': line.strip(),
                        'start_byte_offset': start,
                        'end_byte_offset': start + len(line),
                    })

        return chapters
