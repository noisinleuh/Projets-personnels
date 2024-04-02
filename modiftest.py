import pyxel
from math import sqrt, pi
from random import randint

"""
PROJET PERSONNEL QUE JE CONTINUE LORSQUE J'AI DU TEMPS LIBRE SIMPLEMENT POUR M'AMELIORER EN PROGRAMMATION
"""


pyxel.init(214, 214, title="survie")
pyxel.load("style_.pyxres")


#---------------------Cam---------------------------------

class cam:
    """
    classe de la 'caméra' donc comment va s'afficher mon fond
    """
    def __init__(self):
        """
        variables de la caméra (coordonnées, si il doit bouger le joueur ou non horizontalement et verticalement)
        """
        self.x=3
        self.y=3
        self.bjx=False #bj pour bouge joueur
        self.bjy=False
    
    def depla(self, speed, foret, caillasse, gamer):
        """
        déplace la caméra
        
        Parameters
        ----------
        speed : int
            vitesse de déplacement
        foret : list
            tous les arbres du jeu
        gamer : __main__.gamer
            le joueur

        """
        if pyxel.btn(pyxel.KEY_TAB):
            #accélère le joueur
            speed+=1
        if pyxel.btn(pyxel.KEY_UP) and cam.bjy==False:
            #si on clique sur la fleche du haut et qu'on n'a pas besoin de déplacer le joueur vers le haut
            gamer.in_arbre=False
            #le joueur n'est pas dans un arbre
            if self.y-speed>0:
                #si on ne sort pas du terrain de jeu
                for arbre in foret:
                    if self.y-speed+104+gamer.y-96 in arbre.zoney and self.x+104+gamer.x-96 in arbre.zonex:
                        gamer.in_arbre=True
                for stone in caillasse:
                    if self.y-speed+96+gamer.y-96 in stone.zoney and self.x+104+gamer.x-96 in stone.zonex:
                        gamer.in_arbre=True
                        #si le joueur est dans un arbre on le met dans la variable
                if gamer.in_arbre==False:
                    #sinon on se déplace
                    self.y-=speed
            else:
                #si on sort du terrain on arrete de bouger, on bouge le joueur
                self.bjy=True                
        if pyxel.btn(pyxel.KEY_DOWN) and cam.bjy==False:
            #si on clique sur la fleche du bas et qu'on n'a pas besoin de déplacer le joueur vers le bas
            gamer.in_arbre=False
            if self.y+speed<440 :
                #si on ne sort pas du terrain de jeu
                for arbre in foret:
                    if self.y+speed+104+gamer.y-96 in arbre.zoney and self.x+104+gamer.x-96 in arbre.zonex:
                        gamer.in_arbre=True
                for stone in caillasse:
                    if self.y+speed+112+gamer.y-96 in stone.zoney and self.x+104+gamer.x-96 in stone.zonex:
                        gamer.in_arbre=True
                        #si le joueur est dans un arbre on le met dans la variable
                if gamer.in_arbre==False:
                    #sinon on se déplace
                    self.y+=speed
            else:
                #si on sort du terrain on arrete de bouger, on bouge le joueur
                self.bjy=True  
        if pyxel.btn(pyxel.KEY_LEFT) and cam.bjx==False:
            #si on clique sur la fleche de gauche et qu'on n'a pas besoin de déplacer le joueur vers la gauche
            gamer.in_arbre=False
            if self.x-speed>0:
                #si on ne sort pas du terrain de jeu
                for arbre in foret:
                    if self.x-speed+104+gamer.x-96 in arbre.zonex and self.y+104+gamer.y-96 in arbre.zoney:
                        gamer.in_arbre=True
                for stone in caillasse:
                    if self.x-speed+96+gamer.x-96 in stone.zonex and self.y+104+gamer.y-96 in stone.zoney:
                        gamer.in_arbre=True
                        #si le joueur est dans un arbre on le met dans la variable
                if gamer.in_arbre==False:
                    #sinon on se déplace
                    self.x-=speed
            else :
                #si on sort du terrain on arrete de bouger, on bouge le joueur
                self.bjx=True
        if pyxel.btn(pyxel.KEY_RIGHT) and cam.bjx==False:
            #si on clique sur la fleche de droite et qu'on n'a pas besoin de déplacer le joueur vers la droite
            gamer.in_arbre=False
            if self.x+speed<440:
                #si on ne sort pas du terrain de jeu
                for arbre in foret:
                    if self.x+speed+104+gamer.x-96 in arbre.zonex and self.y+104+gamer.y-96 in arbre.zoney:
                        gamer.in_arbre=True
                for stone in caillasse:
                    if self.x+speed+112+gamer.x-96 in stone.zonex and self.y+104+gamer.y-96 in stone.zoney:
                        gamer.in_arbre=True
                        #si le joueur est dans un arbre on le met dans la variable
                if gamer.in_arbre==False:
                    #sinon on se déplace
                    self.x+=speed
            else :
                #si on sort du terrain on arrete de bouger, on bouge le joueur
                self.bjx=True
                
#---------------------Gamer---------------------------------

