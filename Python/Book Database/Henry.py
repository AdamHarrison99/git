import sys
import time
from tkinter import *
import tkinter as tk
from tkinter import ttk
from DAO import *

DAO = DAO_start()

root = tk.Tk()
root.geometry('1100x500')
root.resizable(False, False)
style = ttk.Style(root)
style.configure('Treeview', rowheight=40)
root.title('Henry Bookstore')

tabControl = ttk.Notebook(root)
SBA_tab = ttk.Frame(tabControl)
SBC_tab = ttk.Frame(tabControl)
SBP_tab = ttk.Frame(tabControl)

tabControl.add(SBA_tab, text='Search By Author')
tabControl.add(SBC_tab, text='Search By Category')
tabControl.add(SBP_tab, text='Search By Publisher')
tabControl.pack(expand = 1, fill ="both")

class SBA():
    def __init__(self, SBA_tab):
        def selected_name_changed(event):
            self.name_changed_helper_start()

        def selected_book_changed(event):
            self.book_changed_helper_start()

        SB_frame = ttk.Frame(SBA_tab, padding=0)
        SB_frame.grid()

        table_frm = ttk.Frame(SB_frame, padding=10)
        table_frm.grid(column=0, row=0)
        self.tree = ttk.Treeview(table_frm, column=("c1", "c2"), show='headings', height=5)
        self.tree.column("# 1", anchor=CENTER, width=300)
        self.tree.heading("# 1", text="Branch Name")
        self.tree.column("# 2", anchor=CENTER, width=300)
        self.tree.heading("# 2", text="Copies Avaliable")

        self.tree.pack()

        select_A_frm = ttk.Frame(SB_frame, padding=10)
        select_A_frm.grid(column=0, row=1)
        select_B_frm = ttk.Frame(SB_frame, padding=10)
        select_B_frm.grid(column=1, row=1)

        ttk.Label(select_A_frm, text="Please select a name:").grid(column=0, row=1)
        ttk.Label(select_B_frm, text="Please select a book:").grid(column=1, row=1)

        self.a_selected_name = tk.StringVar()
        self.b_selected_name = tk.StringVar()

        self.Author_Names = DAO.get_author_names()
        self.Author_Nums = DAO.get_author_nums()
        self.a_name_cb = ttk.Combobox(select_A_frm, textvariable=self.a_selected_name, width=25)
        self.a_name_cb['values'] = DAO.get_author_names()
        self.a_name_cb['state'] = 'readonly'
        self.a_name_cb.bind('<<ComboboxSelected>>', selected_name_changed)
        self.a_name_cb.grid(column=0, row=2)

        self.b_name_cb = ttk.Combobox(select_B_frm, textvariable=self.b_selected_name, width=25)
        self.b_name_cb['state'] = 'readonly'
        self.b_name_cb.bind('<<ComboboxSelected>>', selected_book_changed)
        self.b_name_cb.grid(column=1, row=2)

        ttk.Button(SB_frame, text="Quit", command=root.destroy).grid(column=1, row=3)

        self.price_frm = ttk.Frame(SB_frame, padding=0)
        self.price_frm.grid(column=1, row=0)
        self.price_lable = ttk.Label(self.price_frm, text="Price: ")
        self.price_lable.pack()

    def start(self):
        self.a_name_cb.current(0)
        self.name_changed_helper_start()

    def name_changed_helper_start(self):
        pos = 0
        for j, i in enumerate(self.Author_Names):
            if i == self.a_name_cb.get():
                pos = j
                break

        AuthorClass = Author(DAO.get_author_nums()[pos])
        self.book_codes = AuthorClass.get_book_codes()

        BookClass = Book()
        for code in self.book_codes:
            BookClass.new_book(code)
        self.book_titles = (BookClass.get_book_title())
        self.book_price = (BookClass.get_book_price())

        self.b_name_cb['values'] = self.book_titles

        self.b_name_cb.current(0)
        self.book_changed_helper_start()

    def book_changed_helper_start(self):
        self.tree.delete(*self.tree.get_children())

        pos = 0
        for j, i in enumerate(self.book_titles):
            if i == self.b_name_cb.get():
                pos = j
                break

        BranchClass = Branch(self.book_codes[pos])
        branch_names = BranchClass.get_book_branches()
        copies_per_branch = BranchClass.get_on_hand()

        for i in range(0,len(copies_per_branch)):
            self.tree.insert('', 'end', values=(branch_names[i], copies_per_branch[i]))

        self.price_lable.destroy()
        book_price = self.book_price[pos]

        self.price_lable = ttk.Label(self.price_frm, text="Price: $" + str(book_price))
        self.price_lable.pack()

