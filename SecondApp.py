import json
import sys
import webbrowser
import tkinter as tk
import cryptography
from tkinter import *
from cryptography.fernet import Fernet
import os


fpath_data = os.path.realpath('test2.enc')
fpath_key = os.path.realpath('key.key')
fpath_data = fpath_data.replace('\'','\\\'')
fpath_key = fpath_key.replace('\'','\\\'')


# Global variable to determine if a new entry is done or it is an update to existing record.
newEntry = False
position = 0

# Get the key to decript/encript the data file.
# file = open('key.key', 'rb')
# key = file.read()
# file.close()
key = "Wx7d51FG-wWn1v3z7t-zXgHS8t5erXgdVT0IWLzzb_w="

##################### DECRIPTION METHOD ###########################
## Read file in binary. 
with open("c:\\workarea\\python\\passwords\\test2.enc", 'rb') as f:
    bindata = f.read()

# with open(fpath_data, 'rb') as f:
#      bindata = f.read()


## Decript the binary data from file.
encryptor = Fernet(key)
decrypted = encryptor.decrypt(bindata)

## Decode the binary into text strings and then load using json format.
decrypted = decrypted.decode('utf-8') 
data = json.loads(decrypted)
##################### END DECRIPTION METHOD ########################

# Instantiate the Tk class and user interface window.
window = tk.Tk(screenName = "My Passwords", className = 'Passwords')
window.title("Password Dictionary")
window.geometry('350x450')

frame = tk.Frame(window)
frame.place(relx=0.5, rely=0.5, anchor=CENTER)

tk.Label(frame, text='SITE INFORMATION', font=('Arial Bold', 12))\
    .grid(row=0, column=0, columnspan=2)

List_label = tk.Label(frame, text="Sites").grid(row=1, column=0)

scrollbar = Scrollbar(frame)
scrollbar.grid(row=1, column=2, rowspan=1, sticky=N+S)

listbox = tk.Listbox(frame, width=30, height=10, yscrollcommand=scrollbar.set)
listbox.grid(row=1, column=1, sticky=W, pady=20)
scrollbar.config(command=listbox.yview)

# Sort the data list before loading into the listbox
sorted_data = sorted(data['Sites'], key=lambda x: next(iter(x.values())))

#Load vendor list in text field
#for indx in range(0,len(data['Sites'])):
#    listbox.insert(indx, data['Sites'][indx]['name'])

for indx in range(0,len(sorted_data)):
    listbox.insert(indx, sorted_data[indx]['name'])

# Define the labels and entry fields
label = tk.Label(frame, text="Site Name").grid(row=3, column=0)
entry = tk.Entry(frame, width=30)
label_1 = tk.Label(frame, text="username").grid(row=4, column=0)
entry_1 = tk.Entry(frame, width=30)
label_2 = tk.Label(frame, text="password").grid(row=5, column=0)
entry_2 = tk.Entry(frame, width=30)
label_3 = tk.Label(frame, text="website").grid(row=6, column=0)
entry_3 = tk.Entry(frame, width=30)
label_4 = tk.Label(frame, text="").grid(row=7, column=0)
Label_5 = tk.Label(frame, text="User Message").grid(row=9, column=0, pady=10)
entry_5 = tk.Entry(frame, width=30)

# Initialize with first item and Position the labels and entry fields in the grid
entry.grid(row=3, column=1)
entry.insert(0,sorted_data[0]["name"])
entry_1.grid(row=4, column=1)
entry_1.insert(0,sorted_data[0]["username"])
entry_2.grid(row=5, column=1)
entry_2.insert(0,sorted_data[0]["password"])
entry_3.grid(row=6, column=1)
entry_3.insert(0,sorted_data[0]["website"])
entry_5.grid(row=9, column=1)
entry_5.insert(0,"")

# Place cursor selection on first item
listbox.selection_set(position, last=position)
entry_5.delete(0, END)
entry_5.insert(0, "Double click to select site")

