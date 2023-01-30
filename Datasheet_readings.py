import csv
import time
from pymongo import MongoClient


global attempts
attempts = 4
global client
global db
global noise_collection
global humidity_collection
global Room_IDs
global Humidity_Sensors_IDs
global Noise_Sensors_IDs


Room_IDs  = ['61a2c27d4e26946fa4f21d9d',
'61854281cb7fb64edbffc7d2',
'619c1be969a9366b58902fb6',
'619e97ab7d699e0b307d3da0',
'619ea0687d699e0b307d3da2',
'619ea1357d699e0b307d3da3']

Humidity_Sensors_IDs = ['61a2c1c94e26946fa4f21d97',
'61a2c1dd4e26946fa4f21d98',
'61a2c1e54e26946fa4f21d99',
'61a2c1ed4e26946fa4f21d9a',
'61a2c1f64e26946fa4f21d9b',
'61a2c1ff4e26946fa4f21d9c']

Noise_Sensors_IDs = ['61912ce0d5ee9a5d411f8cf8',
'61a2bfd44e26946fa4f21d8a',
'61a2bfec4e26946fa4f21d8b',
'61a2bffd4e26946fa4f21d8c',
'61a2c0044e26946fa4f21d8d',
'61a2c0104e26946fa4f21d8e']


def con():
    global attempts
    global client
    global db
    global noise_collection
    global light_collection
    global humidity_collection

    try:
        print ("Initialize")
        client = MongoClient("mongodb+srv://admin:admin@cluster0.xxxx.mongodb.net/test")
        client.server_info()
        db = client.iot_2021
        noise_collection = db.noise
        humidity_collection = db.humidity
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
	global noise_collection
	global humidity_collection
	global Room_IDs
	global Humidity_Sensors_IDs
	global Noise_Sensors_IDs

	with open('Humidity and noise sensors data.csv', 'r') as csvfile: 
		readCSV = csv.reader(csvfile)
		next(readCSV) # escaping the first row of the csv file

		for line in readCSV:
			for i in range (0, len(Room_IDs)):

				humidity_collection.insert_one({'value': float(line[i+1]),'roomID': Room_IDs[i], 'deviceID': Humidity_Sensors_IDs[i], 'createdDate': int(time.time()),'createdBy': 'SYSTEM'})
				print ('humidity for', Room_IDs[i], 'is', float(line[i+1]), '%', ' at ', int(time.time()) )
				
				noise_collection.insert_one({'value': float(line[i+7]),'roomID': Room_IDs[i], 'deviceID': Noise_Sensors_IDs[i], 'createdDate': int(time.time()),'createdBy': 'SYSTEM'})
				print('noise for', Room_IDs[i], 'is', float(line[i+7]), 'db', 'at', int(time.time()))
				time.sleep(5)
				

	csvfile.close()

if __name__ == "__main__":
    main()

		
    	