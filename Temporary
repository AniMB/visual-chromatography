from machine import Pin, ADC
import utime
import math


thermistor = ADC(26) # Thermistors measure temperature based on resistance changes.

light_sensor = ADC(27) # Light sensors measure light intensity.

data_collection_led = Pin(17, Pin.OUT) # This LED is used to illuminate the TLC plate for data collection.

actuator_leds = [Pin(i, Pin.OUT) for i in (14, 15, 16)] # These LEDs simulate various actuator states or stages in the experiment.

ir_emitter = Pin(18, Pin.OUT) # The IR emitter sends an IR beam that the IR sensor can detect.
 
ir_sensor = Pin(19, Pin.IN) # The IR sensor detects the IR beam from the IR emitter, used to determine paper position.

"""Constants for calculating temperature from the thermistor's resistance."""
B_CONSTANT = 3950  # The B constant of the thermistor, an empirical value specific to the thermistor.
RESISTANCE_AT_25_C = 10000  # The resistance of the thermistor at 25 degrees Celsius, in ohms.
SERIES_RESISTOR = 10000  # The resistance of the series resistor used in the voltage divider, in ohms.

def read_temperature():
    # Read the analog value from the thermistor and convert it to a voltage.
    value = thermistor.read_u16() * 3.3 / 65535
    # Calculate the thermistor's resistance from the voltage divider equation.
    resistance = (3.3 * SERIES_RESISTOR / value) - SERIES_RESISTOR
    # Calculate the temperature using the simplified Steinhart-Hart equation and the B constant.
    temperature = 1/(math.log(resistance / RESISTANCE_AT_25_C) / B_CONSTANT + 1 / 298.15) - 273.15
    return temperature

def read_light_intensity():
    """Read the raw analog value from the light sensor, which is proportional to the light intensity."""
    return light_sensor.read_u16()

def toggle_data_collection_led(state):
    """Set the state of the data collection LED: 1 for on, 0 for off."""
    data_collection_led.value(state)

def activate_actuator_led(led_number, state):
    """Activate or deactivate a specific actuator LED based on its number and the desired state. """
    if 0 <= led_number < len(actuator_leds):
        actuator_leds[led_number].value(state)

def check_paper_position():
    # Ensure the IR emitter is on to send a beam to the IR sensor.
    ir_emitter.value(1)
    # Check if the IR sensor detects the beam. If not, the beam is interrupted (like by the paper), indicating the desired position.
    return not ir_sensor.value()

def experiment_sequence():
    # Check for the correct paper position using the IR sensor and emitter.
    print("Checking paper position...")
    while not check_paper_position():
        utime.sleep(1)  # Wait for the paper to reach the correct position.
    print("Paper in position.")
    
    # Monitor the temperature with the thermistor until it indicates the saturation solution has reached the desired height.
    print("Monitoring temperature...")
    while read_temperature() < 25:  # Example condition: wait until the temperature exceeds 25°C.
        utime.sleep(1)
    print("Desired temperature reached.")
    
    # Activate an actuator LED to simulate reaching a stage in the experiment.
    activate_actuator_led(0, 1)  # Example: Turn on the first actuator LED.
    
    # Illuminate the TLC plate with the data collection LED and read the light intensity from the light sensor.
    toggle_data_collection_led(1)  # Turn on the data collection LED.
    light_intensity = read_light_intensity()
    print(f"Light intensity: {light_intensity}")
    toggle_data_collection_led(0)  # Turn off the data collection LED after reading the light intensity.
    
    # Signal the completion of the experiment.
    print("Experiment complete.")

# Start the experiment sequence.
experiment_sequence()

