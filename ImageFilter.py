"""
File: project.py
----------------
This program will implement available filters of users choice. The application has the following filter
Normal Filter, GrayScale Filter, Warhol Filter, Rad Filter, Sepia Filter, Hue Rotate Filter, Invert Filter,
Half Tone Filter, Dithering Filter, Black & White Grain Filter, Brightness Filter, Black & White Filter.
More filters can be added easily by following the bellow steps:
1. Add the filter name to the FILTER_LIST. (This name will be displayed in the banner icon of the application).
2. Add the filter algorithm to the program.
3. Add the index of the filter in the FILTER_LIST and a command to call the respective filter function
in the create_filter_canvas(). This function takes the index of the banner icon passed as parameter.
"""

# Imports Tkinter PIL, Random, Math and SimpleImage
import tkinter
import tkinter.ttk
from PIL import Image
import random
import math
from simpleimage import SimpleImage

# CANVAS_SIZE is the size of the Canvas created
# CANVAS_OFFSET is the offset size of the canvas
# FILTER_TEXT_SIZE is the size of the 'Image Filter' Textbox in the welcome page
# FILTER_TEXTBOX_HEIGHT is the height of the 'Image Filter' Banner Textbox in welcome page
# FILTER_LIST holds the list of filters available.
# Add filters to the Filter list, create a function with the filter RGB Values and add the index
# of the filter to the create_filter_canvas() function to enable the filter in the 'Image Filter' Application
# OVAL_HEIGHT is the height of a oval selection icon in the welcome page
# OVAL_WIDTH is the width of a oval selection icon in the welcome page
# OVALS_IN_ROW is the number of oval selection icons in a row in welcome page
# OVALS_IN_COLUMN is the number of oval selection icons in a column in welcome page
# FOOTER_HEIGHT is the height of the footer in the bottom
# NO_OF_FILTERS is the number od filters available in an application
# PAGE_TOGGLE_BUTTON_SIZE is the size of the button used to toggle between pages
# BANNER_CURSOR_WIDTH_THRESHOLD is the width pixel threshold for cursor when moved over banner
# BANNER_CURSOR_HEIGHT_THRESHOLD is the height pixel threshold for cursor when moved over banner
# TOGGLE_CURSOR_THRESHOLD is the pixel threshold for cursor when moved over banner
# PAGE_NO_X_OFFSET is the X offset for the position of the Page number in the canvas
# PAGE_NO_Y_OFFSET is the Y offset for the position of the Page number in the canvas
# FIRE_DETECTOR_THRESHOLD is the threshold for red pixels in the image
# NO_ROWS_WARHOL_FILTER is the number of rows in the output image of Warhol filter
# NO_COLUMNS_WARHOL_FILTER is the number of columns in the output Image of the Warhol Filter
# HUE_ROTATE rotates the hue by given angle in degree. Adjust rotation angles and have fun
# HUE_SATURATION_MULTIPLIER decides the saturation level for the hue rotate filter
# HUE_VALUE_MULTIPLIER is the hue value transformation factor for the hue rotate filter
# BRIGHTNESS of the output image in Brightness Filter. Adjust to your wish
# BRIGHTNESS_BW is the brightness for converting RGB to BW in BW Filter. Adjust to your wish
CANVAS_SIZE = 600
CANVAS_OFFSET = 5
FILTER_TEXT_SIZE = 150
FILTER_TEXTBOX_HEIGHT = 50
FILTER_LIST = ["Normal", "GrayScale", "Warhol", "Rad", "Sepia", "Hue Rotate", "Invert", "Half Tone", "Dithering",
               "BW Grain", "Brightness", "BW"]
OVAL_HEIGHT = 125
OVAL_WIDTH = OVAL_HEIGHT * 2
OVALS_IN_ROW = 2
OVALS_IN_COLUMN = 2
FOOTER_HEIGHT = 50
NO_OF_FILTERS = len(FILTER_LIST)
PAGE_TOGGLE_BUTTON_SIZE = 60
BANNER_CURSOR_WIDTH_THRESHOLD = OVAL_WIDTH // 25
BANNER_CURSOR_HEIGHT_THRESHOLD = OVAL_HEIGHT // 12.5
TOGGLE_CURSOR_THRESHOLD = PAGE_TOGGLE_BUTTON_SIZE // 12.5
PAGE_NO_X_OFFSET = 10
PAGE_NO_Y_OFFSET = 35
NO_OF_PAGES = math.ceil(NO_OF_FILTERS / (OVALS_IN_ROW * OVALS_IN_COLUMN))
FIRE_DETECTOR_THRESHOLD = 1.2
N_ROWS_WARHOL_FILTER = 2
N_COLS_WARHOL_FILTER = 3
HUE_ROTATE = 180
HUE_SATURATION_MULTIPLIER = 1
HUE_VALUE_MULTIPLIER = 1
BRIGHTNESS = 1.5
BRIGHTNESS_BW = 1.1

# Intensity threshold for blue screening, green screening and red screening
# Change thresholds to your wish
BLUE_SCREEN_INTENSITY_THRESHOLD = 1.9
GREEN_SCREEN_INTENSITY_THRESHOLD = 1.45
RED_SCREEN_INTENSITY_THRESHOLD = 2.35

# Path to background image
Background_Image_path = 'images\Background.png'

# Path to Test Image
Image_path = 'images\Test_image.png'

# Path to foreground and background images for Blue screening
foreground_path_blue_screen = 'images/Blue_Screen_foreground.jpg'
background_path_blue_screen = 'images/Blue_Screen_background.jpg'