class gamer:
    """
    classe du joueur
    """
    def __init__(self):
        """
        initialisation des variables du joueur
        """
        self.x=96
        self.y=96
        self.hp=20 #point de vie
        self.hunger=8 #faim
        self.alive=True
        self.spritew=16 #largeur de l'image (opposée pour retourner l'image horizontalement)
        self.spriteh=16 #hauteur de l'image (opposée pour retourner l'image verticalement)
        self.spritev=0 #coordonée de l'image dans la feuille de style (pour animer le joueur)
        self.inventory={"baies":0, "bois":3, "viande":0, "feu":0, "pierre":2} #inventaire
        self.in_arbre=False #le joueur est il dans un arbre
        self.id='gamer' #identification
        self.inv=['pierre','bois']#liste des objets que détient le joueur dans leur ordre d'acquisition
        self.recettes=[]#liste des recettes que le joueur peut réaliser (ex: pioche, feu de camps etc)
         
    def __repr__(self):
        return f"{self.id},{self.alive},{self.x},{self.y},{self.dirx},{self.diry},{self.hp}"
          
    def bj(self, cam, speed, foret, caillasse):
        """
        bouge le joueur
        """
        if pyxel.btn(pyxel.KEY_TAB):
            speed+=1
            #augmente la vitesse
        if pyxel.btn(pyxel.KEY_UP) and cam.bjy==True:
            #si on clique sur la fleche du haut et qu'on a besoin de déplacer le joueur vers le haut
            self.in_arbre=False
            if self.y-speed>1:
                #si on ne sort pas du cadre
                for arbre in foret:
                    if self.y-speed+cam.y+8 in arbre.zoney and self.x+cam.x+8 in arbre.zonex:
                        self.in_arbre=True
                        #si le joueur est dans un arbre on ne se déplace pas
                for stone in caillasse:
                    if self.y-speed+cam.y in stone.zoney and self.x+cam.x+8 in stone.zonex:
                        self.in_arbre=True
                if self.in_arbre==False:
                    #si on n'est pas dans un arbre on bouge
                    self.y-=speed
        if pyxel.btn(pyxel.KEY_DOWN) and cam.bjy==True:
            #si on clique sur la fleche du haut et qu'on a besoin de déplacer le joueur vers le haut
            self.in_arbre=False
            if self.y+speed<214-16:
                #si on ne sort pas du cadre
                for arbre in foret:
                    if self.y+speed+cam.y+8 in arbre.zoney and self.x+cam.x+8 in arbre.zonex:
                        self.in_arbre=True
                for stone in caillasse:
                    if self.y+speed+cam.y+16 in stone.zoney and self.x+cam.x+8 in stone.zonex:
                        self.in_arbre=True
                        #si le joueur est dans un arbre on ne se déplace pas
                if self.in_arbre==False:
                    #si on n'est pas dans un arbre on bouge
                    self.y+=speed
        if pyxel.btn(pyxel.KEY_LEFT) and cam.bjx==True:
            #si on clique sur la fleche du haut et qu'on a besoin de déplacer le joueur vers le haut
            self.in_arbre=False
            if self.x-speed>1:
                #si on ne sort pas du cadre
                for arbre in foret:
                    if self.x-speed+cam.x+8 in arbre.zonex and self.y+cam.y+8 in arbre.zoney:
                        self.in_arbre=True
                for stone in caillasse:
                    if self.x-speed+cam.x in stone.zonex and self.y+cam.y+8 in stone.zoney:
                        self.in_arbre=True
                        #si le joueur est dans un arbre on ne se déplace pas
                if self.in_arbre==False:
                    #si on n'est pas dans un arbre on bouge
                    self.x-=speed
        if pyxel.btn(pyxel.KEY_RIGHT) and cam.bjx==True:
            #si on clique sur la fleche du haut et qu'on a besoin de déplacer le joueur vers le haut
            self.in_arbre=False
            if self.x+speed<214-16:
                #si on ne sort pas du cadre
                for arbre in foret:
                    if self.x+speed+cam.x+16 in arbre.zonex and self.y+cam.y+8 in arbre.zoney:
                        self.in_arbre=True
                
                for stone in caillasse:
                    if self.x+speed+cam.x+8 in stone.zonex and self.y+cam.y+8 in stone.zoney:
                        self.in_arbre=True
                        #si le joueur est dans un arbre on ne se déplace pas
                if self.in_arbre==False:
                    #si on n'est pas dans un arbre on bouge
                    self.x+=speed
        #si le joueur revient au centre (horizontal ou vertical, il ne se déplace plus selon cet axe)
        if self.y in [95,96,97]:
            cam.bjy=False
        if self.x in [95,96,97]:
            cam.bjx=False
            
    def spriting(self):
        """
        determine le skin du joueur pour animer ses déplacment, trop long et 
        répétitif pour annoter mais tout va bien ça marche
        """
        if pyxel.btn(pyxel.KEY_UP) and pyxel.btn(pyxel.KEY_LEFT):
            self.spriteh=16
            self.spritew=16
            self.spritev=32
        elif pyxel.btn(pyxel.KEY_UP) and pyxel.btn(pyxel.KEY_RIGHT):
            self.spriteh=16
            self.spritew=-16
            self.spritev=32
        elif pyxel.btn(pyxel.KEY_DOWN) and pyxel.btn(pyxel.KEY_RIGHT):
            self.spriteh=-16
            self.spritew=-16
            self.spritev=32
        elif pyxel.btn(pyxel.KEY_DOWN) and pyxel.btn(pyxel.KEY_LEFT):
            self.spriteh=-16
            self.spritew=16
            self.spritev=32
        else:
            if pyxel.btn(pyxel.KEY_UP):
                self.spriteh=-16
                self.spritev=0
            elif pyxel.btn(pyxel.KEY_DOWN):
                self.spriteh=16
                self.spritev=0
            elif pyxel.btn(pyxel.KEY_LEFT):
                self.spritew=-16
                self.spritev=16
            elif pyxel.btn(pyxel.KEY_RIGHT):
                self.spritew=16
                self.spritev=16
                
    def chasse(self,i,porcherie, comp):
        """
        chasse un animal

        Parameters
        ----------
        i : int
            indice de l'animal dans sa liste.
        porcherie : list
            liste des animaux d'une espèce.
        comp : int
            compteur de temps.

        Returns
        -------
        porcherie : list
            liste d'animaux avec nouvelles valeurs.
        """
        if comp%30==15: #une fois par seconde
            porcherie[i].hp-=1
            #retire de la vie à l'animal
            porcherie[i].v=96
            #passe l'animal dans son skin rouge pour signifier qu'il perd de la vie
            if porcherie[i].hp<=0:
                #si l'animal n'a plus de vie
                if porcherie[i].id=="cochon":
                    self.inventory["viande"]+=1
                    #les cochons n'apportent qu'une viande
                    porcherie[i]=cochon(cam)
                    #réinitialise ce cochon
                elif porcherie[i].id=='ours':
                    #les ours apportent deux viande
                    porcherie[i]=ours(cam)
                    #réinitialise l'ours
                    self.inventory["viande"]+=2
        else:
            porcherie[i].v=0
            #remet l'animal dans son skin normal
        return porcherie
    
    def faim(self):
        """
        update la faim du joueur, enlève des points de vie si le joueur a trop faim
        """
        if self.hunger<=0:
            self.hp-=1
            if self.hp==0:
                self.alive=False
        else:
            self.hunger-=1
        if self.hunger==10:
            if self.hp<20:
                self.hp+=1
    
    def nourrir(self,food):
        """
        update la faim du joueur lorsqu'il consomme un aliment
        """
        if food=="baies":
            if self.inventory['baies']>=1 and self.hunger+1<=10:
                self.inventory['baies']-=1
                self.hunger+=1
        elif food=='viande':
            if self.inventory['viande']>=1 :
                if self.hunger+2<=10:
                    self.inventory['viande']-=1
                    self.hunger+=2
                elif self.hunger+1<=10:
                    self.inventory['viande']-=1
                    self.hunger+=1
                    
    def linv(self):
        """
        liste des objets dans l'inventaire dans leur ordre d'aquisition
        """
        for el in self.inventory:
            if self.inventory[el]>0 and el not in self.inv:
                self.inv.append(el)
            elif self.inventory[el]==0 and el in self.inv:
                self.inv.remove(el)
        return self.inv
