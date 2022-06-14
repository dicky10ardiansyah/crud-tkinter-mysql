# %s - Mysql
# ? -> Sqlite

from tkinter import*
import tkinter.ttk as ttk
import tkinter.messagebox as tkMessageBox
import pymysql

root = Tk()
root.title("CRUD sederhana Tkinter dan MySql")
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
width = 1280
height = 500
x = (screen_width/2) - (width/2)
y = (screen_height/2) - (height/2)
root.geometry('%dx%d+%d+%d' % (width, height, x, y))
root.resizable(0, 0)

#==================================METHODS============================================
def Database():
    global conn, cursor
    conn = pymysql.connect(host = 'localhost', user = 'root', password = '', db = 'tkinter_crud')
    cursor = conn.cursor()

def Create():
    if  FIRSTNAME.get() == "" or LASTNAME.get() == "" or GENDER.get() == "" or ADDRESS.get() == "" or USERNAME.get() == "" or PASSWORD.get() == "":
        txt_result.config(text="Pastikan semua kolom terisi!", fg="red")
    else:
        Database()
        #cursor.execute("INSERT INTO `member` (firstname, lastname, gender, address, username, password) VALUES(?, ?, ?, ?, ?, ?)",
        cursor.execute("INSERT INTO `member` (firstname, lastname, gender, address, username, password) VALUES(%s, %s, %s, %s, %s, %s)",
                       (str(FIRSTNAME.get()), str(LASTNAME.get()), str(GENDER.get()), str(ADDRESS.get()), str(USERNAME.get()), str(PASSWORD.get())))
        tree.delete(*tree.get_children())
        cursor.execute("SELECT * FROM `member` ORDER BY `lastname` ASC")
        fetch = cursor.fetchall()
        for data in fetch:
            tree.insert('', 'end', values=(data[0], data[1], data[2], data[3], data[4], data[5], data[6]))
        conn.commit()
        FIRSTNAME.set("")
        LASTNAME.set("")
        GENDER.set("")
        ADDRESS.set("")
        USERNAME.set("")
        PASSWORD.set("")
        cursor.close()
        conn.close()
        txt_result.config(text="Data berhasil dibuat!", fg="green")

def Read():
    tree.delete(*tree.get_children())
    Database()
    cursor.execute("SELECT * FROM `member` ORDER BY `lastname` ASC")
    fetch = cursor.fetchall()
    for data in fetch:
        tree.insert('', 'end', values=(data[0], data[1], data[2], data[3], data[4], data[5], data[6]))
    cursor.close()
    conn.close()
    txt_result.config(text="Data database berhasil terbaca.", fg="black")

def Update():
    Database()
    if GENDER.get() == "":
        txt_result.config(text="Gender belum diisi", fg="red")
    else:
        tree.delete(*tree.get_children())
        cursor.execute("UPDATE `member` SET `firstname` = %s, `lastname` = %s, `gender` = %s,  `address` = %s,  `username` = %s, `password` = %s WHERE `id` = %s",
                       (str(FIRSTNAME.get()), str(LASTNAME.get()), str(GENDER.get()), str(ADDRESS.get()), str(USERNAME.get()), str(PASSWORD.get()), int(id)))
        conn.commit()
        cursor.execute("SELECT * FROM `member` ORDER BY `lastname` ASC")
        fetch = cursor.fetchall()
        for data in fetch:
            tree.insert('', 'end', values=(data[0], data[1], data[2], data[3], data[4], data[5], data[6]))
        cursor.close()
        conn.close()
        FIRSTNAME.set("")
        LASTNAME.set("")
        GENDER.set("")
        ADDRESS.set("")
        USERNAME.set("")
        PASSWORD.set("")
        btn_create.config(state=NORMAL)
        btn_read.config(state=NORMAL)
        btn_update.config(state=DISABLED)
        btn_delete.config(state=NORMAL)
        txt_result.config(text="Data berhasil diupdate", fg="green")


def OnSelected(event):
    global id;
    curItem = tree.focus()
    contents =(tree.item(curItem))
    selecteditem = contents['values']
    id = selecteditem[0]
    FIRSTNAME.set("")
    LASTNAME.set("")
    GENDER.set("")
    ADDRESS.set("")
    USERNAME.set("")
    PASSWORD.set("")
    FIRSTNAME.set(selecteditem[1])
    LASTNAME.set(selecteditem[2])
    GENDER.set(selecteditem[3])
    ADDRESS.set(selecteditem[4])
    USERNAME.set(selecteditem[5])
    PASSWORD.set(selecteditem[6])
    btn_create.config(state=DISABLED)
    btn_read.config(state=DISABLED)
    btn_update.config(state=NORMAL)
    btn_delete.config(state=DISABLED)

def Delete():
    if not tree.selection():
       txt_result.config(text="Pilih data sebelum hapus.", fg="red")
    else:
        result = tkMessageBox.askquestion('CRUD Tkinter & MySql', 'Apakah anda yakin ingin menghapus data ini?', icon="warning")
        if result == 'yes':
            curItem = tree.focus()
            contents =(tree.item(curItem))
            selecteditem = contents['values']
            tree.delete(curItem)
            Database()
            cursor.execute("DELETE FROM `member` WHERE `id` = %d" % selecteditem[0])
            conn.commit()
            cursor.close()
            conn.close()
            txt_result.config(text="Data berhasil dihapus", fg="red")