# Path to foreground and background images for Green screening
foreground_path_green_screen = 'images/Green_Screen_foreground.jpg'
background_path_green_screen = 'images/Green_Screen_background.jpg'

# Path to foreground and background images for Red screening
foreground_path_red_screen = 'images/Red_Screen_foreground.jpg'
background_path_red_screen = 'images/Red_Screen_background.jpg'

page_no = 0


def main():
    """
    Creates canvas for User Interface and binds mouse buttons,
    mouse motion and keystrokes to the canvas.
    """
    banner_coordinates = []
    toggle_coordinates = []
    banner_list = []
    toggle_list = []
    canvas = make_canvas(CANVAS_SIZE, CANVAS_SIZE, 'Image Filter')
    draw_square(canvas, "", CANVAS_SIZE, CANVAS_SIZE)
    canvas.pack(expand="YES", fill="both")
    banner_coordinates, toggle_coordinates, banner_list, toggle_list = draw_welcome_page(
        canvas, banner_coordinates, toggle_coordinates, banner_list, toggle_list)
    canvas.focus_set()
    canvas.bind("<Motion>", lambda event: mouse_moved(canvas, event, banner_coordinates,
                                                      toggle_coordinates, banner_list, toggle_list))
    canvas.bind("<Button-1>", lambda event: detect_mouse_click(canvas, event, banner_coordinates,
                                                               toggle_coordinates, banner_list, toggle_list))
    canvas.bind("Leave", reset_welcome_screen(canvas, banner_coordinates,
                                              toggle_coordinates, banner_list, toggle_list))
    canvas.bind("<Escape>", lambda event: canvas.quit())
    canvas.mainloop()


def draw_welcome_page(canvas, banner_coordinates, toggle_coordinates, banner_list, toggle_list):
    """
    This function draws the welcome page on the canvas.
    :param canvas: Canvas where the application and graphics is placed.
    :param banner_coordinates: The co-ordinates of the banners in the canvas.
    :param toggle_coordinates: The co-ordinates of the left and right toggle buttons.
    :param banner_list: List containing the created banner objects.
    :param toggle_list: List containing the created toggle button objects.
    :return: returns banner_coordinates, banner_list, toggle_coordinates,
    toggle_list to the calling function.
    """
    canvas.background = background = tkinter.PhotoImage(file=Background_Image_path)
    canvas.create_image(0, 0, image=background, anchor='nw')
    draw_header(canvas)
    banner_coordinates, banner_list = draw_filter_banner(canvas, banner_coordinates, banner_list)
    toggle_coordinates, toggle_list = draw_toggle_button(canvas, toggle_coordinates, toggle_list)
    draw_page_no(canvas)
    draw_footer(canvas)
    return banner_coordinates, toggle_coordinates, banner_list, toggle_list


def draw_header(canvas):
    """
    This function draws the header in the canvas.
    :param canvas: Canvas where the header is drawn.
    :return:
    """
    canvas.create_rectangle(0, 0, CANVAS_SIZE + 2 * CANVAS_OFFSET, FILTER_TEXTBOX_HEIGHT, fill="black")
    canvas.create_text(CANVAS_SIZE / 2 - FILTER_TEXT_SIZE / 2, FILTER_TEXTBOX_HEIGHT / 2,
                       anchor='w', font='Calibri 20 bold', text='IMAGE FILTER', fill="white")


def draw_filter_banner(canvas, banner_coordinates, banner_list):
    """
    This function draws the filter banner icons in the canvas.
    :param canvas: Canvas where the banner icons are to be drawn.
    :param banner_coordinates: The co-ordinates of the banners in the canvas.
    :param banner_list: List containing the created banner objects.
    :return: Returns banner_coordinates and banner_list ot the calling function.
    """
    banner_coordinates.clear()
    banner_list.clear()
    banner_created = page_no * OVALS_IN_COLUMN * OVALS_IN_ROW
    for column_no in range(OVALS_IN_COLUMN):
        for row_no in range(OVALS_IN_ROW):
            if banner_created < NO_OF_FILTERS:
                up_left_x = (row_no * CANVAS_SIZE / 2) + 25
                up_left_y = (FILTER_TEXTBOX_HEIGHT * 2) + (column_no * (CANVAS_SIZE / 2 - FOOTER_HEIGHT - 25))
                low_right_x = up_left_x + OVAL_WIDTH
                low_right_y = up_left_y + OVAL_HEIGHT
                x = canvas.create_oval(up_left_x, up_left_y, low_right_x, low_right_y,
                                       outline="black", fill="white")
                add_text_in_banners(canvas, banner_created, (up_left_x + low_right_x) / 2,
                                    (up_left_y + low_right_y) / 2, "black")
                banner_coordinates.append(canvas.coords(x))
                banner_list.append(x)
                banner_created += 1
    return banner_coordinates, banner_list


def add_text_in_banners(canvas, filter_index, x_pos, y_pos, color):
    """
    This function adds text to the filter banner icons.
    :param canvas: Canvas with the banner icons where the text is to be placed.
    :param filter_index: The index of the filter whose name is to be placed.
    :param x_pos: The x-position of the banner icon.
    :param y_pos: The y-position of the banner icon.
    :param color: The color of the text to be drawn.
    :return:
    """
    text = FILTER_LIST[filter_index]
    canvas.create_text(x_pos, y_pos, font='Calibri 20 bold', text=text, fill=color)


