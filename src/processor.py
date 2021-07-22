import datetime
import itertools
import json

from connector import Connector


def export_annotations_in_books(book_id, time_format='%Y-%m-%d %H:%M:%S'):
    connector = Connector()

    result = ''

    annotations = connector.find_annotations_in_book(book_id)
    package_type = annotations[0][4]

    index_key = ''
    if package_type == 'PDF':
        index_key = 'fixed_index'
    elif package_type == 'TXT':
        index_key = 'byte_offset'
    elif package_type == 'EPUB':
        index_key = 'chapter_index'

    annotations.sort(key=lambda annotation: json.loads(annotation[1])[0][index_key])
    annotations_by_chapter = itertools.groupby(annotations, key=lambda annotation: json.loads(annotation[1])[0][index_key])

    for chapter, annotations in annotations_by_chapter:
        result += str(chapter) + '\n'

        for annotation in annotations:
            added_time = datetime.datetime.utcfromtimestamp(annotation[0]/1000).strftime(time_format)
            note_text = json.loads(annotation[2])['note_text']
            annotation_sample = annotation[3]

            result += added_time + '\n'
            result += annotation_sample + '\n'

            if len(note_text):
                result += '注：' + note_text + '\n'

    return result
