from traceback import print_tb
import babypepes as bbpp
import babypepesCanvassize as CanvasSize
import importlib


class startSizeFinder:    
    def __init__(self):
        print("Here are the Pepes you Call \n\n")
        self.printSavedPepes()
        self.start()
        

    def start(self):
        findMe = input("Who do you want to find \n")

        importlib.reload(CanvasSize)
        with open('babypepesCanvassize.py') as cs:
            if findMe in cs.read():
                loadCanvasSize = CanvasSize.savedPepesCanvas
                global largTela, altTela, divLarg, divAlt
                largTela, altTela, divLarg, divAlt = loadCanvasSize.get(findMe)
                print("\nlargura da tela = ", largTela,"\naltura da tela = ", altTela, "\nlargura do quadrado = " , largTela/divLarg, "\naltura do quadrado = " , altTela/divAlt)
            else:
                print("This shit never existed before")

    def printSavedPepes(self):
        SavedPepes = CanvasSize.savedPepesCanvas
        for x in SavedPepes:
          print(x)

letsGo = startSizeFinder()