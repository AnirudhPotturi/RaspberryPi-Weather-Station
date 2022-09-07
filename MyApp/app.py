import os
import psycopg2
from flask import Flask, render_template
from multiprocessing import connection
import time
import board
import psycopg2
import datetime
import adafruit_dht
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM) 

app = Flask(__name__)

def get_db_connection():
    # Establishing a connection with the Postgres Database.
    connection = psycopg2.connect(
  	host="192.168.1.171",
    database="NAME OF DATABASE",
    user="ADD YOUR USERNAME TO THE DATATBASE",
    password="ADD YOUR PASSWORD TO THE DATATBASE"
        )  

    return connection


@app.route('/')
def index():

    while True:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute('SELECT * FROM temperatures;')
        weather = cur.fetchall()
        cur.execute('SELECT AVG(temperaturefarenheit) FROM temperatures;')
        avge = cur.fetchone()
        avg = round(avge[0], 2) 
        cur.close()
        conn.close()
        return render_template('index.html', weather=weather, avg=avg)


