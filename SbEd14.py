import tkinter as tk
from tkinter import filedialog, messagebox, ttk, colorchooser
import struct
import webbrowser

file_path = None
offsets = {}
colors = {}

# New global variables to store the previous file path and values
previous_file_path = None
previous_offsets_values = {}
previous_color_values = {}

def read_internal_name(file_path):
    try:
        with open(file_path, 'rb') as file:
            file_content = file.read()
            decoded_text = file_content.decode('utf-8', errors='ignore')
            
            # Internal Name 7002 was not included here because their color and size offsets couldn't be found
            possible_internal_names = ["15002", "2002", "3002", "4002", "5002", "6002", "8002"]

            for internal_name in possible_internal_names:
                if internal_name in decoded_text:
                    return internal_name

            return None
    except Exception as e:
        messagebox.showerror("Error", f"Failed to read internal name: {e}")
        return None

def open_file():
    global file_path  # Declare file_path as global
    file_path = filedialog.askopenfilename(filetypes=[("FIFA Big Files", "*.big")])
    if file_path:
        update_status(f"File Loaded: {file_path}", "blue")
        add_internal_name()
        load_current_values()

def load_current_values():
    global file_path, previous_file_path, previous_offsets_values, previous_color_values  # Declare globals
    if not file_path:
        return
    
    with open(file_path, 'rb') as file:
        for offset in offsets_values.keys():
            file.seek(offset)
            data = file.read(4)
            value = struct.unpack('<f', data)[0]
            offsets_vars[offset].set(value)
            # Update previous values as well
            previous_offsets_values[offset] = value
        
        for offset in color_values.keys():
            file.seek(offset)
            data = file.read(4)
            # Read the color in little-endian format
            color_code = f'#{data[2]:02X}{data[1]:02X}{data[0]:02X}'
            color_values[offset] = color_code
            color_vars[offset].set(color_code)
            color_previews[offset].config(bg=color_code)
            # Update previous color values as well
            previous_color_values[offset] = color_code

def add_internal_name():
    global file_path, previous_file_path, previous_offsets_values, previous_color_values  # Declare globals
    internal_name = read_internal_name(file_path)
    if internal_name:
        internal_name_label.config(text=f"Internal Name: {internal_name}")
        set_offsets_and_colors(internal_name)
        # Store the current file path and values as the last valid ones
        previous_file_path = file_path
        previous_offsets_values = {offset: offsets_vars[offset].get() for offset in offsets_vars}
        previous_color_values = {offset: color_vars[offset].get() for offset in color_vars}
    else:
        messagebox.showerror("Error", "No internal name was detected. Reverting back to the previous file.")
        if previous_file_path:
            file_path = previous_file_path
            load_previous_values()
        else:
            update_status("No valid file to revert to.", "red")
        return

def load_previous_values():
    global file_path  # Declare file_path as global
    if previous_file_path:
        file_path = previous_file_path
        for offset in previous_offsets_values:
            offsets_vars[offset].set(previous_offsets_values[offset])
        for offset in previous_color_values:
            color_vars[offset].set(previous_color_values[offset])
            color_previews[offset].config(bg=previous_color_values[offset])
        update_status(f"Reverted to previous file: {file_path}", "orange")

