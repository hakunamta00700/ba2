import tkinter as tk
import datetime
from tkinter import messagebox
import subprocess
import os
import requests
from requests.exceptions import ConnectionError, Timeout, RequestException
import socket  # Import socket for handling socket.gaierror
import json


# Global URL
url = 'http://192.168.68.124/includes/insert_barcode_injection.php'

# New function to save data locally
def save_data_locally(data):
    with open('local_data.txt', 'a') as file:
        file.write(str(data) + '\n')


# Updated send_data_to_server function
def send_data_to_server(name, shift, barcode1, barcode2, barcode3, barcode4):
    
    data = {
        'name': name,
        'shift': shift,
        'date_time': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'barcode1': barcode1,
        'barcode2': barcode2,
        'barcode3': barcode3,
        'barcode4': barcode4
    }
    try:
        response = requests.post(url, data=data, timeout=5)
        print(response.text)
    except (ConnectionError, Timeout, RequestException, socket.gaierror):
        print("Internet connection issue. Saving data locally.")
        save_data_locally(data)


# New function to check internet availability
def is_internet_available():
    try:
        requests.get('https://www.google.com/', timeout=3)
        return True
    except (ConnectionError, Timeout, RequestException):
        return False


# New function to sync data
def sync_data():
    if not is_internet_available():
        print("Internet is not available. Cannot sync now.")
        return

    with open('local_data.txt', 'r+') as file:
        lines = file.readlines()
        file.seek(0)
        file.truncate()

        data_entries = []
        for line in lines:
            try:
                data_entry = eval(line.strip())
                data_entry['date_time'] = datetime.datetime.strptime(data_entry['date_time'], '%Y-%m-%d %H:%M:%S')
                data_entries.append(data_entry)
            except Exception as e:
                print(f"Failed to parse data: {e}")

        data_entries.sort(key=lambda x: x['date_time'])

        for data in data_entries:
            try:
                data['date_time'] = data['date_time'].strftime('%Y-%m-%d %H:%M:%S')
                response = requests.post(url, data=data, timeout=5)
                print(response.text)
            except (ConnectionError, Timeout, RequestException, socket.gaierror) as e:
                print(f"Failed to sync data: {e}")
                file.write(json.dumps(data) + '\n')


def open_other_file():
    current_directory = os.path.dirname(os.path.abspath(__file__))
    target_script = os.path.join(current_directory, "parts_counter.py")
    subprocess.Popen(["python", target_script])

barcode_scanned_successfully = False

def clear_last_scanned_barcode():
    global barcode_scanned_successfully
    if not barcode_scanned_successfully:
        last_barcode_value.config(text="No barcode has been successfully scanned.")
        return

    # Determine the filename based on tray and UC selection
    tray_value = tray_var.get()
    uc_value = uc_var.get()
    filename = ""
    if tray_value == "TRAY 1" and uc_value == "UC-1":
        filename = "barcodes_TRAY1_UC1.txt"
    elif tray_value == "TRAY 1" and uc_value == "UC-2":
        filename = "barcodes_TRAY1_UC2.txt"
    elif tray_value == "TRAY 2" and uc_value == "UC-1":
        filename = "barcodes_TRAY2_UC1.txt"
    elif tray_value == "TRAY 2" and uc_value == "UC-2":
        filename = "barcodes_TRAY2_UC2.txt"
    else:
        filename = "barcodes_unknown.txt"  # Default file if no tray or UC is selected

    with open(filename, "r") as f:
        lines = f.readlines()

    if len(lines) == 0:
        return  # File is empty, nothing to clear

    # Remove the last line
    lines = lines[:-1]

    # Write the remaining lines back to the file
    with open(filename, "w") as f:
        f.writelines(lines)

    last_barcode_value.config(text="Last scanned barcode cleared.")

    # Reset the flag
    barcode_scanned_successfully = False


