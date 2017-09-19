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

# Length of time in seconds to sleep between status checks
SLEEP_TIME = 0.1

VALID_ACTIONS = ['available', 'busy', 'disturbable', 'finding', 'party', 'alert', 'offline']

class StatusChangedException(Exception):
    """Raised when status changes during sleep state"""
    pass


def custom_sleep(duration, holder_status):
    """custom_sleep to allow to check for change in status while sleeping"""
    count = int(duration/SLEEP_TIME)
    for x in range(0, count+1):
        time.sleep(SLEEP_TIME)
        if status.get_status() != holder_status:
            raise StatusChangedException("Changed from {}".format(holder_status))


def single_led(current_led, r, g, b, brightness):
    """Set color of singe led - base function"""
    if current_led < LED_MIN or current_led > LED_MAX:
        # Check to see if selected light actually exists on Blinkt
        return False
    set_pixel(current_led,r,g,b,brightness)


def trace(current_led, r, g, b, direction):
    """Backwards and forwards animation of lights"""
    clear()
    if direction == "forwards":
        # Three lights on at once, front light is brighter than back light
        single_led(current_led,r,g,b,1)
        single_led(current_led - 1,r,g,b,0.5)
        single_led(current_led - 2,r,g,b,0.1)
    else:
        # Inverts the direction of the three lights
        single_led(current_led,r,g,b,1)
        single_led(current_led + 1,r,g,b,0.5)
        single_led(current_led + 2,r,g,b,0.1)
    show()


def led_line(interval, brightness, led, r, g, b, holder_status):
    """Cause the lights to travel in a line and have brightness close to the normal distribution."""
    if led == 0 or led == 7:
        clear()
        set_pixel(led, r, g, b, (brightness / 20.0))
        show()
        custom_sleep(interval, holder_status)
        
    elif led == 1 or led == 6:
        clear()
        set_pixel(led, r, g, b, (brightness / 10.0))
        show()
        custom_sleep(interval, holder_status)
        
    elif led == 2 or led == 5:
        clear()
        set_pixel(led, r, g, b, (brightness / 5.0))
        show()
        custom_sleep(interval, holder_status)
        
    elif led == 3 or led == 4:
        clear()
        set_pixel(led, r, g, b, brightness)
        show()
        custom_sleep(interval, holder_status)
        

def flashing(r, g, b, number_of_flashes, time_gap, holder_status):
    """Make lights to flash"""
    for x in range(number_of_flashes):
        set_all(r, g, b, 1)
        show()
        custom_sleep(time_gap, holder_status)
        clear()
        show()
        custom_sleep(time_gap / 1.3, holder_status)


def solid_colour(r,g,b, holder_status):
    """Show a solid_colour beginning with LED_line animation"""
    custom_sleep(1, holder_status)
    for x in range(8):
        led_line(0.08, 1.0, x, r, g, b, holder_status)
    for x in range (7,-1,-1):
        led_line(0.08, 1.0, x, r, g, b, holder_status)
    clear()
    set_all(r, g, b, 0.1)
    show()


def animation(r,g,b, holder_status):
    """Coherent backwards and forwards animation using trace function"""
    custom_sleep(0.5, holder_status)
    while True:
        for x in range(-2,10):
            trace(x, r, g, b, "forwards")
            custom_sleep(0.25, holder_status)
        for x in range(7, -3, -1):
            trace(x, r, g, b, "backwards")
            custom_sleep(0.25, holder_status)

    flashing(r, g, b, 2, 0.5, holder_status)
    set_all(r, g, b, 1)
    show()
    custom_sleep(1.5, holder_status)
    clear()
    show()


def party(loop_count, holder_status):
    """Lights randomly appear with random colours"""
    previous_led = 8
    # Party forever...
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
        custom_sleep(0.05, holder_status)
        trace(led, red, green, blue, 'forward')
    flashing(red, green, blue, 2, 0.1, holder_status)
    clear()


def alert(r, g, b, holder_status):
    """Consistent pulse"""
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
            custom_sleep(0.3, holder_status)
        elif brightness >= 0.9:
            custom_sleep(0.3, holder_status)
        else:
            custom_sleep(0.05, holder_status)
            

def error():
    """Respond to errors"""
    print("Error")
    set_all(255, 255, 255, 0.2)


def show_status(new_status):
    """Respond to a status"""
    if new_status not in VALID_ACTIONS:
        raise Exception("Invalid status: {}".format(new_status))

    print ("New status: " + new_status)
    options = {
        "available": [solid_colour, AVAILABLE_COLOR],
        "busy": [solid_colour, BUSY_COLOR],
        "disturbable": [solid_colour, DISTURBABLE_COLOR],
        "finding": [animation, FINDING_COLOR],
        "party": [party, PARTY_LOOP_COUNT],
        "alert": [alert, ALERT_COLOR]
    }

    # TODO: Refactor this so that it doesn't require special knowledge of the actions
    if new_status == "party":
        count = options[new_status][1]
        options[new_status][0](count, new_status)
    elif status == "offline":
        clear()
        set_all(0, 0, 0, 0)
        show()
        print("stopping")
    else:
        color = options[new_status][1]
        options[new_status][0](color[0], color[1], color[2], new_status)


def status_loop():
    """This will constantly check to see if status has changed"""
    current_status = status.get_status()

    show_status(current_status)
    while True:
        try:
            custom_sleep(1, current_status)
            show_status(current_status)

            # previous_status = current_status
            # current_status = status.get_status()
            # if current_status != previous_status:
            #    show_status(current_status)
        except StatusChangedException as e:
            print e.message
            show_status(status.get_status())
        except Exception as e:
            print (e)


if __name__ == "__main__":
    status_loop()
