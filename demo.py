import basic_func
import status
from blinkt import clear, show
import random


@basic_func.expose
def partying(current_status):
    """Lights randomly appear with random colours"""
    previous_led = 8
    # Party forever...
    while True:
        for x in range(2):
            led = random.randint(0, 7)
            red = random.randint(0, 255)
            green = random.randint(0, 255)
            blue = random.randint(0, 255)
            while previous_led == led:
                led = random.randint(0, 7)
            basic_func.single_led(led, red, green, blue, 0.5)
            show()
    clear()
    basic_func.custom_sleep(0.05, current_status)
    basic_func.trace(led, red, green, blue, 'forward')
    basic_func.flashing(red, green, blue, 2, 0.1, current_status)
    clear()


@basic_func.expose
def alert(current_status):
    basic_func.custom_alert(255, 0, 0, current_status)


@basic_func.expose
def available(current_status):
    basic_func.solid_colour(0, 255, 0, current_status)


@basic_func.expose
def busy(current_status):
    basic_func.solid_colour(255, 62, 0, current_status)


@basic_func.expose
def disturbable(current_status):
    basic_func.solid_colour(199, 234, 70, current_status)


@basic_func.expose
def brb(current_status):
    basic_func.animation(255, 62, 0, current_status)


@basic_func.expose
def engaged(current_status):
    '''Shows three LEDs moving along'''
    # can't change status if this is selected -- FIXED
    while True:
        for current_led in range(0, 8):
            basic_func.trace(current_led, 0, 0, 255, "forwards")
            # checks for new status
            basic_func.custom_sleep(0.5, current_status)
        # could make it so the bar fills up gradually


@basic_func.expose
def offline(current_status):
    clear()
    basic_func.set_all(0, 0, 0, 0)
    show()


if __name__ == "__main__":
    status.set_statuses(basic_func.callable_statuses())
    status.set_type('blinkt')
    basic_func.status_loop('available')