def draw_toggle_button(canvas, toggle_coordinates, toggle_list):
    """
    This function draws the toggle button in the canvas.
    :param canvas: Canvas where the toggle buttons are to be drawn.
    :param toggle_coordinates: The co-ordinates of the toggle button in the canvas.
    :param toggle_list: List containing the created toggle button objects.
    :return: Returns toggle_coordinates and toggle_list to the calling function.
    """
    toggle_button_position = 120
    toggle_list.clear()
    toggle_coordinates.clear()
    toggle_list, toggle_coordinates = draw_left_toggle_button(canvas, toggle_button_position,
                                                              toggle_coordinates, toggle_list)
    toggle_list, toggle_coordinates = draw_right_toggle_button(canvas, toggle_button_position,
                                                               toggle_coordinates, toggle_list)
    return toggle_coordinates, toggle_list


def draw_right_toggle_button(canvas, toggle_button_position, toggle_coordinates, toggle_list):
    """
    This function draws the right toggle button in the canvas.
    :param canvas: The canvas where the right toggle button is to be drawn.
    :param toggle_button_position: The position of the right toggle button.
    :param toggle_coordinates: The coordinates of the toggle button in the canvas.
    :param toggle_list: List containing the toggle list objects.
    :return: Returns toggle_list and toggle_coordinates to the calling function.
    """
    up_left_x = CANVAS_SIZE / 2 + toggle_button_position
    up_left_y = CANVAS_SIZE - FOOTER_HEIGHT - 65
    low_right_x = up_left_x + PAGE_TOGGLE_BUTTON_SIZE
    low_right_y = up_left_y + PAGE_TOGGLE_BUTTON_SIZE
    x_pos = (up_left_x + low_right_x) / 2
    y_pos = (up_left_y + low_right_y) / 2
    x = canvas.create_oval(up_left_x, up_left_y, low_right_x, low_right_y, outline="black", fill="white")
    canvas.create_text(x_pos, y_pos, font='Calibri 25 bold', text=">", fill="black")
    toggle_coordinates.append(canvas.coords(x))
    toggle_list.append(x)
    return toggle_list, toggle_coordinates


def draw_left_toggle_button(canvas, toggle_button_position, toggle_coordinates, toggle_list):
    """
    This function draws the left toggle button in the canvas.
    :param canvas: The canvas where the left toggle button is to be drawn.
    :param toggle_button_position: The position of the left toggle button.
    :param toggle_coordinates: The coordinates of the toggle button in the canvas.
    :param toggle_list: List containing the toggle list objects.
    :return: Returns toggle_list and toggle_coordinates to the calling function.
    """
    up_left_x = toggle_button_position
    up_left_y = CANVAS_SIZE - FOOTER_HEIGHT - 65
    low_right_x = up_left_x + PAGE_TOGGLE_BUTTON_SIZE
    low_right_y = up_left_y + PAGE_TOGGLE_BUTTON_SIZE
    x_pos = (up_left_x + low_right_x) / 2
    y_pos = (up_left_y + low_right_y) / 2
    x = canvas.create_oval(up_left_x, up_left_y, low_right_x, low_right_y, outline="black", fill="white")
    canvas.create_text(x_pos, y_pos, font='Calibri 25 bold', text="<", fill="black")
    toggle_coordinates.append(canvas.coords(x))
    toggle_list.append(x)
    return toggle_list, toggle_coordinates


def draw_page_no(canvas):
    """
    This function draws page number in the bottom center of the canvas.
    :param canvas: Canvas where the page number is to be drawn.
    :return:
    """
    canvas.create_text(CANVAS_SIZE / 2 - PAGE_NO_X_OFFSET, CANVAS_SIZE - FOOTER_HEIGHT - PAGE_NO_Y_OFFSET,
                       anchor='w', font='Calibri 20 bold', text=str(page_no + 1), fill="black")


def draw_footer(canvas):
    """
    This function draws footer in the canvas.
    :param canvas: Canvas where the footer is to be drawn.
    :return:
    """
    canvas.create_rectangle(0, CANVAS_SIZE - FOOTER_HEIGHT + 2 * CANVAS_OFFSET, CANVAS_SIZE + 2 * CANVAS_OFFSET,
                            CANVAS_SIZE + 2 * CANVAS_OFFSET, fill="black")
    canvas.create_text(CANVAS_SIZE / 2 - FILTER_TEXT_SIZE / 2, CANVAS_SIZE - FOOTER_HEIGHT / 2 + 2 * CANVAS_OFFSET,
                       anchor='w', font='Calibri 20 bold', text='IMAGE FILTER', fill="white")


def draw_square(canvas, color, size_x, size_y):
    """
    This function draws square on the canvas.
    :param canvas: Canvas where the square is to be drawn.
    :param color: The fill color of the square.
    :param size_x: Length of the square.
    :param size_y: Height of the square.
    :return:
    """
    x = 0
    y = 0
    canvas.create_rectangle(x, y, x + size_x, y + size_y, fill=color)


def mouse_moved(canvas, event, banner_coordinates, toggle_coordinates, banner_list, toggle_list):
    """
    This bound event function handles the mouse position.
    :param canvas: Canvas where the position of the mouse cursor is to be determined.
    :param event: The event which is to be handled by the event handler.
    :param banner_coordinates: The coordinates of the banner icons in the canvas.
    :param toggle_coordinates: The coordinates of the toggle button in the canvas.
    :param banner_list: List containing the banner icon objects.
    :param toggle_list: List containing the toggle button objects.
    :return:
    """
    cursor_x = event.x
    cursor_y = event.y
    check_cursor_in_banner(canvas, cursor_x, cursor_y, banner_coordinates, banner_list)
    check_cursor_in_toggle(canvas, cursor_x, cursor_y, toggle_coordinates, toggle_list)