class SBC():
    def __init__(self, SBC_tab):
        def selected_name_changed(event):
            self.name_changed_helper_start()

        def selected_book_changed(event):
            self.book_changed_helper_start()

        SB_frame = ttk.Frame(SBC_tab, padding=0)
        SB_frame.grid()

        table_frm = ttk.Frame(SB_frame, padding=10)
        table_frm.grid(column=0, row=0)
        self.tree = ttk.Treeview(table_frm, column=("c1", "c2"), show='headings', height=5)
        self.tree.column("# 1", anchor=CENTER, width=300)
        self.tree.heading("# 1", text="Branch Name")
        self.tree.column("# 2", anchor=CENTER, width=300)
        self.tree.heading("# 2", text="Copies Avaliable")

        self.tree.pack()

        select_A_frm = ttk.Frame(SB_frame, padding=10)
        select_A_frm.grid(column=0, row=1)
        select_B_frm = ttk.Frame(SB_frame, padding=10)
        select_B_frm.grid(column=1, row=1)

        ttk.Label(select_A_frm, text="Please select a category:").grid(column=0, row=1)
        ttk.Label(select_B_frm, text="Please select a book:").grid(column=1, row=1)

        self.a_selected_name = tk.StringVar()
        self.b_selected_name = tk.StringVar()

        self.cat_names = DAO.get_book_types()
        self.a_name_cb = ttk.Combobox(select_A_frm, textvariable=self.a_selected_name, width=25)
        self.a_name_cb['values'] = self.cat_names
        self.a_name_cb['state'] = 'readonly'
        self.a_name_cb.bind('<<ComboboxSelected>>', selected_name_changed)
        self.a_name_cb.grid(column=0, row=2)

        self.b_name_cb = ttk.Combobox(select_B_frm, textvariable=self.b_selected_name, width=25)
        self.b_name_cb['state'] = 'readonly'
        self.b_name_cb.bind('<<ComboboxSelected>>', selected_book_changed)
        self.b_name_cb.grid(column=1, row=2)

        ttk.Button(SB_frame, text="Quit", command=root.destroy).grid(column=1, row=3)

        self.price_frm = ttk.Frame(SB_frame, padding=0)
        self.price_frm.grid(column=1, row=0)
        self.price_lable = ttk.Label(self.price_frm, text="Price: ")
        self.price_lable.pack()

    def start(self):
        self.a_name_cb.current(0)
        self.name_changed_helper_start()

    def name_changed_helper_start(self):
        pos = 0
        for i, j in enumerate(self.cat_names):
            if i == self.a_name_cb.get():
                pos = j
        self.book_titles = []
        self.book_price = []
        self.book_codes_init = DAO.get_book_codes()
        self.book_codes = []

        for code in self.book_codes_init:
            BookClass = Book()
            BookClass.new_book(code)

            if BookClass.get_book_type()[0] == self.a_name_cb.get():
                self.book_titles.append(BookClass.get_book_title()[0])
                self.book_price.append(BookClass.get_book_price()[0])
                self.book_codes.append(code)

        self.b_name_cb['values'] = self.book_titles
        self.b_name_cb.current(0)
        self.book_changed_helper_start()

    def book_changed_helper_start(self):
        self.tree.delete(*self.tree.get_children())

        pos = 0
        for j, i in enumerate(self.book_titles):
            if i == self.b_name_cb.get():
                pos = j
                break

        BranchClass = Branch(self.book_codes[pos])
        branch_names = BranchClass.get_book_branches()
        copies_per_branch = BranchClass.get_on_hand()

        for i in range(0,len(copies_per_branch)):
            self.tree.insert('', 'end', values=(branch_names[i], copies_per_branch[i]))

        self.price_lable.destroy()
        book_price = self.book_price[pos]

        self.price_lable = ttk.Label(self.price_frm, text="Price: $" + str(book_price))
        self.price_lable.pack()

