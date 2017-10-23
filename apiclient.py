import requests

class APIClient(object):
    def getProductInformation(self, productId):
        return self.call("http://rfid.remoblaser.ch/api/product/" + str(productId))
        

    def call(self, url):
        response = requests.get(url)
        return response.json()