def check_cursor_in_banner(canvas, cursor_x, cursor_y, banner_coordinates, banner_list):
    """
    This function checks the whether the mouse cursor is present inside the banner icon.
    :param canvas: Canvas inside which the cursor position is to be checked.
    :param cursor_x: x-coordinate of the mouse cursor.
    :param cursor_y: y-coordinate of the mouse cursor.
    :param banner_coordinates: The coordinates of the banner icons.
    :param banner_list: List containing the banner objects.
    :return:
    """
    for i in range(len(banner_coordinates)):
        left_x = banner_coordinates[i][0]
        left_y = banner_coordinates[i][1]
        right_x = banner_coordinates[i][2]
        right_y = banner_coordinates[i][3]

        up_left_x = banner_coordinates[i][0] + BANNER_CURSOR_WIDTH_THRESHOLD
        up_left_y = banner_coordinates[i][1] + BANNER_CURSOR_HEIGHT_THRESHOLD
        low_right_x = banner_coordinates[i][2] - BANNER_CURSOR_WIDTH_THRESHOLD
        low_right_y = banner_coordinates[i][3] - BANNER_CURSOR_HEIGHT_THRESHOLD
        if up_left_x <= cursor_x <= low_right_x and up_left_y <= cursor_y <= low_right_y:
            change_banner_style(canvas, banner_list, i, banner_coordinates)
        else:
            canvas.create_oval(left_x, left_y, right_x, right_y, outline="black", fill='white')
            add_text_in_banners(canvas, (page_no * OVALS_IN_COLUMN * OVALS_IN_ROW) + i,
                                (left_x + right_x) / 2, (left_y + right_y) / 2, "black")


def change_banner_style(canvas, banner_list, banner_coordinate_index, banner_coordinates):
    """
    This function changes the style of the banner icon. It changes Black text with white fill
    to White text with black color fill.
    :param canvas: Canvas in which the banner icon style is to be changed.
    :param banner_list: List containing the banner objects.
    :param banner_coordinate_index: Index of the banner icon whose style is to be changed.
    :param banner_coordinates: The coordinates of the banner icons in the canvas.
    :return:
    """
    up_left_x = banner_coordinates[banner_coordinate_index][0]
    up_left_y = banner_coordinates[banner_coordinate_index][1]
    low_right_x = banner_coordinates[banner_coordinate_index][2]
    low_right_y = banner_coordinates[banner_coordinate_index][3]
    canvas.delete(banner_list[banner_coordinate_index])
    x = canvas.create_oval(up_left_x, up_left_y, low_right_x, low_right_y, fill="black")
    banner_list[banner_coordinate_index] = x
    add_text_in_banners(canvas, (page_no * OVALS_IN_COLUMN * OVALS_IN_COLUMN) + banner_coordinate_index,
                        (up_left_x + low_right_x) / 2,
                        (up_left_y + low_right_y) / 2, "white")
    banner_coordinates[banner_coordinate_index] = canvas.coords(x)


def check_cursor_in_toggle(canvas, cursor_x, cursor_y, toggle_coordinates, toggle_list):
    """
    This function checks whether the cursor is present inside the toggle icons.
    :param canvas: Canvas in which the mouse cursor position is to be checked.
    :param cursor_x: x-coordinate of the mouse cursor.
    :param cursor_y: y-coordinate of the mouse cursor.
    :param toggle_coordinates: Coordinates of the toggle button in the canvas.
    :param toggle_list: List containing the toggle button objects.
    :return:
    """
    for i in range(len(toggle_coordinates)):
        left_x = toggle_coordinates[i][0]
        left_y = toggle_coordinates[i][1]
        right_x = toggle_coordinates[i][2]
        right_y = toggle_coordinates[i][3]

        up_left_x = toggle_coordinates[i][0] + TOGGLE_CURSOR_THRESHOLD
        up_left_y = toggle_coordinates[i][1] + TOGGLE_CURSOR_THRESHOLD
        low_right_x = toggle_coordinates[i][2] - TOGGLE_CURSOR_THRESHOLD
        low_right_y = toggle_coordinates[i][3] - TOGGLE_CURSOR_THRESHOLD
        if up_left_x <= cursor_x <= low_right_x and up_left_y <= cursor_y <= low_right_y:
            change_toggle_style(canvas, i, toggle_coordinates[i], toggle_list[i])
        else:
            canvas.create_oval(left_x, left_y, right_x, right_y, outline="black", fill="white")
            x_pos = (left_x + right_x) / 2
            y_pos = (left_y + right_y) / 2
            if i == 0:
                canvas.create_text(x_pos, y_pos, font='Calibri 25 bold', text="<", fill="black")
            else:
                canvas.create_text(x_pos, y_pos, font='Calibri 25 bold', text=">", fill="black")