#---------------------Fist---------------------------------

class fist:
    """
    les poings du joueur
    """
    def __init__(self, gamer):
        self.x1=gamer.x-8 
        self.y1=gamer.y+8
        self.u1=32
        self.v1=0
        #^coordonnées du premier poing
        self.x2=gamer.x+16
        self.y2=gamer.y+8
        self.u2=32
        self.v2=0
        self.t=[]
        self.tiens={}
        #^coordonnées du deuxième poing        
      
    
    def move(self,gamer):
        """
        anime les poings en fonction de l'orientation du joueur
        encore trop long à annoter juste ça fonctionne
        """
        if gamer.spritev==0:
            if gamer.spriteh==16:
                self.x1=gamer.x-8
                self.y1=gamer.y+8
                self.x2=gamer.x+16
                self.y2=gamer.y+8
            elif gamer.spriteh==-16:
                self.x1=gamer.x-8
                self.y1=gamer.y
                self.x2=gamer.x+16
                self.y2=gamer.y
        elif gamer.spritev==16:
            if gamer.spritew==16 :
                self.x1=gamer.x+8
                self.y1=gamer.y-8
                self.x2=gamer.x+8
                self.y2=gamer.y+16
            if gamer.spritew==-16 :
                self.x1=gamer.x
                self.y1=gamer.y-8
                self.x2=gamer.x
                self.y2=gamer.y+16
        elif gamer.spritev==32:
            if gamer.spritew==16:
                if gamer.spriteh==16 :
                    self.x1=gamer.x+8
                    self.y1=gamer.y-8
                    self.x2=gamer.x-8
                    self.y2=gamer.y+8
                elif gamer.spriteh==-16:   
                    self.x1=gamer.x-8
                    self.y1=gamer.y
                    self.x2=gamer.x+8
                    self.y2=gamer.y+16
            elif gamer.spritew==-16:
                if gamer.spriteh==16 :
                    self.x1=gamer.x
                    self.y1=gamer.y-8
                    self.x2=gamer.x+16
                    self.y2=gamer.y+8
                elif gamer.spriteh==-16 :
                    self.x1=gamer.x+16
                    self.y1=gamer.y
                    self.x2=gamer.x
                    self.y2=gamer.y+16
    
    def tape(self,gamer,seconde):
        """
        anime les poings du joueur lorsqu'il frappe 
        encore plus long je vous en prie ne me le faites pas annoter en entier
        """
        if gamer.spritev==0:
            if gamer.spriteh==16:
                if seconde%30<=15:
                    #change la position des points 2 fois par seconde
                    self.x1=gamer.x
                    self.y1=gamer.y+16
                else:
                    self.x2=gamer.x+8
                    self.y2=gamer.y+16
            elif gamer.spriteh==-16:
                if seconde%30<=15:
                    self.x1=gamer.x
                    self.y1=gamer.y-8
                else:
                    self.x2=gamer.x+8
                    self.y2=gamer.y-8
        elif gamer.spritev==16:
            if gamer.spritew==16 :
                if seconde%30<=15:
                    self.x1=gamer.x+16
                    self.y1=gamer.y
                else:
                    self.x2=gamer.x+16
                    self.y2=gamer.y+8
            if gamer.spritew==-16 :
                if seconde%30<=15:
                    self.x1=gamer.x-8
                    self.y1=gamer.y
                else:
                    self.x2=gamer.x-8
                    self.y2=gamer.y+8
                    
    def tenir(self, objet,gamer):
        """
        affiche les objets que le joueur tient dans ses mains
        """
        if len(self.tiens)<6:
            self.t.append(objet)
            gamer.inventory[objet]-=1
            self.tiens[f'{objet}{len(self.tiens)}']=(randint(1,4),randint(1,4))
                
    def use(self,objet, gamer):
        """
        retir les objets de l'inventaire du joueur quand utilisés
        """
        if (self.v1==136 and self.v2==152) or (self.v1==152 and self.v2==136):
            gamer.inventory['bois']-=1
            gamer.inventory['pierre']-=1
            self.v1,self.v2=0,0
            
            
    def back(self,gamer):
        """
        remet les objets que le joueur avait dans les mains dans l'inventaire
        """
        for el in range(len(self.t)):
            gamer.inventory[self.t[el]]+=1
        self.t=[]
        self.tiens={}

    def much(self, objet):
        """
        donne la quantité d'un objet que le joueur a dans les mains
        """
        m=0
        for el in self.t:
            if el==objet:
                m+=1
        return m
    
    def recette(self,gamer):
        """
        ajoute les recettes que le joueur peut utiliser
        """
        if self.much('bois')==3 and self.much('pierre')==2:
            if 'pioche' not in gamer.recettes:
                gamer.recettes.append('pioche')
            
