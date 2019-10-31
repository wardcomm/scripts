import os
import tkinter as tk

root= tk.Tk()
root.title("pip2 and pip3 upgrade utility")
canvas1 = tk.Canvas(root, width = 300, height = 350, bg = 'lightsteelblue2', relief = 'raised')
canvas1.pack()

label1 = tk.Label(root, text='Upgrade PIP2', bg = 'lightsteelblue2')
label1.config(font=('helvetica', 15))
canvas1.create_window(150, 50, window=label1)

label2 = tk.Label(root, text='Upgrade PIP3', bg = 'lightsteelblue1')
label2.config(font=('helvetica', 15))
canvas1.create_window(150, 125, window=label2)

def upgradePIP ():
    os.system('start cmd /k python.exe -m pip install --upgrade pip') 

def upgradePIP3 ():
    os.chdir('c:\Python36\Scripts')
    os.system('start cmd /k pip install --upgrade pip setuptools wheel')
       
button1 = tk.Button(text='      Upgrade PIP     ', command=upgradePIP, bg='green', fg='white', font=('helvetica', 12, 'bold'))
button2 = tk.Button(text='      Upgrade PIP3     ', command=upgradePIP3, bg='blue', fg='white', font=('helvetica', 12, 'bold'))
canvas1.create_window(150, 80, window=button1)
canvas1.create_window(150, 180, window=button2)




root.mainloop()