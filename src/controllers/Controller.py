from tkinter import messagebox
from tkinter import simpledialog
from tkinter.simpledialog import askstring
import csv
import matplotlib.pyplot as plt 
from tkinter import filedialog
import pandas as pd
from tkinter import *
from math import *


class Controller:

    def __init__(self, video, view, point, filerepo):
        
        self.__video = video   
        self.__view = view
        self.point = point
        self.filerepo = filerepo
        self.ratio = 1
        self.name = None
        self.col_list = ['t','x','y']  #initialisation des colonnes 
        self.pointage_mode = False
        self.origine_mode = False   #tous les modes sont false par défaut et les listes vides
        self.echelle_mode = False
        self.listex = []
        self.listey = []
        self.listet = []
        self.temps = 0
        self.xor=0  #origine est par défaut initialisé en haut à gauche
        self.yor=0
        self.state_echelle = 0
        self.x1 = 0
        self.y1 = 0
        

        self.__view.menufichier.add_command(label = "Ouvrir vidéo",command = video.ouvrir_fichier)
        self.__view.menufichier.add_command(label = "Sauvegarder au format csv",command = self.sauvegarder_fichier)
        self.__view.pause_btn.config(command = video.pause)
        self.__view.next_frame_btn.config(command = video.nextFrame)
        self.__view.first_frame_btn.config(command = video.retour_debut)
        self.__view.menuechelle.add_command(label = "Initialiser echelle",command = self.stat_echelle)
        self.__view.menufichier.add_command(label = "Lire vidéo",command = video.pause)
        self.__view.menuview.add_command(label = "Afficher y(x)",command = self.drawGraphYX)
        self.__view.menuview.add_command(label = "Afficher x(t)",command = self.drawGraphXT)
        self.__view.menuview.add_command(label = "Afficher y(t)",command = self.drawGraphYT)
        self.__view.menupointage.add_command(label= "Mode pointage", command = self.pointage)
        self.__view.menuview.add_command(label="Initialiser origine",command = self.origine)
        self.__view.parent.bind("<Button-1>",self.coor_point)  
        self.__view.parent.bind('<Escape>',self.pointage_out)
        self.__view.parent.bind('<Control_L>',self.set_origine)
        self.__view.parent.bind('<Button-3>',self.definir_echelle)
    
    def origine(self):    #fait passer le mode de l'origine à true
        if not self.__video.filename:
            messagebox.showinfo("Erreur","Pas de vidéo selectionnée")
            return
        self.origine_mode = True
    
    def stat_echelle(self):    #fait passer le mode de l'echelle à true
        if not self.__video.filename:
            messagebox.showinfo("Erreur","Pas de vidéo selectionnée")
            return
        self.echelle_mode = True

    
    def definir_echelle(self,event):  #l'utilisateur en est à son premier clic droit, un point apparaît
        if self.echelle_mode == True:
            if self.state_echelle == 0:
                self.x1 = int(event.x)
                self.y1 = int(event.y)
                self.__video.canvas.create_oval(self.x1+3,self.y1+3,self.x1-3,self.y1-3,fill='pink')
                self.state_echelle = 1

                return
            else:
                x2 = int(event.x)   #deuxième clic droit de l'utilisateur 
                y2 = int(event.y)
                self.__video.canvas.create_oval(x2+3,y2+3,x2-3,y2-3,fill='red')
            self.__video.canvas.create_line(self.x1,self.y1,x2,y2,fill='red')  #une ligne se crée 
            reel_distance = sqrt((self.x1-x2)**2+(self.y1-y2)**2)  #calcul de la réelle distance entre les deux points
            fausse_distance = simpledialog.askfloat("Distance","Quelle est la distance?")  #l'utilisateur rentre la distance souhaitée
            self.ratio = fausse_distance/reel_distance  #calcul du rapport fausse distance/vraie
            self.echelle_mode = False  #sort du mode echelle, le clic droit peut être réutilisé sans créer de point
            self.state_echelle== 0

                

    
    def set_origine(self,event):
        if self.origine_mode:
            self.xor = int(event.x)-310 #doit ajouter ces calculs afin que la position prise soit prise par rapport à la window et non au canvas
            self.yor = int(event.y)-100
        self.origine_mode = False
        return self.__video.canvas.create_oval(self.xor+2,self.yor+2,self.xor-2,self.yor-2,fill='red')


    def pointage(self):
        if not self.__video.filename:
            messagebox.showinfo("Erreur","Pas de vidéo selectionnée")
            return
        self.pointage_mode = True  #entrée du mode pointage 
    def pointage_out(self,event): 
        self.pointage_mode = False
        messagebox.showinfo('pointage mode','vous êtes sortis du mode de pointage')
        
    
    def coor_point(self,event):
        if self.pointage_mode :

            
            xb= int(event.x)-self.xor #calcul des coordonnées de chaque point par rapport à l'origine
            yb= self.yor- int(event.y)
            x1 = int(event.x)
            y1 = int(event.y)
            self.listex.append(xb)  #chaque liste est remplie avec les donénes de chaque point
            self.listey.append(yb)
            self.listet.append(self.temps)
            self.temps += 1 #temps va de 1 en 1 par défaut, ne peut être changé
            
            self.__video.nextFrame() #automatiquement à la next frame
            return self.__video.canvas.create_oval(x1+2,y1+2,x1-2,y1-2,fill='blue') #le point est placé où l'on vient de cliquer

    



        
    def sauvegarder_fichier(self):
        if not self.__video.filename : 
            messagebox.showerror("Erreur", "Vidéo non selectionnée")
            return 
        self.name = askstring('App', 'Comment appeler le fichier?')
        liste_save = []
        for i in range(len(self.listey)):
            x = round(self.listex[i]*self.ratio)
            y = round(self.listey[i]*self.ratio)
            liste_save.append(self.point(x,y))
        self.filerepo.exportDataToCsv(self.name,self.listet,liste_save,";")

    
    def read_x_csv(self):
            if self.name == None:
                 return
            
            filename = self.name+".csv"
            valueX=[]
            
            try:
                fichier = pd.read_csv(filename, usecols=self.col_list,sep=';')
                valueX=round((fichier["x"]).multiply(self.ratio))
            except:
                messagebox.showerror("erreur","mauvais noms de colonnes'[t,x,y]'")
                self.name = None
                return
            return valueX

    def read_y_csv(self):
        if self.name == None:
            return
        filename = self.name+".csv"
        valueY=[]
        
        try:
            fichier = pd.read_csv(filename, usecols=self.col_list,sep=';')
            valueY=round((fichier["y"]).multiply(self.ratio))

        except:
                messagebox.showerror("erreur","mauvais noms de colonnes'[t,x,y]'")
                self.name = None
                return
        return valueY
    
    def read_t_csv(self):
        if self.name == None:
                 return
        filename = self.name+".csv"
        valueT=[]
        
        try:
            fichier = pd.read_csv(filename, usecols=self.col_list,sep=';')
            valueT=(fichier["t"])
        except:
                messagebox.showerror("erreur","mauvais noms de colonnes'[t,x,y]'")
                self.name = None
                return
        return valueT
    
    def drawGraphYX(self):
        if self.name == None:  #si pas de fichier selectionné, possibilité d'importer un fichier csv 
                self.name = filedialog.askopenfilename(initialdir = "",
                                          title = "Select a File",
                                          filetypes = (("csvfiles",
                                                       "*.csv*"),
                                                       ("all files",
                                                        "*.*")))
                self.name = self.name[0:-4]
        x=self.read_x_csv()
        y=self.read_y_csv()
        plt.plot(x,y)
        plt.title("Graphique de y(x)")
        plt.xlabel('x')
        plt.ylabel('y')
        plt.grid()
        plt.show()
    
    def drawGraphXT(self):
        if self.name == None:
                self.name = filedialog.askopenfilename(initialdir = "",
                                          title = "Select a File",
                                          filetypes = (("csvfiles",
                                                       "*.csv*"),
                                                       ("all files",
                                                        "*.*")))
                self.name = self.name[0:-4]
        x=self.read_x_csv()
        t=self.read_t_csv()
        plt.plot(t,x)
        plt.title("Graphique de x(t)")
        plt.xlabel('t')
        plt.ylabel('x')
        plt.grid()
        plt.show()
    
    def drawGraphYT(self):
        if self.name == None:
                self.name = filedialog.askopenfilename(initialdir = "",
                                          title = "Select a File",
                                          filetypes = (("csvfiles",
                                                       "*.csv*"),
                                                       ("all files",
                                                        "*.*")))
                self.name = self.name[0:-4]
        y=self.read_y_csv()
        t=self.read_t_csv()
        plt.plot(t,y)
        plt.title("Graphique de y(t)")
        plt.xlabel('t')
        plt.ylabel('y')
        plt.grid()
        plt.show()
    

    


        



            
            
        
        

        
   
    
       
            
            

        

        