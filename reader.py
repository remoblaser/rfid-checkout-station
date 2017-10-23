import binascii
import sys
import Adafruit_PN532

class Reader(object):
    def __init__(self, app):
        self.app = app
        self.initPN532()

    def initPN532(self):
        # Configuration for a Raspberry Pi:
        CS   = 18
        MOSI = 23
        MISO = 24
        SCLK = 25

        # Create an instance of the PN532 class.
        self.pn532 = Adafruit_PN532.PN532(cs=CS, sclk=SCLK, mosi=MOSI, miso=MISO)

        # Call begin to initialize communication with the PN532.  Must be done before
        # any other calls to the PN532!
        self.pn532.begin()

        ic, ver, rev, support = self.pn532.get_firmware_version()        

        # Configure PN532 to communicate with MiFare cards.
        self.pn532.SAM_configuration()



    def read(self):
        self.app.gui.setLabel("status", "Warte auf scan...")
        # Check if a card is available to read.
        uid = self.pn532.read_passive_target()
        # Try again if no card is available.
        if uid:
            # Authenticate block 4 for reading with default key (0xFFFFFFFFFFFF).
            # Read block 4 data.
            data = self.pn532.mifare_classic_read_block(4)
            if data:
                # Note that 16 bytes are returned, so only show the first 4 bytes for the block.
                self.app.gui.queueFunction(self.app.gui.setLabel, "status", "Product ID: {0}".format(int(binascii.hexlify(data[:4]), 16)))
                self.app.addProduct(int(binascii.hexlify(data[:4]), 16))
                # Example of writing data to block 4.  This is commented by default to
                # prevent accidentally writing a card.
                # Set first 4 bytes of block to 0xFEEDBEEF.
                # data[0:4] = [0xFE, 0xED, 0xBE, 0xEF]
                # # Write entire 16 byte block.
                # pn532.mifare_classic_write_block(4, data)
                # print('Wrote to block 4, exiting program!')
                # # Exit the program to prevent continually writing to card.
                # sys.exit(0)