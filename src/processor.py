import datetime
import itertools
import json
import os

from chapter import Chapter, EPUBChapter, DuoKanChapter, PDFChapter, TXTChapter
from connector import Connector
from setting import SortType, OutlineType, ExportBook, ExportSetting


def _get_chapter(package_type, file_path, use_duokan_notes):
    '''
    package_type: str
      File type
    file_path: str
      Path to book
    use_duokan_notes: boolean
      If true, then file_path is the path to exported duokan notes
    '''
    chapter = None

    if not file_path:
        return chapter

    if use_duokan_notes:
        return DuoKanChapter(file_path)

    if package_type == 'EPUB':
        chapter = EPUBChapter(file_path)
    elif package_type == 'PDF':
        chapter = PDFChapter(file_path)
    elif package_type == 'TXT':
        chapter = TXTChapter(file_path)

    return chapter


def _get_chapter_name(chapter, package_type, index, annotations, use_duokan_notes):
    arg = index

    if package_type == 'EPUB':
        arg = json.loads(annotations[0][1])[0]['chapter_id']
    elif package_type == 'PDF':
        arg = index
    elif package_type == 'TXT':
        arg = annotations[0][3]

    if use_duokan_notes:
        arg = annotations[0]

    chapter_name = chapter.getChapterName(arg)

    return chapter_name


def get_annotations_in_book(exportBook, exportSetting):
    connector = Connector(exportSetting.db_path)

    annotations = connector.find_annotations_in_book(exportBook.book_id)
    package_type = annotations[0][4]

    index_key = ''
    if package_type == 'PDF':
        index_key = 'fixed_index'
    elif package_type == 'TXT':
        index_key = 'byte_offset'
    elif package_type == 'EPUB':
        index_key = 'chapter_index'

    chapter = _get_chapter(package_type, exportBook.file_path, exportBook.use_duokan_notes)

    annotations.sort(key=lambda annotation: json.loads(annotation[1])[0][index_key])
    annotations_by_chapter = itertools.groupby(annotations, key=lambda annotation: json.loads(annotation[1])[0][index_key])

    annotations_by_chapter_with_chapter_name = []
    for index, annotations in annotations_by_chapter:
        annotations = list(annotations)

        if exportBook.file_path:
            # If not specific file path, then use info in
            # annotations.annotation_range as chapter name
            chapter_name = _get_chapter_name(chapter, package_type, index,
                                             annotations, exportBook.use_duokan_notes)
        else:
            chapter_name = str(index)

        annotation_by_chapter_with_chapter_name = []
        for annotation in annotations:
            added_time = datetime.datetime.utcfromtimestamp(annotation[0]/1000).strftime(exportSetting.time_format)
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


def export_annotations_in_book(exportBook, exportSetting):
    file_dir = exportSetting.export_dir
    file_name = exportBook.file_name
    file_path = os.path.join(file_dir, file_name + '.' + 'txt')

    content = get_annotations_in_book(exportBook, exportSetting)

    content = file_name + '\n' + exportBook.author + '\n\n' + content

    with open(file_path, 'w') as f:
        f.write(content)
