import time
import random
from blinkt import set_all, clear, show, set_brightness, set_pixel
import status

LED_MIN = 0
LED_MAX = 7
#Blinkt highest and lowest lights

AVAILABLE_COLOR = [0, 255, 0]
BUSY_COLOR = [255, 0, 0]
DISTURBABLE_COLOR = [94, 18, 0]
FINDING_COLOR = [0, 0, 255]
ALERT_COLOR = [200, 3, 8]
PARTY_LOOP_COUNT = 10
#CONSTANTS




#customSleep to allow to check for change in status while sleeping
def customSleep( duration, holderStatus ):
    count = int(duration/0.01)
    for x in range(0, count+1):
        time.sleep(0.01)
        if status.get_status() != holderStatus:
             raise Exception("Status changed")

#set color of singe led - base function 
def single_led(current_led, r,g,b, brightness):
    if current_led < LED_MIN or current_led > LED_MAX:
        #check to see if selected light actually exists on Blinkt
        return False
    set_pixel(current_led,r,g,b,brightness)

#backwards and forwards animation of lights
def trace(current_led,r,g,b,direction):
    clear()
    if direction == "forwards":
        #three lights on at once, front light is brighter than back light
        single_led(current_led,r,g,b,1)
        single_led(current_led - 1,r,g,b,0.5)
        single_led(current_led - 2,r,g,b,0.1)
    else:
        #inverts the direction of the three lights
        single_led(current_led,r,g,b,1)
        single_led(current_led + 1,r,g,b,0.5)
        single_led(current_led + 2,r,g,b,0.1)
    show()

#cause the lights to travel in a line
#and have brightness close to the normal distribution.
def LED_line(interval,brightness,led,r,g,b, holderStatus):
    if led == 0 or led == 7:
        clear()
        set_pixel(led,r,g,b,(brightness / 20.0))
        show()
        customSleep(interval, holderStatus)
        
    elif led == 1 or led == 6:
        clear()
        set_pixel(led,r,g,b,(brightness / 10.0))
        show()
        customSleep(interval, holderStatus)
        
    elif led == 2 or led == 5:
        clear()
        set_pixel(led,r,g,b,(brightness / 5.0))
        show()
        customSleep(interval, holderStatus)
        
    elif led == 3 or led == 4:
        clear()
        set_pixel(led,r,g,b,brightness)
        show()
        customSleep(interval, holderStatus)
        
#make lights to flash
def flashing(r,g,b,number_of_flashes,time_gap, holderStatus):
    for x in range(number_of_flashes):
        set_all(r,g,b,1)
        show()
        customSleep(time_gap, holderStatus)
        clear()
        show()
        customSleep(time_gap / 1.3, holderStatus)

#show a solid_colour beginning with LED_line animation
def solid_colour(r,g,b, holderStatus):
    customSleep(1, holderStatus)
    for x in range(8):
        LED_line(0.08,1.0,x,r,g,b, holderStatus)
    for x in range (7,-1,-1):
        LED_line(0.08,1.0,x,r,g,b, holderStatus)
    clear()
    set_all(r,g,b,0.1)
    show()

#coherent backwards and forwards animation using trace function
def animation(r,g,b, holderStatus):
    customSleep(0.5, holderStatus)
    for y in range(3):
        for x in range(-2,10):
            trace(x,r,g,b,"forwards")
            customSleep(0.25, holderStatus)
        if y != 2:
            for x in range (7,-3,-1):
                trace(x,r,g,b,"backwards")
                customSleep(0.25, holderStatus)
    flashing(r,g,b,2,0.5, holderStatus)
    set_all(r,g,b,1)
    show()
    customSleep(1.5, holderStatus)
    clear()
    show()

#lights randomly appear with random colours
def party(loop_count, holderStatus):  
    previous_led = 8
    #for x in range(loop_count * 20):
    #party forever...
    while True:
        for x in range(2):
            difference = False
            led = random.randint(0,7)
            red = random.randint(0,255)
            green = random.randint(0,255)
            blue = random.randint(0,255)
            while difference == False:
                if previous_led == led:
                    led = random.randint(0,7)
                    difference = False
                else:
                    difference = True
            single_led(led,red,green,blue,0.5)
            show()
        clear()
        customSleep(0.05, holderStatus)
        trace(led,red,green,blue,'forward')
    flashing(red, green, blue, 2, 0.1, holderStatus)
    clear()

#consistent pulse
def alert(r, g, b, holderStatus):
    clear()
    brightness = 0.0
    direction = True
    running = True
    while running:
        if direction == True:
            brightness += 0.1
            if brightness >= 0.9:
                direction = False
        else:
            if brightness > 0.15: 
                brightness -= 0.1
            else:
                brightness = 0.0
            if brightness <= 0.000001:
                direction = True
        set_all(r, g, b, brightness)
        show()
        print (brightness)
        if brightness == 0.0:
            customSleep(0.3, holderStatus)
        elif brightness >= 0.9:
            customSleep(0.3, holderStatus)
        else:
            customSleep(0.05, holderStatus)
            
#respond to errors   
def error():
    print("Error")
    set_all(255, 255, 255, 0.2)

#respond to a status
def show_status(status):
      print ("New status: " + status)
      options = {"available" : [solid_colour, AVAILABLE_COLOR],
                 "busy" : [solid_colour, BUSY_COLOR],
                 "disturbable" : [solid_colour, DISTURBABLE_COLOR],
                 "finding" : [animation, FINDING_COLOR],
                 "party" : [party, PARTY_LOOP_COUNT],
                 "alert" : [alert, ALERT_COLOR]
          }

      if status == "party" :
          count = options[status][1]
          options[status][0](count, status)
      elif status == "offline":
          clear()
          set_all(0, 0, 0, 0)
          show()
          print("stopping")
      else:
          color = options[status][1]
          options[status][0](color[0], color[1], color[2], status)


def status_loop():
    #this will constantly check to see if status has changed
    current_status = status.get_status()
    show_status(current_status)
    while True:
        try:
            #time.sleep(1)
            previous_status = current_status
            current_status = status.get_status()
            if current_status != previous_status:
                show_status(current_status)
        except Exception as e:
            print (e)
        
status_loop()
