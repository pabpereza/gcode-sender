## Picamera based QR code reader on a Raspberry Pi 3

This guide will show you how to create a QR code reader by using the `zbarlight` python library and `picamera` to take the picture. We will not be using `open cv` or any other image processing libraries. 

### What you'll need

* Raspberry Pi 2 / 3
* MicroSD Card with Raspbian on it ([Tutorial](https://github.com/rijinmk/guide-to-install-any-os-terminal-rpi3))
* A picamera module (like [this](https://www.raspberrypi.org/products/camera-module-v2/))
* Micro USB cable
* Keyboard, Mouse, Monitor
* HDMI cable for the monitor

If you are using the Raspberry Pi headless (Without a monitor, keyboard or mouse), You will need to connect to the internet using the ethernet port (for Raspberry Pi 2) or through the Wifi (on a Raspberry Pi 3 [[Tutorial](https://github.com/rijinmk/guide-to-wifi-terminal-rpi3)] ) and then you will have to use [SSH](https://github.com/rijinmk/guide-to-ssh-rpi3) to connect to your Raspberry Pi. 

### Installation process 

Here onwards everything will be on the terminals. Press `CTRL + ALT + T` to open up the terminals. 

#### STEP 1 - Initial installations

 The apt-get must always be kept updated. 

```bash 
sudo apt-get update -y && sudo apt-get upgrade -y
```

This will take some time depending on your internet speed and also the amount of package's that are installed onto your Raspberry Pi's OS.

#### STEP 2 - Installing and running `picamera` 

You will need to install this to access the picamera hardware python. To install this you will need to use `apt-get`. 

```bash
sudo apt-get install python-picamera python3-picamera
```

This will install picamera module for using Picamera hardware from python

 

#### STEP 3 - Installing `zbarlight`

This is the brain of our QR code reader. This library helps us to decode an image into their basic codes. 

First we have to install the following: 

```bash
sudo apt-get install libzbar0 libzbar-dev
```

Then we have to install the `zbarlight`

```bash 
sudo pip install zbarlight
```

After this you can run the `reader.py` python program that I have written to test if it works. It will first save capture 'foo.jpg' using picamera and then will attempt to read QR code from the same image.
This `reader.py` program does the following: 

* Runs get_image function to capture 'foo.jpg' using PiCamera
* Checks if it has QR Codes 
* Prints qr code information if available
* If there is no QR code present after we run it through `zbarlight` then 'No QR code found' message will be printed 


If you want to run the code enter

```bash
sudo python reader.py
```

*Credits:*  
Major thanks to the original contributor of this:  
https://github.com/rijinmk

*Reference:*  
https://github.com/rijinmk/code-qr-code-reader-rpi3



