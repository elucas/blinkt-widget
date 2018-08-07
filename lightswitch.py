import basic_func
from blinkt import clear, show, set_all
# is this already taken from blinkt_functions?
import status

# Device-unique functions
# This one is for a light

light_color = (255, 255, 255)


# @basic_func.expose
# def on(current_status):
#     basic_func.solid_colour(light_color[0], light_color[1], light_color[2],\
# current_status)

# @basic_func.expose
# def off(current_status):
#     clear()
#     set_all(0, 0, 0, 0)
#     show()

# @basic_func.expose
# def red(current_status):
# 	light_color = (153, 0, 0)
# 	basic_func.solid_colour(light_color[0], light_color[1], light_color[2\
# ], current_status)


@basic_func.expose
def low_0(current_status):
    clear()
    set_all(light_color[0], light_color[1], light_color[2], 0.0)
    show()


@basic_func.expose
def low_25(current_status):
    clear()
    set_all(light_color[0], light_color[1], light_color[2], 0.25)
    show()


@basic_func.expose
def low_50(current_status):
    clear()
    set_all(light_color[0], light_color[1], light_color[2], 0.5)
    show()


@basic_func.expose
def low_75(current_status):
    clear()
    set_all(light_color[0], light_color[1], light_color[2], 0.75)
    show()


@basic_func.expose
def low_100(current_status):
    clear()
    set_all(light_color[0], light_color[1], light_color[2], 1.0)
    show()


if __name__ == "__main__":
    status.set_statuses(basic_func.callable_statuses())
    status.set_type('lightswitch')
    basic_func.status_loop('off')
