import tkinter as tk
from PIL import Image, ImageTk
import numpy as np
import cv2
import kociemba as kc
from colordetection import color_detector
from config import config
from PIL import ImageFont, ImageDraw, Image

width = 60  # width of a facelet in pixels
facelet_id = [[[0 for col in range(3)] for row in range(3)] for face in range(6)]
colorpick_id = [0 for i in range(6)]
curcol = None
t = ("U", "R", "F", "D", "L", "B")
cols = ("yellow", "green", "red", "white", "blue", "orange")
from constants import (
    COLOR_PLACEHOLDER,
    LOCALES,
    ROOT_DIR,
    CUBE_PALETTE,
    MINI_STICKER_AREA_TILE_SIZE,
    MINI_STICKER_AREA_TILE_GAP,
    MINI_STICKER_AREA_OFFSET,
    STICKER_AREA_TILE_SIZE,
    STICKER_AREA_TILE_GAP,
    STICKER_AREA_OFFSET,
    STICKER_CONTOUR_COLOR,
    CALIBRATE_MODE_KEY,
    SWITCH_LANGUAGE_KEY,
    TEXT_SIZE,
    E_INCORRECTLY_SCANNED,
    E_ALREADY_SOLVED
)



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
########################################################################################################################

# ############################### Solve the displayed cube with a local or remote server ###############################

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
    """Connect to the server and return the solving maneuver."""
    display.delete(1.0, tk.END)  # clear output window

    try:
        defstr = get_definition_string()
    except BaseException as e:
        show_text(f'Cubo invalido {e.__doc__}')
        return
    
    show_text(defstr)
    try:
        if(defstr != 'UUUUUUUUURRRRRRRRRFRFFFFFFFDDDDDDDDDLLLLLLLLLBBBBBBBBB'):
            algo = kc.solve(defstr)

            count = count_moves(algo)
            show_text(f'Solucion: {algo}\n')
            show_text(f'Numero de movimientos: {count}')
        else:
            show_text('\nCubo ya resuelto')
    except BaseException as e:
        show_text(e.args[0])
        return

########################################################################################################################

# ################################# Functions to change the facelet colors #############################################


def clean():
    """Restore the cube to a clean cube."""
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
                    #if side in self.result_state:
                    #    foreground_color = color_detector.get_prominent_color(self.result_state[side][index])

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
    manual_mode = True
    mode_label.pack_forget()
    auto_button.pack_forget()
    manual_button.pack_forget()
    mode_title.config(text="Modo Manual")
    mode_title.pack(side=tk.TOP, pady=10)
    manual_label.pack(side=tk.TOP, pady=20)

    global display

    bsolve = tk.Button(text="Solve", height=2, width=10, relief=tk.RAISED, command=solve)
    bsolve_window = canvas.create_window(10 + 10.5 * width, 10 + 6.5 * width, anchor=tk.NW, window=bsolve)
    bclean = tk.Button(text="Clean", height=1, width=10, relief=tk.RAISED, command=clean)
    bclean_window = canvas.create_window(10 + 10.5 * width, 10 + 7.5 * width, anchor=tk.NW, window=bclean)
    bempty = tk.Button(text="Empty", height=1, width=10, relief=tk.RAISED, command=empty)
    bempty_window = canvas.create_window(10 + 10.5 * width, 10 + 8 * width, anchor=tk.NW, window=bempty)
    brandom = tk.Button(text="Random", height=1, width=10, relief=tk.RAISED, command=random)
    brandom_window = canvas.create_window(10 + 10.5 * width, 10 + 8.5 * width, anchor=tk.NW, window=brandom)
    display = tk.Text(height=7, width=39)
    text_window = canvas.create_window(10 + 6.5 * width, 10 + .5 * width, anchor=tk.NW, window=display)
    canvas.bind("<Button-1>", click)
    create_facelet_rects(width)
    create_colorpick_rects(width)

def get_font(size=TEXT_SIZE):
        """Load the truetype font with the specified text size."""
        font_path = '{}/assets/arial-unicode-ms.ttf'.format(ROOT_DIR)
        return ImageFont.truetype(font_path, size)

def render_text(text, pos, color=(255, 255, 255), size=TEXT_SIZE, anchor='lt'):
        """
        Render text with a shadow using the pillow module.
        """
        global frame

        font = get_font(24)

        # Convert opencv frame (np.array) to PIL Image array.
        frame2 = Image.fromarray(frame)

        # Draw the text onto the image.
        draw = ImageDraw.Draw(frame2)
        draw.text(pos, text, font=font, fill=color, anchor=anchor,
                  stroke_width=1, stroke_fill=(0, 0, 0))

        # Convert the pillow frame back to a numpy array.
        frame = np.array(frame2)


def draw_stickers(stickers, offset_x, offset_y):
        """Draws the given stickers onto the given frame."""

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


def draw_2d_cube_state():
        
        global frame
        global width, height

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

def show_frame():
    global image_id, frame

    ret, frame = cam.read()
   # Hola que tal
    if ret and not manual_mode:
        fr = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(fr)
        photo = ImageTk.PhotoImage(image=img)
       
        canvas.photo = photo

        if image_id:
            canvas.itemconfig(image_id, image=photo)
        else:
            image_id = canvas.create_image((0, 0), image=photo, anchor='nw')
            canvas.configure(width=photo.width(), height=photo.height())
           
    render_text("HOLA COMO ANDAS", (20, height - 20), anchor='lb')
    draw_2d_cube_state()
    draw_preview_stickers()
    cv2.imshow("Qbr - Rubik's cube solver", frame)
    root.after(20, show_frame)


def select_mode_auto():
    global manual_mode, cam, width, height

    cam = cv2.VideoCapture(1)
    cam.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cam.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    width = int(cam.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cam.get(cv2.CAP_PROP_FRAME_HEIGHT))
    
    manual_mode = False
    mode_label.pack_forget()
    auto_button.pack_forget()
    manual_button.pack_forget()
    mode_title.config(text="Modo Automático")
    mode_title.pack(side=tk.TOP, pady=10)
    canvas.pack(fill='both', expand=True)
    show_frame()

def select_mode_manual():
    set_manual_mode()

def close_app(event):
    root.destroy()

# --- main ---

image_id = None

colors_to_calibrate = ['green', 'red', 'blue', 'orange', 'white', 'yellow']
average_sticker_colors = {}
result_state = {}

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
mode_label = tk.Label(root, text="Selecciona modo:")
mode_label.pack()

canvas = tk.Canvas(root)

manual_label = tk.Label(root, text="Seleccion manual de colores")

# Buttons
auto_button = tk.Button(root, text="Automático", command=select_mode_auto)
auto_button.pack(pady=10)

manual_button = tk.Button(root, text="Manual", command=select_mode_manual)
manual_button.pack(pady=10)

root.bind("<Escape>", close_app)  # Asociar la tecla Escape con la función de cierre

canvas = tk.Canvas(root, width=12 * width + 20, height=9 * width + 20)
canvas.pack()

root.mainloop()
