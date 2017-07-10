import time
import random
from blinkt import set_all, clear, show, set_brightness, set_pixel
import status

LED_MIN = 0
LED_MAX = 7
#Blinkt highest and lowest lights


#different light patterns
def single_led(current_led, r,g,b, brightness):
    if current_led < LED_MIN or current_led > LED_MAX:
        #check to see if selected light actually exists on Blinkt
        return False
    set_pixel(current_led,r,g,b,brightness)
    
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
    
def LED_line(interval,brightness,led,r,g,b):
    if led == 0 or led == 7:
        #dim at ending lights
        clear()
        set_pixel(led,r,g,b,(brightness / 12))
        show()
        time.sleep(interval)
    elif led == 1 or led == 6:
        clear()
        set_pixel(led,r,g,b,(brightness / 8))
        show()
        time.sleep(interval)
    elif led == 2 or led == 5:
        clear()
        set_pixel(led,r,g,b,(brightness / 4))
        show()
        time.sleep(interval)
    elif led == 3 or led == 4:
        #brighter in the middle lights
        clear()
        set_pixel(led,r,g,b,brightness)
        show()
        time.sleep(interval)

def flashing(r,g,b,number_of_flashes,time_gap):
    # make the lights flash
    for x in range(number_of_flashes):
        set_all(r,g,b,1)
        show()
        time.sleep(time_gap)
        clear()
        show()
        time.sleep(time_gap / 1.3)

def solid_colour(r,g,b):
    #lights go side to side then solid when called
    time.sleep(1)
    for x in range(8):
        LED_line(0.12,1,x,r,g,b)
    for x in range (7,-1,-1):
        LED_line(0.12,1,x,r,g,b)
    clear()
    set_all(r,g,b,0.1)
    show()
    
def animation(r,g,b):
    #lights animate when called
    time.sleep(0.5)
    for y in range(3):
        for x in range(-2,10):
            trace(x,r,g,b,"forwards")
            time.sleep(0.25)
        if y != 2:
            for x in range (7,-3,-1):
                trace(x,r,g,b,"backwards")
                time.sleep(0.25)
    flashing(r,g,b,2,0.5)
    set_all(r,g,b,1)
    show()
    time.sleep(1.5)
    clear()
    show()

def party(time_to_last_for):
    #lights randomly appear with random colours
    previous_led = 8
    for x in range(time_to_last_for * 20):
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
        time.sleep(0.05)
        trace(led,red,green,blue,'forward')
    flashing(red,green,blue,2,0.1)
    clear()

def error():
    #lights flash red 8 times when called
    print("Error")
    flashing(255,0,0,8,0.25)


def show_status():
    global previous_status 
    current_status = status.get_status()
    status_name = current_status['name']
    for array in status.STATUSES:
        if array == status_name:
            light_type = current_status['lights']            
            if current_status['monocolour'] == 'no':
                length = current_status['length']
                globals()[light_type](length)
            else:
                r = current_status['red']
                g = current_status['green']
                b = current_status['blue']
                globals()[light_type](r,g,b)
    previous_status = current_status

def status_loop():
    #this will constantly check to see if status has changed
    show_status()
    global previous_status
    while True:
        if status.get_status() != previous_status:
            #only change lights if status has changed
            show_status()

status_loop()