def change_toggle_style(canvas, toggle_coordinate_index, toggle_coordinate, toggle_index):
    """
    This function will change the style of the toggle button. It changes Black text with
    white color fill to White text with black color fill.
    :param canvas: Canvas in which the toggle button style is to be changed.
    :param toggle_coordinate_index: Index of the toggle button whose style is to be changed.
    :param toggle_coordinate: Coordinates of the toggle button in the canvas.
    :param toggle_index: Index of the toggle button object which is to be removed from the canvas.
    :return:
    """
    up_left_x = toggle_coordinate[0]
    up_left_y = toggle_coordinate[1]
    low_right_x = toggle_coordinate[2]
    low_right_y = toggle_coordinate[3]
    x_pos = (up_left_x + low_right_x) / 2
    y_pos = (up_left_y + low_right_y) / 2
    canvas.delete(toggle_index)
    if toggle_coordinate_index == 0 and page_no > 0:
        canvas.create_oval(up_left_x, up_left_y, low_right_x, low_right_y, outline="white", fill="black")
        canvas.create_text(x_pos, y_pos, font='Calibri 25 bold', text="<", fill="white")
    if toggle_coordinate_index == 1 and page_no < NO_OF_PAGES - 1:
        canvas.create_oval(up_left_x, up_left_y, low_right_x, low_right_y, outline="white", fill="black")
        canvas.create_text(x_pos, y_pos, font='Calibri 25 bold', text=">", fill="white")


def detect_mouse_click(canvas, event, banner_coordinates, toggle_coordinates, banner_list, toggle_list):
    """
    This function detects whether the left click is made.
    :param canvas: Canvas inside which whether the mouse click is made is to be checked.
    :param event: Event which is to be handled by the event handler.
    :param banner_coordinates: Coordinates of the banner icons in the canvas.
    :param toggle_coordinates: Coordinates of the toggle icons in the canvas.
    :param banner_list: List containing the banner icon objects in the canvas.
    :param toggle_list: List containing the toggle icon objects in the canvas.
    :return:
    """
    global page_no
    cursor_x = event.x
    cursor_y = event.y
    banner_index = detect_banner(banner_coordinates, cursor_x, cursor_y)
    toggle_index = detect_toggle(toggle_coordinates, cursor_x, cursor_y)
    if banner_index != "Clicked Wrongly":
        create_filter_canvas(banner_index)
    if toggle_index == 1 and page_no < (NO_OF_PAGES - 1):
        page_no += 1
    if toggle_index == 0 and page_no > 0:
        page_no -= 1
    reset_welcome_screen(canvas, banner_coordinates, toggle_coordinates, banner_list, toggle_list)


def detect_banner(banner_coordinates, cursor_x, cursor_y):
    """
    This function detects which filter banner icon is pressed.
    :param banner_coordinates: Coordinates of the banner icons in the canvas.
    :param cursor_x: x-coordinate of the mouse cursor.
    :param cursor_y: y-coordinate of the mouse cursor.
    :return: Returns the index of the banner icons if mouse click is made inside the banner boundary.
    If pressed outside the banner boundary it returns "Clicked Wrongly" to the calling function.
    """
    for i in range(len(banner_coordinates)):
        up_left_x = banner_coordinates[i][0] + BANNER_CURSOR_WIDTH_THRESHOLD
        up_left_y = banner_coordinates[i][1] + BANNER_CURSOR_HEIGHT_THRESHOLD
        low_right_x = banner_coordinates[i][2] - BANNER_CURSOR_WIDTH_THRESHOLD
        low_right_y = banner_coordinates[i][3] - BANNER_CURSOR_HEIGHT_THRESHOLD
        if up_left_x <= cursor_x <= low_right_x and up_left_y <= cursor_y <= low_right_y:
            return (page_no * OVALS_IN_COLUMN * OVALS_IN_ROW) + i
    return "Clicked Wrongly"


def detect_toggle(toggle_coordinates, cursor_x, cursor_y):
    """
    This function detects the toggle button which is pressed.
    :param toggle_coordinates: Coordinates of the toggle button present in the canvas.
    :param cursor_x: x-coordinate of the cursor.
    :param cursor_y: y-coordinate of the cursor.
    :return: Return the toggle button index if click is made inside the toggle button boundary.
    Else returns "Clicked Wrongly" to the calling function.
    """
    for i in range(len(toggle_coordinates)):
        up_left_x = toggle_coordinates[i][0] + TOGGLE_CURSOR_THRESHOLD
        up_left_y = toggle_coordinates[i][1] + TOGGLE_CURSOR_THRESHOLD
        low_right_x = toggle_coordinates[i][2] - TOGGLE_CURSOR_THRESHOLD
        low_right_y = toggle_coordinates[i][3] - TOGGLE_CURSOR_THRESHOLD
        if up_left_x <= cursor_x <= low_right_x and up_left_y <= cursor_y <= low_right_y:
            return i
    return "Clicked Wrongly"


def reset_welcome_screen(canvas, banner_coordinates, toggle_coordinates, banner_list, toggle_list):
    """
    This function will delete all the existing objects in the canvas and recreate all the objects in the canvas.
    :param canvas: Canvas which must be recreated.
    :param banner_coordinates: Coordinates of the banner icons in the canvas.
    :param toggle_coordinates: Coordinates of the banner icons in the canvas.
    :param banner_list: List containing banner objects of the canvas.
    :param toggle_list: List containing toggle objects of the canvas.
    :return:
    """
    canvas.delete("all")
    draw_welcome_page(canvas, banner_coordinates, toggle_coordinates, banner_list, toggle_list)


def create_filter_canvas(banner_index):
    """
    Calls filter function according to the user's selection.
    :param banner_index: Index of the filter which is to be implemented.
    :return:
    """
    image = SimpleImage(Image_path)
    print("Please wait. Opening {} Filter....".format(FILTER_LIST[banner_index]))
    if banner_index == 0:
        normal_filter(image)
    elif banner_index == 1:
        grayscale_filter(image)
    elif banner_index == 2:
        warhol_filter(image)
    elif banner_index == 3:
        rad_filter(image)
    elif banner_index == 4:
        sepia_filter(image)
    elif banner_index == 5:
        hue_rotate_filter(image)
    elif banner_index == 6:
        invert_filter(image)
    elif banner_index == 7:
        image = Image.open(Image_path)
        halftone_filter(image)
    elif banner_index == 8:
        image = Image.open(Image_path)
        dithering_filter(image)
    elif banner_index == 9:
        image = Image.open(Image_path)
        bw_grain_filter(image)
    elif banner_index == 10:
        image = Image.open(Image_path)
        brightness_filter(image)
    elif banner_index == 11:
        image = Image.open(Image_path)
        bw_filter(image)


