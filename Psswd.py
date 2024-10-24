import json
import sys
import webbrowser
import tkinter as tk
import cryptography
from tkinter import *
from cryptography.fernet import Fernet
import os


fpath_data = os.path.realpath('./test3.enc')
fpath_key = os.path.realpath('./key.key')

# Global variable to determine if a new entry is done or it is an update to existing record.
newEntry = False
position = 0
Focused = False

# Get the key to decript/encript the data file.
file = open(fpath_key, 'rb')
key = file.read()
file.close()
#key = "Wx7d51FG-wWn1v3z7t-zXgHS8t5erXgdVT0IWLzzb_w="

##################### DECRIPTION METHOD ###########################
## Read file in binary. 
#with open("c:\\workarea\\python\\passwords\\test3.enc", 'rb') as f:
#    bindata = f.read()

with open(fpath_data, 'rb') as f:
    bindata = f.read()

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
window.geometry('350x500')

frame = tk.Frame(window)
frame.place(relx=0.5, rely=0.5, anchor=CENTER)

tk.Label(frame, text='SITE INFORMATION', font=('Arial Bold', 12))\
    .grid(row=0, column=0, columnspan=2)

List_label = tk.Label(frame, text="Sites").grid(row=1, column=0)

scrollbar = Scrollbar(frame)
scrollbar.grid(row=1, column=2, rowspan=1, sticky=N+S)

listbox = tk.Listbox(frame, width=30, height=10, yscrollcommand=scrollbar.set, selectmode=SINGLE)
listbox.grid(row=1, column=1, sticky=W, pady=20)
scrollbar.config(command=listbox.yview)

# Sort the data list before loading into the listbox
sorted_data = sorted(data['Sites'], key=lambda x: next(iter(x.values())))

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
label_4 = tk.Label(frame, text="notes").grid(row=7, column=0)
entry_4 = tk.Text(frame,  width=30, height=5, font=("Arial", 8))
label_5 = tk.Label(frame, text="").grid(row=8, column=0)
Label_6 = tk.Label(frame, text="User Message").grid(row=10, column=0, pady=10)
entry_6 = tk.Entry(frame, width=30)

# Initialize with first item and Position the labels and entry fields in the grid
entry.grid(row=3, column=1)
entry.insert(0,sorted_data[0]["name"])
entry_1.grid(row=4, column=1)
entry_1.insert(0,sorted_data[0]["username"])
entry_2.grid(row=5, column=1)
entry_2.insert(0,sorted_data[0]["password"])
entry_3.grid(row=6, column=1)
entry_3.insert(0,sorted_data[0]["website"])
entry_4.grid(row=7, column=1)
entry_4.insert('1.0',sorted_data[0]["notes"])
entry_6.grid(row=10, column=1)
entry_6.insert(0,"")

# Place cursor selection on first item
listbox.selection_set(position)

entry_6.delete(0, END)
entry_6.insert(0, "Double click to select site")

# Get new site information, delete field data and load selection.
def getSite():
    global position

    position = int(listbox.curselection()[0])

    entry.delete(0, END)
    entry_1.delete(0, END)
    entry_2.delete(0, END)
    entry_3.delete(0, END)
    entry_4.delete('1.0', END)
    entry.insert(0,sorted_data[position]["name"]) 
    entry_1.insert(0, sorted_data[position]["username"])
    entry_2.insert(0, sorted_data[position]["password"])
    entry_3.insert(0, sorted_data[position]["website"])
    entry_4.insert('1.0', sorted_data[position]["notes"])

# Delete the site from dictionary, position the list pointer to the top and get site. Update file.
def delete():
    global position, Focused 

    if Focused == False : return

    # Avoid Focusing a site and then clicking on another site before pressing DELETE
    curr_position = int(listbox.curselection()[0])
    if curr_position != position:
        entry_6.delete(0, END)
        entry_6.insert(0, "Double click to select site")
        return

    position = int(listbox.curselection()[0]) 
    listbox.delete(position, last=position)
    sorted_data.remove(sorted_data[position])
    position = position - 1
    listbox.select_set(listbox.index(ACTIVE))
    getSite()
    newEntry = False
    Focused = False

    entry_6.delete(0, END)
    entry_6.insert(0, "Double click to select site")

# create data dictionary to put in file
    data = {"Sites":sorted_data}

########################### ENCRIPT METHOD
    #Convert dictionary into strings with dumps and then encode string to binary with encode.
    bindata = json.dumps(data).encode('utf-8')
    encrypted = encryptor.encrypt(bindata)

    #Write the encrypted data into the file.
    #with open("c:\\workarea\\python\\passwords\\test3.enc",'wb') as f:
    #    f.write(encrypted)

    with open(fpath_data,'wb') as f:
        f.write(encrypted)
