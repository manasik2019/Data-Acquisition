import socket
from struct import *
import time
from pymongo import MongoClient



global db
global light_collection
global sock1
global sock2
global attempts
attempts = 4
global client

Room_IDs  = ['61a2c27d4e26946fa4f21d9d',
'61854281cb7fb64edbffc7d2',
'619c1be969a9366b58902fb6',
'619e97ab7d699e0b307d3da0',
'619ea0687d699e0b307d3da2',
'619ea1357d699e0b307d3da3']

Light_Sensors_IDs = ['619e95257d699e0b307d3d9f',
'619e9e987d699e0b307d3da1',
'61a2c0a44e26946fa4f21d93',
'61a2c0bd4e26946fa4f21d94',
'61a2c0cb4e26946fa4f21d95',
'61a2c0e94e26946fa4f21d96']

def con(): # define a function to connect to mongoDB
    global attempts
    global client
    global db
    global light_collection
    try:
        print ("Initialize")
        client = MongoClient("mongodb+srv://admin:admin@cluster0.xxxx.mongodb.net/test")
        client.server_info()
        db = client.iot_2021
        light_collection = db.light

        


        print ("Connection Succesful")

    except:
        attempts = attempts - 1
        if attempts == 0:
            print("Unsuccessful connection  to MongoDb")
            sys.exit()
        else:
            print("Connection Failed-Retrying with ",attempts)
            con()


def main():
    con()
    global client
    global db
    global light_collection
    global sock1
    global sock2


    HOST = socket.gethostbyname(socket.gethostname())  # Device IP address
    
    print ("Server ", HOST, "Port:", " 50000, 50001")

    while(1):
        try:
            for i in range (0, 3):

                sock1 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # Creating UDP Socket for IPV4
                sock1.bind((socket.gethostname(), 50000))
                sock1.settimeout(0.1)
                data, addr = sock1.recvfrom(128) # buffer size is 2048 byte
                light = "%1.4f" %unpack_from ('!f', data, 56)
                light_collection.insert_one({'value': light, 'roomID': Room_IDs[i], 'deviceID':Light_Sensors_IDs[i], 'createdDate': int(time.time()),'createdBy':'SYSTEM' }) #sending data to mongodb
                print ("The Measured Light from ", Room_IDs[i],  light, " LUX")
                sock1.close()
                time.sleep(5) 

                sock2 = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # Creating UDP Socket for IPV4
                sock2.bind((socket.gethostname(), 50001))
                sock2.settimeout(0.1)
                data1, addr1 = sock2.recvfrom(128) # buffer size is 2048 byte
                light1 = "%1.4f" %unpack_from ('!f', data1, 56)
                light_collection.insert_one({'value': light1, 'roomID': Room_IDs[i+3], 'deviceID': Light_Sensors_IDs[i+3] , 'createdDate': int(time.time()),'createdBy':'SYSTEM' })
                print ("The Measured Light from", Room_IDs[i+3], light1, " LUX") # Print the result
                sock2.close()
                time.sleep(5)
            
        except Exception as e:
            print(e)
            pass


                 
if __name__ == "__main__":
    main()
