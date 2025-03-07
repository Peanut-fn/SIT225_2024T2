import serial
import time
import random

arduino = serial.Serial('COM8', 9600, timeout=1)

def send_command():
    """Send a random number to Arduino and log the event."""
    blink_count = random.randint(1, 5)  
    arduino.write(f"{blink_count}\n".encode())  
    print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] → Sent to Arduino: {blink_count}")
    return blink_count

def wait_for_response():
    """Listen for Arduino's response and wait accordingly."""
    while True:
        if arduino.in_waiting > 0:
            try:
                response = arduino.readline().decode().strip()  
                wait_time = int(response)  
                print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}] ← Received from Arduino: {wait_time}")
                
                
                time.sleep(wait_time)
                print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}]  Paused for {wait_time} seconds.")
                break  
            except ValueError:
                print(f"[{time.strftime('%Y-%m-%d %H:%M:%S')}]  Invalid response, retrying...")

def start_communication():
    """Continuously send and receive data between Python and Arduino."""
    while True:
        send_command()  
        time.sleep(0.2)  
        wait_for_response()  

if __name__ == "__main__":
    start_communication()