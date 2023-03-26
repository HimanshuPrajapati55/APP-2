from pathlib import Path
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage, filedialog
from moviepy.editor import *
from tkinter.filedialog import askopenfilename
import cv2
import os
import subprocess
import tkinter.messagebox as mbox
from PIL import Image, ImageTk
from tkinter.messagebox import askyesno
from tkinter.ttk import Progressbar

OUTPUT_PATH = Path(__file__).parent
ASSETS_PATH = OUTPUT_PATH / \
    Path(r"C:\Users\ASUS\Desktop\new\build\assets\frame0")


def relative_to_assets(path: str) -> Path:
    return ASSETS_PATH / Path(path)


window = Tk()
window.title("Video Editing App")
window.geometry("360x800")

canvas = Canvas(
    window,
    height=800,
    width=360,
    bd=0,
    highlightthickness=0,
    relief="ridge"
)

cap = None
photo = None

def import_video():
    global playing, cap, photo
    # Use a file dialog to select a video file
    file_path = filedialog.askopenfilename(
        title="Open Video",
        filetypes=(("Video files", "*.mp4"), ("All files", "*.*"))
    )
    if not file_path:
        return

    # Create a VideoCapture object to read the video frames
    cap = cv2.VideoCapture(file_path)

    playing = True

    fps = cap.get(cv2.CAP_PROP_FPS)
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    duration = frame_count / fps

    # Calculate the width of each second on the timeline
    timeline_width = 360.0 / duration

    # Loop through the frames and display them on the canvas
    while True:
        # Read the next frame
        ret, frame = cap.read()
        if not ret:
            break

        # Convert the OpenCV frame to a PIL image
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image = Image.fromarray(image)

        # Resize the image to fit the canvas
        image = image.resize((360, 336))

        # Create a PhotoImage object from the PIL image
        photo = ImageTk.PhotoImage(image)

        # Display the image on the canvas
        canvas.create_image(0, 49, image=photo, anchor="nw")
        

        current_time = cap.get(cv2.CAP_PROP_POS_MSEC) / 1000.0
        current_position = current_time * timeline_width

        # Display the current position on the timeline
        canvas.create_rectangle(
            current_position,
            420.0,
            current_position + 2.0,
            430.0,
            fill="#FFFFFF",
            outline="")
        

        # Update the canvas
        window.update()

        while not playing:
            window.update()

    # Release the VideoCapture object
    cap.release()

# Define a function to play the video


def play_video():
    global playing
    playing = True

# Define a function to pause the video

def pause_video():
    global playing
    playing = False

def delete_video():
    global cap, photo
    
    # Release the VideoCapture object and delete the photo object
    cap.release()
    photo = None
        
    # Enable the "Open Video" button
    import_video.config(state="normal")
    
    # Set cap to None
    cap = None

def export_video():
    global cap, photo

    if cap is None:
        return

    export_path = filedialog.asksaveasfilename(
        title="Export Video",
        defaultextension=".mp4",
        filetypes=(("Video files", "*.mp4"), ("All files", "*.*"))
    )
    if not export_path:
        return

    # Define the output video format
    fourcc = cv2.VideoWriter_fourcc(*"mp4v")

    # Define the output video dimensions and frame rate
    width, height = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = int(cap.get(cv2.CAP_PROP_FPS))

    # Create a VideoWriter object to write the output video
    out = cv2.VideoWriter(export_path, fourcc, fps, (width, height))

    # Reset the video capture to the beginning
    cap.set(cv2.CAP_PROP_POS_FRAMES, 0)

    # Create the progress bar widget
    progress = Progressbar(window, orient="horizontal", length=300, mode="determinate")
    progress.place(x=30, y=700)
    # Create the cancel button widget
    cancel_button = Button(window, text="Cancel", command=cancel_export)
    cancel_button.place(x=250, y=700)


    i = 0
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    canceled = False
    while True:
        ret, frame = cap.read()
        if not ret or canceled:
            break
        out.write(frame)

        # Update the progress bar
        i += 1
        progress["value"] = i / total_frames * 100
        window.update()

    # Release the VideoWriter and VideoCapture objects
    out.release()
    cap.release()

    # Destroy the progress bar widget
    progress.destroy()
    cancel_button.destroy()

    if canceled:
        # Delete the partially exported file
        Path(export_path).unlink(missing_ok=True)
        return

    # Display a message box to confirm the video export
    subprocess.Popen(['notify-send', 'Video exported successfully!', '-t', '3000'])

def cancel_export():
    global cap
    response = askyesno("Cancel export", "Do you want to cancel the export?")
    if response:
        cap.release()

canvas.place(x=0, y=0)
canvas.create_rectangle(
    0.0,
    0.0,
    360.0,
    800.0,
    fill="#000000",
    outline="")

canvas.create_rectangle(
    0.0,
    433.0,
    360.0,
    497.0,
    fill="#2C2C2C",
    outline="")