def load_files():
    files_content = {}
    files_to_check = [
        "scan_log.txt",
        "barcodes_unknown.txt",
        "barcodes_TRAY1_UC1.txt",
        "barcodes_TRAY1_UC2.txt",
        "barcodes_TRAY2_UC1.txt",
        "barcodes_TRAY2_UC2.txt",
    ]
    for file_name in files_to_check:
        with open(file_name, "r") as f:
            files_content[file_name] = f.readlines()
    return files_content


files_content = load_files()


# Function to show the "pass" label for a brief duration and then hide it
def show_pass_label():
    result_label.config(
        text="PASS",
        font=("Helvetica", 50),
        fg="black",
        bg="green",  # Set the background color to lime green
    )
    root.after(10000, hide_pass_label)  # After(10 seconds), call hide_pass_label


# Function to hide the "pass" label
def hide_pass_label():
    result_label.config(
        text="", bg="SystemButtonFace"
    )  # Clear the text and reset background color


def clear_red_background():  # Function to clear red background of barcode cells
    barcode1_entry.configure(bg="white")
    barcode2_entry.configure(bg="white")
    barcode3_entry.configure(bg="white")
    barcode4_entry.configure(bg="white")


def disable_barcodes():  # Function to disable all barcodes
    barcode1_entry.configure(state="disabled")
    barcode2_entry.configure(state="disabled")
    barcode3_entry.configure(state="disabled")
    barcode4_entry.configure(state="disabled")
    root.after(5000, lambda: enable_barcodes())


def disable_barcodesindef():  # shut off barcodes till button clicked
    barcode1_entry.configure(state="disabled")
    barcode2_entry.configure(state="disabled")
    barcode3_entry.configure(state="disabled")
    barcode4_entry.configure(state="disabled")
    name_entry.configure(state="disabled")
    shift_entry.configure(state="disabled")


def barcodes_disabled_start():
    barcode1_entry.configure(state="disabled")
    barcode2_entry.configure(state="disabled")
    barcode3_entry.configure(state="disabled")
    barcode4_entry.configure(state="disabled")


def enable_nameshift():  # enable name fields
    name_entry.configure(state="normal")
    shift_entry.configure(state="normal")


def enable_barcodes():  # re enable barcodes after indef is used
    barcode1_entry.configure(state="normal")
    barcode2_entry.configure(state="normal")
    barcode3_entry.configure(state="normal")
    barcode4_entry.configure(state="normal")
    clear_red_background()
    barcode1_entry.focus_set()


def clear_barcode_entries():  # clear barcode fields
    barcode1_var.set("")
    barcode2_var.set("")
    barcode3_var.set("")
    barcode4_var.set("")
    barcode1_entry.focus_set()


def clear_user_shift(*args):  # clear user fields
    name_var.set("")
    shift_var.set("")
    barcode1_var.set("")
    barcode2_var.set("")
    barcode3_var.set("")
    barcode4_var.set("")
    enable_nameshift()
    name_label.focus_set()
    name_entry.focus_set()


def clear_result():  # not fully sure what used for
    result_label.config(text="", bg="SystemButtonFace")


def show_tray_popup():  # used to pop up a reminder to select your uc
    messagebox.showinfo(
        "Reminder",
        "Please select UC-1 or UC-2 before trying to scan barcodes.",
    )
    barcode1_entry.focus_set()


def check_barcodes_against_first(
    barcode1, barcode2, barcode3, barcode4
):  # used to check all barcodes against the first barcode
    invalid_barcodes = []
    for barcode_name, barcode_value in [
        ("barcode2", barcode2),
        ("barcode3", barcode3),
        ("barcode4", barcode4),
    ]:
        if barcode_value != barcode1:
            invalid_barcodes.append(barcode_name)
            barcode1_entry.focus_set()
    return invalid_barcodes


def highlight_invalid_barcodes(barcodes):  # used to highlight bad barcodes
    for barcode in barcodes:
        barcode_entry = globals()[f"{barcode}_entry"]
        barcode_entry.configure(bg="red")
        barcode1_entry.focus_set()