def normal_filter(image):
    """
    This function shows the image for which filters are to applied.
    :param image: Image to be displayed.
    :return:
    """
    image.show()


def grayscale_filter(image):
    """
    This functions applies Grayscale filter to the image.
    :param image: Image for which Grayscale filter is to be applied.
    :return:
    """
    for pixel in image:
        average = (pixel.red + pixel.blue + pixel.green) / 3
        pixel.red = average
        pixel.blue = average
        pixel.green = average
    image.show()


def warhol_filter(image):
    """
    This functions applies Warhol filter to the image.
    :param image: Image for which Warhol filter is to be applied.
    :return:
    """
    patch_size = image.width
    width_output = N_COLS_WARHOL_FILTER * patch_size  # Width of the output image
    height_output = N_ROWS_WARHOL_FILTER * patch_size  # Height of the output image

    final_image = SimpleImage.blank(width_output, height_output)

    # This generate a pinkish patch
    # make_recolored_patch() will update the RGB color values of pixels of the image
    patch = make_recolored_patch(1.5, 0, 1.5, image)
    width = patch.width
    height = patch.height
    rpos = 0

    # Iterate through the pixels of the image for N_ROWS * N_COLS times and
    # also change the position where the pixels are to be placed
    # Generates a random RGB color value for every patch in the output image
    for row_no in range(N_ROWS_WARHOL_FILTER):
        cpos = 0
        for column_no in range(N_COLS_WARHOL_FILTER):
            red_scale = random.uniform(0.5, 1.5)
            green_scale = random.uniform(0.5, 1.5)
            blue_scale = random.uniform(0.5, 1.5)
            for y in range(height):
                for x in range(width):
                    pixel = patch.get_pixel(x, y)
                    final_image.set_pixel(x + cpos, y + rpos, pixel)
            patch = make_recolored_patch(red_scale, green_scale, blue_scale, image)
            cpos += width
        rpos += height
    final_image.show()


def make_recolored_patch(red_scale, green_scale, blue_scale, patch):
    """
    Implement this function to make a patch for the Warhol Filter. It
    loads the patch image and recolors it.
    :param patch: The input image to the function.
    :param red_scale: A number to multiply each pixels' red component by.
    :param green_scale: A number to multiply each pixels' green component by.
    :param blue_scale: A number to multiply each pixels' blue component by.
    :return: the newly generated patch.
    """
    for pixel in patch:
        pixel.red = pixel.red * red_scale
        pixel.green = pixel.green * green_scale
        pixel.blue = pixel.blue * blue_scale
    return patch


def rad_filter(image):
    """
    This functions applies Rad filter to the image.
    :param image: Image for which Rad filter is to be applied.
    :return:
    """
    for pixel in image:
        pixel.red = pixel.red * 1.5
        pixel.green = pixel.green * 0.7
        pixel.blue = pixel.blue * 1.5
    image.show()


def blue_screen_filter():
    """
    This functions carries out blue screening.
    :return:
    """
    foreground = SimpleImage(foreground_path_blue_screen)
    background = SimpleImage(background_path_blue_screen)
    background.make_as_big_as(foreground)
    for pixel in foreground:
        average = (pixel.red + pixel.green + pixel.blue) // 3
        if pixel.blue <= average * BLUE_SCREEN_INTENSITY_THRESHOLD:
            x = pixel.x
            y = pixel.y
            background.set_pixel(x, y, foreground.get_pixel(x, y))
    background.show()


def red_screen_filter():
    """
    This functions carries out red screening.
    :return:
    """
    foreground = SimpleImage(foreground_path_red_screen)
    background = SimpleImage(background_path_red_screen)
    background.make_as_big_as(foreground)
    for pixel in foreground:
        average = (pixel.red + pixel.green + pixel.blue) // 3
        if pixel.red <= average * RED_SCREEN_INTENSITY_THRESHOLD:
            x = pixel.x
            y = pixel.y
            background.set_pixel(x, y, foreground.get_pixel(x, y))
    background.show()


def green_screen_filter():
    """
    This functions carries out green screening.
    :return:
    """
    foreground = SimpleImage(foreground_path_green_screen)
    background = SimpleImage(background_path_green_screen)
    background.make_as_big_as(foreground)
    for pixel in foreground:
        average = (pixel.red + pixel.green + pixel.blue) // 3
        if pixel.green <= average * GREEN_SCREEN_INTENSITY_THRESHOLD:
            x = pixel.x
            y = pixel.y
            background.set_pixel(x, y, foreground.get_pixel(x, y))
    background.show()


def fire_detector(image):
    """
    This function detects fire in the given image.
    :param image: Image in which fire is to be detected.
    :return:
    """
    for pixel in image:
        if pixel.red >= pixel.blue * FIRE_DETECTOR_THRESHOLD and pixel.red >= pixel.green * FIRE_DETECTOR_THRESHOLD:
            pixel.red = 255
            pixel.blue = 0
            pixel.green = 0
        else:
            average = (pixel.red + pixel.green + pixel.blue) // 3
            pixel.red = average
            pixel.green = average
            pixel.blue = average
    image.show()


