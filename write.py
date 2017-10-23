import binascii
import sys

import Adafruit_PN532 as PN532

# PN532 configuration for a Raspberry Pi:
CS   = 18
MOSI = 23
MISO = 24
SCLK = 25


# Create and initialize an instance of the PN532 class.
pn532 = PN532.PN532(cs=CS, sclk=SCLK, mosi=MOSI, miso=MISO)
pn532.begin()
pn532.SAM_configuration()

# Step 1, wait for card to be present.
print('Produkt ID schreiben')
print('Platziere den Tag auf den Reader...')
uid = pn532.read_passive_target()
while uid is None:
    uid = pn532.read_passive_target()
print('')
print('Karte gefunden. UID: 0x{0}'.format(binascii.hexlify(uid)))
print('')
print('==============================================================')
print('KARTE BIS ZUM FERTIGSTELLEN NICHT ENTFERNEN!')
print('==============================================================')
print('')

productId = None
while productId is None:
    enteredId = input('Produkt ID eingeben: ')
    print('')
    # Assume a number must have been entered.
    try:
        productId = int(enteredId)
    except ValueError:
        # Something other than a number was entered.  Try again.
        print('Fehler! ID ist keine Zahl.')
        continue

print('Schreibe Tag...')

# Nummer shiften sodass wir ein Hex Byte Array erstellen um dieses anschliessend auf den Tag zu schreiben
data = bytearray(16)
data[0] = (productId>>24) & 0xff
data[1] = (productId>>16) & 0xff
data[2] = (productId>>8) & 0xff
data[3] = productId & 0xff

# Finally write the card.
if not pn532.mifare_classic_write_block(4, data):
    print('Fehler! Tag konnte nicht beschrieben werden.')
    sys.exit(-1)
print('Tag wurde erfolgreich beschrieben.')