def set_offsets_and_colors(internal_name):
    global offsets, colors
    if internal_name == "15002":
        offsets = {
            "Home Team Name X": 0xEB4,
            "Home Team Name Y": 0xEB8,
            "Away Team Name X": 0xEF4,
            "Away Team Name Y": 0xEF8,
            "Home Score X": 0xF74,
            "Home Score Y": 0xF78,
            "Away Score X": 0xF34,
            "Away Score Y": 0xF38,
            "Time Text X": 0x1434,
            "Time Text Y": 0x1438,
            "Stoppage Time Text X": 0x13F4,
            "Stoppage Time Text Y": 0x13F8,
            "Home Crest X": 0x1274,
            "Home Crest Y": 0x1278,
            "Away Crest X": 0x1234,
            "Away Crest Y": 0x1238,
            "Full Scoreboard X": 0xBDC,
            "Full Scoreboard Y": 0xBE0,
            "Home Team Name Size": 0x578,
            "Away Team Name Size": 0x5D8,
            "Home Score Size": 0x698,
            "Away Score Size": 0x638,
            "1st Digit of Time Size": 0x8D8,
            "2nd Digit of Time Size": 0x894,
            "Colon Seperator of Time Size": 0x91C,
            "3rd Digit of Time Size": 0x850,
            "4th Digit of Time Size": 0x80C,
            "Home Crest Size (Width)": 0x1264,
            "Home Crest Size (Height)": 0x1270,
            "Away Crest Size (Width)": 0x1224,
            "Away Crest Size (Height)": 0x1230
        }
        colors = {
            "Home Team Color": 0x574,
            "Away Team Color": 0x5D4,
            "Home Score Color": 0x694,
            "Away Score Color": 0x634,
            "1st Digit of Time Color": 0x8D4,
            "2nd Digit of Time Color": 0x890,
            "Colon Seperator of Time Color": 0x918,
            "3rd Digit of Time Color": 0x84C,
            "4th Digit of Time Color": 0x808
        }
    elif internal_name == "8002":
        offsets = {
            # Positions
            "Home Team Name X": 0x1608,
            "Home Team Name Y": 0x160C,
            "Away Team Name X": 0x1648,
            "Away Team Name Y": 0x164C,
            "Home Score X": 0x1688,
            "Home Score Y": 0x168C,
            "Away Score X": 0x16C8,
            "Away Score Y": 0x16CC,
            "Time Text X": 0x1708,
            "Time Text Y": 0x170C,
            "Stoppage Time X": 0x40E8,
            "Stoppage Time Y": 0x40EC,
            "Home Color Bar X": 0x17C8,
            "Home Color Bar Y": 0x17CC,
            "Away Color Bar X": 0x1888,
            "Away Color Bar Y": 0x188C,
            "Full Scoreboard X": 0x1230,
            "Full Scoreboard Y": 0x1234,
            # Sizes
            "Team Name Shadow Size": 0x4F8,
            "Team Name Size": 0x53C,
            "Score Shadow Size": 0x59C,
            "Score Size": 0x5E0,
            "Time Text Shadow Size": 0x640,
            "Time Text Size": 0x684,
            "Stoppage Time Text Size": 0x8F8
        }

        colors = {
            # Colors
            "Team Name Shadow Color": 0x4F4,
            "Team Name Color": 0x538,
            "Score Shadow Color": 0x598,
            "Score Color": 0x5DC,
            "Time Text Shadow Color": 0x63C,
            "Time Text Color": 0x680,
            "Stoppage Time Text Color": 0x8F4
        }
    elif internal_name == "6002":
        offsets = {
            # Positions
            "Home Team Name X": 0x2ACC,
            "Home Team Name Y": 0x2AD0,
            "Away Team Name X": 0x2B0C,
            "Away Team Name Y": 0x2B10,
            "Home Team Name Shadow X": 0x294C,
            "Home Team Name Shadow Y": 0x2950,
            "Away Team Name Shadow X": 0x298C,
            "Away Team Name Shadow Y": 0x2990,
            "Home Score X": 0x9404,
            "Home Score Y": 0x9408,
            "Score Seperator X": 0x9484,
            "Score Seperator Y": 0x9488,
            "Score Seperator Shadow X": 0x9444,
            "Score Seperator Shadow Y": 0x9448,
            "Away Score X": 0x9384,
            "Away Score Y": 0x9388,
            "Home Score Shadow X": 0x93C4,
            "Home Score Shadow Y": 0x93C8,
            "Away Score Shadow X": 0x9344,
            "Away Score Shadow Y": 0x9348,
            "Time Text X": 0x96C4,
            "Time Text Y": 0x96C8,
            "Stoppage Time Text X": 0x9584,
            "Stoppage Time Text Y": 0x9588,
            "Full Scoreboard X": 0x28B4,
            "Full Scoreboard Y": 0x28B8,
            # Sizes
            "Team Name Shadow Size": 0x9A4,
            "Team Name Size": 0x9E8,
            "Home Score Shadow Size": 0xAEC,
            "Home Score Size": 0xB30,
            "Away Score Shadow Size": 0xA64,
            "Away Score Size": 0xAA8,
            "Score Seperator Shadow Size": 0xB74,
            "Score Seperator Size": 0xBB8,
            "Time Text Shadow Size": 0xC18,
            "Time Text Size": 0xC5C,
            "Stoppage Time Text Size": 0x6DC
        }

        colors = {
            # Colors
            "Team Name Shadow Color": 0x9A0,
            "Team Name Color": 0x9E4,
            "Home Score Shadow Color": 0xAE8,
            "Home Score Color": 0xB2C,
            "Away Score Shadow Color": 0xA60,
            "Away Score Color": 0xAA4,
            "Score Seperator Shadow Color": 0xB70,
            "Score Seperator Color": 0xBB4,
            "Time Text Shadow Color": 0xC14,
            "Time Text Color": 0xC58,
            "Stoppage Time Text Color": 0x6D8
        }
    elif internal_name == "5002":
        offsets = {
            # Positions
            "Home Team Name X": 0x2F84,
            "Home Team Name Y": 0x2F88,
            "Away Team Name X": 0x2FC4,
            "Away Team Name Y": 0x2FC8,
            "Home Team Name Shadow X": 0x2E04,
            "Home Team Name Shadow Y": 0x2E08,
            "Away Team Name Shadow X": 0x2E44,
            "Away Team Name Shadow Y": 0x2E48,
            "Home Score X": 0xD604,
            "Home Score Y": 0xD608,
            "Away Score X": 0xD584,
            "Away Score Y": 0xD588,
            "Home Score Shadow X": 0xD5C4,
            "Home Score Shadow Y": 0xD5C8,
            "Away Score Shadow X": 0xD544,
            "Away Score Shadow Y": 0xD548,
            "Time Text X": 0xD8C4,
            "Time Text Y": 0xD8C8,
            "Stoppage Time Text X": 0xD784,
            "Stoppage Time Text Y": 0xD788,
            "Full Scoreboard X": 0x2D6C,
            "Full Scoreboard Y": 0x2D70,
            # Sizes
            "Team Name Shadow Size": 0xACC,
            "Team Name Size": 0xB10,
            "Home Score Shadow Size": 0xC30,
            "Home Score Size": 0xC74,
            "Away Score Shadow Size": 0xB8C,
            "Away Score Size": 0xBD0,
            "Time Text Shadow Size": 0xCF0,
            "Time Text Size": 0xD34,
            "Stoppage Time Text Size": 0x3B8
        }

        colors = {
            # Colors
            "Team Name Shadow Color": 0xAC8,
            "Team Name Color": 0xB0C,
            "Home Score Shadow Color": 0xC2C,
            "Home Score Color": 0xC70,
            "Away Score Shadow Color": 0xB88,
            "Away Score Color": 0xBCC,
            "Time Text Shadow Color": 0xCEC,
            "Time Text Color": 0xD30,
            "Stoppage Time Text Color": 0x3B4
        }
    elif internal_name == "4002":
        offsets = {
            # Positions
            "Home Team Name X": 0x19A8,
            "Home Team Name Y": 0x19AC,
            "Away Team Name X": 0x19E8,
            "Away Team Name Y": 0x19EC,
            "Home Score X": 0x1A28,
            "Home Score Y": 0x1A2C,
            "Score Seperator X": 0x1AE8,
            "Score Seperator Y": 0x1AEC,
            "Away Score X": 0x1A68,
            "Away Score Y": 0x1A6C,
            "Time Text X": 0x1AA8,
            "Time Text Y": 0x1AAC,
            "Stoppage Time Text X": 0x1128,
            "Stoppage Time Text Y": 0x112C,
            "Full Scoreboard X": 0xE10,
            "Full Scoreboard Y": 0xE14,
            # Sizes
            "Team Name Shadow Size": 0x7B4,
            "Team Name Size": 0x7F8,
            "Home Score Shadow Size": 0x858,
            "Home Score Size": 0x89C,
            "Away Score Shadow Size": 0x8FC,
            "Away Score Size": 0x940,
            "Score Seperator Shadow Size": 0xA00,
            "Score Seperator Size": 0xA44,
            "Time Text Size": 0x9A0,
            "Stoppage Time Text Size": 0x490
        }

        colors = {
            # Colors
            "Team Name Shadow Color": 0x7B0,
            "Team Name Color": 0x7F4,
            "Home Score Shadow Color": 0x854,
            "Home Score Color": 0x898,
            "Away Score Shadow Color": 0x8F8,
            "Away Score Color": 0x93C,
            "Score Seperator Shadow Color": 0x9FC,
            "Score Seperator Color": 0xA40,
            "Time Text Color": 0x99C,
            "Stoppage Time Text Color": 0x48C
        }
    elif internal_name == "3002":
        offsets = {
            # Positions
            "Home Team Name X": 0x26A8,
            "Home Team Name Y": 0x26AC,
            "Away Team Name X": 0x2668,
            "Away Team Name Y": 0x266C,
            "Home Score Shadow X": 0x79D0,
            "Home Score Shadow Y": 0x79D4,
            "Score Seperator Shadow X": 0x7A50,
            "Score Seperator Shadow Y": 0x7A54,
            "Away Score Shadow X": 0x7950,
            "Away Score Shadow Y": 0x7954,
            "Home Score X": 0x7A10,
            "Home Score Y": 0x7A14,
            "Score Seperator X": 0x7A90,
            "Score Seperator Y": 0x7A94,
            "Away Score X": 0x7990,
            "Away Score Y": 0x7994,
            "Time Text X": 0x7ED0,
            "Time Text Y": 0x7ED4,
            "Stoppage Time Text X": 0x7C10,
            "Stoppage Time Text Y": 0x7C14,
            "Full Scoreboard X": 0x2590,
            "Full Scoreboard Y": 0x2594,
            # Sizes
            "Team Name Size": 0x8F4,
            "Home Score Shadow Size": 0x9DC,
            "Home Score Size": 0xA20,
            "Away Score Shadow Size": 0x954,
            "Away Score Size": 0x998,
            "Score Seperator Shadow Size": 0xA64,
            "Score Seperator Size": 0xAA8,
            "Time Text Shadow Size": 0xB08,
            "Time Text Size": 0xB4C,
            "Stoppage Time Text Size": 0x5B0
        }

        colors = {
            # Colors
            "Team Name Color": 0x8F0,
            "Home Score Shadow Color": 0x9D8,
            "Home Score Color": 0xA1C,
            "Away Score Shadow Color": 0x950,
            "Away Score Color": 0x994,
            "Score Seperator Shadow Color": 0xA60,
            "Score Seperator Color": 0xAA4,
            "Time Text Shadow Color": 0xB04,
            "Time Text Color": 0xB48,
            "Stoppage Time Text Color": 0x5AC
        }
    elif internal_name == "2002":
        offsets = {
            # Positions
            "Home Team Name X": 0x2960,
            "Home Team Name Y": 0x2964,
            "Away Team Name X": 0x29A0,
            "Away Team Name Y": 0x29A4,
            "Home Score Shadow X": 0xB850,
            "Home Score Shadow Y": 0xB854,
            "Score Seperator Shadow X": 0xB890,
            "Score Seperator Shadow Y": 0xB894,
            "Away Score Shadow X": 0xB8D0,
            "Away Score Shadow Y": 0xB8D4,
            "Home Score X": 0xB910,
            "Home Score Y": 0xB914,
            "Score Seperator X": 0xB950,
            "Score Seperator Y": 0xB954,
            "Away Score X": 0xB990,
            "Away Score Y": 0xB994,
            "Time Text X": 0xBD90,
            "Time Text Y": 0xBD94,
            "Stoppage Time Text X": 0xBB10,
            "Stoppage Time Text Y": 0xBB14,
            "Full Scoreboard X": 0x2888,
            "Full Scoreboard Y": 0x288C,
            # Sizes
            "Team Name Shadow Size": 0x7A8,
            "Team Name Size": 0x7EC,
            "Home Score Shadow Size": 0x868,
            "Home Score Size": 0x934,
            "Away Score Shadow Size": 0x8F0,
            "Away Score Size": 0x9BC,
            "Score Seperator Shadow Size": 0x8AC,
            "Score Seperator Size": 0x978,
            "Time Text Shadow Size": 0xA1C,
            "Time Text Size": 0xA60
        }

        colors = {
            # Colors
            "Team Name Shadow Color": 0x7A4,
            "Team Name Color": 0x7E8,
            "Home Score Shadow Color": 0x864,
            "Home Score Color": 0x930,
            "Away Score Shadow Color": 0x8EC,
            "Away Score Color": 0x9B8,
            "Score Seperator Shadow Color": 0x8A8,
            "Score Seperator Color": 0x974,
            "Time Text Shadow Color": 0xA18,
            "Time Text Color": 0xA5C
        }
    else:
        messagebox.showerror("Error", "Invalid internal name detected.")
        return    

    recreate_widgets()