class SBP():
    def __init__(self, SBP_tab):
        def selected_name_changed(event):
            self.name_changed_helper_start()

        def selected_book_changed(event):
            self.book_changed_helper_start()

        SB_frame = ttk.Frame(SBP_tab, padding=0)
        SB_frame.grid()

        table_frm = ttk.Frame(SB_frame, padding=10)
        table_frm.grid(column=0, row=0)
        self.tree = ttk.Treeview(table_frm, column=("c1", "c2"), show='headings', height=5)
        self.tree.column("# 1", anchor=CENTER, width=300)
        self.tree.heading("# 1", text="Branch Name")
        self.tree.column("# 2", anchor=CENTER, width=300)
        self.tree.heading("# 2", text="Copies Avaliable")

        self.tree.pack()

        select_A_frm = ttk.Frame(SB_frame, padding=10)
        select_A_frm.grid(column=0, row=1)
        select_B_frm = ttk.Frame(SB_frame, padding=10)
        select_B_frm.grid(column=1, row=1)

        ttk.Label(select_A_frm, text="Please select a publisher:").grid(column=0, row=1)
        ttk.Label(select_B_frm, text="Please select a book:").grid(column=1, row=1)

        self.a_selected_name = tk.StringVar()
        self.b_selected_name = tk.StringVar()

        self.PublisherClass = Publisher()
        self.pub_codes_init = self.PublisherClass.get_publisher_codes()
        self.pub_codes = []
        for code in DAO.get_book_codes():
            for pub_code in self.pub_codes_init:
                BookClass = Book()
                BookClass.new_book(code)
                if BookClass.get_publisher_code()[0] == pub_code:
                    self.pub_codes.append(pub_code)

        self.publisher_names = self.PublisherClass.get_publisher_names()

        self.a_name_cb = ttk.Combobox(select_A_frm, textvariable=self.a_selected_name, width=25)
        self.a_name_cb['values'] = self.publisher_names
        self.a_name_cb['state'] = 'readonly'
        self.a_name_cb.bind('<<ComboboxSelected>>', selected_name_changed)
        self.a_name_cb.grid(column=0, row=2)

        self.b_name_cb = ttk.Combobox(select_B_frm, textvariable=self.b_selected_name, width=25)
        self.b_name_cb['state'] = 'readonly'
        self.b_name_cb.bind('<<ComboboxSelected>>', selected_book_changed)
        self.b_name_cb.grid(column=1, row=2)

        ttk.Button(SB_frame, text="Quit", command=root.destroy).grid(column=1, row=3)

        self.price_frm = ttk.Frame(SB_frame, padding=0)
        self.price_frm.grid(column=1, row=0)
        self.price_lable = ttk.Label(self.price_frm, text="Price: ")
        self.price_lable.pack()

    def start(self):
        self.a_name_cb.current(0)
        self.name_changed_helper_start()

    def name_changed_helper_start(self):
        pos = 0
        for j, i in enumerate(self.publisher_names):
            if i == self.a_name_cb.get():
                pos = j
                break

        self.book_titles = []
        self.book_price = []
        self.book_codes_init = DAO.get_book_codes()
        self.book_codes = []

        for code in self.book_codes_init:
            BookClass = Book()
            BookClass.new_book(code)

            if BookClass.get_publisher_code()[0] == self.pub_codes[pos]:
                self.book_titles.append(BookClass.get_book_title()[0])
                self.book_price.append(BookClass.get_book_price()[0])
                self.book_codes.append(code)

        self.b_name_cb['values'] = self.book_titles
        self.b_name_cb.current(0)
        self.book_changed_helper_start()

    def book_changed_helper_start(self):
        self.tree.delete(*self.tree.get_children())

        pos = 0
        for j, i in enumerate(self.book_titles):
            if i == self.b_name_cb.get():
                pos = j
                break

        BranchClass = Branch(self.book_codes[pos])
        branch_names = BranchClass.get_book_branches()
        copies_per_branch = BranchClass.get_on_hand()

        for i in range(0,len(copies_per_branch)):
            self.tree.insert('', 'end', values=(branch_names[i], copies_per_branch[i]))

        self.price_lable.destroy()
        book_price = self.book_price[pos]

        self.price_lable = ttk.Label(self.price_frm, text="Price: $" + str(book_price))
        self.price_lable.pack()

SBA = SBA(SBA_tab)
SBA.start()

SBC = SBC(SBC_tab)
SBC.start()

SBP = SBP(SBP_tab)
SBP.start()

SBA_tab.bind("<ButtonPress-1>", SBA)
SBC_tab.bind("<ButtonPress-1>", SBC)
SBP_tab.bind("<ButtonPress-1>", SBP)

root.mainloop()
