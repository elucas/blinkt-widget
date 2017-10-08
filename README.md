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
+ This is not the finish product so there will be bugs!


### Getting Started!
1. Run webpage.py & blinkt_status_display.py
2. Visit [pi_local_ip_address]:5000 in any browser to edit your status!
3. You can use any password for the first time you login (but make sure you remember it! - otherwise clear the blinkt_hash file and it will reset)

## Avahi
* Install "avahi-utils": `sudo apt-get install avahi-utils`
* Copy `blinkt.service` to `/etc/avahi/services`