def process_tray1_uc1(
    barcode1, barcode2, barcode3, barcode4
):  # Used to process tray 1 UC-1 when selected
    error_messages = []
    invalid_barcodes = check_barcodes_against_first(
        barcode1, barcode2, barcode3, barcode4
    )
    if not all(
        barcode.startswith("HKAD")
        for barcode in [barcode1, barcode2, barcode3, barcode4]
    ):
        error_messages.append(
            "You have scanned a barcode that is not TRAY 1 UC-1!!. STOP! Check labels on part Alert supervisor and quality department!"
        )
    elif invalid_barcodes:
        error_messages.append(
            "Some of your barcodes are not the same as the first one! Do not pass part. Recheck your labels!"
        )
        highlight_invalid_barcodes(invalid_barcodes)
    elif any(
        barcode.startswith("TKAE")
        for barcode in [barcode1, barcode2, barcode3, barcode4]
    ):
        error_messages.append(
            "You have scanned a Tray 2 Tennessee label!! DO NOT PASS PART! STOP! Check labels on part Alert supervisor and quality department!"
        )
    else:
        for barcode in [barcode1, barcode2, barcode3, barcode4]:
            if barcode.startswith("HKAD"):
                barcode_number = int(barcode[4:])
                if barcode_number < 64000:
                    error_messages.append(
                        "You have scanned an old series label! STOP! Check labels on part Alert supervisor and quality department!"
                    )
    return error_messages


def process_tray1_uc2(
    barcode1, barcode2, barcode3, barcode4
):  # used to process tray 1 UC2 when selected
    error_messages = []
    invalid_barcodes = check_barcodes_against_first(
        barcode1, barcode2, barcode3, barcode4
    )
    if not all(
        barcode.startswith("TKAD")
        for barcode in [barcode1, barcode2, barcode3, barcode4]
    ):
        error_messages.append(
            "You have scanned a barcode that is not TRAY 1 UC-2!!. STOP! Check labels on part Alert supervisor and quality department!"
        )
    elif invalid_barcodes:
        error_messages.append(
            "Some of your barcodes are not the same as the first one! Do not pass part. Recheck your labels!"
        )
        highlight_invalid_barcodes(invalid_barcodes)
    return error_messages


def process_tray2_uc1(
    barcode1, barcode2, barcode3, barcode4
):  # used to process tray 2 uc1 when selected
    error_messages = []
    invalid_barcodes = check_barcodes_against_first(
        barcode1, barcode2, barcode3, barcode4
    )
    if not all(
        barcode.startswith("HKAE")
        for barcode in [barcode1, barcode2, barcode3, barcode4]
    ):
        error_messages.append(
            "Wrong barcodes scanned. You have scanned barcodes that are not tray 2 UC-1!! STOP! Check labels on part Alert supervisor and quality department!"
        )
    elif invalid_barcodes:
        error_messages.append(
            "Some of your barcodes are not the same as the first one! Do not pass part. Recheck your labels!"
        )
        highlight_invalid_barcodes(invalid_barcodes)
    else:
        for barcode in [barcode1, barcode2, barcode3, barcode4]:
            if barcode.startswith("HKAE"):
                barcode_number = int(barcode[4:])
                if barcode_number < 64000:
                    error_messages.append(
                        "You have scanned an old series label! Please inform your supervisor and quality department!"
                    )
                    highlight_invalid_barcodes(
                        ["barcode1", "barcode2", "barcode3", "barcode4"]
                    )
    return error_messages


def process_tray2_uc2(
    barcode1, barcode2, barcode3, barcode4
):  # used to process tray 2 uc2 when selected
    error_messages = []
    invalid_barcodes = check_barcodes_against_first(
        barcode1, barcode2, barcode3, barcode4
    )
    if invalid_barcodes:
        error_messages.append(
            "Some of your barcodes are not the same as the first one! Do not pass part. Recheck your labels!"
        )
        highlight_invalid_barcodes(invalid_barcodes)
    if not all(
        barcode.startswith("TKAE")
        for barcode in [barcode1, barcode2, barcode3, barcode4]
    ):
        error_messages.append(
            "Wrong barcode scanned. You have scanned a barcode that is not tray 2 UC-2!! STOP! Check labels on part Alert supervisor and quality department!"
        )

    return error_messages


