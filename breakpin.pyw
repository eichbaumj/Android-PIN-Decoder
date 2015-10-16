#test data
#salt_dec = 4670701647374984108
#contents = "c58823e2bc182759448f8a4fb56401c8e1d651d7e86c51e67038727a27be71067ea376dc"

from tkinter import *
import tkinter.messagebox
from tkinter.filedialog import askopenfilename
import struct
import hashlib
import sqlite3

version = "1.0"

global passwordKey
global settingsDB

def getPasswordFile():
    global passwordKey
    fname = askopenfilename(filetypes=(("key files", "*.key"), ("All files", "*.*")))
    if fname:
        f = open(fname, 'rt')
        passwordKey = f.read()
        f.close()
        passcontent.set(passwordKey)
        return

def getSettingsFile():
    global settingsDB
    fname = askopenfilename(filetypes=(("databases", "*.db"), ("All files", "*.*")))
    if fname:
        conn = sqlite3.connect(fname)
        c = conn.cursor()
        c.execute('select name, value from secure')
        for row in c:
            if row[0] == "lockscreen.password_salt":
                settingsDB = row[1]
        conn.close()
        dbcontent.set(settingsDB)
        return
        
def decode_pin():
    global settingsDB
    global passwordKey
    try:
        salt_hex = hex(int(settingsDB)).split('x')[1]
        for i in range(10000):
            password = ("{0:04}".format(i)+salt_hex)
            sha1 = hashlib.sha1(bytes(password, 'UTF-8')).hexdigest()
            md5 = hashlib.md5(bytes(password, 'UTF-8')).hexdigest()
            if passwordKey.lower() == sha1+md5:
                pin.set(i)
                break
    except:
        return

def aboutMe():
    tkinter.messagebox.showinfo(title="About", message=("Android PIN Breaker " + version +  "\nBy James Eichbaum\nCopyright 2015"))
    return

app = Tk()
app.title("Android PIN Breaker")
width = app.winfo_screenwidth()
height = app.winfo_screenheight()
app.geometry('{}x{}+{}+{}'.format(610,200,int(width/2)-200,int(height/2)-125))

#Menu Bar
menubar = Menu(app)

#File Menu
filemenu = Menu(menubar,tearoff=0)
filemenu.add_command(label = "Quit", command=app.quit)
menubar.add_cascade(label = "File", menu=filemenu)

#Help Menu
helpmenu = Menu(menubar, tearoff=0)
helpmenu.add_cascade(label="About", command=aboutMe)
menubar.add_cascade(label="Help", menu=helpmenu)

app.config(menu=menubar)

#Open pattern.key Button
patternbutton = Button(app, text = "Select password.key", command = getPasswordFile, width = 15)
patternbutton.place(x=15,y=20)

#Label: Password.key label:
passlabel = StringVar()
passlabel.set("hash:")
label01 = Label(app,textvariable=passlabel, height = 2)
label01.place(x=130,y=15)

#Label: Password.key Contents:
passcontent = StringVar()
passcontent.set("")
label02 = Label(app,textvariable=passcontent, height = 2, fg = "blue")
label02.place(x=160,y=15)

#Open pattern.key Button
settingsbutton = Button(app, text = "Select settings.db", command = getSettingsFile, width = 15)
settingsbutton.place(x=15,y=50)

#Label: Settings.db label:
settingslabel = StringVar()
settingslabel.set("salt:")
label03 = Label(app,textvariable=settingslabel, height = 2)
label03.place(x=130,y=45)

#Label: Settings.db Contents:
dbcontent = StringVar()
dbcontent.set("")
label04 = Label(app,textvariable=dbcontent, height = 2, fg = "blue")
label04.place(x=160,y=45)

#Open Decode Button
decodebutton = Button(app, text = "Decode", command = decode_pin, width = 15)
decodebutton.place(x=250,y=100)

#Label: Result label:
resultlabel = StringVar()
resultlabel.set("PIN:")
label05 = Label(app,textvariable=resultlabel, height = 2)
label05.place(x=275,y=130)

#Label: Settings.db Contents:
pin = StringVar()
pin.set("")
label06 = Label(app,textvariable=pin, height = 2, fg = "red")
label06.place(x=300,y=130)





app.mainloop()

