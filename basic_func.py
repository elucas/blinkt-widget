import time
from blinkt import set_clear_on_exit, clear, set_all, show, set_pixel
import status
from functools import wraps

LED_MIN = 0
LED_MAX = 7
# Blinkt highest and lowest lights

# Length of time in seconds to sleep between status checks
SLEEP_TIME = 0.1

# User-callable functions get added to this dict using @expose decorator below
EXPOSED_FUNCTION_DICT = {}

set_clear_on_exit(False)


def expose(f):
    """Decorator used to select which functions can be called"""

    @wraps(f)
    def wrapper(*args, **kwds):
        return f(*args, **kwds)

    EXPOSED_FUNCTION_DICT[f.__name__] = f
    return wrapper


class StatusChangedException(Exception):
    """Raised when status changes during sleep state"""
    pass


def custom_sleep(duration, current_status):
    """custom_sleep to allow to check for change in status while sleeping"""
    count = int(duration / SLEEP_TIME)
    for x in range(0, count + 1):
        time.sleep(SLEEP_TIME)
        new_status = status.get_status(current_status)
        if new_status != current_status:
            raise StatusChangedException(new_status)


def single_led(current_led, r, g, b, brightness):
    """Set color of singe led - base function"""
    if current_led < LED_MIN or current_led > LED_MAX:
        # Check to see if selected light actually exists on Blinkt
        return False
    set_pixel(current_led, r, g, b, brightness)


def trace(current_led, r, g, b, direction):
    """Backwards and forwards animation of lights"""
    clear()
    if direction == "forwards":
        # Three lights on at once, front light is brighter than back light
        single_led(current_led, r, g, b, 0.1)
        single_led(current_led - 1, r, g, b, 0.5)
        single_led(current_led - 2, r, g, b, 1)
    else:
        # Inverts the direction of the three lights
        single_led(current_led, r, g, b, 1)
        single_led(current_led + 1, r, g, b, 0.5)
        single_led(current_led + 2, r, g, b, 0.1)
    show()


def led_line(interval, brightness, led, r, g, b, current_status):
    """Cause the lights to travel in a line
	and have brightness close to the normal distribution."""
    if led == 0 or led == 7:
        clear()
        set_pixel(led, r, g, b, (brightness / 20.0))
        show()
        custom_sleep(interval, current_status)

    elif led == 1 or led == 6:
        clear()
        set_pixel(led, r, g, b, (brightness / 10.0))
        show()
        custom_sleep(interval, current_status)

    elif led == 2 or led == 5:
        clear()
        set_pixel(led, r, g, b, (brightness / 5.0))
        show()
        custom_sleep(interval, current_status)

    elif led == 3 or led == 4:
        clear()
        set_pixel(led, r, g, b, brightness)
        show()
        custom_sleep(interval, current_status)


def flashing(r, g, b, number_of_flashes, time_gap, current_status):
    """Make lights to flash"""
    for x in range(number_of_flashes):
        set_all(r, g, b, 1)
        show()
        custom_sleep(time_gap, current_status)
        clear()
        show()
        custom_sleep(time_gap / 1.3, current_status)


def solid_colour(r, g, b, current_status):
    """Show a solid_colour beginning with LED_line animation"""
    custom_sleep(1, current_status)
    for x in range(8):
        led_line(0.08, 1.0, x, r, g, b, current_status)
    for x in range(7, -1, -1):
        led_line(0.08, 1.0, x, r, g, b, current_status)
    clear()
    set_all(r, g, b, 1.0)
    show()


def animation(r, g, b, current_status):
    """Coherent backwards and forwards animation using trace function"""
    custom_sleep(0.5, current_status)
    while True:
        for x in range(-2, 10):
            trace(x, r, g, b, "forwards")
            custom_sleep(0.25, current_status)
        for x in range(7, -3, -1):
            trace(x, r, g, b, "backwards")
            custom_sleep(0.25, current_status)

    flashing(r, g, b, 2, 0.5, current_status)
    set_all(r, g, b, 1)
    show()
    custom_sleep(1.5, current_status)
    clear()
    show()


def custom_alert(r, g, b, current_status):
    """Consistent pulse"""
    clear()
    brightness = 0.0
    direction = True
    running = True
    while running:
        if direction:
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
        if brightness == 0.0:
            custom_sleep(0.3, current_status)
        elif brightness >= 0.9:
            custom_sleep(0.3, current_status)
        else:
            custom_sleep(0.05, current_status)


def get_exposed_function_names():
    return EXPOSED_FUNCTION_DICT.keys()


def is_exposed(unknown_status):
    return unknown_status in EXPOSED_FUNCTION_DICT


def show_status(new_status):
    """Respond to a status"""
    if not is_exposed(new_status):
        raise Exception("Invalid status: {}".format(new_status))

    print("New status: " + new_status)
    # !MAGIC HAPPENS HERE!
    EXPOSED_FUNCTION_DICT[new_status](new_status)


def status_loop(default):
    """Constantly check to see if status has changed"""
    current_status = status.get_status(default)
    new_status = current_status
    while True:
        try:
            if new_status:
                current_status = new_status
                new_status = None
                show_status(current_status)

            custom_sleep(1, current_status)
        except StatusChangedException as e:
            print
            e.message
            new_status = e.message
        except Exception as e:
            print(e)


def callable_statuses():
    callable_statuses_list = []

    for item in EXPOSED_FUNCTION_DICT:
        callable_statuses_list.append(item)
    return callable_statuses_list