canvas.create_rectangle(
    0.0,
    49.0,
    360.0,
    385.0,
    fill="#333333",
    outline="")

canvas.create_rectangle(
    0.0,
    497.0,
    360.0,
    565.0,
    fill="#191919",
    outline="")

canvas.create_rectangle(
    0.0,
    635.0,
    360.0,
    712.0,
    fill="#191919",
    outline="")

canvas.create_rectangle(
    0.0,
    566.0,
    360.0,
    635.0,
    fill="#262626",
    outline="")

button_image_1 = PhotoImage(
    file=relative_to_assets("button_1.png"))
button_1 = Button(
    image=button_image_1,
    command=lambda: print("button_1 clicked"),
    relief="flat",
    bg="#191919"
)

button_1.place(
    x=15.0,
    y=506.0,
    width=48.0,
    height=46.22222900390625
)

button_image_2 = PhotoImage(
    file=relative_to_assets("button_2.png"))
button_2 = Button(
    image=button_image_2,
    borderwidth=0,
    highlightthickness=0,
    command=export_video,
    relief="flat",
    bg="#000000"
)
button_2.place(
    x=312.0,
    y=1.0,
    width=48.0,
    height=48.0
)


button_image_3 = PhotoImage(
    file=relative_to_assets("button_3.png"))
button_3 = Button(
    image=button_image_3,
    borderwidth=0,
    highlightthickness=0,
    command=import_video,
    relief="flat",
    bg="#000000"

)

button_3.place(
    x=2.0,
    y=1.0,
    width=48.0,
    height=48.0
)

button_image_4 = PhotoImage(
    file=relative_to_assets("button_4.png"))
button_4 = Button(
    image=button_image_4,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("button_4 clicked"),
    relief="flat",
    bg="#000000"
)
button_4.place(
    x=233.0,
    y=385.0,
    width=28.0,
    height=28.0
)

button_image_5 = PhotoImage(
    file=relative_to_assets("button_5.png"))
button_5 = Button(
    image=button_image_5,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("button_5 clicked"),
    relief="flat",
    bg="#000000"
)
button_5.place(
    x=305.0,
    y=385.0,
    width=28.0,
    height=28.0
)

button_image_6 = PhotoImage(
    file=relative_to_assets("button_6.png"))
button_6 = Button(
    image=button_image_6,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("button_6 clicked"),
    relief="flat",
    bg="#000000"
)
button_6.place(
    x=151.0,
    y=736.0,
    width=48.0,
    height=48.0
)

button_image_7 = PhotoImage(
    file=relative_to_assets("button_7.png"))
button_7 = Button(
    image=button_image_7,
    borderwidth=0,
    highlightthickness=0,
    command=delete_video,
    relief="flat",
    bg="#000000"
)
button_7.place(
    x=86.0,
    y=736.0,
    width=48.0,
    height=48.0
)

button_image_8 = PhotoImage(
    file=relative_to_assets("button_8.png"))
button_8 = Button(
    image=button_image_8,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("button_8 clicked"),
    relief="flat",
    bg="#000000"
)
button_8.place(
    x=31.0,
    y=736.0,
    width=48.0,
    height=48.0
)

button_image_9 = PhotoImage(
    file=relative_to_assets("button_9.png"))
button_9 = Button(
    image=button_image_9,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("button_9 clicked"),
    relief="flat",
    bg="#000000"
)
button_9.place(
    x=216.0,
    y=736.0,
    width=48.0,
    height=48.0
)

button_image_10 = PhotoImage(
    file=relative_to_assets("button_10.png"))
button_10 = Button(
    image=button_image_10,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("button_10 clicked"),
    relief="flat",
    bg="#000000"
)
button_10.place(
    x=281.0,
    y=737.0,
    width=48.0,
    height=48.0
)

button_image_11 = PhotoImage(
    file=relative_to_assets("button_11.png"))
button_11 = Button(
    image=button_image_11,
    borderwidth=0,
    highlightthickness=0,
    command=lambda: print("button_11 clicked"),
    bg="#333333"
)
button_11.place(
    x=15.0,
    y=441.0,
    width=48.0,
    height=48.0,

)

button_image_12 = PhotoImage(
    file=relative_to_assets("button_12.png"))
button_12 = Button(
    image=button_image_12,
    borderwidth=0,
    highlightthickness=0,
    command=play_video,
    bg="#000000"
)
button_12.place(
    x=15.0,
    y=384.0,
    width=28.0,
    height=28.0
)

button_image_13 = PhotoImage(
    file=relative_to_assets("button_13.png"))
button_13 = Button(
    image=button_image_13,
    borderwidth=0,
    highlightthickness=0,
    command=pause_video,
    relief="flat",
    bg="#000000"
)
button_13.place(
    x=67.0,
    y=384.0,
    width=28.0,
    height=28.0
)
window.resizable(False, False)
window.mainloop()
