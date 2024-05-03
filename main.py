import serial, pyautogui
from termcolor import colored

import sys, time
 
import pygame
from pygame.locals import *
 
pygame.init()
 
fps = 60
fpsClock = pygame.time.Clock()
 
width, height = 1000, 800
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('This is totally a processing window')

pygame.font.init() 
my_font = pygame.font.SysFont('Arial', 30)
title_font = pygame.font.SysFont('Arial', 60)


try: 
    ser = serial.Serial("/dev/cu.usbmodem1421201", 9600) 
except Exception as e:
    print(e)
    ser = serial.Serial("COM6", 9600)


import multiprocessing
class WebAppMProcess(multiprocessing.Process):

    def __init__(self, port=2204, **kwargs):
        
        self.ns = multiprocessing.Manager().Namespace()
        ns_event = multiprocessing.Event()
        import flirapp
        super().__init__(target=flirapp.app_mworker, args=(self.ns, ns_event, port), **kwargs)
        self.flir_mdata = flirapp.FlirNodeMData(self.ns, ns_event)
        self.port = port


def get_input(input_stream, base_calibration):
    # Gets any data packages found in the input buffer
    total = [0, 0, 0]
    extra_parameters = {"LeftClick": 0, "RightClick": 0}

    while "{" in input_stream and "}" in input_stream: #Complete Data Package Found
        
        try:
          # Remove any extra data
          input_stream = input_stream[input_stream.index("{"):]

          # Find all relevant data
          data = input_stream[:input_stream.index("}") + 1]


          # Use the data
          x, y, l, r, z = *map(float, data[1:-1].split(",")),

          extra_parameters["LeftClick"] = l
          extra_parameters["RightClick"] = r
      
          total[0] += x - base_calibration[0]
          total[1] += y - base_calibration[1]
          total[2] += z - base_calibration[2]

          if base_calibration == [0,0,0]:
            base_calibration = total[:]


          # Remove from the stream
          input_stream = input_stream[input_stream.index("}") + 1:]
        except Exception:
          input_stream = ""
          return input_stream, total, extra_parameters, base_calibration

    return input_stream, total, extra_parameters, base_calibration

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
    
import math
knob = pygame.image.load("knob.png")
bg = pygame.image.load("temp.jpg")
def output_loop(total):
 
  screen.fill((50, 50, 50))
  # screen.blit(pygame.transform.scale(bg, (width, height)), (0, 0))
  
  for event in pygame.event.get():
    if event.type == pygame.QUIT:
      pygame.quit()
      sys.exit()


  text_surface = title_font.render(f'Mouse Controlling Demo', False, (255, 255, 255))
  screen.blit(text_surface, (150,25))
  
  x, y, z = 0,1,2

 
  screen.blit(pygame.transform.scale(knob, (400, 400)), (100, height // 2 - 200))
  if total[0] != 0 or total[1] != 0:
    center = [300, height // 2]
    
    angle = math.atan2(total[1], total[0])
    length = 175

    # Calculate the endpoint coordinates
    end_x = center[0] + length * math.cos(angle)
    end_y = center[1] - length * math.sin(angle)
    # Draw the line
    pygame.draw.line(screen, (128,0,0), center, (end_x, end_y), 5)
    # Draw a point at the end of the line
    pygame.draw.circle(screen, (128,0,0), (int(end_x), int(end_y)), 10)
  else:
     pygame.draw.circle(screen, (128, 0, 0), (300, height // 2), 10)

  mulitplier = 1
  movement = abs(total[0]) + abs(total[1])
  color = (0, 128, 0)
  
  if movement > 100:
     color = (128, 128, 0)
  if movement > 200:
     color = (128, 0, 0)
    
  pygame.draw.rect(screen, color, (width - 200, height // 2 - 150, 50, min(300, int(abs(movement * mulitplier)))))

  
  for i in range(3):
    text_surface = my_font.render(f'{"XYZ"[i]}: {round(total[i], 2)}', False, (255, 255, 255))
    screen.blit(text_surface, (200 + i * 250,height - 100))

  
  pygame.display.flip()
  fpsClock.tick(fps)

def main():
    multipler = 1 # Multiplier to how fast the mouse works
    read_time = 250 # How long the serial reads for (in ms)
    input_stream = "" # Input buffer
    previous_mouse_clicks = [False, False] # For holding the previous values of the left/right mouse buttons
    base_calibration = [0, 0, 0]
    x, y = 500, 500
    frame_id = 0

    while True:
        # Get new information from the serial connection
        new_packets = ser.read(read_time).decode("utf-8")

        # Add new data to buffer
        input_stream += new_packets 
      

        # Get any current packets from the buffer
        input_stream, total, extra_parameters, base_calibration = get_input(input_stream, base_calibration) 

        
           
        
        # Handle left click / right click functionality
        handle_mouse_clicks(extra_parameters["LeftClick"], extra_parameters["RightClick"], previous_mouse_clicks)

        # Removing values of low movement
        # print(total[2])
        # total[2] -= 120

        total = [item * 20 for item in total]

        if total[1] < 0: total[1] *= 2
        if total[0] < 0: total[0] *= 2
        
        total = [0 if abs(total[i]) < 40 or abs(total[i]) > 1200 else total[i] for i in range(3)]    

        # Moving the mouse
        x += total[0] * multipler
        y += total[1] * multipler

        pyautogui.move(x * 0.5, y * 0.5)
        x, y = x * 0.5, y*.5

        webapp_mprocess.flir_mdata.update(frame_id, time.perf_counter(), {"x": total[0], "y": total[1], "z": total[2], "leftClick": extra_parameters["LeftClick"], "rightClick": extra_parameters["RightClick"]})
        frame_id += 1
        

        # Printing debug output
        #debug_output(total)
        output_loop(total)

if __name__ == "__main__":
  webapp_mprocess = None


  webapp_mprocess = WebAppMProcess()
  print("Starting webapp process...")
  webapp_mprocess.start()
  try:
    main()

  finally:
    if webapp_mprocess is not None:
                
      print("Terminating webapp process...")
      webapp_mprocess.terminate()
      webapp_mprocess.join(timeout=5.0)
      
      if webapp_mprocess.is_alive():
          print("Could not terminate webapp, killing...")
          webapp_mprocess.kill()
          webapp_mprocess.join(timeout=5.0)

      if webapp_mprocess.is_alive():
          print("Could not terminate webapp process!")
      else:
          print("Done terminating webapp process.")