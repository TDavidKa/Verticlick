# Verticlick
### The Mouse of The Future :)

## What This Is

The average computer mouse as we know it was a solution to an important need in computing. It is an impressive landmark of
computer development, allowing for even more interactivity between users and their devices. However, it is not the perfect
hardware device- it is a source of repetitive stress on our wrists, which can cause issues such as carpal tunnel and radial
wrist pain. In response, alternatives such as trackpads and ergonomic mice were developed, to allow users to have a more
natural resting position for their hand while using a computer. Track pads do help with repetitive stress by replacing wrist 
movement with finger movement, but they lose out on accuracy and functionality. On the other hand, while ergonomic mice are 
still new, and often advertised as an office device, they give back that accuracy while solving the traditional wrist pain 
problems. The main problem is that they are not extended for groups such as gamers or developers who often require a numpad for 
productivity on the side of their mouse.

As a response, our team has produced Verticlick, an advanced ergonomic mouse with additional features. Similar to ‘mmo’ or 
‘gaming’ mice, we have added a numpad to the side of our ergonomic mouse, to appeal to those aforementioned groups. Both 
ergonomic and traditional mice have pros and cons, such as the pros of functionality versus the cons of wrist stress in the 
traditional mouse. With our product, we aim to combine the pros of both, while alleviating their cons. We would like to 
evaluate the mouse’s success in two ways: Ease of switching to this mouse over the traditional mouse, and reduction of 
repetitive movements.


## What You Need
- Adafruit Circuit Playground Bluefruit (https://www.adafruit.com/product/4333)
- A USB-A to MicroUSB connector
- A Mac or Windows device with a USB-A port
- Arduino IDE

## Included Files
- main.py
     - the file to be run on the user's device to run mouse movements
- Verticlick.ino
     - the file inputted into the Bluefruit device via Arduino IDE
- Anker MX Vertical Mouse - 6259427
     - files to 3d print a mouse casing, from https://www.thingiverse.com/thing:6259427
     - includes Battery Cover, Body, Bottom, and Button
 
## How to Use
1. Plug in your Adafruit Circuit Playground Bluefruit into your device
2. Open Verticlick.ino in the Arduino IDE
   (If you have previously set up an Adafruit Circuit Playground Bluefruit device, skip to step 2F)
     A. Go to File -> Preferences -> Additional Boards Manager URLs and input the following link:
        https://adafruit.github.io/arduino-board-index/package_adafruit_index.json
     B. In the Boards Manager tab (from the side menu), install the "Adafruit nRF52" package
     C. Go to Tools -> Board -> Adafruit nRF52 -> Adafruit Circuit Playground Bluefruit
     D. Go to Tools -> Programmer -> Bootloader DFU for Bluefruit nRF52
     E. Go to Tools -> Burn Bootloader
     F. Double tap the "reset" button on the Bluefruit. This should make the LEDs turn green
     G. Make sure the Bluefruit device is connected via the "Select Board and Port" menu
     H. Select "upload"
3. Run main.py
   Note: you may have to modify the COM port manually, depending on your device
4. Enjoy!

## Functions
- Move the Bluefruit device around on a flat surface to control your device's mouse
- Click the left and right buttons on the Bluefruit to left and right click buttons, respectively

## Known Issues
- Mouse movement is slow and clunky
- Will entirely crash the python file if unplugged
