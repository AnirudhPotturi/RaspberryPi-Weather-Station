from multiprocessing import connection
import time
import board
import psycopg2
import datetime
import adafruit_dht
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM) 
GPIO.setwarnings(False)
GPIO.setup(18, GPIO.OUT, initial=GPIO.LOW)

# Establishing a connection with the Postgres Database.
connnection = psycopg2.connect(
   host="192.168.1.171",
    database="NAME OF DATABASE",
    user="ADD YOUR USERNAME TO THE DATATBASE",
    password="ADD YOUR PASSWORD TO THE DATATBASE"
    )

print("Connected")

# Initialize the DHT22 sensor and specify the Data Pin connected to the GPIO Port. In my case it was GPIO Port 4:
TemperatureHumiditySensor = adafruit_dht.DHT22(board.D4)

# Creating a cursor object which will later help us execute Postgres commands.
cursor = connnection.cursor()

i=0

while True:

    try:
        GPIO.output(18, GPIO.HIGH)
        # Reading the Temperature
        TemperatureCelsius = TemperatureHumiditySensor.temperature

        # Converting the temperature from Celsius to Farenheit.
        TemperatureFarenheit = TemperatureCelsius * (9 / 5) + 32

        # Reading the Humidity
        Humidity = TemperatureHumiditySensor.humidity
        #print(
        #    "Temp: {:.3f} F / {:.3f} C    Humidity: {}% ".format(
        #        TemperatureFarenheit, TemperatureCelsius, Humidity
        #    )
        #)

        CurrentTime = datetime.datetime.now() #.strftime('%Y/%m/%d %I:%M:%S')

        #Inserting elements into table 
        cursor.execute('INSERT INTO temperatures VALUES(%s, %s, %s)' , (CurrentTime, TemperatureFarenheit, Humidity))
        i+=1

        connnection.commit()

        GPIO.output(18, GPIO.LOW)

    except RuntimeError as error:
        # Errors happen fairly often, DHT's are hard to read, just keep going
        print(error.args[0])
        GPIO.output(18, GPIO.LOW)
        time.sleep(2.0)
        
    except Exception as error:
        TemperatureHumiditySensor.exit()
        GPIO.output(18, GPIO.LOW)
        raise error

    time.sleep(30.0)

    if i % 10 == 0 and i > 10:
        #cursor.execute('SELECT * FROM temperatures LIMIT 5')----------- 
        #connnection.commit()
        #result = cursor.fetchall()
        cursor.execute('DELETE FROM temperatures WHERE ctid IN (SELECT ctid FROM temperatures ORDER BY time LIMIT 10)')
        connnection.commit()
    

    

    

#op = [float(d[0]) for d in result] 
#print(op)


#Closing the connection - Commented during deployment
connnection.close()