def tray_selected(
    *args,
):  # used to define what the radio buttons do when selected what ones are not selected and whatnot
    tray_value = tray_var.get()

    if tray_value == "TRAY 1":
        uc1_button.configure(state="normal")
        uc2_button.configure(state="normal")
    elif tray_value == "TRAY 2":
        uc1_button.configure(state="normal")
        uc2_button.configure(state="normal")
    else:
        uc1_button.configure(state="disabled")
        uc2_button.configure(state="disabled")

    # Clear the UC selection when changing trays
    uc_var.set("")


scanning_in_progress = False
last_barcode_set = ""


def scan_barcodes(
    *args,
):  # used when scanning in barcodes to tell program what is and what is not selected user is alerted in this block if they dont select the items
    global scanning_in_progress, last_barcode_set

    if scanning_in_progress:
        return

    name = name_var.get()
    shift = shift_var.get()
    barcode1 = barcode1_var.get()
    barcode2 = barcode2_var.get()
    barcode3 = barcode3_var.get()
    barcode4 = barcode4_var.get()

    if not name or not shift:
        result_label.config(
            text="LOG IN WITH YOUR NAME AND SHIFT BEFORE SCANNING BARCODES.",
            font=("Helvetica", 14),
            fg="red",
            bg="yellow",
        )
        return
    else:
        result_label.config(text="", bg="SystemButtonFace")  # Clear the alert

    if len(barcode4) == 10:
        process_barcodes()

    tray_value = tray_var.get()
    uc_value = uc_var.get()

    if tray_value in ["TRAY 1", "TRAY 2"] and not uc_value:
        result_label.config(
            text="PLEASE SELECT EITHER UC-1 OR UC-2.",
            font=("Helvetica", 14),
            fg="red",
            bg="yellow",
        )
        return

    if tray_value in ["TRAY 1", "TRAY 2"] and uc_value not in ["UC-1", "UC-2"]:
        result_label.config(
            text="PLEASE SELECT EITHER UC-1 OR UC-2.",
            font=("Helvetica", 14),
            fg="red",
            bg="yellow",
        )
        return

    if tray_value == "HKAD" and not uc_value:
        result_label.config(
            text="PLEASE SELECT EITHER UC-1 OR UC-2.",
            font=("Helvetica", 14),
            fg="red",
            bg="yellow",
        )
        return

    if tray_value == "HKAD" and uc_value not in ["UC-1", "UC-2"]:
        result_label.config(
            text="PLEASE SELECT EITHER UC-1 OR UC-2.",
            font=("Helvetica", 14),
            fg="red",
            bg="yellow",
        )
        return

    if tray_value == "HKAE" and not uc_value:
        result_label.config(
            text="PLEASE SELECT EITHER UC-1 OR UC-2.",
            font=("Helvetica", 14),
            fg="red",
            bg="yellow",
        )
        return


