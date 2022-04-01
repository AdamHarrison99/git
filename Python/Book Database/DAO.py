import mysql.connector

mydb = mysql.connector.connect(
    user='user',
    passwd='password',
    database='comp3421',
    host='127.0.0.1')

mycur = mydb.cursor()

class Author():
    def __init__(self, author_num):
        sql = "SELECT * FROM HENRY_WROTE WHERE AUTHOR_NUM LIKE '" + str(author_num) + "';"
        mycur.execute(sql)

        self.book_codes = []
        self.sequences = []
        for row in mycur:
            self.book_codes.append(row[0])
            self.sequences.append(row[2])

    def get_book_codes(self):
        return self.book_codes

    def get_sequences(self):
        return self.sequences

class Book():
    def __init__(self):
        self.book_titles = []
        self.publisher_code = []
        self.book_type = []
        self.book_price = []
        self.paperback = []

    def new_book(self, book_num):
        sql = "SELECT * FROM HENRY_BOOK WHERE BOOK_CODE LIKE '" + book_num + "';"
        mycur.execute(sql)

        for row in mycur:
            self.book_titles.append(row[1])
            self.publisher_code.append(row[2])
            self.book_type.append(row[3])
            self.book_price.append(row[4])
            self.paperback.append(row[5])

    def get_book_title(self):
        return self.book_titles

    def get_book_price(self):
        return self.book_price

    def get_book_type(self):
        return self.book_type

    def get_publisher_code(self):
        return self.publisher_code

    def get_book_paperback(self):
        return self.paperback

class Branch():
    def __init__(self, book_num):
        sql = "SELECT * FROM HENRY_INVENTORY WHERE BOOK_CODE LIKE '" + book_num + "';"
        mycur.execute(sql)

        self.branch_nums = []
        self.on_hand = []
        self.branch_names = []
        self.branch_locations = []
        self.num_employees = []
        for row in mycur:
            self.branch_nums.append(row[1])
            self.on_hand.append(row[2])

        for num in self.branch_nums:
            sql = "SELECT * FROM HENRY_BRANCH WHERE BRANCH_NUM LIKE '" + str(num) + "';"
            mycur.execute(sql)

            for row in mycur:
                self.branch_names.append(row[1])
                self.branch_locations.append(row[1])
                self.num_employees.append(row[1])

    def get_book_branches(self):
        return self.branch_names

    def get_book_branches_nums(self):
        return self.branch_nums

    def get_on_hand(self):
        return self.on_hand

    def get_branch_locations(self):
        return self.branch_locations

    def get_num_employees(self):
        return self.num_employees

class Publisher():
    def __init__(self):
        sql = "SELECT * FROM HENRY_PUBLISHER;"
        mycur.execute(sql)

        self.publisher_codes = []
        self.publisher_names = []
        self.publisher_citys = []

        for row in mycur:
            self.publisher_codes.append(row[0])
            self.publisher_names.append(row[1])
            self.publisher_citys.append(row[2])

    def get_publisher_codes(self):
        return self.publisher_codes

    def get_publisher_names(self):
        return self.publisher_names

    def get_publisher_citys(self):
        return self.publisher_citys

class DAO_start():
    def __init__(self):
        sql = "SELECT * FROM HENRY_AUTHOR ORDER BY AUTHOR_FIRST ASC;"
        mycur.execute(sql);

        self.author_names = []
        self.author_num = []
        for row in mycur:
            self.author_names.append(row[2] + " " + row[1])
            self.author_num.append(row[0])

        sql = "SELECT * FROM HENRY_BOOK ORDER BY TITLE ASC;"
        mycur.execute(sql);

        self.book_codes = []
        self.book_titles = []
        self.publisher_codes = []
        self.types = []
        self.prices = []
        self.paperback = []

        for row in mycur:
            self.book_codes.append(row[0])
            self.book_titles.append(row[1])
            self.publisher_codes.append(row[2])
            self.types.append(row[3])
            self.prices.append(row[4])
            self.paperback.append(row[5])

    def get_author_names(self):
        return self.author_names

    def get_author_nums(self):
        return self.author_num

    def get_book_codes(self):
        return self.book_codes

    def get_book_titles(self):
        return self.book_titles

    def get_book_publisher_codes(self):
        return self.publisher_codes

    def get_book_types(self):
        return self.types

    def get_book_prices(self):
        return self.prices

    def get_book_paperback(self):
        return self.paperback
