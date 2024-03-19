# This is a sample code that demonstrates wireless communication.
# You are expected to use this code and modify it to suit your project needs.

# ------------------------------------------------------------------------
# In this project, a red LED is connected to GP14.
# The red LED is controlled based on the value of a light sensor's output.
# The light sensor output is connected to GP26 (ADC pin).
# The red LED status and the value of the red LED pin (GP14) are communicated wirelessly to a server.
# The status and value are displayed on the webpage. In addition, the user interface has
# a circle indicating the LED turns color depending upon the status of the physical LED. 
# ------------------------------------------------------------------------


# -----------------------------------------------------------------------
# The following list of libraries are required. Do not remove any. 
import machine
import network
import usocket as socket
import utime as time
import _thread
import json
# -------------------------------------------------------------------------

# -------------------------------------------------------------------------

# The below portion of the code is to be tweaked based on your needs. 

# Configure GP14 as output and define it as redLED_pin 
redLED_pin = machine.Pin(14, machine.Pin.OUT)
redLED_status = "Off" # Define a variable called redLED_status and set it to "Off"

# Define a function to get the red LED status
def get_redLED_status():
    return "On" if redLED_pin.value() == 1 else "Off"
# Note that the function returns the status.

# Define a function to periodically check the ADC pin and control the red LED pin.
def check_adc_and_control_redLED():
    global redLED_status  # Declare redLED_status as global. 
    adc = machine.ADC(26) # Configure GP26 as ADC pin.
    while True:
        LightSensor_value = adc.read_u16() # read the value of the ADC pin and save it in a variable.
        print("ADC Value:", LightSensor_value)

        if LightSensor_value > 4000: # the threshold value must be tuned based on test environment. 
            print("Mobile light off; turning on the red LED")
            redLED_pin.on() # set the GP14 pin to high (value = 1). 
        else:
            print("Mobile light on; turning off the red LED")
            redLED_pin.off() # set the GP14 pin to low (value = 0).

        redLED_status = get_redLED_status()  # Update redLED_status
        print("Red LED Status:", redLED_status)
        time.sleep(1) # wait for 1 second. 
# --------------------------------------------------------------------------

# --------------------------------------------------------------------------
# Below given code should not be modified (except for the name of ssid and password). 
# Create a network connection
ssid = 'RPI_PICO_AP'       #Set access point name 
password = '12345678'      #Set your access point password
ap = network.WLAN(network.AP_IF)
ap.config(essid=ssid, password=password)
ap.active(True)            #activating

while ap.active() == False:
  pass
print('Connection is successful')
print(ap.ifconfig())

# ---------------------------------------------------------------------------

# ---------------------------------------------------------------------------
# Below given code defines the web page response. Your html code must be used in this section.
# 
# Define HTTP response
def web_page():
    redLED_status = get_redLED_status()
    LED_color = "red" if redLED_status == "On" else "gray"
 
# Modify the html portion appropriately.
# Style section below can be changed.
# In the Script section some changes would be needed (mostly updating variable names and adding lines for extra elements). 

    html = """<html><head>
    <title>Pico Web Server</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <link rel="icon" href="data:,">
    <style>
        html {
            font-family: Helvetica;
            text-align: center;
            background-color: #b0b2b2;
        }
        h1 {
            color: #0F3376;
            padding: 2vh;
        }
        p {
            font-size: 1.5rem;
        }
        

        .circle {
            width: 20px;
            height: 20px;
            border-radius: 50%;
            display: inline-block;
            margin-left: 10px;
        }
    </style>
    
    <script>
        function updateStatus() {
            var xhr = new XMLHttpRequest();
            xhr.onreadystatechange = function() {
                if (xhr.readyState == 4 && xhr.status == 200) {
                    var data = JSON.parse(xhr.responseText);
                   
                    document.getElementById("RedLEDStatus").innerHTML = data.RedLEDStatus;
                    var buzzerColor = data.RedLEDStatus === "On" ? "red" : "gray";
                    document.getElementById("buzzerIndicator").style.backgroundColor = buzzerColor;
                    
                }
            };
            xhr.open("GET", "/status", true);
            xhr.send();
        }
        setInterval(updateStatus, 1000); // Refresh every 1 second
    </script>
    </head>
    <body>
     
    <p>RedLED Status: <strong id="RedLEDStatus">""" + redLED_status + """</strong><div class="circle" id="buzzerIndicator" style="background-color: """ + LED_color + """;"></div></p>
  
    </body>
    </html>"""
    return html
# --------------------------------------------------------------------
# This section could be tweaked to return status of multiple sensors or actuators.

# Define a function to get the status of the red LED.
# The function retuns status. 
def get_status():
    status = {
        "RedLEDStatus": redLED_status,
        # You will add lines of code if status of more sensors is needed.
    }
    return json.dumps(status)
# ------------------------------------------------------------------------

# -------------------------------------------------------------------------
# This portion of the code remains as it is.

# Start the ADC monitoring function in a separate thread
_thread.start_new_thread(check_adc_and_control_redLED, ())

# Create a socket server
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('', 80))
s.listen(5)

# --------------------------------------------------------------------------

# --------------------------------------------------------------------------

# This section of the code will have minimum changes. 
while True:
    conn, addr = s.accept()
    print('Got a connection from %s' % str(addr))
    request = conn.recv(1024)
    if request:
        request = str(request)
        print('Content = %s' % request)
        LED_on = request.find('/?redLED_pin=on') # this part of the code could be modified
        LED_off = request.find('/?redLED_pin=off') # this part of the code could be modified
        
# this part of the code could be modified
    if LED_on == 6: 
        print('LED ON')
        redLED_pin.value(1)
    elif LED_off == 6:
        print('LED OFF')
        redLED_pin.value(0)

# this part of the code remains as it is. 
    if request.find("/status") == 6:
        response = get_status()
        conn.send("HTTP/1.1 200 OK\n")
        conn.send("Content-Type: application/json\n")
        conn.send("Connection: close\n\n")
        conn.sendall(response)
    else:
        response = web_page()
        conn.send("HTTP/1.1 200 OK\n")
        conn.send("Content-Type: text/html\n")
        conn.send("Connection: close\n\n")
        conn.sendall(response)
    conn.close()