def sepia_filter(image):
    """
    This functions applies Sepia filter to the image.
    :param image: Image for which Sepia filter is to be applied.
    :return:
    """
    for pixel in image:
        new_red = (pixel.red * 0.393 + pixel.green * 0.769 + pixel.blue * 0.189)
        new_green = (pixel.red * 0.349 + pixel.green * 0.686 + pixel.blue * 0.168)
        new_blue = (pixel.red * 0.272 + pixel.green * 0.534 + pixel.blue * 0.131)
        if new_red > 255:
            new_red = 255
        if new_blue > 255:
            new_blue = 255
        if new_green > 255:
            new_green = 255
        pixel.red = new_red
        pixel.blue = new_green
        pixel.green = new_blue
    image.show()


def hue_rotate_filter(image):
    """
    This functions calculates value and saturation for the Hue Rotate filter.
    Change HUE_VALUE_MULTIPLIER, HUE_SATURATION_MULTIPLIER and HUE_ROTATE in the constants if needed.
    :param image: Image for which Hue Rotate filter is to be applied.
    :return:
    """
    vsu = HUE_VALUE_MULTIPLIER * HUE_SATURATION_MULTIPLIER * math.cos(HUE_ROTATE * math.pi / 180)
    vsw = HUE_VALUE_MULTIPLIER * HUE_SATURATION_MULTIPLIER * math.sin(HUE_ROTATE * math.pi / 180)
    for pixel in image:
        apply_hue_filter(pixel, vsu, vsw)
    image.show()


def apply_hue_filter(pixel, vsu, vsw):
    """
    This function applies Hue rotate filter to the image.
    :param pixel: Pixel on which hue rotation is to be done.
    :param vsu: The value U matrix constant for Hue Rotate filter.
    :param vsw: The saturation value for Hue rotate filter.
    :return:
    """
    new_red = (.299 * HUE_VALUE_MULTIPLIER + .701 * vsu + .168 * vsw) * pixel.red \
              + (.587 * HUE_VALUE_MULTIPLIER - .587 * vsu + .330 * vsw) * pixel.green \
              + (.114 * HUE_VALUE_MULTIPLIER - .114 * vsu - .497 * vsw) * pixel.blue
    new_green = (.299 * HUE_VALUE_MULTIPLIER - .299 * vsu - .328 * vsw) * pixel.red \
                + (.587 * HUE_VALUE_MULTIPLIER + .413 * vsu + .035 * vsw) * pixel.green \
                + (.114 * HUE_VALUE_MULTIPLIER - .114 * vsu + .292 * vsw) * pixel.blue
    new_blue = (.299 * HUE_VALUE_MULTIPLIER - .300 * vsu + 1.25 * vsw) * pixel.red \
               + (.587 * HUE_VALUE_MULTIPLIER - .588 * vsu - 1.05 * vsw) * pixel.green \
               + (.114 * HUE_VALUE_MULTIPLIER + .886 * vsu - .203 * vsw) * pixel.blue
    pixel.red = new_red
    pixel.blue = new_green
    pixel.green = new_blue


def invert_filter(image):
    """
    This functions applies Invert filter to the image.
    :param image: Image for which Invert filter is to be applied.
    :return:
    """
    for pixel in image:
        pixel.red = 255 - pixel.red
        pixel.green = 255 - pixel.green
        pixel.blue = 255 - pixel.blue
    image.show()


def halftone_filter(image):
    """
    This functions applies Half Tone filter to the image.
    :param image: Image for which Half Tone filter is to be applied.
    :return:
    """
    width, height = image.size
    new_image = Image.new("RGB", (width, height), "white")
    pixels = new_image.load()
    for i in range(0, width, 2):
        for j in range(0, height, 2):
            p1 = get_pixel(image, i, j)
            p2 = get_pixel(image, i, j + 1)
            p3 = get_pixel(image, i + 1, j)
            p4 = get_pixel(image, i + 1, j + 1)
            gray1 = apply_grayscale(p1)
            gray2 = apply_grayscale(p2)
            gray3 = apply_grayscale(p3)
            gray4 = apply_grayscale(p4)
            saturation = (gray1 + gray2 + gray3 + gray4) / 4
            apply_halftone(saturation, pixels, i, j)
    new_image.show()


def apply_grayscale(pixel):
    """
    This function applies grayscale effect to the pixels.
    :param pixel: Pixels for which grayscale filter is to be applied.
    :return: Returns gray scale pixel values to the Filter function.
    """
    gray = (pixel[0] * 0.299) + (pixel[1] * 0.587) + (pixel[2] * 0.114)
    return gray


def apply_halftone(saturation, pixels, i, j):
    """
    Applies Half tone filter to the pixels of the image.
    :param saturation: Saturation value of the pixel.
    :param pixels: Pixel of the image to which filter is to be applied.
    :param i: x-coordinate of the pixel.
    :param j: y-coordinate of the pixel.
    :return:
    """
    if saturation > 223:
        pixels[i, j] = (255, 255, 255)
        pixels[i, j + 1] = (255, 255, 255)
        pixels[i + 1, j] = (255, 255, 255)
        pixels[i + 1, j + 1] = (255, 255, 255)
    elif saturation > 159:
        pixels[i, j] = (255, 255, 255)
        pixels[i, j + 1] = (0, 0, 0)
        pixels[i + 1, j] = (255, 255, 255)
        pixels[i + 1, j + 1] = (255, 255, 255)
    elif saturation > 95:
        pixels[i, j] = (255, 255, 255)
        pixels[i, j + 1] = (0, 0, 0)
        pixels[i + 1, j] = (0, 0, 0)
        pixels[i + 1, j + 1] = (255, 255, 255)
    elif saturation > 32:
        pixels[i, j] = (0, 0, 0)
        pixels[i, j + 1] = (255, 255, 255)
        pixels[i + 1, j] = (0, 0, 0)
        pixels[i + 1, j + 1] = (0, 0, 0)
    else:
        pixels[i, j] = (0, 0, 0)
        pixels[i, j + 1] = (0, 0, 0)
        pixels[i + 1, j] = (0, 0, 0)
        pixels[i + 1, j + 1] = (0, 0, 0)


