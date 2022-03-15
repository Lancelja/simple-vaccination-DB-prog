from tkinter import *
from tkinter.ttk import Combobox
from PIL import ImageTk, Image
import sqlite3

root = Tk()
root.title('Vaccine Tracker')
root.geometry("300x300")
root.eval('tk::PlaceWindow . center')

#Creating database 
DB = sqlite3.connect('Vaccine_Tracker.db')

#cursor
cur = DB.cursor()

#--------------TABLE CREATION-------------------
#Uncoment this if you want to create a table then comment it again once DB and table is created

#Tables
'''
cur.execute("""CREATE TABLE Patients (
           ID integer,
           f_name text,
           l_name text,
           priority_class text,
           vacc_name text,
           doc_name text)
    """)'''

#--------------FUNCTIONS-------------------
#Submit/Add Record Method
def submit():
    DB = sqlite3.connect('Vaccine_Tracker.db')  
    cur = DB.cursor() #cursor
    #insert record
    cur.execute("INSERT INTO Patients VALUES (:ID, :f_name, :l_name, :priority_class, :vacc_name, :doc_name)",
        {
            'ID': ID.get(),
            'f_name': f_name.get(),
            'l_name': l_name.get(),
            'priority_class': priobox.get(),
            'vacc_name': vaccbox.get(),
            'doc_name': doc_name.get(),
        }         
     )
    DB.commit() #commit DB
    DB.close() #closing DB connection
    
    #clears boxes upon submit
    ID.delete(0, END)
    f_name.delete(0, END)
    l_name.delete(0, END)
    priobox.delete(0, END)
    vaccbox.delete(0, END)
    doc_name.delete(0, END)


#Show Record Method
def show():
    newWindow = Toplevel(root)
    newWindow.title("Patient Records")
    newWindow.geometry("350x255")
    
    DB = sqlite3.connect('Vaccine_Tracker.db')  #Creating database
    cur = DB.cursor() #cursor
    cur.execute("SELECT * FROM Patients")
    records = cur.fetchall()
    print(records)

    #loops records
    print_records = " "
    for records in records:
        print_records += str(records[0]) + "\t" + str(records[1]) + "\t" + str(records[2]) + "\t" + str(records[3]) + "\t" + str(records[4]) + "\t" + str(records[5]) + "\n"
    
    records_label = Label(newWindow, text=print_records)
    records_label.grid(row=8, column=0, columnspan=1)

    DB.commit() #commit DB
    DB.close() #closing DB connection


#Delete Record
def delete():
    newWindow = Toplevel(root)
    newWindow.title("Delete Patient")
    newWindow.geometry("350x255")
    
    delete_label = Label(newWindow,text="Enter ID: ")
    delete_label.grid(row=0,column=0)
    delete_box = Entry(newWindow,width=30)
    delete_box.grid(row=0,column=1,padx=20)

    def delete_p():
        #pass
        DB = sqlite3.connect('Vaccine_Tracker.db')  #Creating database
        cur = DB.cursor() #cursor

        cur.execute("DELETE FROM Patients WHERE id=" + delete_box.get())
        delete_box.delete(0,END)

        DB.commit() #commit DB
        DB.close() #closing DB connection

    #Delete Button
    delete_btn = Button(newWindow, text="Delete Patient", command=delete_p)
    delete_btn.grid(row=1, column=1,columnspan=1, pady=5)