def recreate_widgets():
    global offsets_vars, offsets_values, color_vars, color_values, color_previews

    # Clear previous widgets
    for widget in positions_frame.winfo_children():
        widget.destroy()
    for widget in sizes_frame.winfo_children():
        widget.destroy()
    for widget in colors_frame.winfo_children():
        widget.destroy()

    # Define new variables and values
    offsets_vars = {offset: tk.StringVar() for offset in offsets.values()}
    offsets_values = {offset: 0.0 for offset in offsets.values()}
    color_vars = {offset: tk.StringVar(value='#000000') for offset in colors.values()}
    color_values = {offset: "#000000" for offset in colors.values()}
    color_previews = {}

    # Add positions to Positions tab
    row = 0
    for label_text, offset in offsets.items():
        if "Size" not in label_text:
            col = 0 if "X" in label_text else 4
            tk.Label(positions_frame, text=label_text).grid(row=row, column=col, padx=10, pady=5)
            entry = tk.Entry(positions_frame, textvariable=offsets_vars[offset])
            entry.grid(row=row, column=col+1, padx=10, pady=5)
            entry.bind("<KeyRelease>", lambda e, offset=offset, var=offsets_vars[offset]: update_value(offset, var))
            entry.bind('<KeyPress-Up>', lambda e, var=offsets_vars[offset]: increment_value(e, var))
            entry.bind('<KeyPress-Down>', lambda e, var=offsets_vars[offset]: increment_value(e, var))
            if col == 4:
                row += 1

    # Add sizes to Sizes tab
    row = 0
    for label_text, offset in offsets.items():
        if "Size" in label_text:
            tk.Label(sizes_frame, text=label_text).grid(row=row, column=0, padx=10, pady=5)
            entry = tk.Entry(sizes_frame, textvariable=offsets_vars[offset])
            entry.grid(row=row, column=1, padx=10, pady=5)
            entry.bind("<KeyRelease>", lambda e, offset=offset, var=offsets_vars[offset]: update_value(offset, var))
            entry.bind('<KeyPress-Up>', lambda e, var=offsets_vars[offset]: increment_value(e, var))
            entry.bind('<KeyPress-Down>', lambda e, var=offsets_vars[offset]: increment_value(e, var))
            row += 1

    # Add colors to Colors tab
    row = 0
    for label_text, offset in colors.items():
        tk.Label(colors_frame, text=label_text).grid(row=row, column=0, padx=10, pady=5)
        entry = tk.Entry(colors_frame, textvariable=color_vars[offset])
        entry.grid(row=row, column=1, padx=10, pady=5)
        entry.bind('<KeyPress>', lambda e, var=color_vars[offset]: restrict_color_entry(e, var))
        entry.bind('<KeyRelease>', lambda e, offset=offset, var=color_vars[offset]: update_color_preview(offset, var.get()))
        color_preview = tk.Label(colors_frame, bg=color_values[offset], width=2)
        color_preview.grid(row=row, column=2, padx=10, pady=5)
        color_preview.bind("<Button-1>", lambda e, offset=offset, var=color_vars[offset]: choose_color(offset, var))
        color_previews[offset] = color_preview
        update_func = lambda offset=offset, var=color_vars[offset]: update_color(offset, var)
        tk.Button(colors_frame, text="Update", command=update_func).grid(row=row, column=3, padx=10, pady=5)
        row += 1