#---------------------Arbre---------------------------------
                    
class arbre:
    """
    les arbres... je sais pas comment être plus claire
    """
    def __init__(self,x,y):
        self.etat=4 
        #entre 4 et 1 c'est le nombre de pommes, en dessous (jusqu'à -4) c'est le bois
        self.x=x
        self.x_=self.x #pour animer le tout petit mouvement de l'arbre lorsqu'il est frappé
        self.y=y
        self.zonex=[i for i in range(x+5,x+27)]
        self.zoney=[i for i in range(y+5,y+27)]
        #zone de l'arbre à ne pas traverser
        self.u=64
        self.v1=16
        #coordonnées des 2 premieres pommes
        self.v2=32
        #coordonnées des 2 autres pommes
        self.w1=32
        #largeur de la premiere ligne de pommes
        self.h=16
        self.w2=32
        #largeur de la deuxieme ligne de pommes
        self.last=0
            
    def baies (self):
        """
        ajuste l'affichage de l'arbre en fonction du nombre de baies
        """
        if self.etat<3:
            self.w2=0
            if self.etat==1:
                self.w1=16
            else:
                self.w1=32
        else:
            self.w1=32
            if self.etat==3:
                self.w2=16
            else:
                self.w2=32
        if self.etat<1:
            self.w1=0
            self.w2=0
            
    def recolte(self,seconde, comp,gamer):
        """
        ce qu'il se passe lorsqu'on frappe l'arbre
        """
        if comp%30==15 :
            #une fois par seconde
            if self.etat>-4:
                #retire des pommes/du bois à l'arbre si il est en état de perdre des ressources
                self.etat-=1
                self.x_=self.x-1
                #^petite animation de l'abre
                if self.etat>=0:
                    gamer.inventory["baies"]+=1
                    #ajoute les baies à l'inventaire
                else:
                    gamer.inventory["bois"]+=1
                    #ajoute le bois à l'inventaire
                self.last=seconde
        else:
            #remet l'arbre correctement
            self.x_=self.x
            
#---------------------Cochon---------------------------------

