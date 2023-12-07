import tkinter as tk
import os
import cv2
import serial
import numpy as np
import kociemba as kc
from config import config
from colordetection import color_detector
from PIL import ImageFont, ImageDraw, Image, ImageTk

width = 60  # Width of a facelet in pixels
facelet_id = [[[0 for col in range(3)] for row in range(3)] for face in range(6)]
colorpick_id = [0 for i in range(6)]
curcol = None
t = ("U", "R", "F", "D", "L", "B")  # Available moves
cols = ("yellow", "green", "red", "white", "blue", "orange")  # Facelet colors

# Global
ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

# Colors
COLOR_PLACEHOLDER = (150, 150, 150)

# Camera interface
MINI_STICKER_AREA_TILE_SIZE = 14
MINI_STICKER_AREA_TILE_GAP = 2
MINI_STICKER_AREA_OFFSET = 20

STICKER_AREA_TILE_SIZE = 30
STICKER_AREA_TILE_GAP = 4
STICKER_AREA_OFFSET = 20

STICKER_CONTOUR_COLOR = (36, 255, 12)
TEXT_SIZE = 18

# Config
CUBE_PALETTE = 'cube_palette'

#serialPort = serial.Serial(port='COM4', baudrate=9600, timeout=0, parity=serial.PARITY_EVEN, stopbits=1)


def show_text(txt):
    """Display messages."""
    print(txt)
    display.insert(tk.INSERT, txt)
    root.update_idletasks()