def save_file():
    global file_path
    if not file_path:
        messagebox.showerror("Error", "No file loaded.")
        return
    
    try:
        with open(file_path, 'r+b') as file:  # Open the file in read and write binary mode
            # First, read the entire content of the file
            file_content = file.read()
            file.seek(0)  # Rewind to the beginning of the file

            # Update all offsets with the current values
            for offset, var in offsets_vars.items():
                value = var.get()
                try:
                    # Ensure the value is a float
                    value = float(value)
                    packed_value = struct.pack('<f', value)
                    # Debug: Print the value and packed bytes
                    print(f"Offset: {offset}, Value: {value}, Packed: {packed_value.hex()}")
                    # Ensure correct file positioning
                    file.seek(offset)
                    file.write(packed_value)
                except ValueError:
                    messagebox.showerror("Error", f"Invalid float value at offset {offset}: {value}")
                    return

            for offset, var in color_vars.items():
                color_code = var.get()
                try:
                    # Convert color to little-endian format and pack it
                    color_bytes = bytes.fromhex(color_code[1:])[::-1]
                    # Debug: Print the color code and packed bytes
                    print(f"Offset: {offset}, Color Code: {color_code}, Packed: {color_bytes.hex()}")
                    # Ensure correct file positioning
                    file.seek(offset)
                    file.write(color_bytes)
                except ValueError:
                    messagebox.showerror("Error", f"Invalid color code at offset {offset}: {color_code}")
                    return

        update_status("File saved successfully.", "green")

    except Exception as e:
        messagebox.showerror("Error", f"Failed to save file: {e}")

