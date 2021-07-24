from PyPDF2 import PdfFileReader


class PyPDF2Outline:
    @staticmethod
    def getOutlines(path):
        with open(path, 'rb') as f:
            pdf = PdfFileReader(f)
            outlines = pdf.getOutlines()
            outlines = PyPDF2Outline._processOutlines(pdf, outlines)

        return outlines

    @staticmethod
    def _processOutlines(pdf, outlines, level=0):
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
