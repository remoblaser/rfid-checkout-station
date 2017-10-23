from reader import Reader
from apiclient import APIClient
from appJar import gui
import gtk, pygtk


class App(object):
    def __init__(self):
        self.gui = gui("RFID Warenkorbsystem", self.getResolution())
        self.gui.setResizable(False)
        self.gui.setGeometry("fullscreen")
        self.gui.setSticky("news")
        self.gui.setExpand("both")
        self.gui.setFont(18)
        self.gui.startLabelFrame("Details")
        self.gui.addLabel("status", 'Initialisiere PN532...')
        self.gui.addButton("Clear", self.clear)
        self.gui.stopLabelFrame()
        self.gui.addGrid("products", [["Produkt", "Preis"], []])
        self.gui.setGridWidth("products", 1920)
        reader = Reader(self)
        
        self.apiClient = APIClient()

        self.gui.registerEvent(reader.read)
        self.gui.go()

    def getResolution(self):
        window = gtk.Window()
        screen = window.get_screen()
        return str(screen.get_width()) + "x" + str(screen.get_height())

    def addProduct(self, productId):
        productInformation = self.apiClient.getProductInformation(productId)
        price = int(productInformation['price']) / 10
        self.gui.addGridRow("products", [productInformation['name'],  "CHF " + str(price)])

    def clear(self, event):
        self.gui.removeGrid("products")
        self.gui.addGrid("products", [["Produkt", "Preis"], []])


app = App()