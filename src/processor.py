import datetime
import itertools
import json

from chapter import EPUBChapter, DuoKanChapter, PDFChapter, TXTChapter
from connector import Connector


def export_annotations_in_books(book_id, file_path='', use_duokan_notes=False, time_format='%Y-%m-%d %H:%M:%S'):
    connector = Connector()

    result = ''

    annotations = connector.find_annotations_in_book(book_id)
    package_type = annotations[0][4]

    index_key = ''
    chapter = None
    if package_type == 'PDF':
        index_key = 'fixed_index'
        chapter = PDFChapter(file_path)
    elif package_type == 'TXT':
        index_key = 'byte_offset'
        chapter = TXTChapter(file_path)
    elif package_type == 'EPUB':
        index_key = 'chapter_index'
        chapter = EPUBChapter(file_path)

    if use_duokan_notes:
        chapter = DuoKanChapter(file_path)

    annotations.sort(key=lambda annotation: json.loads(annotation[1])[0][index_key])
    annotations_by_chapter = itertools.groupby(annotations, key=lambda annotation: json.loads(annotation[1])[0][index_key])

    for index, annotations in annotations_by_chapter:
        annotations = list(annotations)

        chapter_name = str(index)

        if use_duokan_notes:
            chapter_name = chapter.getChapterName(annotations[0])
        elif package_type == 'EPUB':
            chapter_id = json.loads(annotations[0][1])[0]['chapter_id']
            chapter_name = chapter.getChapterName(chapter_id)
        elif package_type == 'PDF':
            chapter_name = chapter.getChapterName(index)
        elif package_type == 'TXT':
            chapter_name = chapter.getChapterName(annotations[0][3])

        result += '\n' + chapter_name + '\n'

        for annotation in annotations:
            added_time = datetime.datetime.utcfromtimestamp(annotation[0]/1000).strftime(time_format)
            note_text = json.loads(annotation[2])['note_text']
            annotation_sample = annotation[3]

            result += added_time + '\n'
            result += annotation_sample + '\n'

            if len(note_text):
                result += '注：' + note_text + '\n'

    return result.strip()
