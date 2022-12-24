# Pin Your Note - Kalyani Reddy
# Import Necessary modules
import sqlite3 as sql
from tkinter import *
from tkinter import messagebox
from tabulate import tabulate
# Create database connection and connect to table
try:
    con = sql.connect('pin_your_note1.db')
    cur = con.cursor()
    cur.execute('''CREATE TABLE notes_table
                         (date text, notes_title text, notes text)''')
except:
    print("Connected to table of database")

# Declaring functions to take, edit, view and delete notes:
# Insert a row of data
def add_notes():
        today = date_entry.get()
        notes_title = notes_title_entry.get()
        notes = notes_entry.get("1.0","end-1c")
        # if no values are given
        if len(today)<=0 and len(notes_title)<=0 and len(notes)<=1:
            messagebox.showerror(message="enter required details")
        else:
            cur.execute("INSERT INTO notes_table values ('%s','%s','%s')"%(today,notes_title,notes))
            messagebox.showinfo(message="Note added")
            con.commit()

# Display all the notes
def view_notes():
    date = date_entry.get()
    notes_title = notes_title_entry.get()
    # if no input is given, display all the notes
    if len(date)<=0 and len(notes_title)<=0:
        sql_statement = "select * from notes_table"
    elif len(date)<=0 and len(notes_title)>0:
        sql_statement = "select * from notes_table where notes_title = '%s'"%(notes_title)
    elif len(date)>0 and len(notes_title)<=0:
        sql_statement = "select * from notes_table where date = '%s'"%(date)
    else:
        sql_statement = "Select * from notes_table where date = '%s' and notes_title = '%s'" % (date,notes_title)
    # execute the query
    cur.execute(sql_statement)
    # obtain all the contents of query
    row = cur.fetchall()
    # check if none was retrived
    n = len(row)
    if len(row)<=0:
        messagebox.showerror(message="No note found")
    else:
        keys = ['Date','Title','Notes']

        messagebox.showinfo(message= tabulate(row,headers=keys,tablefmt='fancy_grid'))



# delete the notes
def delete_notes():
    date = date_entry.get()
    notes_title = notes_title_entry.get()
    choice = messagebox.askquestion(message="Do you want to delete all the notes?")
    if choice == 'yes' or choice =='YES':
        sql_statement = 'Delete from notes_table'
    else:
        if len(date)<=0 and len(notes_title)<=0:
            messagebox.showerror(message="ENTER REQUIRED DETAILS")
            return
        else:
            sql_statement = " Delete from notes_table where date = '%s' and notes_title = '%s'"%(date,notes_title)

    cur.execute(sql_statement)
    messagebox.showinfo(message='Note(s) deleted')
    con.commit()

# update the notes
def update_notes():
    today = date_entry.get()
    notes_title = notes_title_entry.get()
    notes = notes_entry.get("1.0","end-1c")
    if len(today)<=0 and len(notes_title)<=0 and len(notes)<=1:
        messagebox.showerror(message="Enter Required Details")
    else:
        sql_statement = "update notes_table set notes= '%s' where date='%s' and notes_title='%s'"%(notes,today,notes_title)
        cur.execute(sql_statement)
    messagebox.showinfo(message="Notes updated")
    con.commit()

# Creating a user interface for Python Pin Your Note Project:
# View a window:
window = Tk()
# set dimensions for window and title
window.geometry('600x400')
window.title('Pin your note - Kalyani Reddy')
title_label = Label(window,text = 'Pin your note - Kalyani Reddy').pack()
# date inputs
date_label = Label(window,text = "Date:").place(x=10,y=20)
date_entry = Entry(window,width=20)
date_entry.place(x=50,y=20)
# title inputs
notes_title_label = Label(window,text = "Notes Title:").place(x=10,y=50)
notes_title_entry = Entry(window,width=30)
notes_title_entry.place(x=80,y=50)
# notes inputs
note_label = Label(window, text="Notes:").place(x=10, y=90)
notes_entry = Text(window, width=50, height=5)
notes_entry.place(x=60,y=90)

# perform notes function
button1 = Button(window, text = 'Add notes',bg = 'orange',fg = 'black',command=add_notes).place(x=10,y=190)
button2 = Button(window,text = 'View notes',bg = 'orange',fg = 'black',command=view_notes).place(x=110,y=190)
button3 = Button(window,text = 'Delete notes',bg = 'orange',fg = 'black',command=delete_notes).place(x=210,y=190)
button4 = Button(window,text = 'Update notes',bg = 'orange',fg = 'black',command=update_notes).place(x=320,y=190)

window.mainloop()
con.close()