def update_value(offset, var):
    try:
        value = float(var.get())
        offsets_values[offset] = value
        update_status("Value Updated!", "green")
    except ValueError:
        update_status("Invalid value", "red")

def increment_value(event, var):
    try:
        value = float(var.get())
        if event.state & 0x0001:  # Shift key
            value += 0.1 if event.keysym == 'Up' else -0.1
        else:
            value += 1.0 if event.keysym == 'Up' else -1.0
        var.set(round(value, 1))
    except ValueError:
        update_status("Invalid value", "red")

def update_color_preview(offset, color):
    color_previews[offset].config(bg=color)

def choose_color(offset, var):
    color_code = colorchooser.askcolor()[1]
    if color_code:
        var.set(color_code)
        update_color_preview(offset, color_code)

def update_color(offset, var):
    color_values[offset] = var.get()
    update_color_preview(offset, var.get())

def update_status(message, color):
    status_label.config(text=message, fg=color)

def about():
    about_window = tk.Toplevel(root)
    about_window.title("About")
    about_window.geometry("420x270")
    about_window.resizable(False, False)
    bold_font = ("Helvetica", 12, "bold")
    tk.Label(about_window, text="FLP Scoreboard Editor 14 By FIFA Legacy Project.", pady=10, font=bold_font).pack()
    tk.Label(about_window, text="Version 1.1 [Build 13 November 2024]", pady=10).pack()
    tk.Label(about_window, text="© 2024 FIFA Legacy Project. All Rights Reserved.", pady=10).pack()
    tk.Label(about_window, text="Designed & Developed By Emran_Ahm3d.", pady=10).pack()
    tk.Label(about_window, text="Special Thanks to JuicyShaqMeat for the Research.", pady=10).pack()
    link = tk.Label(about_window, text="Official Forum Thread for Feedback and Bug Reports", fg="blue", cursor="hand2")
    link.pack(pady=5)
    link.bind("<Button-1>", lambda e: webbrowser.open_new("https://www.soccergaming.com/index.php?threads/download-flp-scoreboard-editor-14.6473355/post-6801850"))
    tk.Label(about_window, text="Discord: @emran_ahm3d", pady=10).pack()

