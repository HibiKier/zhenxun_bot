import requests
import os
import pyzbar.pyzbar as pyzbar
import random
import cv2
import zxing


# try:
    # f.write(r.content)
    # f.close()
    #解码二维码
image = cv2.imread("qrCode/47456898.png")
barcode = pyzbar.decode(image)
reader1 = zxing.BarCodeReader()
barcode1 = reader1.decode("qrCode/47456898.png")
print(barcode1)
print(barcode)
# except:
#     print("ERROR")