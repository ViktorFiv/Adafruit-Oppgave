import time
from Adafruit_IO import Client, Feed, RequestError
import pyfirmata
import mysql.connector

run_count = 0
ADAFRUIT_IO_USERNAME = "ViktorFiv"
ADAFRUIT_IO_KEY = "aio_tPzc01fbTkKeQerZkJwVk8zzFLWk"

mydb = mysql.connector.connect(
	host="localhost",
	user="root",
	password="Vkitor76",
	database="mydb"
)

aio = Client(ADAFRUIT_IO_USERNAME, ADAFRUIT_IO_KEY)

board = pyfirmata.Arduino('COM7')
 
it = pyfirmata.util.Iterator(board)
it.start()

mycursor = mydb.cursor()

print("connected")

sql= "INSERT INTO sensor(verdi, tid) VALUES (%s%s)"
verdi = 1.0
tid = datetime.datetime.now()

val = (verdi, tid)

print("Executing...")

mycursor.execute(sql, val)
mydb.commit()

print("Done")

digital_output = board.get_pin('d:13:o')

try:
	digital = aio.feeds('digital')
except RequestError:
	feed = Feed(name='digital')
	digital = aio.create_feed(feed)

while True:
	print('Sending count:', run_count)
	run_count += 1
	aio.send_data('counter', run_count)
	
	data = aio.receive(digital.key)
	
	print('Data: ', data.value)
	
	if data.value == "ON":
		digital_output.write(True)
	else:
		digital_output.write(False)
	
	time.sleep(2)