def process_barcodes(
    *args,
):  # entire process barcodes function main chunk of program used after 4 barcodes have been scanned into program
    global scanning_in_progress, last_barcode_set

    scanning_in_progress = True
    name = name_var.get()
    shift = shift_var.get()
    barcode1 = barcode1_var.get()
    barcode2 = barcode2_var.get()
    barcode3 = barcode3_var.get()
    barcode4 = barcode4_var.get()

    error_messages = []
    invalid_barcodes = []

    # Do all error checking first
    if not tray_var.get():
        error_messages.append("PLEASE SELECT A TRAY BEFORE SCANNING BARCODES.")
        barcode1_entry.focus_set()

    if not name or not shift:
        error_messages.append(
            "LOG IN WITH YOUR NAME AND SHIFT BEFORE SCANNING BARCODES."
        )
        barcode1_entry.focus_set()

    # Call the appropriate function based on tray and UC selection

    if tray_var.get() == "TRAY 1":
        if uc_var.get() == "UC-1":
            error_messages += process_tray1_uc1(barcode1, barcode2, barcode3, barcode4)
        elif uc_var.get() == "UC-2":  # Fix is here: Use 'elif' instead of 'if'
            error_messages += process_tray1_uc2(barcode1, barcode2, barcode3, barcode4)
    elif tray_var.get() == "TRAY 2":
        if uc_var.get() == "UC-1":
            error_messages += process_tray2_uc1(barcode1, barcode2, barcode3, barcode4)
        elif uc_var.get() == "UC-2":  # Fix is here: Use 'elif' instead of 'if'
            error_messages += process_tray2_uc2(barcode1, barcode2, barcode3, barcode4)

    # Restoring the background color of the barcode entries if there are no error messages
    if not error_messages:
        for barcode in ["barcode1", "barcode2", "barcode3", "barcode4"]:
            barcode_entry = globals()[f"{barcode}_entry"]
            barcode_entry.configure(bg="white")

    # If there are error messages, show them and return
    if error_messages:
        error_message = "\n".join(error_messages)
        result_label.config(
            text=error_message,
            font=("Helvetica", 14),
            fg="black",
            bg="red",
            wraplength=200,
        )
        clear_barcode_entries()
        barcode1_entry.focus_set()
        # Clear the red background after 10 seconds
        root.after(10000, clear_red_background)
        root.after(10000, clear_result)  # Clear the error message after 10 seconds
        scanning_in_progress = False
        disable_barcodesindef()
        return  # Return early if there are error messages

    now = datetime.datetime.now()
    log_time = now.strftime("%d %B %H:%M")
    barcode_set = f"{barcode1}, {barcode2}, {barcode3}, {barcode4}"

    # Determine the filename based on tray and UC selection
    tray_value = tray_var.get()
    uc_value = uc_var.get()
    filename = ""
    if tray_value == "TRAY 1" and uc_value == "UC-1":
        filename = "barcodes_TRAY1_UC1.txt"
    elif tray_value == "TRAY 1" and uc_value == "UC-2":
        filename = "barcodes_TRAY1_UC2.txt"
    elif tray_value == "TRAY 2" and uc_value == "UC-1":
        filename = "barcodes_TRAY2_UC1.txt"
    elif tray_value == "TRAY 2" and uc_value == "UC-2":
        filename = "barcodes_TRAY2_UC2.txt"
    else:
        filename = "barcodes_unknown.txt"  # Default file if no tray or UC is selected

    # Check for duplicate barcodes in the corresponding file
    duplicate_barcodes = False
    with open(filename, "r") as f:
        log_lines = f.readlines()
        for line in log_lines:
            if barcode_set in line:
                duplicate_barcodes = True
                break

    if duplicate_barcodes:
        duplicate_message = f"Duplicate Entry: The scanned barcode set {barcode_set} has already been scanned into the database."
        # Highlight the barcode entries to indicate duplicate entry
        highlight_invalid_barcodes(["barcode1", "barcode2", "barcode3", "barcode4"])
        # Show the duplicate message in the result label
        result_label.config(
            text=duplicate_message,
            font=("Helvetica", 14),
            fg="black",
            bg="red",
            wraplength=200,
        )
        root.after(15000, clear_result)  # Clear the duplicate message after 15 seconds
        clear_barcode_entries()
        barcode1_entry.focus_set()
        disable_barcodesindef()
    else:

        send_data_to_server(name, shift, barcode1, barcode2, barcode3, barcode4)

        # Save the barcodes to the determined file
        with open(filename, "a") as f:
            f.write(f"{name} ({shift}): {barcode_set} {log_time}\n")
            global barcode_scanned_successfully
            barcode_scanned_successfully = True

        # Update the last barcode set for duplicate checking
        last_barcode_set = barcode_set
        last_barcode_value.config(
            text=last_barcode_set
        )  # Update the last_barcode_value label

        # Clear the barcode entries and focus on the first entry for the next scan
        clear_barcode_entries()
        # Show the "PASS" label
        show_pass_label()
        barcode1_entry.focus_set()
        disable_barcodesindef()
        sync_data()

    scanning_in_progress = False