class cochon:
    
    
    def __init__(self, cam):
        """
        initialise les cochons
        """
        self.x=randint(54,600)
        self.y=randint(54,600)
        while self.x in [i for i in range(cam.x-16, cam.x+214)] and  self.y in [i for i in range(cam.y-16, cam.y+214)]:
            self.x=randint(54,600)
            self.y=randint(54,600)
        #^position hors de la caméra à l'initialisation
        self.hp=3
        self.dirx=randint(-1,1)
        self.diry=randint(-1,1)
        self.u=40
        self.v=0
        self.w=16
        self.h=16
        #coordonnées de l'image, me simplifient beaucoup la vie
        self.proie=False
        #^est-ce que le cochon est actuellement en proie, si oui il doit fuir
        self.id="cochon"
    
    def __repr__(self):
        return (f"id={self.id}, x={self.x}, y={self.y}, hp={self.hp}, dirx={self.dirx}, diry={self.diry}, u={self.u}, v={self.v}, w={self.w}, h={self.h}")
            
    def move_in_bound(self):
        """
        bouge le cochon dans les limites du jeu

        """
        if self.x+self.dirx>1 and self.x+self.dirx<440+214-16:
            self.x+=self.dirx
        else:
            #si plus dans les limites, change de direction
            self.dirx=randint(-1,1)
        if self.y+self.diry>1 and self.y+self.diry<440+214-16:
            self.y+=self.diry
        else:
            self.diry=randint(-1,1)
        
        
    def avoid(self,gamer,cam):
        """
        évite le joueur
        """
        if en_proie(self.x, self.y, self.dirx, self.diry,gamer.x+cam.x, gamer.y+cam.y):
            if en_proie(self.x, self.y, self.dirx*42, self.diry,gamer.x+cam.x, gamer.y+cam.y):
                if self.dirx==0:
                    self.dirx=1
                else:
                    self.dirx=-self.dirx
            if en_proie(self.x, self.y, self.dirx, self.diry*42,gamer.x+cam.x, gamer.y+cam.y):
                if self.diry==0:
                    self.diry=1
                else:
                    self.diry=-self.diry
                    
    def fuite(self,ours):
        """
        évite les ours
        """
        if en_proie(self.x, self.y, self.dirx, self.diry,ours.x,ours.y):
            if en_proie(self.x, self.y, self.dirx*47, self.diry,ours.x, ours.y):
                if self.dirx==0:
                    self.dirx=1
                else:
                    self.dirx=-self.dirx
            if en_proie(self.x, self.y, self.dirx, self.diry*47,ours.x, ours.y):
                if self.diry==0:
                    self.diry=1
                else:
                    self.diry=-self.diry
            
#---------------------Ours----------------------------------

class ours:
    def __init__(self,cam):
        """
        initialise les ours, très similaire au cochons
        """
        self.x=randint(54,600)
        while self.x in [i for i in range(cam.x-16, cam.x+214)]:
            self.x=randint(54,600)
        self.y=randint(54,600)
        while self.y in [i for i in range(cam.y-16, cam.y+214)]:
            self.y=randint(54,600)
        self.hp=3
        self.dirx=randint(-1,1)
        self.diry=randint(-1,1)
        self.u=56
        self.v=0
        self.w=16
        self.h=16
        self.id="ours"
    
    def move_in_bound(self):
        """
        bouge l'ours dans les limites du jeu

        """
        if self.x+self.dirx>1 and self.x+self.dirx<400+214-16:
            self.x+=self.dirx
        else: 
            self.dirx=randint(-1,1)
        if self.y+self.diry>1 and self.y+self.diry<400+214-16:
            self.y+=self.diry
        else: 
            self.diry=randint(-1,1)
            
    def suivre(self, cochon):
        """
        prend les cochons en proie
        """
        if en_proie(self.x, self.y, self.dirx*2, self.diry*2, cochon.x, cochon.y):
            if cochon.x>self.x:
                self.dirx=1
            elif cochon.x<self.x:
                self.dirx=-1
            else:
                self.dirx=0
            if cochon.y>self.y:
                self.diry=1
            elif cochon.y<self.y:
                self.diry=-1
            else:
                self.diry=0
                
    def sj(self, gamer,cam):
        """
        poursuit le joueur
        """
        if gamer.x+cam.x+8 in [self.x+i+8 for i in range(-28,44)] and gamer.y+cam.y+8 in [self.y+i+8 for i in range(-28,44)]:
            if gamer.x+cam.x>self.x:
                self.dirx=1
            elif gamer.x+cam.x<self.x:
                self.dirx=-1
            else:
                self.dirx=0
            if gamer.y+cam.y>self.y:
                self.diry=1
            elif gamer.y+cam.y<self.y:
                self.diry=-1
            else:
                self.diry=0
    
    def miam(self, proie,comp):
        """
        produit des dégat sur la proie, cochon ou joueur
        """
        if comp%30==15:    
            proie.hp-=1
            if proie.id=="cochon":
                proie.v=96
                if proie.hp<1:
                    proie=cochon(cam)
            elif proie.id=='gamer':
                if proie.hp<1:
                    proie.alive=False
        elif proie.id=="cochon":
            proie.v=0
        return proie
