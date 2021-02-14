# README:



## <u>About</u>

For this project, I built a mock console with a RPG game on it, controlled by a physical controller containing the ESP-32. The mock console, built from legos, contains the Raspberry Pi, augmented with some heat sinks and fans that I ripped from old computers. The controller is comprised of an ESP-32, connected to four controller components: 2 push buttons, 1 STPS switch, and 1 joystick. (I did all the animations by hand). In my game, you plait y as a knight trying to fend off slimes and various enemies which progressively get more aggressive and intelligent after each round of killing. This game allows for the switching of difficulties (AI activated ) via the STPS switich.

Demo of the Game itself:

Demo of the entire system:



## <u>Installation/Setup</u>

### Program Installations

1. Clone this github repo

   ```
   git clone https://github.com/bnhwa/PI_RPG.git
   ```

   

2. pygame and tkinter libraries need to be installed. On the raspberry pi (versions 3b+ and 4), you can do this with pip3 (if you have pip for older versions of the pi or a regular computer use it instead)

   ```
   pip install pygame
   pip install tk
   
   ```

   ### For the Pi Specifically (if you want to use the controller): 

   1. Installing Arduino: if you don't have Arduino on the Pi, go to [here](https://www.arduino.cc/en/software) and download the latest version of the Linux 32-bit ARM. 

      1. Once you have the Zip downloaded, go to the directory you want to install it in, extract it, then go into that folder via the commandline and run

         ```
         ./install
         ```

         

      2. Open the Arduino IDE and follow the instructions [here](https://randomnerdtutorials.com/getting-started-with-esp32/) to configure Arduino for the ESP32 and download the ESP32 board configuration. Once this is done, select board "ESP32 Wrover module"

   2. Then, plug in the controller usb to the computer, and see if a new serial port appears. If none appears, use the default given. Check settings.txt and change `serial` to the USB port that will be used

      ```
      serial=<yourport>
      fullscreen=2
      ```

   3. If you are on the Pi, using a monitor with screen resolution greater than (1534,732), set `fullscreen=2` for performance purposes


### Hardware Setup (If you want to use the Controller)

1. Connect the controller USB to the ESP32

2. Open the Arduino IDE, upload `controller_module.pde` to the controller

   

## <u>Running</u> (on any computer)

### If you want to use the Controller:

Go to the directory of `game.py` and run `python game_pi.py` Voila.

1. If you are on the Pi, run `sudo python game_pi.py`

### If you want to just play the game using standard keyboard controls:

Go to the directory of `game.py` and run `python game.py` Voila.

If you want to change screen resolution, set by default to fullscreen, go to `settings.txt` which is in the same directory and write

```
fullscreen=1
```