root = tk.Tk()
root.title(
    "Daejin barcode verification program designed by clint terry"
)  # Set the desired program name here
# Adjust the window dimensions to fit the GUI
window_width = 2000
window_height = 800
root.attributes("-fullscreen", False)
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x_coordinate = int((screen_width / 2) - (window_width / 2))
y_coordinate = int((screen_height / 2) - (window_height / 2))
root.geometry(f"{window_width}x{window_height}+{x_coordinate}+{y_coordinate}")


def handle_keys(event):
    # Key sequence to exit full-screen mode (e.g., pressing "Ctrl+e")
    if event.state == 4 and event.keysym == "e":
        root.attributes("-fullscreen", False)
    # Key sequence to close the application (e.g., pressing "Ctrl+q")
    elif event.state == 4 and event.keysym == "q":
        root.quit()


def auto_tab(event, next_widget):
    entry_widget = event.widget
    if len(entry_widget.get()) == 10:  # Assuming a barcode has a length of 10
        next_widget.focus_set()


# Bind the handle_keys function to all key events
root.bind_all("<Key>", handle_keys)

root.lift()

clear_last_scanned_button = tk.Button(root, text="Clear Last Scanned", font=("Helvetica", 20), command=clear_last_scanned_barcode)
clear_last_scanned_button.place(x=355, y=195)


tray_var = tk.StringVar()
tray_var.trace("w", tray_selected)
uc_var = tk.StringVar()

tray1_button = tk.Radiobutton(
    root,
    text="TRAY 1",
    variable=tray_var,
    value="TRAY 1",
    font=("Helvetica", 20),
    command=tray_selected,
)
tray2_button = tk.Radiobutton(
    root,
    text="TRAY 2",
    variable=tray_var,
    value="TRAY 2",
    font=("Helvetica", 20),
    command=tray_selected,
)

tray1_button.place(x=1300, y=242)
tray2_button.place(
    x=1300, y=310
)  # Change the y-coordinate to the correct position for Tray 2

uc1_button = tk.Radiobutton(
    root,
    text="UC-1",
    variable=uc_var,
    value="UC-1",
    font=("Helvetica", 20),
    state="disabled",
)
uc2_button = tk.Radiobutton(
    root,
    text="UC-2",
    variable=uc_var,
    value="UC-2",
    font=("Helvetica", 20),
    state="disabled",
)

uc1_button.place(x=1300, y=380)
uc2_button.place(x=1300, y=450)

# Deselect the radio buttons
tray1_button.deselect()
tray2_button.deselect()
uc1_button.deselect()
uc2_button.deselect()


close_button = tk.Button(root, text="Close", font=("Helvetica", 20), command=root.quit)
close_button.place(x=100, y=300)

Log_button = tk.Button(
    root, text="Log Off", font=("Helvetica", 20), command=clear_user_shift
)
Log_button.place(x=100, y=250)

clear_button = tk.Button(
    root, text="Clear Barcodes", font=("Helvetica", 20), command=clear_barcode_entries
)
clear_button.place(x=550, y=850)

disable_button = tk.Button(
    root,
    text="Disable ALL inputs",
    font=("Helvetica", 20),
    command=disable_barcodesindef,
)
disable_button.place(x=100, y=195)

enable_button = tk.Button(
    root, text="Enable Scanner", font=("Helvetica", 20), command=enable_barcodes
)
enable_button.place(x=550, y=800)

enableshift_button = tk.Button(
    root, text="Enable name/shift", font=("Helvetica", 20), command=enable_nameshift
)
enableshift_button.place(x=742, y=25)

shift_var = tk.StringVar()
shift_var.set("")


def update_shift3():
    shift_var.set("Third Shift")
    enable_barcodes()
    barcode1_entry.focus_set()


Thirdshift_button = tk.Button(
    root, text="Third Shift", font=("Helvetica", 20), command=update_shift3
)
Thirdshift_button.place(x=400, y=140)


def update_shift2():
    shift_var.set("Second Shift")
    enable_barcodes()
    barcode1_entry.focus_set()


