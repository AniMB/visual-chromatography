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
light_intensity=''
# Configure GP14 as output and define it as redLED_pin 
data_collection_led = machine.Pin(12, machine.Pin.OUT) # This LED is used to illuminate the TLC plate for data collection.

actuator_leds = [machine.Pin(i, machine.Pin.OUT) for i in (13, 15, 14)] # These LEDs simulate various actuator states or stages in the experiment.

ir_emitter = machine.Pin(11, machine.Pin.OUT) # The IR emitter sends an IR beam that the IR sensor can detect.
thermistor = machine.ADC(26)# Thermistors measure temperature based on resistance changes.

light_sensor=machine.ADC(28)# Light sensors measure light intensity.

ir_sensor = machine.ADC(27) # The IR sensor detects the IR beam from the IR emitter, used to determine paper position.



# provides the status of the ouptut
def get_output_status():
  if actuator_leds[0].value()==1:
    if actuator_leds[1].value()==1:
      if data_collection_led.value()==1:
        if actuator_leds[2].value()==1:
          return light_intensity
        return "Scanning"

      return "Spraying"
    return "Saturating"
  
# new thermistor detection code which will detect a fluctuation in temperature.
def colour_error():
   if data_collection_led.value()==1:
      return "on"
def interpret_thermistor():
  temp_thermistor_value = thermistor.read_u16()
  time.sleep(1)
  if ((temp_thermistor_value - thermistor.read_u16()) > 1000) or ((temp_thermistor_value - thermistor.read_u16()) < -1000):
      return True
  else:
      return False


def read_light_intensity():

  """Read the raw analog value from the light sensor, which is proportional to the light intensity, then decide which colour it matches up with."""
  colour=''
  while light_sensor.read_u16() > 50000:
      if (light_sensor.read_u16() >19600 and light_sensor.read_u16() <20200):
          colour="blue"
          return "blue"
      elif(light_sensor.read_u16() > 29000 and light_sensor.read_u16() <29600):
          colour="red-pink"
          return "red-pink"
      elif(light_sensor.read_u16() > 34500 and light_sensor.read_u16() <34900):
          colour="pink"
          return "pink"
      elif(light_sensor.read_u16() > 32000 and light_sensor.read_u16() <32800):
          colour="yellow"
          return "yellow"
      elif(light_sensor.read_u16() > 33400 and light_sensor.read_u16() <34200):
          colour="white"
          return "white"
  return colour

def toggle_data_collection_led(state):
  """Set the state of the data collection LED: 1 for on, 0 for off."""
  data_collection_led.value(state)


def activate_actuator_led(led_number, state):
  """Activate or deactivate a specific actuator LED based on its number and the desired state. """
  if 0 <= led_number < len(actuator_leds):
      actuator_leds[led_number].value(state)

  # turns off the leds
def reset_leds():
  activate_actuator_led(0,0)
  activate_actuator_led(1,0)
  activate_actuator_led(2,0)

def check_paper_position():
  # Ensure the IR emitter is on to send a beam to the IR sensor.
  ir_emitter.value(1)
  # Check if the IR sensor detects the beam. If not, the beam is interrupted (like by the paper), indicating the desired position.
  return ir_sensor.read_u16()


def experiment_sequence():

  reset_leds()

  # Check for the correct paper position using the IR sensor and emitter.
  print("Checking paper position...")
  while check_paper_position()<5000:
      time.sleep(0)  # Wait for the paper to reach the correct position.
  print("Paper in position.")

  # Activate an actuator LED to simulate reaching a stage in the experiment.
  activate_actuator_led(0, 1)
  
  # Monitor the temperature with the thermistor until it indicates the saturation solution has reached the desired height.
  print("Monitoring temperature...")
  while interpret_thermistor() is False:  
      time.sleep(0)
  print("Desired temperature reached.")
  
  # Activate an actuator LED to simulate reaching a stage in the experiment.
  activate_actuator_led(1, 1)  # Example: Turn on the first actuator LED.
  time.sleep(3)
  # Illuminate the TLC plate with the data collection LED and read the light intensity from the light sensor.
  toggle_data_collection_led(1)  # Turn on the data collection LED.
  print("Collecting data")
  global light_intensity
  light_intensity= read_light_intensity()
  print(f"Light intensity/colour: {light_intensity}")
  time.sleep(1)
  toggle_data_collection_led(0)  # Turn off the data collection LED after reading the light intensity.
  
  # Activate an actuator LED to indicate completion of experiment
  activate_actuator_led(2, 1)

  # Signal the completion of the experiment.
  print("Experiment complete.")

  time.sleep(10)
  reset_leds()


# --------------------------------------------------------------------------

# --------------------------------------------------------------------------
# Below given code should not be modified (except for the name of ssid and password). 
# Create a network connection
ssid = 'Chemists'       #Set access point name 
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

    
 
