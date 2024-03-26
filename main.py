import os, pty, serial, pyautogui, json
from termcolor import colored
past_values = [0] * 3

multipler = 1
read_time = 250
input_stream = ""

try: 
    ser = serial.Serial("/dev/cu.usbmodem1421201", 9600) 
except Exception as e:
    print(e)
    ser = serial.Serial("COM6", 9600)

# initialize the values for these variables
previous_mouse_clicks = [False, False]

def get_input(input_stream):
    # Gets any data packages foundi n the input buffer

    total = [0, 0, 0]
    extra_parameters = {}
    while "{" in input_stream and "}" in input_stream: #Complete Data Package Found
        
        # Remove any extra data
        input_stream = input_stream[input_stream.index("{"):]

        # Find all relevant data
        data = input_stream[:input_stream.index("}") + 1]


        # Use the data
        ID, x, y, z, l, r = *map(float, data[1:-1].split(",")),
        extra_parameters["LeftClick"] = l
        extra_parameters["RightClick"] = r
        
        total[0] += x
        total[1] += y
        total[2] += z


        # Remove from the stream
        input_stream = input_stream[input_stream.index("}") + 1:]

    return input_stream, total, extra_parameters

def debug_output(total):
    # Prints out mouse movement values in a color format for easy readbility
    print(*[colored(f"{str(round(abs(i), 3))[:5]}", "red") if i < 0 else colored(f"{str(round(abs(i),3))[:5]}", "green") for i in total], "\n"*10 )

def handle_mouse_clicks(leftMouseDown, rightMouseDown, previous_mouse_clicks):

    # Detection for the left mouse clicks
    if not previous_mouse_clicks[0] and leftMouseDown:
        pyautogui.mouseDown()

    elif previous_mouse_clicks[0] and not leftMouseDown:
        pyautogui.mouseUp()

    previous_mouse_clicks[0] = leftMouseDown

    # Detection for the right mouse clicks
    if not previous_mouse_clicks[1] and rightMouseDown:
        pyautogui.mouseDown(button="right")
    elif previous_mouse_clicks[1] and not rightMouseDown:
        pyautogui.mouseUp(button="right")
    
    previous_mouse_clicks[1] = rightMouseDown
    

while True:
    # Get new information from the serial connection
    new_packets = ser.read(read_time).decode("utf-8")

    # Add new data to buffer
    input_stream += new_packets 

    # Get any current packets from the buffer
    input_stream, total, extra_parameters = get_input(input_stream) 
    
    # Handle left click / right click functionality
    handle_mouse_clicks(extra_parameters["LeftClick"], extra_parameters["RightClick"], previous_mouse_clicks)

    # Removing values of low movement
    total = [0 if abs(total[i]) < 5 else total[i] for i in range(3)]    

    # Moving the mouse
    pyautogui.move(total[1] * multipler, total[0] * multipler)

    # Printing debug output
    debug_output(total)