#Update record
def update():
    global newWindow
    newWindow = Toplevel(root)
    newWindow.title("Update Patient Info")
    newWindow.geometry("350x255")

    update_label = Label(newWindow,text="Enter ID: ")
    update_label.grid(row=0,column=0)
    update_box = Entry(newWindow,width=30)
    update_box.grid(row=0,column=1,padx=20)

    def find_record():
        #pass
        global fname_edit
        global lname_edit
        global prioclass_edit
        global vaccname_edit
        global docname_edit

        DB = sqlite3.connect('Vaccine_Tracker.db')  #Creating database
        cur = DB.cursor() #cursor

        cur.execute("SELECT * FROM Patients WHERE id=" + update_box.get())
        records = cur.fetchall()

        fname_label = Label(newWindow, text = "First Name: ")
        fname_label.grid(row=2, column=0)
        lname_label = Label(newWindow, text = "Last Name: ")
        lname_label.grid(row=3, column=0)
        prioclass_label = Label(newWindow, text = "Priority Class: ")
        prioclass_label.grid(row=4, column=0)
        vaccname_label = Label(newWindow, text = "Vaccine: ")
        vaccname_label.grid(row=5, column=0)
        docname_label = Label(newWindow, text = "Doctor: ")
        docname_label.grid(row=6, column=0)

        fname_edit = Entry(newWindow, width=30)
        fname_edit.grid(row=2, column=1)
        lname_edit = Entry(newWindow, width=30)
        lname_edit.grid(row=3, column=1)
        #prioclass_edit = Entry(newWindow, width=30)
        #prioclass_edit.grid(row=4, column=1)
        #vaccname_edit = Entry(newWindow, width=30)
        #vaccname_edit.grid(row=5, column=1)
        prio_lvl = ("A", "B", "C")
        prioclass_edit=Combobox(newWindow, values=prio_lvl)
        prioclass_edit.grid(row=4, column=1, ipadx=20)
        vaccines = ("Pfizer", "Moderna", "Astra", "Sinovac", "Sputnik", "Johnson&Johnson", "Covaxin", "Sinopharm")
        vaccname_edit=Combobox(newWindow, values=vaccines)
        vaccname_edit.grid(row=5, column=1, ipadx=20)
        docname_edit = Entry(newWindow, width=30)
        docname_edit.grid(row=6, column=1)

        #shows searched record
        for records in records:
            fname_edit.insert(0, records[1])
            lname_edit.insert(0, records[2])
            prioclass_edit.insert(0, records[3])
            vaccname_edit.insert(0, records[4])
            docname_edit.insert(0, records[5])

        update_btn = Button(newWindow, text="Update Patient", command=save_edit)
        update_btn.grid(row=7, column=1,columnspan=1, pady=5)

        DB.commit() #commit DB
        DB.close() #closing DB connection

    def save_edit():
        DB = sqlite3.connect('Vaccine_Tracker.db')  #Creating database
        cur = DB.cursor() #cursor

        cur.execute("""UPDATE Patients SET
             f_name = :first,
             /*l_name = :last,*/
             priority_class = :prioclass,
             vacc_name = :vacc,
             doc_name = :doc
             WHERE id = :id""",
             {
              'first': fname_edit.get(),
              'last': lname_edit.get(),
              'prioclass': prioclass_edit.get(),
              'vacc': vaccname_edit.get(),
              'doc': docname_edit.get(),
              'id': update_box.get()  
              })

        DB.commit() #commit DB
        DB.close() #closing DB connection
        fname_edit.delete(0,END)
        lname_edit.delete(0,END)
        prioclass_edit.delete(0,END)
        vaccname_edit.delete(0,END)
        docname_edit.delete(0,END)

    search_btn = Button(newWindow, text="Search Patient", command=find_record)
    search_btn.grid(row=1, column=1,columnspan=1, pady=5)

   # saveedit_btn = Button(newWindow, text="Update Patient", command=save_edit)
   # saveedit_btn.grid(row=7, column=1,columnspan=1, pady=5)


#Ends Program
def exit():
    root.destroy()

#--------------MENU---------------------
#entry boxes
ID = Entry(root, width=30)
ID.grid(row=0, column=1, padx=20)
f_name = Entry(root, width=30)
f_name.grid(row=1, column=1,)
l_name = Entry(root, width=30)
l_name.grid(row=2, column=1,)
#priority_class = Entry(root, width=30)
#priority_class.grid(row=3, column=1)
#vacc_name = Entry(root, width=30)
#vacc_name.grid(row=4, column=1)

#dropdown menu
prio_lvl = ("A", "B", "C")
priobox=Combobox(root, values=prio_lvl)
priobox.grid(row=3, column=1, ipadx=20)
vaccines = ("Pfizer", "Moderna", "Astra", "Sinovac", "Sputnik", "Johnson&Johnson", "Covaxin", "Sinopharm")
vaccbox=Combobox(root, values=vaccines)
vaccbox.grid(row=4, column=1, ipadx=20)

doc_name = Entry(root, width=30)
doc_name.grid(row=5, column=1)

#Labels
IDLabel = Label(root, text = "Patient ID: ")
IDLabel.grid(row=0, column=0)
f_nameLabel = Label(root, text = "First Name: ")
f_nameLabel.grid(row=1, column=0)
l_nameLabel = Label(root, text = "Last Name: ")
l_nameLabel.grid(row=2, column=0)
priority_classLabel = Label(root, text = "Priority Class: ")
priority_classLabel.grid(row=3, column=0)
vacc_nameLabel = Label(root, text = "Vaccine: ")
vacc_nameLabel.grid(row=4, column=0)
doc_nameLabel = Label(root, text = "Doctor: ")
doc_nameLabel.grid(row=5, column=0)


#--------------BUTTONS-------------------
#Submit Button
submit_btn = Button(root, text="Add Patient", command=submit)
submit_btn.grid(row=6, column=0, columnspan=1, pady=5)

#Show Button
show_btn = Button(root, text="Show Patients", command=show)
show_btn.grid(row=6, column=1,columnspan=2, pady=5)

#Delete Button
show_btn = Button(root, text="Delete Patient", command=delete)
show_btn.grid(row=7, column=0,columnspan=1, pady=5)

#Update Button
show_btn = Button(root, text="Update Patient", command=update)
show_btn.grid(row=7, column=1,columnspan=2, pady=5)

#Exit Button
show_btn = Button(root, text="Exit", command=exit)
show_btn.grid(row=8, column=0,columnspan=1, pady=5, ipadx=20)

#Label for output records
#show_label = Label(root, text = "Records")
#how_label.grid(row=8, column=0, columnspan=2, pady=0, ipadx=100)


#commit DB
DB.commit()
#closing DB connection
DB.close()
root.mainloop()