from controllers.Controller import Controller
from views.view import View
from models.points import Point
from models.Video import Video
from models.fileRepo import FileRepo
import tkinter as tk
import sys
from tkinter import messagebox 


class Application(tk.Tk):

    def __init__(self):
        
        super().__init__()
        self["bg"]="linen"
        view = View(self)
        
        # create a video model
        video = Video(self)
        # create a view and place it on the root window
        controller = Controller(video, view,Point,FileRepo())
        view.menufichier.add_command(label = "Quitter",command = self.quitter)
        
        
        view.setController(controller)
        
        
    def quitter(self):
        if messagebox.askyesno('App','Are you sure you want to quit?'):
                self.destroy()
                sys.exit     
    

        
        
        

        
    
       

if __name__ == '__main__':
    app = Application()
    app.mainloop()
    
