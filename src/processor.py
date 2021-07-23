import datetime
import itertools
import json

from chapter import Chapter, EPUBChapter, DuoKanChapter, PDFChapter, TXTChapter
from connector import Connector


def _get_chapter(package_type, file_path, use_duokan_notes):
    '''
    package_type: str
      File type
    file_path: str
      Path to book
    use_duokan_notes: boolean
      If true, then file_path is the path to exported duokan notes
    '''
    if not file_path:
        return Chapter()

    chapter = Chapter()

    if package_type == 'EPUB':
        chapter = EPUBChapter(file_path)
    elif package_type == 'PDF':
        chapter = PDFChapter(file_path)
    elif package_type == 'TXT':
        chapter = TXTChapter(file_path)

    if use_duokan_notes:
        chapter = DuoKanChapter(file_path)

    return chapter


def _get_chapter_name(chapter, package_type, index, annotations, use_duokan_notes):
    chapter_name = str(index)

    if package_type == 'EPUB':
        chapter_id = json.loads(annotations[0][1])[0]['chapter_id']
        chapter_name = chapter.getChapterName(chapter_id)
    elif package_type == 'PDF':
        chapter_name = chapter.getChapterName(index)
    elif package_type == 'TXT':
        chapter_name = chapter.getChapterName(annotations[0][3])

    if use_duokan_notes:
        chapter_name = chapter.getChapterName(annotations[0])

    return chapter_name


def export_annotations_in_books(book_id, file_path='', use_duokan_notes=False, time_format='%Y-%m-%d %H:%M:%S'):
    connector = Connector()

    annotations = connector.find_annotations_in_book(book_id)
    package_type = annotations[0][4]

    index_key = ''
    if package_type == 'PDF':
        index_key = 'fixed_index'
    elif package_type == 'TXT':
        index_key = 'byte_offset'
    elif package_type == 'EPUB':
        index_key = 'chapter_index'

    chapter = _get_chapter(package_type, file_path, use_duokan_notes)

    annotations.sort(key=lambda annotation: json.loads(annotation[1])[0][index_key])
    annotations_by_chapter = itertools.groupby(annotations, key=lambda annotation: json.loads(annotation[1])[0][index_key])

    annotations_by_chapter_with_chapter_name = []
    for index, annotations in annotations_by_chapter:
        annotations = list(annotations)
        chapter_name = _get_chapter_name(chapter, package_type, index,
                                         annotations, use_duokan_notes)

        annotation_by_chapter_with_chapter_name = []
        for annotation in annotations:
            added_time = datetime.datetime.utcfromtimestamp(annotation[0]/1000).strftime(time_format)
            note_text = json.loads(annotation[2])['note_text']
            annotation_sample = annotation[3]

            result = added_time + '\n' + annotation_sample + '\n'

            if len(note_text):
                result += '注：' + note_text + '\n'

            annotation_by_chapter_with_chapter_name.append((chapter_name, result))

        annotations_by_chapter_with_chapter_name.append(annotation_by_chapter_with_chapter_name)

    annotations_by_chapter_name = []
    i = 0
    while i < len(annotations_by_chapter_with_chapter_name):
        annotations_i = annotations_by_chapter_with_chapter_name[i]
        annotation_by_chapter_name = annotations_i

        j = i + 1

        while j < len(annotations_by_chapter_with_chapter_name):
            annotations_j = annotations_by_chapter_with_chapter_name[j]

            if annotations_i[0][0] == annotations_j[0][0]:
                annotation_by_chapter_name += annotations_j
                j = j + 1
            else:
                break

        annotations_by_chapter_name.append(annotation_by_chapter_name)
        i = j

    result = ''
    for annotation_by_chapter_name in annotations_by_chapter_name:
        result += '\n' + annotation_by_chapter_name[0][0] + '\n'
        for chapter_name, annotation in annotation_by_chapter_name:
            result += annotation

    return result.strip()
