#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb 10 16:45:12 2022

@author: ymaabout
"""

class FileRepo:
    
    def exportDataString(self,Ltimes,Lpoints,delim): 
        string = ""
        for i in range (len(Ltimes)):
            string = string  + str(Ltimes[i]) + delim + str(Lpoints[i].getX()) + delim + str(Lpoints[i].getY())+"\n"
        return string
    
    def exportDataToCsv(self,filename,Ltimes,Lpoints,delim):
         nom = ""
         nom = filename + ".csv"
         try:
         
             with open(nom, 'w') as f:
                    try:
                        f.write("t;x;y\n")
                        f.write(self.exportDataString(Ltimes,Lpoints,delim))
                    except :
                        print("ne peut pas écrire dans le fichier")
                
         except :
          print("ne peut pas ouvrir/créer le fichier")
        
    
            