#---------------------Pierres----------------------------------
class Stone:
    def __init__(self,x,y):
        """
        Initialise les pierres
        """
        self.etat=2
        #entre 4 et 1 c'est le nombre de pommes, en dessous (jusqu'à -4) c'est le bois
        self.x=x
        self.x_=self.x #pour animer le tout petit mouvement de l'arbre lorsqu'il est frappé
        self.y=y
        self.zonex=[i for i in range(x,x+16)]
        self.zoney=[i for i in range(y,y+16)]
        #zone de l'arbre à ne pas traverser
        self.u=128
        self.v=16
        self.w=16
        #largeur de la premiere ligne de pommes
        self.h=16
        #largeur de la deuxieme ligne de pommes
        self.last=0
            
            
    def pierre (self):
        """
        ajuste l'affichage de l'arbre en fonction du nombre de baies
        """
        if self.etat==2:
            self.v=16
        elif self.etat==1:
            self.v=32
        else:
            self.v=48
            
    def recolte(self, seconde,comp,gamer):
        """
        Ce qu'il se passe lorsque la pierre est tapée
        """
        if comp%30==15 :
            #une fois par seconde
            if self.etat>0:
                #retire des pommes/du bois à l'arbre si il est en état de perdre des ressources
                self.etat-=1
                self.x_=self.x-1
                #petite animation de l'abre
                gamer.inventory["pierre"]+=1
                self.last=seconde
        else:
            self.x_=self.x

#-----------------La Souris------------------------------------- 
class Mouse:
    def __init__(self,seconde):
        self.x=pyxel.mouse_x
        self.y=pyxel.mouse_y
        self.last=seconde #derniere fois que la souris a bougé
        self.show=False #cache la souris
    

#---------------------Variables---------------------------------
def en_proie(x,y,dirx,diry,autre_x,autre_y):
    """
    Dis si un être vivant est chassé
    """
    if x+dirx+8 in [autre_x+i+8 for i in range(-28,44)] and y+diry+8 in [autre_y+i+8 for i in range(-28,44)]:
        return True
    else:
        return False

cam=cam()#caméra
gamer=gamer()#joueur
fist=fist(gamer)#poings
comp=0 #temps en nombre d'images
seconde=0 #secondes 
foret=[arbre(17*8,16*8), arbre(13*8,18*8), arbre(15*8,22*8), arbre(18*8,12*8), arbre(28*8,16*8), arbre(33*8,13*8), arbre(42*8,21*8), arbre(2*8,17*8), arbre(26*8,10*8)]#tous les arbres
caillasse=[Stone(14*8,26*8)]#toutes les pierres
porcherie=[]#tous les cochons
for i in range(3):
    porcherie.append(cochon(cam))
arg=[] #tous les ours
for i in range(3):
    arg.append(ours(cam))
P=False #pause
Help=False #aide/tuto
Mouse=Mouse(0) #souris
ressources={'baies': [(56,64),(40,120)], 'bois': [(72,0),(40,136)], 'viande': [(88,0),(40,128)], 'pierre':[(152,0),[40,152]],'pioche':[(168,0)]} #ressources disponibles

