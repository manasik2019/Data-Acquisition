from socket import *
import time
from pymongo import MongoClient
import sys

global attempts
attempts = 4
global client
global db
global temperature_collection
global noise_collection
global light_collection
global humidity_collection
global Room_IDs
global Temperature_Sensors_IDs


Room_IDs  = ['61a2c27d4e26946fa4f21d9d',
'61854281cb7fb64edbffc7d2',
'619c1be969a9366b58902fb6',
'619e97ab7d699e0b307d3da0',
'619ea0687d699e0b307d3da2',
'619ea1357d699e0b307d3da3']


Temperature_Sensors_IDs = ['619ebd9a7d699e0b307d3da4',
'619ebe257d699e0b307d3da5',
'61a2c0304e26946fa4f21d8f',
'61a2c03b4e26946fa4f21d90',
'61a2c0494e26946fa4f21d91',
'61a2c0574e26946fa4f21d92']


def con():
    global attempts
    attempts = 4
    global client
    global db
    global temperature_collection
    global Room_IDs
    global Temperature_Sensors_IDs
   
    try:
        print ("Initialize")
        client = MongoClient("mongodb+srv://admin:admin@cluster0.xxxx.mongodb.net/test")
        client.server_info()
        db = client.iot_2021
        temperature_collection = db.temperature
        
        print ("Connection Succesful")

    except:
        attempts = attempts - 1
        if attempts == 0:
            print("Unsuccessful connection  to MongoDb")
            sys.exit()
        else:
            print("Connection Failed-Retrying with ",attempts)
            con()
        

#print(client)

 
def main():
    con()
    global attempts
    attempts = 4
    global client
    global db
    global temperature_collection
    global Room_IDs
    global Temperature_Sensors_IDs
    
    address= ( '192.168.10.2', 5000) #define server IP and port
    client_socket =socket(AF_INET, SOCK_DGRAM) #Set up the Socket
    client_socket.settimeout(1) #Only wait 1 second for a response
            
    while(1):
        

        for i in range (0, 3):

            data = b'Temperature1' #Set data request to Temperature from 1st sensor
            client_socket.sendto( data, address) #Send the data request
            try:
                rec_data, addr = client_socket.recvfrom(2048) #Read response from arduino
                temp1 = float(rec_data) #Convert string rec_data to float temp
                temperature_collection.insert_one({'value': temp1,'roomID': Room_IDs[i], 'deviceID': Temperature_Sensors_IDs[i], 'createdDate': int(time.time()),'createdBy': 'SYSTEM'}) #sending data to mongodb
                print ('Temperature for', Room_IDs[i], temp1, 'Degrees C') # Print the result
            except Exception as e:
                print(e)
                pass
            
            data = b'Temperature2' #Set data request to Temperature from second sensor
            client_socket.sendto( data, address) #Send the data request
            try:
                rec_data, addr = client_socket.recvfrom(2048) #Read response from arduino
                temp2 = float(rec_data) #Convert string rec_data to float temp
                temperature_collection.insert_one({'value': temp2,'roomID': Room_IDs[i+3], 'deviceID': Temperature_Sensors_IDs[i+3], 'createdDate': int(time.time()),'createdBy': 'SYSTEM'})
                print ('Temperature for', Room_IDs[i+3], temp2, 'Degrees C') # Print the result
            except Exception as e:
                print(e)
                pass
     
            time.sleep(5)
                                                                                                                                                                              
     
if __name__ == "__main__":
    main()