def show_info():
    messagebox.showinfo("Scoreboard Editor v1.1", "Developed by [Your Name]\nVersion 1.1")

def show_documentation():
    webbrowser.open("https://soccergaming.com/index.php?threads/emrans-fifa-14-overlays-research.6473147/")

def restrict_color_entry(event, var):
    if event.keysym == 'BackSpace' and var.get() == '#':
        return 'break'

def exit_app():
    if messagebox.askyesno("Exit", "Are you sure you want to exit?"):
        root.destroy()

# Main Window
root = tk.Tk()
root.title("FLP Scoreboard Editor 14 (v1.1)")
root.geometry("700x500")
root.resizable(False, False)

# Menu
menubar = tk.Menu(root)
filemenu = tk.Menu(menubar, tearoff=0)
filemenu.add_command(label="Open                        ", command=open_file)
filemenu.add_command(label="Save", command=save_file)
filemenu.add_separator()
filemenu.add_command(label="Exit", command=exit_app)
menubar.add_cascade(label="    File    ", menu=filemenu)

helpmenu = tk.Menu(menubar, tearoff=0)
helpmenu.add_command(label="About                        ", command=about)
helpmenu.add_separator()
helpmenu.add_command(label="Documentation", command=show_documentation)
menubar.add_cascade(label="    Help    ", menu=helpmenu)