secondshift_button = tk.Button(
    root, text="Second Shift", font=("Helvetica", 20), command=update_shift2)
secondshift_button.place(x=230, y=140)


def update_shift1():
    shift_var.set("First Shift")
    enable_barcodes()
    barcode1_entry.focus_set()


count_button = tk.Button(root, text="Open parts counter", font=("Helvetica", 20), command=open_other_file)
count_button.place(x=546, y=140)




secondshift_button = tk.Button(
    root, text="First Shift", font=("Helvetica", 20), command=update_shift1
)
secondshift_button.place(x=100, y=140)

last_barcode_label = tk.Label(
    root, text="Last Scanned Barcode Set:", font=("Helvetica",)
)
last_barcode_label.place(x=100, y=370)
last_barcode_value = tk.Label(
    root, text="", font=("Helvetica", 12), wraplength=150
)  # Set wraplength to 400 pixels
last_barcode_value.place(x=100, y=400)

root.attributes("-topmost", True)
root.after_idle(root.attributes, "-topmost", True)

name_var = tk.StringVar()
name_label = tk.Label(root, text="Name:", font=("Helvetica", 30))
name_label.place(x=100, y=10)
name_entry = tk.Entry(
    root, justify="center", textvariable=name_var, font=("Helvetica", 30)
)
name_entry.place(x=250, y=10)
name_entry.focus_set()
name_var.trace("w", scan_barcodes)

shift_var = tk.StringVar()
shift_label = tk.Label(root, text="Shift:", font=("Helvetica", 30))
shift_label.place(x=100, y=70)
shift_entry = tk.Entry(
    root, justify="center", textvariable=shift_var, font=("Helvetica", 30)
)
shift_entry.place(x=250, y=70)
shift_var.trace("w", scan_barcodes)

barcode1_var = tk.StringVar()
barcode1_label = tk.Label(root, text="Barcode 1:", font=("Helvetica", 30))
barcode1_label.place(x=300, y=450)
barcode1_entry = tk.Entry(root, textvariable=barcode1_var, font=("Helvetica", 30))
barcode1_entry.place(x=500, y=450)
barcode1_var.trace("w", scan_barcodes)

barcode2_var = tk.StringVar()
barcode2_label = tk.Label(root, text="Barcode 2:", font=("Helvetica", 30))
barcode2_label.place(x=300, y=500)
barcode2_entry = tk.Entry(root, textvariable=barcode2_var, font=("Helvetica", 30))
barcode2_entry.place(x=500, y=500)
barcode2_var.trace("w", scan_barcodes)

barcode3_var = tk.StringVar()
barcode3_label = tk.Label(root, text="Barcode 3:", font=("Helvetica", 30))
barcode3_label.place(x=300, y=550)
barcode3_entry = tk.Entry(root, textvariable=barcode3_var, font=("Helvetica", 30))
barcode3_entry.place(x=500, y=550)
barcode3_var.trace("w", scan_barcodes)

barcode4_var = tk.StringVar()
barcode4_label = tk.Label(root, text="Barcode 4:", font=("Helvetica", 30))
barcode4_label.place(x=300, y=600)
barcode4_entry = tk.Entry(root, textvariable=barcode4_var, font=("Helvetica", 30))
barcode4_entry.place(x=500, y=600)
barcode4_var.trace("w", scan_barcodes)

result_label = tk.Label(root, text="", font=("Helvetica", 50), width=20, height=5)
result_label.place(x=1200, y=500, width=700, height=500)
barcodes_disabled_start()


def on_switch_key_press(event):
    enable_barcodes()


# Add the bindings here
barcode1_entry.bind("<KeyRelease>", lambda event: auto_tab(event, barcode2_entry))
barcode2_entry.bind("<KeyRelease>", lambda event: auto_tab(event, barcode3_entry))
barcode3_entry.bind(
    "<KeyRelease>", lambda event: auto_tab(event, barcode4_entry)
)  # Bind the F12 key to the on_switch_key_press function
root.bind("<F12>", on_switch_key_press)


root.mainloop()
