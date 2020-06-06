
import machine, onewire, ds18x20, time, ucollections
def relay_on():
    relay_pin.off()

def relay_off():
    relay_pin.on()	

def get_temp():
    ds_sensor.convert_temp()
    return ds_sensor.read_temp(rom_sensor)

def server():
	html = """<!DOCTYPE html>
	<html>
	    <head> <title>ESP8266 Pins</title> </head>
	    <body> <h1>{}</h1> </body>
	</html>
	"""

	import socket
	addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]

	print("Making Socket")

	s = socket.socket()
	print("Binding")
	s.bind(addr)
	print("Listening")
	s.listen(1)

	print('listening on', addr)

	while True:
	    cl, addr = s.accept()
	    print('client connected from', addr)
	   
            cl_file = cl.makefile('rwb', 0)
	    while True:
		line = cl_file.readline()
                sline = str(line) 
                if sline.find('Referer:') != -1 or sline.find("GET") != -1:
                    if sline.find("r_on") != -1:
                        relay_on()
                    elif sline.find("r_off") != -1:
                        relay_off()
                print("Dealing with %s" % line)
                if not line or line == b'\r\n':
		    break
	    
            response = html.format(get_temp())
	   
             
                        
            cl.send('HTTP/1.0 200 OK\r\nContent-type: text/html\r\n\r\n')
	    cl.send(response)
	    cl.close()



relay_pin = machine.Pin(5, machine.Pin.OUT)

relay_off()

ds_pin = machine.Pin(2)
time.sleep_ms(750)

ds_sensor = ds18x20.DS18X20(onewire.OneWire(ds_pin))
time.sleep_ms(750)

roms = ds_sensor.scan()
time.sleep_ms(750)

print(roms)

rom_sensor = roms[0]


