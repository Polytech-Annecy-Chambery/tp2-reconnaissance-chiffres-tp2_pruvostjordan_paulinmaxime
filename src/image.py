from skimage import io
from skimage.transform import resize
import matplotlib.pyplot as plt
import numpy as np

class Image:
    def __init__(self):
        """Initialisation d'une image composee d'un tableau numpy 2D vide
        (pixels) et de 2 dimensions (H = height et W = width) mises a 0
        """
        self.pixels = None
        self.H = 0
        self.W = 0
    

    def set_pixels(self, tab_pixels):
        """ Remplissage du tableau pixels de l'image self avec un tableau 2D (tab_pixels)
        et affectation des dimensions de l'image self avec les dimensions 
        du tableau 2D (tab_pixels) 
        """
        self.pixels = tab_pixels
        self.H, self.W = self.pixels.shape


    def load(self, file_name):
        """ Lecture d'un image a partir d'un fichier de nom "file_name"""
        self.pixels = io.imread(file_name)
        self.H,self.W = self.pixels.shape 
        print("lecture image : " + file_name + " (" + str(self.H) + "x" + str(self.W) + ")")


    def display(self, window_name):
        """Affichage a l'ecran d'une image"""
        fig = plt.figure(window_name)
        if (not (self.pixels is None)):
            io.imshow(self.pixels)
            io.show()
        else:
            print("L'image est vide. Rien à afficher")


    #==============================================================================
    # Methode de binarisation
    # 2 parametres :
    #   self : l'image a binariser
    #   S : le seuil de binarisation
    #   on retourne une nouvelle image binarisee
    #==============================================================================
    def binarisation(self, S):
        im_bin = Image()
        
        # affectation a l'image im_bin d'un tableau de pixels de meme taille
        # que self dont les intensites, de type uint8 (8bits non signes),
        # sont mises a 0
        im_bin.set_pixels(np.zeros((self.H, self.W), dtype=np.uint8))
        for y in range(0,self.H):
            for x in range(0,self.W):
                if self.pixels[y][x] > S: im_bin.pixels[y][x] = 255
                else : im_bin.pixels[y][x] = 0
        return im_bin
        # TODO: boucle imbriquees pour parcourir tous les pixels de l'image im_bin
        # et calculer l'image binaire
        
        
        return im_bin    



    #==============================================================================
    # Dans une image binaire contenant une forme noire sur un fond blanc
    # la methode 'localisation' permet de limiter l'image au rectangle englobant
    # la forme noire
    # 1 parametre :
    #   self : l'image binaire que l'on veut recadrer
    #   on retourne une nouvelle image recadree
    #==============================================================================
    def localisation(self):
        res = Image()
        k=0
        presence = False
        haut, bas, gauche, droite = -1,-1,-1,-1
        while presence == False and k < self.H and haut == -1: # on a pas trouvé le haut 
            presence = False
            for l in range (0, self.W):
                if self.pixels[k][l] == 0:
                    presence = True
            if presence == True:
                haut = k
            k+=1

        k = self.H - 1
        presence = False
        
        while presence == False and k >= 0 and bas == -1:# on a pas trouvé le bas 
            presence = False
            for l in range (0, self.W):
                if self.pixels[k][l] == 0:
                    presence = True
            if presence == True:
                bas = k + 1
            k-=1

                
        k = 0 # on check G 
        presence = False

        while presence == False and k < self.W and gauche == -1: # on a pas trouvé la gauche  
            presence = False
            for l in range (0, self.H):
                if self.pixels[l][k] == 0:
                    presence = True
            if presence == True:
                gauche = k
            k+=1

        k = self.W - 1 # on check D 
        presence = False

        while presence == False and k >= 0 and droite == -1: # on a pas trouvé la droite
            presence = False
            for l in range (0, self.H):
                if self.pixels[l][k] == 0:
                    presence = True
            if presence == True:
                droite = k
            k-=1
            
        res.set_pixels(np.array(self.pixels[haut:bas,gauche:droite], dtype=np.uint8))
        return res
        

    #==============================================================================
    # Methode de redimensionnement d'image
    #==============================================================================
    def resize(self, new_H, new_W):
        self.H = new_H
        self.W = new_W
        self.pixels = np.uint8(resize(self.pixels, (new_H, new_W), 0))
        return self


    #==============================================================================
    # Methode de mesure de similitude entre l'image self et un modele im
    #==============================================================================
    def similitude(self, im):
        res = Image()
        res.set_pixels(np.zeros((self.H, self.W), dtype=np.uint8))
        count = 0
        for k in range(0,self.H):
            for l in range(0,self.W):
                if im.pixels[k][l] == self.pixels[k][l]:
                    count+=1
        count = count / ((self.H)*(self.W))
        return count