from tkinter import *
from tkinter import messagebox
import PIL.Image, PIL.ImageTk
import cv2
from tkinter import filedialog

class Video:
    
    def __init__(self, parent):
        self.height=None
        self.cap=None
        self.image=None
        self.width=None
        self.parent=parent
        self.window = self.parent
        self.window.attributes('-fullscreen',True)

        #get the dimension of the screen
        screen_width = self.window.winfo_screenwidth()
        screen_height = self.window.winfo_screenheight()
        self.canvas = Canvas(self.parent,height=screen_height,width=screen_width)
        self.canvas['bg'] = 'linen'
        self.canvas.pack()
        self.delay = 20
        self.filename = None  # ms
        

      
   

    # get only one frame    #models
    def get_frame(self):   
        try:
            if self.cap.isOpened():
                ret, frame = self.cap.read()
                return (ret, cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        except:
            messagebox.showerror('Alert','End of the video.')
        
     
    def open_vid(self):
        if not self.filename:
            return
        self.pause = True
        self.cap = cv2.VideoCapture(self.filename)
        self.width = self.cap.get(cv2.CAP_PROP_FRAME_WIDTH)
        self.height = self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
        self.canvas.config(width = self.width, height = self.height)
        self.play_video()

    def play_video(self):
        if not self.filename:
            messagebox.showinfo("Erreur","Pas de vidéo selectionnée")
            return
        ret, frame = self.get_frame()
        if ret:
            self.photo = PIL.ImageTk.PhotoImage(image = PIL.Image.fromarray(frame))
            self.canvas.create_image(0, 0, image = self.photo, anchor = NW)
        if not self.pause:
            self.window.after(self.delay, self.play_video)
    
    def retour_debut(self):
         if not self.filename:
             messagebox.showinfo("Erreur","Pas de vidéo selectionnée")
             return 
         self.cap.set(cv2.CAP_PROP_POS_FRAMES, 0)                                               
         ret, frame = self.get_frame() 
         if ret:   
                self.pause = True                                                                              
                self.photo = PIL.ImageTk.PhotoImage(image = PIL.Image.fromarray(frame))
                self.canvas.create_image(0, 0, image = self.photo, anchor = NW)
        

            
    def ouvrir_fichier(self):
        self.filename = filedialog.askopenfilename(initialdir = "",
                                          title = "Select a File",
                                          filetypes = (("Videofiles",
                                                       "*.mp4*"),
                                                       ("all files",
                                                        "*.*")))
        if self.filename[-3:] != "mp4" and self.filename[-3:] != "avi":
            messagebox.showerror('Alert','Veuillez choisir un format .mp4 ou .avi')
            
        
        else:
            try:
                self.open_vid()  #try et return afin de pouvoir faire les tests unitaires sans avoir de messages d'erreur
            except:
                return 
    
    def pause(self):
        self.pause = not self.pause
        try :
         self.play_video()  #try et return afin de pouvoir faire les tests unitaires sans avoir de messages d'erreur
        except :
            return
        
    
    
    def nextFrame(self):  
        if not self.filename:
            messagebox.showinfo("Erreur","Pas de vidéo selectionnée")
            return
        self.pause=True                                                                         
        if type(self.get_frame())==type(None): 
            return
                                                                                              
        ret, frame = self.get_frame()
        if ret:
            self.photo = PIL.ImageTk.PhotoImage(image = PIL.Image.fromarray(frame))
            self.canvas.create_image(0, 0, image = self.photo, anchor = NW)
            
    
    


        