def update():
    #change les variables dans le jeu 30 fois par seconde
    global cam, gamer, fist, comp, seconde, foret, porcherie, P, arg, Help,Mouse, caillasse #variables universelles
    if gamer.alive==True:  
        if Help:
            if pyxel.btnp(pyxel.KEY_BACKSPACE):
                Help=False
                P=False
        if P==True:
            if pyxel.btnp(pyxel.KEY_RETURN):
                P=False
        else:
            inarbrex=False
            inarbrey=False
            color=pyxel.pget(gamer.x-1,gamer.y-1)
            if color==5 or color==6 or color==12:
                speed=1
            else:
                speed=2
            cam.depla(speed, foret, caillasse, gamer)
            gamer.spriting()
            if cam.bjx==True or cam.bjy==True:
                gamer.bj(cam,speed, foret,caillasse)
            fist.move(gamer)
            comp+=1
            if comp==30:
                seconde+=1
                comp=0
                if seconde%4==0:
                    for cochon in porcherie:
                        cochon.dirx=randint(-1,1)
                        cochon.diry=randint(-1,1)
                    for ours in arg:
                        ours.dirx=randint(-1,1)
                        ours.diry=randint(-1,1)
            for indice in range(len(porcherie)):
                porcherie[i].v=0
            for indice in range(len(arg)):
                arg[i].v=0    
            if pyxel.btnp(pyxel.KEY_SPACE):
                if fist.v1==120 or fist.v2==120 :
                    gamer.nourrir('baies', fist)
                if fist.v1==128 or fist.v2==128:
                    gamer.nourrir('viande',fist)
            if pyxel.btn(pyxel.KEY_BACKSPACE):
                fist.back(gamer)
            if pyxel.btn(pyxel.KEY_SPACE):
                fist.tape(gamer,comp)
                if gamer.in_arbre:
                    for arbre in foret:
                        if cam.y+gamer.y+10 in arbre.zoney and cam.x+gamer.x+10 in arbre.zonex:
                            arbre.recolte(seconde,comp,gamer)
                            arbre.baies()
                        elif cam.y+gamer.y-2 in arbre.zoney and cam.x+gamer.x-2 in arbre.zonex:
                            arbre.recolte(seconde,comp,gamer)
                            arbre.baies()
                    for stone in caillasse:
                        if cam.y+gamer.y-8 in stone.zoney and cam.x+gamer.x+8 in stone.zonex:
                            stone.recolte(seconde,comp,gamer)
                            stone.pierre()
                        elif cam.y+gamer.y+16 in stone.zoney and cam.x+gamer.x+8 in stone.zonex:
                            stone.recolte(seconde,comp,gamer)
                            stone.pierre()
                        elif cam.y+gamer.y+8 in stone.zoney and cam.x+gamer.x-8 in stone.zonex:
                            stone.recolte(seconde,comp,gamer)
                            stone.pierre()
                        elif cam.y+gamer.y+8 in stone.zoney and cam.x+gamer.x+16 in stone.zonex:
                            stone.recolte(seconde,comp,gamer)
                            stone.pierre()
                for indice in range(len(porcherie)):
                    if gamer.x+cam.x+8 in [porcherie[indice].x+i+8 for i in range(-28,44)] and gamer.y+cam.y+8 in [porcherie[indice].y+i+8 for i in range(-28,44)]:
                        porcherie=gamer.chasse(indice,porcherie,comp)
                for indice in range(len(arg)):
                    if gamer.x+cam.x+8 in [arg[indice].x+i+8 for i in range(-28,44)] and gamer.y+cam.y+8 in [arg[indice].y+i+8 for i in range(-28,44)]:
                        arg=gamer.chasse(indice,arg,comp)
            for arbre in foret:
                if arbre.etat<4 and seconde-arbre.last==10 and comp%30==0 :
                    arbre.etat+=1
                    arbre.baies()
                    arbre.last=seconde
            for stone in caillasse:
                if stone.etat<2 and seconde-stone.last==25 and comp%30==0:
                    stone.etat=2
                    stone.pierre()
                    stone.last=seconde
            for cochon in porcherie:
                cochon.avoid(gamer,cam)
                cochon.move_in_bound()
                for ours in arg:
                    cochon.fuite(ours)
            for ours in arg:
                ours.move_in_bound()
                for indice in range(len(porcherie)):
                    ours.suivre(porcherie[indice])
                    if porcherie[indice].x+8 in [ours.x+i+8 for i in range(-2,18)] and porcherie[indice].y+8 in [ours.y+i+8 for i in range(-2,18)]:
                        cochon=ours.miam(porcherie[indice],comp)
                        porcherie[indice]=cochon
                if gamer.x+cam.x+8 in [ours.x+i+8 for i in range(-2,18)] and gamer.y+cam.y+8 in [ours.y+i+8 for i in range(-2,18)]:
                    gamer=ours.miam(gamer,comp)
                ours.sj(gamer,cam)
            if pyxel.btnp(pyxel.KEY_RETURN):
                    P=True
            if pyxel.mouse_x in [i for i in range(9,9+20*len(gamer.inv))] and pyxel.mouse_y in [j for j in range(188,188+17)]:
                if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT) :
                    fist.tenir(gamer.inv[(pyxel.mouse_x-9)//20], gamer)
                    fist.recette(gamer)
            if pyxel.btnp(pyxel.KEY_A):
                if len(gamer.inv)>=1:
                    if gamer.inv[0]=='baies' or gamer.inv[0]=='viande' :
                        gamer.nourrir(gamer.inv[0])
            if pyxel.btnp(pyxel.KEY_Z):
                if len(gamer.inv)>=2:
                    if gamer.inv[1]=='baies' or gamer.inv[1]=='viande' :
                        gamer.nourrir(gamer.inv[1])
            if pyxel.btnp(pyxel.KEY_E):
                if len(gamer.inv)>=3:
                    if gamer.inv[2]=='baies' or gamer.inv[2]=='viande' :
                        gamer.nourrir(gamer.inv[2])
            if seconde%20==0 and comp==0:
                gamer.faim()
            gamer.inv=gamer.linv()
        if pyxel.mouse_x>=205 and pyxel.mouse_y<=9:
            if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
                Help=True
                P=True
        if pyxel.mouse_x!= Mouse.x or pyxel.mouse_y!=Mouse.y:
            Mouse.x = pyxel.mouse_x 
            Mouse.y = pyxel.mouse_y
            Mouse.last = seconde
            Mouse.show=True
        elif Mouse.last==seconde-4:
            Mouse.show=False
                    
            

def draw():
    """
    dessine 30 fois par seconde
    """
    global cam, gamer, fist, foret, porcherie, P,arg, Help,Mouse,caillasse
    if gamer.alive==True:
        pyxel.cls(11)
        pyxel.bltm(0, 0, 0, cam.x, cam.y, 214, 214,0)
        pyxel.blt(gamer.x, gamer.y, 0, 16, gamer.spritev, gamer.spritew, gamer.spriteh, 0)
        pyxel.blt(fist.x1,fist.y1,0,32,fist.v1,8,8,0)
        pyxel.blt(fist.x2,fist.y2,0,32,fist.v2,8,8,0)
        for t in range(len(fist.t)):
            if t%2==0:
                pyxel.blt(fist.x1+1-fist.tiens[f'{fist.t[t]}{t}'][0],fist.y1+1-fist.tiens[f'{fist.t[t]}{t}'][1],0,ressources[fist.t[t]][1][0],ressources[fist.t[t]][1][1],8,8,0)
            else:
                pyxel.blt(fist.x2+2-fist.tiens[f'{fist.t[t]}{t}'][0],fist.y2+2-fist.tiens[f'{fist.t[t]}{t}'][1],0,ressources[fist.t[t]][1][0],ressources[fist.t[t]][1][1],8,8,0)
        for cochon in porcherie:
            if cochon.x in [i for i in range(cam.x-32, cam.x+246)]:
                if cochon.y in [i for i in range(cam.y-32, cam.y+246)]:
                    pyxel.blt(cochon.x-cam.x,cochon.y-cam.y,0,cochon.u,cochon.v,cochon.w,cochon.h,0)
        for ours in arg:
            if ours.x in [i for i in range(cam.x-32, cam.x+246)]:
                if ours.y in [i for i in range(cam.y-32, cam.y+246)]:
                    pyxel.blt(ours.x-cam.x,ours.y-cam.y,0,ours.u,ours.v,ours.w,ours.h,11)
        for arbre in foret:
            pyxel.blt(arbre.x_-cam.x,arbre.y-cam.y,0,32,16,32,32,0)
            if arbre.w1==0:
                None
            elif arbre.x in [i for i in range(cam.x-32, cam.x+246)]:
                if arbre.y in [i for i in range(cam.y-32, cam.y+246)]:
                    pyxel.blt(arbre.x_-cam.x,arbre.y-cam.y,0,arbre.u,arbre.v1,arbre.w1,arbre.h,0)
            if arbre.w2!=0:
                if arbre.x in [i for i in range(cam.x-32, cam.x+246)]:
                    if arbre.y in [i for i in range(cam.y-32, cam.y+246)]:
                        pyxel.blt(arbre.x_-cam.x,arbre.y-cam.y+16,0,arbre.u,arbre.v2,arbre.w2,arbre.h,0)
        for stone in caillasse:
            pyxel.blt(stone.x_-cam.x,stone.y-cam.y,0,stone.u,stone.v,stone.w,stone.h,11)
        if P==True:
            pyxel.rect(214/2+3, 214/2-13, 10, 25, 7)
            pyxel.rect(214/2-12, 214/2-13, 10, 25, 7)
            pyxel.rectb(214/2+3, 214/2-13, 10, 25, 0)
            pyxel.rectb(214/2-12, 214/2-13, 10, 25, 0)
        pyxel.rect(3,3,160,5,1)
        pyxel.rect(3,3,gamer.hp*8,5,3)
        pyxel.blt(3,3,0,0,112,160,5,0)
        pyxel.rect(3,10,160,5,8)
        pyxel.rect(3,10,gamer.hunger*16,5,14)
        pyxel.blt(3,10,0,0,112,160,5,0)
        
        pyxel.rect(7,185,203,27,1)
        pyxel.rectb(6,184,205,29,7)
        for i in range(10):
            pyxel.rectb(9+(20*i),188,17,17,7)
        for el in range(len(gamer.inv)):
            pyxel.blt(10+20*el,189,0,ressources[gamer.inv[el]][0][0],ressources[gamer.inv[el]][0][1],16,16,1)
            pyxel.text(11+20*el,190,f"x{gamer.inventory[gamer.inv[el]]}",7)
        pyxel.text(22,206,"A",7)
        pyxel.text(42,206,"Z",7)
        pyxel.text(62,206,"E",7)
        pyxel.text(82,206,"R",7)
        pyxel.text(102,206,"T",7)
        pyxel.text(122,206,"Y",7)
        pyxel.text(142,206,"U",7)
        pyxel.text(162,206,"I",7)
        pyxel.text(182,206,"O",7)
        pyxel.text(202,206,"P",7)
        pyxel.blt(205,0,0,0,32,9,9,6)
        print(fist.t)
        for rec in range(len(gamer.recettes)):
            pyxel.blt(190+20*rec,11,0,ressources[gamer.recettes[rec]][0][0],ressources[gamer.recettes[rec]][0][1],16,16,8)
            pyxel.rectb(189+20*rec,10,18,18,7)
        if Help:
            pyxel.rect(10,10,214-20,214-20,1)
            pyxel.text(20,15,"This is a survival game,\n\n\nPress the arrows to move\n\nPress return to pause the game\n\nPress space to hit\n\nPress the letters written below\nany item of your inverntory to use\nsaid item\n\n\nYou can hunt pigs and bears\n\nBears can hunt pigs and you\n\nYou can collect berries and wood from\ntrees\n\n\nThe green gauge is your life, once empty\nyou die\n\nThe red gauge is your hunger, once empty\nyou loose life, once full you gain life\n\n\nPRESS BACKSPACE TO RESUME GAME",10)
            pyxel.rectb(9,9,214-18,214-18,10)
    else: 
        pyxel.cls(0)
        pyxel.text(90, 100, "GAME OVER :(", 8)
        pyxel.text(50, 110, "ESPACE OU ENTREE POUR REJOUER", 8)
    if Mouse.show:
        pyxel.blt(pyxel.mouse_x,pyxel.mouse_y,0,8,96,8,8,11)
        #pyxel.text(2,58,f"{pyxel.mouse_x in [i for i in range(9,9+20*len(gamer.inv))] and pyxel.mouse_y in [j for j in range(188,188+17)]}",7)
        
       
pyxel.run(update,draw) #lance le jeu