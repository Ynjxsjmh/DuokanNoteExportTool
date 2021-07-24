from enum import Enum


class SortType(Enum):
    CHAPTER = 0
    TIME    = 1


class OutlineType(Enum):
    ORIGIN = 0
    MD     = 1
    ORG    = 2


class ExportBook():
    def __init__(self):
        self._book_id = None
        self._file_path = ''
        self._use_duokan_notes = False

    @property
    def book_id(self):
        return self._book_id

    @book_id.setter
    def book_id(self, book_id):
        self._book_id = book_id

    @property
    def use_duokan_notes(self):
        return self._use_duokan_notes

    @use_duokan_notes.setter
    def use_duokan_notes(self, use_duokan_notes):
        self._use_duokan_notes = use_duokan_notes

    @property
    def file_path(self):
        return self._file_path

    @file_path.setter
    def file_path(self, file_path):
        self._file_path = file_path


class ExportSetting:
    def __init__(self):
        self._db_path = ''
        self._time_format = '%Y-%m-%d %H:%M:%S'
        self._sort_type = SortType.CHAPTER
        self._outline_type = OutlineType.ORIGIN
        self._export_dir = ''
        self.export_books = []

    @property
    def db_path(self):
        return self._db_path

    @db_path.setter
    def db_path(self, db_path):
        self._db_path = db_path

    @property
    def time_format(self):
        return self._time_format

    @time_format.setter
    def time_format(self, time_format):
        self._time_format = time_format

    @property
    def sort_type(self):
        return self._sort_type

    @sort_type.setter
    def sort_type(self, sort_type):
        self._sort_type = sort_type

    @property
    def outline_type(self):
        return self._outline_type

    @outline_type.setter
    def outline_type(self, outline_type):
        self._outline_type = outline_type

    @property
    def export_dir(self):
        return self._export_dir

    @export_dir.setter
    def export_dir(self, export_dir):
        self._export_dir = export_dir

    def __str__(self):
        return 'db_path: {}, time_format: {}, sort_type: {}, outline_type: {}, export_dir: {}'.format(
            self._db_path,
            self._time_format,
            self._sort_type,
            self._outline_type,
            self._export_dir,
        )