def Exit():
    result = tkMessageBox.askquestion('CRUD Tkinter & MySql', 'Yakin ingin keluar?', icon="warning")
    if result == 'yes':
        root.destroy()
        exit()

#==================================VARIABLES==========================================
FIRSTNAME = StringVar()
LASTNAME = StringVar()
GENDER = StringVar()
ADDRESS = StringVar()
USERNAME = StringVar()
PASSWORD = StringVar()

#==================================FRAME==============================================
Top = Frame(root, width=900, height=50, bd=2, relief="raise")
Top.pack(side=TOP)
Left = Frame(root, width=300, height=500, bd=2, relief="raise")
Left.pack(side=LEFT)
Right = Frame(root, width=600, height=500, bd=2, relief="raise")
Right.pack(side=RIGHT)
Forms = Frame(Left, width=300, height=450)
Forms.pack(side=TOP)
Buttons = Frame(Left, width=300, height=100, bd=2, relief="raise")
Buttons.pack(side=BOTTOM)
RadioGroup = Frame(Forms)
Male = Radiobutton(RadioGroup, text="Laki-laki", variable=GENDER, value="Male", font=('arial', 16)).pack(side=LEFT)
Female = Radiobutton(RadioGroup, text="Perempuan", variable=GENDER, value="Female", font=('arial', 16)).pack(side=LEFT)

#==================================LABEL WIDGET=======================================
txt_title = Label(Top, width=900, font=('arial', 24), text = "CRUD sederhana Tkinter & MySql")
txt_title.pack()
txt_firstname = Label(Forms, text="Nama depan:", font=('arial', 16), bd=15)
txt_firstname.grid(row=0, sticky="e")
txt_lastname = Label(Forms, text="Nama belakang:", font=('arial', 16), bd=15)
txt_lastname.grid(row=1, sticky="e")
txt_gender = Label(Forms, text="Gender:", font=('arial', 16), bd=15)
txt_gender.grid(row=2, sticky="e")
txt_address = Label(Forms, text="Alamat:", font=('arial', 16), bd=15)
txt_address.grid(row=3, sticky="e")
txt_username = Label(Forms, text="Username:", font=('arial', 16), bd=15)
txt_username.grid(row=4, sticky="e")
txt_password = Label(Forms, text="Password:", font=('arial', 16), bd=15)
txt_password.grid(row=5, sticky="e")
txt_result = Label(Buttons)
txt_result.pack(side=TOP)

#==================================ENTRY WIDGET=======================================
firstname = Entry(Forms, textvariable=FIRSTNAME, width=30)
firstname.grid(row=0, column=1)
lastname = Entry(Forms, textvariable=LASTNAME, width=30)
lastname.grid(row=1, column=1)
RadioGroup.grid(row=2, column=1)
address = Entry(Forms, textvariable=ADDRESS, width=30)
address.grid(row=3, column=1)
username = Entry(Forms, textvariable=USERNAME, width=30)
username.grid(row=4, column=1)
password = Entry(Forms, textvariable=PASSWORD, show="*", width=30)
password.grid(row=5, column=1)

#==================================BUTTONS WIDGET=====================================
btn_create = Button(Buttons, width=10, text="Create", command=Create)
btn_create.pack(side=LEFT)
btn_read = Button(Buttons, width=10, text="Read", command=Read )
btn_read.pack(side=LEFT)
btn_update = Button(Buttons, width=10, text="Update", command=Update, state=DISABLED)
btn_update.pack(side=LEFT)
btn_delete = Button(Buttons, width=10, text="Delete", command=Delete)
btn_delete.pack(side=LEFT)
btn_exit = Button(Buttons, width=10, text="Exit", command=Exit)
btn_exit.pack(side=LEFT)

#==================================LIST WIDGET========================================
scrollbary = Scrollbar(Right, orient=VERTICAL)
scrollbarx = Scrollbar(Right, orient=HORIZONTAL)
tree = ttk.Treeview(Right, columns=("MemberID", "Firstname", "Lastname", "Gender", "Address", "Username", "Password"), selectmode="extended", height=500, yscrollcommand=scrollbary.set, xscrollcommand=scrollbarx.set)
scrollbary.config(command=tree.yview)
scrollbary.pack(side=RIGHT, fill=Y)
scrollbarx.config(command=tree.xview)
scrollbarx.pack(side=BOTTOM, fill=X)
tree.heading('MemberID', text="MemberID", anchor=W)
tree.heading('Firstname', text="Nama depan", anchor=W)
tree.heading('Lastname', text="Nama belakang", anchor=W)
tree.heading('Gender', text="Gender", anchor=W)
tree.heading('Address', text="Alamat", anchor=W)
tree.heading('Username', text="Username", anchor=W)
tree.heading('Password', text="Password", anchor=W)
tree.column('#0', stretch=NO, minwidth=0, width=0)
tree.column('#1', stretch=NO, minwidth=0, width=0)
tree.column('#2', stretch=NO, minwidth=0, width=120)
tree.column('#3', stretch=NO, minwidth=0, width=120)
tree.column('#4', stretch=NO, minwidth=0, width=80)
tree.column('#5', stretch=NO, minwidth=0, width=200)
tree.column('#6', stretch=NO, minwidth=0, width=120)
tree.column('#7', stretch=NO, minwidth=0, width=120)
tree.pack()
tree.bind('<Double-Button-1>', OnSelected)

#==================================INITIALIZATION=====================================
if __name__ == '__main__':
    Read()
    root.mainloop()
