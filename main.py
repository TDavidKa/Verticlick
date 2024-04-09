import serial, pyautogui
from termcolor import colored

import sys
 
import pygame
from pygame.locals import *
 
pygame.init()
 
fps = 60
fpsClock = pygame.time.Clock()
 
width, height = 640, 480
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('This is totally a processing window')


try: 
    ser = serial.Serial("/dev/cu.usbmodem1421201", 9600) 
except Exception as e:
    print(e)
    ser = serial.Serial("COM6", 9600)



def get_input(input_stream):
    # Gets any data packages found in the input buffer
    total = [0, 0, 0]
    extra_parameters = {}
    while "{" in input_stream and "}" in input_stream: #Complete Data Package Found
        
        # Remove any extra data
        input_stream = input_stream[input_stream.index("{"):]

        # Find all relevant data
        data = input_stream[:input_stream.index("}") + 1]


        # Use the data
        x, y, l, r = *map(float, data[1:-1].split(",")),

        extra_parameters["LeftClick"] = l
        extra_parameters["RightClick"] = r
    
        total[0] += x
        total[1] += y

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
    
bg = pygame.image.load("temp.jpg")
def output_loop(total):
 
  screen.fill((0, 0, 0))
  screen.blit(pygame.transform.scale(bg, (width, height)), (0, 0))
  
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      pygame.quit()
      sys.exit()
  
  total[0] *= -1
  mulitplier = 2
  if total[0] > 0:
    pygame.draw.rect(screen, (0, 128, 0), (width // 2, height // 2, total[0] * mulitplier, 20), 0)
  else:
      pygame.draw.rect(screen, (0, 128, 0), (width // 2 + total[0] * mulitplier, height // 2, abs(total[0]) * mulitplier, 20), 0)

  if total[1] > 0:
    pygame.draw.rect(screen, (128, 0, 0), (width // 2, height // 2, 20, total[1] * mulitplier), 0)
  else:
    pygame.draw.rect(screen, (128, 0, 0), (width // 2, height // 2 + total[1] * mulitplier, 20, abs(total[1]) * mulitplier), 0)

  
  pygame.display.flip()
  fpsClock.tick(fps)

def main():
    multipler = 1 # Multiplier to how fast the mouse works
    read_time = 250 # How long the serial reads for (in ms)
    input_stream = "" # Input buffer
    previous_mouse_clicks = [False, False] # For holding the previous values of the left/right mouse buttons


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
        output_loop(total)

main()