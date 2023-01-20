import machine
import usocket as socket
import time
import network
from machine import Pin
import dht
from time import sleep


import socket

# AF_INET - use Internet Protocol v4 addresses
# SOCK_STREAM means that it is a TCP socket.
# SOCK_DGRAM means that it is a UDP socket.
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('',80)) # specifies that the socket is reachable by any address the machine happens to have
s.listen(5)   


sensor = dht.DHT11(Pin(15))

timeout = 0 # WiFi Connection Timeout variable 

wifi = network.WLAN(network.STA_IF)

# Restarting WiFi
wifi.active(False)
time.sleep(0.5)
wifi.active(True)

wifi.connect('POCO','Akshaya@1234')

if not wifi.isconnected():
    print('connecting..')
    while (not wifi.isconnected() and timeout < 5):
        print(5 - timeout)
        timeout = timeout + 1
        time.sleep(1)
        
if(wifi.isconnected()):
    print('Connected...')
    print('network config:', wifi.ifconfig())
    
    try:
        sleep(2)
        sensor.measure()
        temp= sensor.temperature()
        hum = sensor.humidity()
        print('Temperature: ',temp)
        print('Humidity: ', hum)
    except OSError as e:
        print('Failed to read sensor.')
        
# HTML Document
def web_page():
    html = """<!DOCTYPE HTML><html>
<head>
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <link rel="stylesheet" href="https://use.fontawesome.com/releases/v5.7.2/css/all.css" integrity="sha384-fnmOCqbTlWIlj8LyTjo7mOUStjsKC4pOpQbqyi7RrhN7udi9RwhKkMHpvLbHG9Sr" crossorigin="anonymous">
  <style>
    html {
     font-family: Arial;
     display: inline-block;
     margin: 0px auto;
     text-align: center;
    }
    h2 { font-size: 3.0rem; }
    p { font-size: 3.0rem; }
    .units { font-size: 1.2rem; }
    .dht-labels{
      font-size: 1.5rem;
      vertical-align:middle;
      padding-bottom: 15px;
    }
  </style>
</head>


 <script>   
   var ajaxRequest = new XMLHttpRequest();  
   
   function ajaxLoad(ajaxURL)  
   {  
    ajaxRequest.open('GET',ajaxURL,true);  
    ajaxRequest.onreadystatechange = function()  
    {  
     if(ajaxRequest.readyState == 4 && ajaxRequest.status==200)  
     {  
      var ajaxResult = ajaxRequest.responseText;  
      var tmpArray = ajaxResult.split("|");  
      document.getElementById('temp').innerHTML = tmpArray[0];  
      document.getElementById('humi').innerHTML = tmpArray[1];  
     }  
    }  
    ajaxRequest.send();  
   }  
     
   function updateDHT()   
   {   
     ajaxLoad('getDHT');   
   }  
     
   setInterval(updateDHT, 3000);  
    
  </script>  
    




<body>
  <h2>ESP DHT Server</h2>
  <p>
    <i class="fas fa-thermometer-half" style="color:#059e8a;"></i> 
    <span class="dht-labels">Temperature</span> 
    <span>"""+str(temp)+"""</span>
    <sup class="units">&deg;C</sup>
  </p>
  <p>
    <i class="fas fa-tint" style="color:#00add6;"></i> 
    <span class="dht-labels">Humidity</span>
    <span>"""+str(hum)+"""</span>
    <sup class="units">%</sup>
  </p>
</body>
</html>"""
    return html

# Output Pin Declaration 
LED = machine.Pin(2,machine.Pin.OUT)
LED.value(0)

while True:
    
    # Socket accept() 
    conn, addr = s.accept()
    print("Got connection from %s" % str(addr))
    
    # Socket receive()
    request=conn.recv(1024)
    print("")
    print("Content %s" % str(request))

    # Socket send()
    request = str(request)
    update = request.find('/getDHT')
    if update == 6:
        d.measure()
        t = d.temperature()
        h = d.humidity()
        response = str(t) + "|"+ str(h)
        led.value(not led.value())
    else:
        response = web_page()
        
    # Create a socket reply
    conn.send('HTTP/1.1 200 OK\n')
    conn.send('Content-Type: text/html\n')
    conn.send('Connection: close\n\n')
    conn.sendall(response)
    
    # Socket close()
    conn.close()