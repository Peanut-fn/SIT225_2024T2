import serial  # Import the serial library for communication with Arduino
import time    # Import the time library for delays and timestamps
import random  # Import the random library to generate random numbers

# Initialize the serial connection with Arduino on COM8 at 9600 baud rate
# 'timeout=1' ensures the read operation doesn't block indefinitely
arduino = serial.Serial('COM8', 9600, timeout=1)

def send_command():
    """
    Send a random number to Arduino and log the event.
    Returns the number of blinks sent to Arduino.
    """
    # Generate a random number between 1 and 5 to determine the blink count
    blink_count = random.randint(1, 5)
    # Send the blink count as a string followed by a newline character
    arduino.write(f"{blink_count}\n".encode())
    # Log the sent blink count with a timestamp
    print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] → Sent to Arduino: {blink_count}")
    return blink_count

def wait_for_response():
    """
    Listen for Arduino's response and wait accordingly.
    The response indicates how long to wait (in seconds).
    """
    while True:
        # Check if there is any incoming data from Arduino
        if arduino.in_waiting > 0:
            try:
                # Read the incoming line from Arduino, decode it, and remove any whitespace
                response = arduino.readline().decode().strip()
                # Convert the response to an integer (wait time)
                wait_time = int(response)
                # Log the received wait time with a timestamp
                print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] ← Received from Arduino: {wait_time}")
                
                # Pause execution for the received number of seconds
                time.sleep(wait_time)
                # Log the pause duration with a timestamp
                print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}]  Paused for {wait_time} seconds.")
                break  # Exit the loop once a valid response is processed
            except ValueError:
                # Log the error if the response could not be converted to an integer
                print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}]  Invalid response, retrying...")

def start_communication():
    """
    Continuously send and receive data between Python and Arduino.
    """
    while True:
        # Send a random blink count to Arduino
        send_command()
        # Small delay between sending commands
        time.sleep(0.2)
        # Wait for a response from Arduino and handle it
        wait_for_response()

# Entry point of the script
if __name__ == "__main__":
    start_communication()