def create_facelet_rects(a):
    """Initialize the facelet grid on the canvas."""
    offset = ((1, 0), (2, 1), (1, 1), (1, 2), (0, 1), (3, 1))
    for f in range(6):
        for row in range(3):
            y = 10 + offset[f][1] * 3 * a + row * a
            for col in range(3):
                x = 10 + offset[f][0] * 3 * a + col * a
                facelet_id[f][row][col] = canvas.create_rectangle(x, y, x + a, y + a, fill="grey")
                if row == 1 and col == 1:
                    canvas.create_text(x + width // 2, y + width // 2, font=("", 14), text=t[f], state=tk.DISABLED)
    for f in range(6):
        canvas.itemconfig(facelet_id[f][1][1], fill=cols[f])


def create_colorpick_rects(a):
    """Initialize the "paintbox" on the canvas."""
    global curcol
    global cols
    for i in range(6):
        x = (i % 3)*(a+5) + 7*a
        y = (i // 3)*(a+5) + 7*a
        colorpick_id[i] = canvas.create_rectangle(x, y, x + a, y + a, fill=cols[i])
        canvas.itemconfig(colorpick_id[0], width=4)
        curcol = cols[0]


def get_definition_string():
    """Generate the cube definition string from the facelet colors."""
    color_to_facelet = {}
    for i in range(6):
        color_to_facelet.update({canvas.itemcget(facelet_id[i][1][1], "fill"): t[i]})
    s = ''
    for f in range(6):
        for row in range(3):
            for col in range(3):
                s += color_to_facelet[canvas.itemcget(facelet_id[f][row][col], "fill")]
    return s

################################ Solve the displayed cube with a local or remote server ###############################

def count_moves(sequence):
    move_list = sequence.split()
    total_moves = 0

    for move in move_list:
        if len(move) == 1:
          total_moves += 1
        elif len(move) == 2 and move[1] == '2':
          total_moves += 2
        else:
          total_moves += 1

    return total_moves


def solve():
    """Get solution from kociemba library."""
    display.delete(1.0, tk.END)  # clear output window

    try:
        defstr = get_definition_string()
    except BaseException as e:
        show_text(f'Cubo invalido {e.__doc__}')
        return
    
    try:
        if(defstr != 'UUUUUUUUURRRRRRRRRFRFFFFFFFDDDDDDDDDLLLLLLLLLBBBBBBBBB'):
            algo = kc.solve(defstr)

            count = count_moves(algo)
            show_text(f'Solution: {algo}\n')
            show_text(f'Number of movements: {count}\n')
            show_text("Sending via Bluetooth...\n")
            #send_bluetooth(algo)
        else:
            show_text('Already solved')
    except BaseException as e:
        show_text(e.args[0])
        return
    
def send_bluetooth(solution):
    #serialPort.flush()
    #serialPort.write(str.encode(solution))
    show_text("Sended")

################################## Functions to change the facelet colors #############################################

def clean():
    """Restore the cube to a clean cube"""
    for f in range(6):
        for row in range(3):
            for col in range(3):
                canvas.itemconfig(facelet_id[f][row][col], fill=canvas.itemcget(facelet_id[f][1][1], "fill"))


def empty():
    """Remove the facelet colors except the center facelets colors."""
    for f in range(6):
        for row in range(3):
            for col in range(3):
                if row != 1 or col != 1:
                    canvas.itemconfig(facelet_id[f][row][col], fill="grey")


def random():
    """Generate a random cube and set the corresponding facelet colors."""

########################################################################################################################

# ################################### Edit the facelet colors ##########################################################

def click(_unused):
    """Define how to react on left mouse clicks."""
    global curcol
    idlist = canvas.find_withtag("current")
    if len(idlist) > 0:
        if idlist[0] in colorpick_id:
            curcol = canvas.itemcget("current", "fill")
            for i in range(6):
                canvas.itemconfig(colorpick_id[i], width=1)
            canvas.itemconfig("current", width=5)
        else:
            canvas.itemconfig("current", fill=curcol)



def draw_2d_cube_state():
        grid = {
            'white' : [1, 0],
            'orange': [0, 1],
            'green' : [1, 1],
            'red'   : [2, 1],
            'blue'  : [3, 1],
            'yellow': [1, 2],
        }

        # The offset in-between each side (white, red, etc).
        side_offset = MINI_STICKER_AREA_TILE_GAP * 3

        # The size of 1 whole side (containing 9 stickers).
        side_size = MINI_STICKER_AREA_TILE_SIZE * 3 + MINI_STICKER_AREA_TILE_GAP * 2

        # The X and Y offset is placed in the bottom-right corner, minus the
        # whole size of the 4x3 grid, minus an additional offset.
        offset_x = width - (side_size * 4) - (side_offset * 3) - MINI_STICKER_AREA_OFFSET
        offset_y = height - (side_size * 3) - (side_offset * 2) - MINI_STICKER_AREA_OFFSET

        for side, (grid_x, grid_y) in grid.items():
            index = -1
            for row in range(3):
                for col in range(3):
                    index += 1
                    x1 = int(
                        (offset_x + MINI_STICKER_AREA_TILE_SIZE * col) +
                        (MINI_STICKER_AREA_TILE_GAP * col) +
                        ((side_size + side_offset) * grid_x)
                    )
                    y1 = int(
                        (offset_y + MINI_STICKER_AREA_TILE_SIZE * row) +
                        (MINI_STICKER_AREA_TILE_GAP * row) +
                        ((side_size + side_offset) * grid_y)
                    )
                    x2 = int(x1 + MINI_STICKER_AREA_TILE_SIZE)
                    y2 = int(y1 + MINI_STICKER_AREA_TILE_SIZE)

                    foreground_color = COLOR_PLACEHOLDER
                    if side in result_state:
                        foreground_color = color_detector.get_prominent_color(result_state[side][index])

                    # shadow
                    cv2.rectangle(
                        frame,
                        (x1, y1),
                        (x2, y2),
                        (0, 0, 0),
                        -1
                    )

                    # foreground color
                    cv2.rectangle(
                        frame,
                        (x1 + 1, y1 + 1),
                        (x2 - 1, y2 - 1),
                        foreground_color,
                        -1
                    )



def set_manual_mode():
    global display

    mode_label.pack_forget()
    auto_button.pack_forget()
    manual_button.pack_forget()

    bsolve = tk.Button(text="Solve", height=2, width=10, relief=tk.RAISED, command=solve)
    canvas.create_window(10 + 10.5 * width, 10 + 6.5 * width, anchor=tk.NW, window=bsolve)
    bclean = tk.Button(text="Clean", height=1, width=10, relief=tk.RAISED, command=clean)
    canvas.create_window(10 + 10.5 * width, 10 + 7.5 * width, anchor=tk.NW, window=bclean)
    bempty = tk.Button(text="Empty", height=1, width=10, relief=tk.RAISED, command=empty)
    canvas.create_window(10 + 10.5 * width, 10 + 8 * width, anchor=tk.NW, window=bempty)
    brandom = tk.Button(text="Random", height=1, width=10, relief=tk.RAISED, command=random)
    canvas.create_window(10 + 10.5 * width, 10 + 8.5 * width, anchor=tk.NW, window=brandom)
    display = tk.Text(height=7, width=39)
    canvas.create_window(10 + 6.5 * width, 10 + .5 * width, anchor=tk.NW, window=display)
    canvas.bind("<Button-1>", click)
    create_facelet_rects(width)
    create_colorpick_rects(width)

def get_font(size=TEXT_SIZE):
        """Load the truetype font with the specified text size."""
        font_path = '{}/assets/arial-unicode-ms.ttf'.format(ROOT_DIR)
        return ImageFont.truetype(font_path, size)

def render_text(text, pos, color=(255, 255, 255), size=TEXT_SIZE, anchor='lt'):
        """Render text with a shadow using the pillow module.
        """
        global frame

        font = get_font(size)

        # Convert opencv frame (np.array) to PIL Image array.
        frame2 = Image.fromarray(frame)

        # Draw the text onto the image.
        draw = ImageDraw.Draw(frame2)
        draw.text(pos, text, font=font, fill=color, anchor=anchor,
                  stroke_width=1, stroke_fill=(0, 0, 0))

        # Convert the pillow frame back to a numpy array.
        frame = np.array(frame2)


def draw_stickers(stickers, offset_x, offset_y):
        """Draws the given stickers onto the given frame.
        """
        global frame

        index = -1
        for row in range(3):
            for col in range(3):
                index += 1
                x1 = (offset_x + STICKER_AREA_TILE_SIZE * col) + STICKER_AREA_TILE_GAP * col
                y1 = (offset_y + STICKER_AREA_TILE_SIZE * row) + STICKER_AREA_TILE_GAP * row
                x2 = x1 + STICKER_AREA_TILE_SIZE
                y2 = y1 + STICKER_AREA_TILE_SIZE

                # shadow
                cv2.rectangle(
                    frame,
                    (x1, y1),
                    (x2, y2),
                    (0, 0, 0),
                    -1
                )

                # foreground color
                cv2.rectangle(
                    frame,
                    (x1 + 1, y1 + 1),
                    (x2 - 1, y2 - 1),
                    color_detector.get_prominent_color(stickers[index]),
                    -1
                )


def draw_preview_stickers():
    """Draw the current preview state onto the given frame."""
    draw_stickers(preview_state, STICKER_AREA_OFFSET, STICKER_AREA_OFFSET)


def draw_snapshot_stickers():
    """Draw the current snapshot state onto the given frame."""
    y = STICKER_AREA_TILE_SIZE * 3 + STICKER_AREA_TILE_GAP * 2 + STICKER_AREA_OFFSET * 2
    draw_stickers(snapshot_state, STICKER_AREA_OFFSET, y)


def find_contours(dilatedFrame):
    """Find the contours of a 3x3x3 cube."""
    contours, _ = cv2.findContours(dilatedFrame, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    final_contours = []

    # Step 1/4: filter all contours to only those that are square-ish shapes.
    for contour in contours:
        perimeter = cv2.arcLength(contour, True)
        approx = cv2.approxPolyDP(contour, 0.1 * perimeter, True)
        if len (approx) == 4:
            area = cv2.contourArea(contour)
            (x, y, w, h) = cv2.boundingRect(approx)

            # Find aspect ratio of boundary rectangle around the countours.
            ratio = w / float(h)

            # Check if contour is close to a square.
            if ratio >= 0.8 and ratio <= 1.2 and w >= 30 and w <= 60 and area / (w * h) > 0.4:
                final_contours.append((x, y, w, h))

    # Return early if we didn't found 9 or more contours.
    if len(final_contours) < 9:
        return []

    # Step 2/4: Find the contour that has 9 neighbors (including itself)
    # and return all of those neighbors.
    found = False
    contour_neighbors = {}
    for index, contour in enumerate(final_contours):
        (x, y, w, h) = contour
        contour_neighbors[index] = []
        center_x = x + w / 2
        center_y = y + h / 2
        radius = 1.5

        # Create 9 positions for the current contour which are the
        # neighbors. We'll use this to check how many neighbors each contour
        # has. The only way all of these can match is if the current contour
        # is the center of the cube. If we found the center, we also know
        # all the neighbors, thus knowing all the contours and thus knowing
        # this shape can be considered a 3x3x3 cube. When we've found those
        # contours, we sort them and return them.
        neighbor_positions = [
            # top left
            [(center_x - w * radius), (center_y - h * radius)],

            # top middle
            [center_x, (center_y - h * radius)],

            # top right
            [(center_x + w * radius), (center_y - h * radius)],

            # middle left
            [(center_x - w * radius), center_y],

            # center
            [center_x, center_y],

            # middle right
            [(center_x + w * radius), center_y],

            # bottom left
            [(center_x - w * radius), (center_y + h * radius)],

            # bottom middle
            [center_x, (center_y + h * radius)],

            # bottom right
            [(center_x + w * radius), (center_y + h * radius)],
        ]

        for neighbor in final_contours:
            (x2, y2, w2, h2) = neighbor
            for (x3, y3) in neighbor_positions:
                # The neighbor_positions are located in the center of each
                # contour instead of top-left corner.
                # logic: (top left < center pos) and (bottom right > center pos)
                if (x2 < x3 and y2 < y3) and (x2 + w2 > x3 and y2 + h2 > y3):
                    contour_neighbors[index].append(neighbor)

    # Step 3/4: Now that we know how many neighbors all contours have, we'll
    # loop over them and find the contour that has 9 neighbors, which
    # includes itself. This is the center piece of the cube. If we come
    # across it, then the 'neighbors' are actually all the contours we're
    # looking for.
    for (contour, neighbors) in contour_neighbors.items():
        if len(neighbors) == 9:
            found = True
            final_contours = neighbors
            break

    if not found:
        return []

    # Step 4/4: When we reached this part of the code we found a cube-like
    # contour. The code below will sort all the contours on their X and Y
    # values from the top-left to the bottom-right.

    # Sort contours on the y-value first.
    y_sorted = sorted(final_contours, key=lambda item: item[1])

    # Split into 3 rows and sort each row on the x-value.
    top_row = sorted(y_sorted[0:3], key=lambda item: item[0])
    middle_row = sorted(y_sorted[3:6], key=lambda item: item[0])
    bottom_row = sorted(y_sorted[6:9], key=lambda item: item[0])

    sorted_contours = top_row + middle_row + bottom_row
    return sorted_contours

def scanned_successfully():
    """Validate if the user scanned 9 colors for each side.
    """
    color_count = {}
    for side, preview in result_state.items():
        for bgr in preview:
            key = str(bgr)
            if key not in color_count:
                color_count[key] = 1
            else:
                color_count[key] = color_count[key] + 1
    invalid_colors = [k for k, v in color_count.items() if v != 9]
    return len(invalid_colors) == 0

def draw_contours(contours):
    global frame
    """Draw contours onto the given frame.
    """
    if calibrate_mode:
        # Only show the center piece contour.
        (x, y, w, h) = contours[4]
        cv2.rectangle(frame, (x, y), (x + w, y + h), STICKER_CONTOUR_COLOR, 2)
    else:
        for index, (x, y, w, h) in enumerate(contours):
            cv2.rectangle(frame, (x, y), (x + w, y + h), STICKER_CONTOUR_COLOR, 2)

def update_preview_state(contours):
        """Get the average color value for the contour for every X amount of frames
        to prevent flickering and more precise results.
        """
        global frame
        max_average_rounds = 8
        for index, (x, y, w, h) in enumerate(contours):
            if index in average_sticker_colors and len(average_sticker_colors[index]) == max_average_rounds:
                sorted_items = {}
                for bgr in average_sticker_colors[index]:
                    key = str(bgr)
                    if key in sorted_items:
                        sorted_items[key] += 1
                    else:
                        sorted_items[key] = 1
                most_common_color = max(sorted_items, key=lambda i: sorted_items[i])
                average_sticker_colors[index] = []
                preview_state[index] = eval(most_common_color)
                break

            roi = frame[y+7:y+h-7, x+14:x+w-14]
            avg_bgr = color_detector.get_dominant_color(roi)
            closest_color = color_detector.get_closest_color(avg_bgr)['color_bgr']
            preview_state[index] = closest_color
            if index in average_sticker_colors:
                average_sticker_colors[index].append(closest_color)
            else:
                average_sticker_colors[index] = [closest_color]

def update_snapshot_state():
    """Update the snapshot state based on the current preview state.
    """
    snapshot_state = list(preview_state)
    center_color_name = color_detector.get_closest_color(snapshot_state[4])['color_name']
    result_state[center_color_name] = snapshot_state
    if len(result_state.keys()) == 6:
        print("solve!")
        print(result_state)
        #{'yellow': [(147, 94, 44), (147, 94, 44), (147, 94, 44), (63, 64, 199), (110, 224, 228), (218, 222, 220), (101, 137, 255), (101, 137, 255), (63, 64, 199)], 'blue': [(110, 224, 228), (58, 145, 50), (147, 94, 44), (110, 224, 228), (147, 94, 44), (218, 222, 220), (58, 145, 50), (101, 137, 255), (58, 145, 50)], 'white': [(218, 222, 220), (218, 222, 220), (147, 94, 44), (147, 94, 44), (218, 222, 220), (101, 137, 255), (58, 145, 50), (110, 224, 228), (110, 224, 228)], 'green': [(218, 222, 220), (218, 222, 220), (147, 94, 44), (147, 94, 44), (58, 145, 50), (101, 137, 255), (58, 145, 50), (110, 224, 228), (110, 224, 228)], 'orange': [(101, 137, 255), (218, 222, 220), (101, 137, 255), (147, 94, 44), (101, 137, 255), (147, 94, 44), (63, 64, 199), (101, 137, 255), (110, 224, 228)], 'red': [(218, 222, 220), (58, 145, 50), (58, 145, 50), (147, 94, 44), (63, 64, 199), (58, 145, 50), (218, 222, 220), (58, 145, 50), (63, 64, 199)]} 
    draw_snapshot_stickers()

def get_text_size(text, size=TEXT_SIZE):
    """Get text size based on the default freetype2 loaded font.
    """
    return get_font(size)#.getsize(text)

def draw_scanned_sides():
    """Display how many sides are scanned by the user.
    """
    text = f'Caras escaneadas: {len(result_state.keys())}'
    render_text(text, (20, height - 20), anchor='lb')

def draw_current_color_to_calibrate():
    """Display the current side's color that needs to be calibrated.
    """
    global done_calibrating, current_color_to_calibrate_index
    offset_y = 20
    font_size = int(TEXT_SIZE * 1.25)
    if done_calibrating:
        text = 'calibratedSuccessfully'
        render_text(text, (int(width / 2), offset_y), size=font_size, anchor='mt')
    else:
        current_color = colors_to_calibrate[current_color_to_calibrate_index]
        text = 'currentCalibratingSide: {}'.format(current_color)
        render_text(text, (int(width / 2), offset_y), size=font_size, anchor='mt')

def draw_calibrated_colors():
    """Display all the colors that are calibrated while in calibrate mode.
    """
    global frame, calibrated_colors
    offset_y = 20
    for index, (color_name, color_bgr) in enumerate(calibrated_colors.items()):
        x1 = 90
        y1 = int(offset_y + STICKER_AREA_TILE_SIZE * index)
        x2 = x1 + STICKER_AREA_TILE_SIZE
        y2 = y1 + STICKER_AREA_TILE_SIZE

        # shadow
        cv2.rectangle(
            frame,
            (x1, y1),
            (x2, y2),
            (0, 0, 0),
            -1
        )

        # foreground
        cv2.rectangle(
            frame,
            (x1 + 1, y1 + 1),
            (x2 - 1, y2 - 1),
            tuple([int(c) for c in color_bgr]),
            -1
        )
        render_text(color_name, (20, y1 + STICKER_AREA_TILE_SIZE / 2 - 3), anchor='lm')

def reset_calibrate_mode():
    """Reset calibrate mode variables.
    """
    global done_calibrating, current_color_to_calibrate_index, calibrated_colors

    calibrated_colors = {}
    current_color_to_calibrate_index = 0
    done_calibrating = False

def draw_2d_cube_state():
        global frame, width, height

        grid = {
            'white' : [1, 0],
            'orange': [0, 1],
            'green' : [1, 1],
            'red'   : [2, 1],
            'blue'  : [3, 1],
            'yellow': [1, 2],
        }

        # The offset in-between each side (white, red, etc).
        side_offset = MINI_STICKER_AREA_TILE_GAP * 3

        # The size of 1 whole side (containing 9 stickers).
        side_size = MINI_STICKER_AREA_TILE_SIZE * 3 + MINI_STICKER_AREA_TILE_GAP * 2

        # The X and Y offset is placed in the bottom-right corner, minus the
        # whole size of the 4x3 grid, minus an additional offset.
        offset_x = width - (side_size * 4) - (side_offset * 3) - MINI_STICKER_AREA_OFFSET
        offset_y = height - (side_size * 3) - (side_offset * 2) - MINI_STICKER_AREA_OFFSET

        for side, (grid_x, grid_y) in grid.items():
            index = -1
            for row in range(3):
                for col in range(3):
                    index += 1
                    x1 = int(
                        (offset_x + MINI_STICKER_AREA_TILE_SIZE * col) +
                        (MINI_STICKER_AREA_TILE_GAP * col) +
                        ((side_size + side_offset) * grid_x)
                    )
                    y1 = int(
                        (offset_y + MINI_STICKER_AREA_TILE_SIZE * row) +
                        (MINI_STICKER_AREA_TILE_GAP * row) +
                        ((side_size + side_offset) * grid_y)
                    )
                    x2 = int(x1 + MINI_STICKER_AREA_TILE_SIZE)
                    y2 = int(y1 + MINI_STICKER_AREA_TILE_SIZE)

                    foreground_color = COLOR_PLACEHOLDER
                    if side in result_state:
                        foreground_color = color_detector.get_prominent_color((result_state[side][index]))

                    # shadow
                    cv2.rectangle(
                        frame,
                        (x1, y1),
                        (x2, y2),
                        (0, 0, 0),
                        -1
                    )

                    # foreground color
                    cv2.rectangle(
                        frame,
                        (x1 + 1, y1 + 1),
                        (x2 - 1, y2 - 1),
                        foreground_color,
                        -1
                    )

def set_mode_auto():
    global manual_mode, cam, width, height, canvas

    cam = cv2.VideoCapture(0)
    print('Webcam successfully started')
    cam.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    width = int(cam.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cam.get(cv2.CAP_PROP_FRAME_HEIGHT))
    
    manual_mode = False
    mode_label.pack_forget()
    auto_button.pack_forget()
    manual_button.pack_forget()
    canvas.pack(fill='both', expand=True)
    show_frame()

def show_cam():
    global image_id, frame, canvas
    # Si se hace esto antes de generar la imagen que se asigna a photo, que pasa
    # Se crea photo a partir de la lectura de la captura de la cámara (guardada en frame)
    fr = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    img = Image.fromarray(fr)
    photo = ImageTk.PhotoImage(image=img)
       
    canvas.photo = photo

    if image_id:
        canvas.itemconfig(image_id, image=photo)
    else:
        image_id = canvas.create_image((0, 0), image=photo, anchor='nw')
        canvas.configure(width=photo.width(), height=photo.height())


def show_frame():
    global image_id, frame, calibrate_mode, all_detected_on_calibrating, contours

    _, frame = cam.read()
    key = cv2.waitKey(10) & 0xff

    grayFrame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    blurredFrame = cv2.blur(grayFrame, (3, 3))
    cannyFrame = cv2.Canny(blurredFrame, 30, 60, 3)
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (9, 9))
    dilatedFrame = cv2.dilate(cannyFrame, kernel)

    contours = find_contours(dilatedFrame)
    if len(contours) == 9:
        draw_contours(contours)
        if not calibrate_mode:
            update_preview_state(contours)

    if calibrate_mode:
        draw_current_color_to_calibrate()
        draw_calibrated_colors()
    else:
        draw_preview_stickers()
        draw_snapshot_stickers()
        draw_scanned_sides()
        draw_2d_cube_state()

    show_cam()
    root.after(10, show_frame)


def close_app(event):
    try:
        cam.release()
    except:
        pass

    cv2.destroyAllWindows()
    root.destroy()

def update_key(event):
    global contours, done_calibrating, current_color_to_calibrate_index
    # Update the snapshot when space bar is pressed.
    if not calibrate_mode:
        update_snapshot_state()
    elif done_calibrating is False:
        current_color = colors_to_calibrate[current_color_to_calibrate_index]
        (x, y, w, h) = contours[4]
        roi = frame[y+7:y+h-7, x+14:x+w-14]
        avg_bgr = color_detector.get_dominant_color(roi)
        calibrated_colors[current_color] = avg_bgr
        current_color_to_calibrate_index += 1
        done_calibrating = current_color_to_calibrate_index == len(colors_to_calibrate)
        if done_calibrating:
            color_detector.set_cube_color_pallete(calibrated_colors)
            config.set_setting(CUBE_PALETTE, color_detector.cube_color_palette)


def set_calibrate_mode(event):
    # Toggle calibrate mode.
    global calibrate_mode
    reset_calibrate_mode()
    calibrate_mode = not calibrate_mode

### Main ###
if __name__ == "__main__":
    image_id = None
    contours = None

    colors_to_calibrate = ['green', 'red', 'blue', 'orange', 'white', 'yellow']
    average_sticker_colors = {}
    result_state = {}

    calibrate_mode = False
    calibrated_colors = {}
    current_color_to_calibrate_index = 0
    done_calibrating = False

    snapshot_state = [(255,255,255), (255,255,255), (255,255,255),
                                (255,255,255), (255,255,255), (255,255,255),
                                (255,255,255), (255,255,255), (255,255,255)]
    preview_state  = [(255,255,255), (255,255,255), (255,255,255),
                                (255,255,255), (255,255,255), (255,255,255),
                                (255,255,255), (255,255,255), (255,255,255)]

    root = tk.Tk()
    root.title("Rubik's Cube Solver")

    # Title Label
    title_label = tk.Label(root, text="Rubik's Cube Solver", font=("Helvetica", 20))
    title_label.pack(pady=10)

    # Mode Title Label
    mode_title = tk.Label(root, text="", font=("Helvetica", 16))

    # Mode Label
    mode_label = tk.Label(root, text="Select mode:")
    mode_label.pack()

    # Buttons
    auto_button = tk.Button(root, text="Atomatic", command=set_mode_auto)
    auto_button.pack(pady=10)

    manual_button = tk.Button(root, text="Manual", command=set_manual_mode)
    manual_button.pack(pady=10)

    root.bind("<Escape>", close_app)  # Asociar la tecla Escape con la función de cierre
    root.bind('c', set_calibrate_mode)
    root.bind('<space>', update_key)

    canvas = tk.Canvas(root, width=12 * width + 20, height=9 * width + 20)
    canvas.pack()

    root.mainloop()
