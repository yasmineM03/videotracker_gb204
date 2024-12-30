
from tkinter import *
import sys

class View(Frame):
    def __init__(self, parent):
        self.parent = parent
        
        




        self.parent.title('Video Tracker')
        
        menubar = Menu(self.parent)
        self.parent.config(menu=menubar)
        self.menufichier = Menu(menubar,tearoff=0)
        self.menuview = Menu(menubar,tearoff=0)
        self.menuechelle = Menu(menubar,tearoff=0)
        self.menupointage = Menu(menubar,tearoff=0)
        menubar.add_cascade(label="Fichier", menu=self.menufichier)
        menubar.add_cascade(label="Echelle",menu = self.menuechelle)
        

        menubar.add_cascade(label="View",menu = self.menuview)
        menubar.add_cascade(label="Pointage",menu = self.menupointage)

        
    
        self.pause_btn = Button(self.parent,text ='▶',width = "20",height="3",font="50")
        self.pause_btn.pack(side=BOTTOM, padx=20, pady=20)
        self.next_frame_btn= Button(self.parent, text = "⏩", width = "20",height="3",font="50")
        self.next_frame_btn.pack(side=BOTTOM, padx=20, pady=20)
        self.first_frame_btn= Button(self.parent, text = "⏮", width = "20",height="3",font="50")
        self.first_frame_btn.pack(side=TOP, padx=20, pady=20)

    
        
        

        
    
    def setController(self, controller):
        self.controller = controller

    
