import unittest
import filecmp
import sys
sys.path.append("../")
from src.models.fileRepo import FileRepo
from src.models.points import Point
from src.models.Video import Video

class testFileRepo(unittest.TestCase):
    def setUp(self) -> None:
        self.listePoints = [Point(2,8),Point(6,7)]
        self.listeTemps = [2,3]            
        
        
    
    def tearDown(self):
        pass
    
    def test_isString(self):
        self.h = FileRepo()
        self.chaine = self.h.exportDataString(self.listeTemps,self.listePoints,",")
        self.assertTrue(type(self.chaine) is str)
    
    def test_sameLength(self):
        self.assertTrue(len(self.listePoints) is len(self.listeTemps))
    
    def test_convertStr(self):
        v = FileRepo()
        chaine = "2,2,8\n3,6,7\n"
        chaine1 = v.exportDataString(self.listeTemps,self.listePoints,",")
        self.assertTrue(chaine1 == chaine)
    
    def test_convertCsv(self):
        v = FileRepo()
        v.exportDataToCsv("test1",self.listeTemps,self.listePoints,";")
        result = filecmp.cmp("test.csv", "test1.csv")  #test.csv a été crée manuellement 
        self.assertTrue(result)
    
class testVideo(unittest.TestCase):
    def setup(self):
        self.__video = Video
        self.pause = Video.pause
        self.filename = Video.filename 
        
    def test_pause(self):
        self.pause = True
        Video.pause(self)
        self.assertTrue(self.pause == False)
    
    """def test_getFrameFalse(self):
        r = Video.get_frame(self) #si il n'y a pas de vidéo sélectionnée
        self.assertFalse(r)"""   # Ne marche pas avec intégration continue mais run sans erreur sur spyder/vscode
        

    

        
        




        
        
        
        
        
        
    
        
        
        
        
        
        
if __name__ == '__main__':
    unittest.main(verbosity=2)