# Modify the html portion appropriately.
# Style section below can be changed.
# In the Script section some changes would be needed (mostly updating variable names and adding lines for extra elements). 

  html = """
  <html lang="en">
  <head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>The Chemists</title>

  <style>
    :root {
      --primary-color: #007bff;
      --hover-color: #0056b3;
      --error-color: #ff4136;
      --error-hover-color: #c2302a;
      --background-color: #f4f4f4;
      --text-color: #333;
      --button-font-weight: bold;
      --button-text-transform: uppercase;
    }

    body {
      font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
      margin: 0;
      padding: 0;
      background-color: var(--background-color);
      color: var(--text-color);
    }

    .header {
      display: flex;
      justify-content: center;
      text-align: center;
      align-items: center;
      padding: 20px;
      background-color: #fff;
      box-shadow: 0 2px 5px rgba(0,0,0,0.1);
    }

    .group-members, .results {
      display: grid;
      grid-template-columns: repeat(3, 1fr);
      gap: 10px;
      justify-items: center;
      align-items: center;
      width: 90%;
      max-width: 600px;
      margin: 20px auto;
      padding: 10px;
      background-color: #fff;
      box-shadow: 0 2px 4px rgba(0,0,0,0.1);
      border-radius: 8px;
    }

    .process-indicator {
      display: grid;
      grid-template-columns: repeat(4, auto);
      gap: 15px;
      justify-items: center;
      padding: 20px;
    }

    .process-unit {
      display: flex;
      flex-direction: column;
      align-items: center;
    }

    .process-circle {
      width: 30px;
      height: 30px;
      border: 2px solid var(--primary-color);
      border-radius: 50%;
      background-color: #fff;
      display: flex;
      justify-content: center;
      align-items: center;
      transition: transform 0.3s ease;
    }

    .process-circle:hover {
      transform: scale(1.1);
    }

    .process-text {
      margin-top: 8px;
      color: var(--primary-color);
      font-size: 0.8em;
      text-align: center;
    }

    .button, .emergency-stop {
      padding: 15px 30px;
      border: none;
      border-radius: 5px;
      cursor: pointer;
      font-weight: var(--button-font-weight);
      text-transform: var(--button-text-transform);
      transition: background-color 0.3s ease;
      display: block;
      margin: 10px auto;
    }

    .button {
      background-color: var(--primary-color);
      color: white;
    }

    .button:hover {
      background-color: var(--hover-color);
    }

    .emergency-stop {
      background-color: var(--error-color);
      color: white;
    }

    .emergency-stop:hover {
      background-color: var(--error-hover-color);
    }

    .results {
      grid-template-columns: 1fr;
      text-align: center;
    }
  </style>
  </head>
  <body>

  <div class="header">
    <h1 style="font-size: 1.2em; padding: 10px;"> Project Title
  </h1>
  </div>


  <div class="group-members">
    <div>Rohann</div>
    <div>Rohan</div>
    <div>Animish</div>
  </div>

  <div class="process-indicator">
    <div class="process-unit">
      <div class="process-circle" id="sat" style="background-color: yellow;"></div>
      <span class="process-text" >Saturation</span>
    </div>
    <div class="process-unit">
      <div class="process-circle" id="spray" ></div>
      <span class="process-text">Spray</span>
    </div>
    <div class="process-unit">
      <div class="process-circle" id="scan"></div>
      <span class="process-text" >Scan</span>
    </div>
    <div class="process-unit">
      <div class="process-circle" id="error" ></div>
      <span class="process-text" >Completion</span>
    </div>
  </div>

  <div class="button-container">
    <div class="start-button-container" style="display:flex; justify-content:center; ">
     <button class="button" style="margin-left: 500px;" onclick="startSpray()">Start Spray</button>
    <button class="button" style="margin-right: 500px;"onclick="startScan()">Start Scan</button></a>
  </div><a href="/?error>
     <button class="emergency-stop" onclick="emergencyStop()">Emergency Stop</button></a>
  </div>

  <div class="results">
    <p class="result-text">Results</p>
  </div>

  <script>
   
 function updateStatus() {
  var xhr = new XMLHttpRequest();
  xhr.onreadystatechange = function() {
      if (xhr.readyState == 4 && xhr.status == 200) {
        var results = JSON.parse(xhr.responseText);
        var results_element = document.querySelector(".results-text");
        results_element.textContent = results.output_status;
        document.getElementById('error').style.backgroundColor=data.completion_status==="on"? "green":"yellow";
      }
    }
  };
 xhr.open("GET", "/status", true);
 xhr.send();
          
    function startSpray() {
      var element = document.getElementById('sat');
      element.style.backgroundColor = 'green';
      var element = document.getElementById('spray');
      element.style.backgroundColor = 'yellow';
      var element = document.getElementById('scan');
      element.style.backgroundColor = 'white';
    }
    function completion(){
      var element = document.getElementById('scan');
      element.style.backgroundColor = 'green';
    }
    function startScan() {
      var element = document.getElementById('sat');
      element.style.backgroundColor = 'green';
      var element = document.getElementById('spray');
      element.style.backgroundColor = 'green';
      var element = document.getElementById('scan');
      element.style.backgroundColor = 'yellow';
      setTimeout(completion, 6000);
      
      
      
    }
    
    function emergencyStop() {
      var element = document.getElementById('sat');
      element.style.backgroundColor = 'red';
      var element = document.getElementById('spray');
      element.style.backgroundColor = 'red';
      var element = document.getElementById('scan');
      element.style.backgroundColor = 'red';
      var element = document.getElementById('error');
      element.style.backgroundColor = 'red';
        
      
    }
    setInterval(updateStatus, 1000); // Refresh every 1 second
  
  </script>

  </body>
  </html>"""
  return html
# --------------------------------------------------------------------
# This section could be tweaked to return status of multiple sensors or actuators.

# Define a function to get the status of the red LED.
# The function retuns status. 
def get_status():
    status = {
       "output_status":get_output_status(),
       "completion_status":colour_error(),
        

        # You will add lines of code if status of more sensors is needed.
    }
    return json.dumps(status)
# ------------------------------------------------------------------------

# -------------------------------------------------------------------------
# This portion of the code remains as it is.

# Start the ADC monitoring function in a separate thread
_thread.start_new_thread(experiment_sequence, ())

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
        LED_on = request.find('/?error') # this part of the code could be modified
        
        
# this part of the code could be modified
    if LED_on == 6: 
      print('Emergency Stop')
      exit()
    

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