def dithering_filter(image):
    """
    This functions applies Dithering filter to the image.
    :param image: Image for which Dithering filter is to be applied.
    :return:
    """
    width, height = image.size
    new_image = Image.new("RGB", (width, height), "white")
    pixels = new_image.load()

    for i in range(0, width, 2):
        for j in range(0, height, 2):
            p1 = get_pixel(image, i, j)
            p2 = get_pixel(image, i, j + 1)
            p3 = get_pixel(image, i + 1, j)
            p4 = get_pixel(image, i + 1, j + 1)

            red = (p1[0] + p2[0] + p3[0] + p4[0]) / 4
            green = (p1[1] + p2[1] + p3[1] + p4[1]) / 4
            blue = (p1[2] + p2[2] + p3[2] + p4[2]) / 4

            r = [0, 0, 0, 0]
            g = [0, 0, 0, 0]
            b = [0, 0, 0, 0]

            for x in range(0, 4):
                r[x] = get_saturation(red, x)
                g[x] = get_saturation(green, x)
                b[x] = get_saturation(blue, x)

            pixels[i, j] = (r[0], g[0], b[0])
            pixels[i, j + 1] = (r[1], g[1], b[1])
            pixels[i + 1, j] = (r[2], g[2], b[2])
            pixels[i + 1, j + 1] = (r[3], g[3], b[3])
    new_image.show()


def get_saturation(value, quadrant):
    """
    This function returns the saturation value of the pixel of the image.
    :param value: RGB color value of the pixel.
    :param quadrant: Quadrant of the color wheel.
    :return: Returns saturation value of the pixel.
    """
    if value > 223:
        return 255
    elif value > 159:
        if quadrant != 1:
            return 255

        return 0
    elif value > 95:
        if quadrant == 0 or quadrant == 3:
            return 255

        return 0

    elif value > 32:
        if quadrant == 1:
            return 255

        return 0
    else:
        return 0


def get_pixel(image, i, j):
    """
    This function is used to get the pixel from an image.
    :param image: Image from which pixel is to be extracted.
    :param i: x-coordinate of the pixel in the image.
    :param j: y-coordinate of the pixel in the image.
    :return: Returns the extracted pixel to the calling function.
    """
    width, height = image.size
    if i > width or j > height:
        return None

    pixel = image.getpixel((i, j))
    return pixel


def bw_grain_filter(image):
    """
    This functions applies Black and White Grain filter to the image.
    :param image: Image for which Black and White grain filter is to be applied.
    :return:
    """
    image = image.convert('1')
    image.show()


def brightness_filter(image):
    """
    This functions adjusts the brightness of the image.
    Adjust the BRIGHTNESS constant to change the brightness.
    :param image: Image for which brightness is to be adjusted.
    :return:
    """
    output_image = Image.new('RGB', image.size)
    for x in range(image.size[0]):
        for y in range(image.size[1]):
            red, green, blue = image.getpixel((x, y))

            red = int(red * BRIGHTNESS)
            red = min(255, max(0, red))

            green = int(green * BRIGHTNESS)
            green = min(255, max(0, green))

            blue = int(blue * BRIGHTNESS)
            blue = min(255, max(0, blue))

            output_image.putpixel((x, y), (red, green, blue))
    output_image.show()


def bw_filter(image):
    """
    This functions applies Black and White filter to the image.
    Adjust BRIGHTNESS_BW constant according to image.
    :param image: Image for which Black and White filter is to be applied
    :return:
    """
    output_image = Image.new('RGB', image.size)
    separator = 255 / BRIGHTNESS_BW / 2 * 3
    for x in range(image.size[0]):
        for y in range(image.size[1]):
            red, green, blue = image.getpixel((x, y))
            total = red + green + blue
            if total > separator:
                output_image.putpixel((x, y), (255, 255, 255))
            else:
                output_image.putpixel((x, y), (0, 0, 0))
    output_image.show()


""" 
---------- DO NOT MODIFY ANY CODE BELOW THIS LINE -----------

# This function is provided to you and should not be modified.
# It creates a window that contains a drawing canvas that you
# will use to make your drawings.
"""


def make_canvas(width, height, title=None):
    """
    DO NOT MODIFY
    Creates and returns a drawing canvas
    of the given int size with a blue border,
    ready for drawing.
    :param width: Width of the canvas.
    :param height: Height of the canvas.
    :param title: Title of the canvas. Default set to None.
    :return: Returns canvas to the calling function.
    """
    top = tkinter.Tk()
    top.minsize(width=width, height=height)
    if title:
        top.title(title)
    canvas = tkinter.Canvas(top, width=width + 1, height=height + 1)
    canvas.pack()
    canvas.xview_scroll(8, 'units')  # add this so (0, 0) works correctly
    canvas.yview_scroll(8, 'units')  # otherwise it's clipped off

    return canvas


if __name__ == '__main__':
    main()
