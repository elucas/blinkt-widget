# blinkt-widget
RasPi Blinkt IoT widgetry - Ongoing project used with work-experience students

Web-controlled status indicator built on top of the Blinkt HAT and library
* https://github.com/pimoroni/blinkt
* https://shop.pimoroni.com/products/blinkt

== Components
* Status demon - Blinkt wrapper
* Flask app to control getting/setting state


### Setup crontab to start scripts on boot
crontab is a background process which allows you to execute scripts at specific times

1. Create launcher.sh file in same dir and add the following lines:

```
#!/bin/sh
# launcher.sh
# navigate to home directory, then to this directory, then execute python script, then back home

cd /
cd home/pi/bbt
sudo python bbt.py
cd /
```

2. Make it an executable by typing "chmod 755 launcher.sh" in terminal

3. Edit crontab using terminal:

```
sudo crontab -e
@reboot sh /home/pi/YOURDIRECTORY/launcher.sh
```

### Notes:
+ Please read the license
+ This project can be placed in any directory
+ This is not the finished product so there will be bugs!


### Getting Started!
1. Run dashboard.py
2. Visit localhost:5000 in any browser to edit your status! If they are reported as missing, make sure they are powered up.
3. Look at demo.py and basic_func.py to create a new function in demo.py

## Avahi
* Install "avahi-utils": `sudo apt-get install avahi-utils`
* Copy `blinkt.service` to `/etc/avahi/services`

## Hooking up a new device
1. Download Raspbian
2. Put the micro SD card in the USB reader and plug it in to the back of the Ubuntu computer
3. Use Etcher to burn Raspbian to the SD card
4. BEFORE BOOTING: Copy the ssh and wpa_supplicant.conf (AFTER EDITING IT) files to the /boot drive
5. Put the micro SD card into the pi and plug it into power - let it boot up. Give it a couple minutes.
6. Put the SD card back in the USB reader and transfer api.py, basic_func.py, status.py and either lightswitch.py or demo.py to /home/pi/yourfolderhere
7. Copy blinkt.service to /etc/avahi/services
8. Put the SD card into the pi and plug it in
9. Open terminal, type ssh pi@raspberrypi and then cd /etc/hostname and then sudo nano hostname and change raspberrypi to something like blinkt4
10. Also in terminal, do crontab -e and add these lines:
```
@reboot python /home/pi/yourfolderhere/api.py
@reboot python /home/pi/yourfolderhere/demo.py (OR lightswitch.py, depending on which one you picked)
```

## What all the different files do
api.py talks to dashboard.py and tells it the device's current status, found from status.py. What it does during this status is defined by demo.py (or whatever you decide to call it; there's another called lightswitch.py). You will find multiple 'building block' processes in basic_func.py. blinkt.service announces the device as a blinkt service to avahi.py, which tells dashboard.py the locations of api.py. ssh and wpa_supplicant.conf are to be copied to the boot drive of the SD card before you boot it up for the first time. 
The bin folder contains the git-hooks folder which contains the pre-commit folder which contains the shell files: install-git-hooks.sh, pre-commit-runner.sh, and python-flake8.  These three files are designed to compare an changes in this repo to pep8 standards, before they are committed.
The install-get-hooks.sh file makes a symbolic link between the repo files and the git hooks folder, so that all python files can checked against every type of relevant hook.
The pre-commit-runner.sh file iterates through every file in the repo, and compare