############################ END OF DECRIPTION METHOD

# Save and edit or a new entry. If new entry create a dict with new site and insert into data dict
# if an edit update data dict and in both cases update the list. Udpate the file
def save():
    global newEntry, position, Focused

    # Focused means that the selected record was double clicked, not just clicked once.
    if Focused == False : return

    # Avoid Focusing a site and then clicking on another site before pressing SAVE
    curr_position = int(listbox.curselection()[0])
    if curr_position != position:
        entry_6.delete(0, END)
        entry_6.insert(0, "Double click to select site")
        return

    # Make sure that the name is not empty. If so, signal the user and return.
    n = entry.get()
    if n == '':
        entry_6.delete(0, END)
        entry_6.insert(0, "Empty Name. Re-enter Name")
        return

    if newEntry: 
    # Make sure Name is not already in the sorted data set. If so, signal the user to enter new name and exit.
        for indx in range (0,len(sorted_data)):
            if n in sorted_data[indx].values(): 
                entry_6.delete(0, END)
                entry_6.insert(0, "Repeated Name. Re-enter Name")
                return
        # The name is not repeated so enter the new record in the sorted data list.
        record = {"name": entry.get(), "username": entry_1.get() , "password": entry_2.get(), "website": entry_3.get(), "notes": entry_4.get("1.0","end")}
        sorted_data.append(record)
        
        # Now sort the records before displaying in the listbox
        new_sorted_data = sorted(sorted_data, key=lambda x: next(iter(x.values())))
        listbox.delete(0, END)
        for indx in range(0,len(new_sorted_data)):
            listbox.insert(indx, new_sorted_data[indx]['name'])
        
        # Redefine the sorted_data list now newly sorted
        sorted_data.clear()
        for indx in range (0,len(new_sorted_data)):
            sorted_data.append(new_sorted_data[indx])
        
        # Figure out the position of th enew entry
        for indx in range (0,len(sorted_data)):
            if n in sorted_data[indx].values(): 
                position = indx
                break
        
        # Set variables to correct values.
        newEntry = False
    else :
        # Save entry into an existing data record and refresh the listbox by inserting updated record.
        sorted_data[position]["name"] = entry.get()
        sorted_data[position]['username'] = entry_1.get()
        sorted_data[position]['password'] = entry_2.get()
        sorted_data[position]['website'] = entry_3.get()
        sorted_data[position]['notes'] = entry_4.get("1.0","end")
        listbox.delete(position)
        listbox.insert(position, sorted_data[position]['name'])
    
    Focused = False

    # Ensure the list cursor stays in selected record.
    listbox.selection_set(position)
    listbox.see(position)


# create data dictionary to put in file
    data = {"Sites":sorted_data}

# reset the user message text for selection to new site 
    entry_6.delete(0, END)
    entry_6.insert(0, "Double click to select site")

# This code to be un-commented and used to create a 
# json backup file once in a while using the save button
    with open("./information.json", 'w') as f:
        json.dump(data, f, indent=2)

############################## ENCRIPTION METHOD
    #Convert dictionary into strings with dumps and then encode string to binary with encode.
    bindata = json.dumps(data).encode('utf-8')
    encrypted = encryptor.encrypt(bindata)

    #Write the encrypted data into the file.
    #with open("c:\\workarea\\python\\passwords\\test3.enc",'wb') as f:
    #    f.write(encrypted)

    with open(fpath_data,'wb') as f:
        f.write(encrypted)
############################### END OF ENCRIPTION METHOD

# New record entry, delete data fields and set flag for save.
def new():
    global newEntry, position, Focused

    #position = len(sorted_data)-1

    Focused = True

    entry.delete(0, END)
    entry_1.delete(0, END)
    entry_2.delete(0, END)
    entry_3.delete(0, END)
    entry_4.delete('1.0', END)

    newEntry = True
    
    entry_6.delete(0, END)
    entry_6.insert(0, "Press SAVE to save changes")


# Event handler for listbox double click. This action updates site information on user output.
def list_clicked(event):
    
    global Focused

    Focused = True

    entry_6.delete(0, END)
    entry_6.insert(0, "Click SAVE to save changes.")

    getSite()




# Bind the listox events to list_clicked.
listbox.bind('<Double-Button-1>', list_clicked)

button_delete = tk.Button(frame, text="DELETE", command=delete)
button_delete.grid(row=8, column=1, sticky=W)

button_save = tk.Button(frame, text=" SAVE ", command=save)
button_save.grid(row=8, column=1)

button_new = tk.Button(frame, text=" NEW ", command=new)
button_new.grid(row=8, column=1, sticky=E)

window.mainloop()

# Update the JSON file to show last modifications.
with open("./information.json", 'w') as f:
    json.dump(data, f, indent=2)