# Get new site information, delete field data and load selection.
def getSite():
    global position

    position = int(listbox.curselection()[0])
    entry.delete(0, END)
    entry_1.delete(0, END)
    entry_2.delete(0, END)
    entry_3.delete(0, END)
    entry.insert(0,sorted_data[position]["name"]) 
    entry_1.insert(0, sorted_data[position]["username"])
    entry_2.insert(0, sorted_data[position]["password"])
    entry_3.insert(0, sorted_data[position]["website"])
    

# Delete the site from dictionary, position the list pointer to the top and get site. Update file.
def delete():
    global position 

    position = int(listbox.curselection()[0]) 
    listbox.delete(position, last=position)
    sorted_data.remove(sorted_data[position])
    position = position - 1
    listbox.select_set(listbox.index(ACTIVE))
    getSite()
    newEntry = False

# create data dictionary to put in file
    data = {"Sites":sorted_data}

########################### ENCRIPT METHOD
    #Convert dictionary into strings with dumps and then encode string to binary with encode.
    bindata = json.dumps(data).encode('utf-8')
    encrypted = encryptor.encrypt(bindata)

    #Write the encrypted data into the file.
    with open("c:\\workarea\\python\\passwords\\test2.enc",'wb') as f:
        f.write(encrypted)
############################ END OF DECRIPTION METHOD

# Save and edit or a new entry. If new entry create a dict with new site and insert into data dict
# if an edit update data dict and in both cases update the list. Udpate the file
def save():
    global newEntry, position

    if newEntry: 
        # Make sure that the name is not empty and does not exist already in the list of Sites.
        n = entry.get()
        if n == '':
            entry_5.delete(0, END)
            entry_5.insert(0, "Empty Name- No entry made")
        else:
            for indx in range (0,len(sorted_data)):
                if n in sorted_data[indx].values(): 
                    entry_5.delete(0, END)
                    entry_5.insert(0, "Name in Sites rename SAVE again")
                    return
            listbox.selection_clear(0, last=position)
            record = {"name": entry.get(), "username": entry_1.get() , "password": entry_2.get(), "website": entry_3.get()}
            sorted_data.append(record)
            newpos = len(sorted_data)-1
            listbox.insert(newpos, sorted_data[newpos]['name'])
            position = newpos
            entry_5.delete(0, END)
            newEntry = False
    else :
        sorted_data[position]["name"] = entry.get()
        sorted_data[position]['username'] = entry_1.get()
        sorted_data[position]['password'] = entry_2.get()
        sorted_data[position]['website'] = entry_3.get()
        listbox.delete(position)
        listbox.insert(position, sorted_data[position]['name'])
    
    listbox.selection_set(position, last=position)
    listbox.yview_moveto(position)

# create data dictionary to put in file
    data = {"Sites":sorted_data}

# This code to be un-commented and used to create a 
# json backup fileonce in a while using the save button
#    with open("information.json", 'w') as f:
#        json.dump(data, f, indent=2)

############################## ENCRIPTION METHOD
    #Convert dictionary into strings with dumps and then encode string to binary with encode.
    bindata = json.dumps(data).encode('utf-8')
    encrypted = encryptor.encrypt(bindata)

    #Write the encrypted data into the file.
    with open("c:\\workarea\\python\\passwords\\test2.enc",'wb') as f:
        f.write(encrypted)
############################### END OF ENCRIPTION METHOD

# New record entry, delete field and set flag for save.
def new():
    global newEntry, position

    position = len(sorted_data)-1

    entry.delete(0, END)
    entry_1.delete(0, END)
    entry_2.delete(0, END)
    
    newEntry = True

    entry_5.insert(0, "Press SAVE when done")


# Event handler for listbox double click. This action updates site information on user output.
def list_clicked(event):
    getSite()
    #webbrowser.open("www.google.com")

# Bind the listox events to list_clicked.
#listbox.bind('<<ListboxSelect>>', list_clicked)
listbox.bind('<Double-Button-1>', list_clicked)

button_delete = tk.Button(frame, text="DELETE", command=delete)
button_delete.grid(row=8, column=1, sticky=W)

button_save = tk.Button(frame, text=" SAVE ", command=save)
button_save.grid(row=8, column=1)

button_new = tk.Button(frame, text=" NEW ", command=new)
button_new.grid(row=8, column=1, sticky=E)

window.mainloop()