root.config(menu=menubar)

# Tabs
notebook = ttk.Notebook(root)
positions_frame = ttk.Frame(notebook)
sizes_frame = ttk.Frame(notebook)
colors_frame = ttk.Frame(notebook)

notebook.add(positions_frame, text="Positions")
notebook.add(sizes_frame, text="Sizes")
notebook.add(colors_frame, text="Colors")
notebook.pack(expand=1, fill="both")

# Frame to hold both labels
bottom_frame = tk.Frame(root)
bottom_frame.pack(side=tk.BOTTOM, fill=tk.X)

# Internal Name Label
internal_name_label = tk.Label(bottom_frame, text="Internal Name: Not Loaded", anchor=tk.E)
internal_name_label.pack(side=tk.RIGHT, padx='10', pady=0)

# Status Bar
status_label = tk.Label(bottom_frame, text="Ready", anchor=tk.W, fg="blue")
status_label.pack(side=tk.LEFT, padx='5', pady=0)

# Define a function to place the SAVE button at the bottom right
def place_save_button():
    save_button = ttk.Button(root, text="SAVE", style="Large.TButton", command=save_file)
    save_button.place(relx=1.0, rely=1.0, anchor='se', x=-20, y=-30)

# Add the SAVE button
root.style = ttk.Style()
root.style.configure('Large.TButton', font=('Helvetica', 15), foreground='green')
place_save_button()

# Recreate the widgets based on the internal name
if file_path:
    add_internal_name()

root.mainloop()