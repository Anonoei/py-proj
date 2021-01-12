# =======================================================
# =                                                     =
# =     MMM    M   M        MMM    MM    M       MMM    =
# =     M  M    M M        M      M  M   M      M       =
# =     MMM      M         M      MMMM   M      M       =
# =     M        M     X    MMM   M  M   MMMM    MMM    =
# =                                                     =    
# =======================================================
# Author: Devon Adams (https://github.com/devonadams)
# License: GPLv3
# This is a python graphical calculator
#!/usr/bin python

from tkinter import Tk, Label, Button

class MyFirtGUI:
    def __init__(self, master):
        self.master = master
        master.title("PyCalc.py")

        self.label = Label(master, text="This is my first py GUI")
        self.label.pack()

        self.greet_button = Button(master, text="Greet", command=self.greet)
        self.greet_button.pack()

        self.close_button = Button(master, text="Close", command=master.quit)
        self.close_button.pack()

    def greet(self):
        print("Greetings!")

rook = Tk()
my_gui = MyFirstGUI(root)
root.mainloop()
