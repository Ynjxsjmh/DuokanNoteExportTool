import sqlite3


class Connector:
    def __init__(self, db_path='../data/Bookshelf.db'):
        self.con = sqlite3.connect(db_path)

    def __del__(self):
        self.con.close()

    def find_annotations_in_book(self, book_id):
        cur = self.con.cursor()

        sql = '''
        SELECT annotations.added_date AS added_date,
               annotation_range, annotation_body, annotation_sample,
               package_type
        FROM annotations
        INNER JOIN books on annotations.book_id = books._id
        WHERE books._id = ?;
        '''

        cur.execute(sql, (book_id,))

        results = cur.fetchall()

        return results

    def find_book_by_id(self, book_id):
        cur = self.con.cursor()

        sql = '''
        SELECT _id, book_name, author
        FROM books
        WHERE _id = ?;
        '''

        cur.execute(sql, (book_id,))

        result = cur.fetchone()

        return result

    def find_all_books(self):
        cur = self.con.cursor()

        sql = '''
        SELECT _id, book_name, author, book_uri
        FROM books;
        '''

        cur.execute(sql)

        results = cur.fetchall()

        return results
