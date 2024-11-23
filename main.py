import tkinter as tk
import datetime
from tkinter import messagebox
import subprocess
import os
import requests
from requests.exceptions import ConnectionError, Timeout, RequestException
import socket  # Import socket for handling socket.gaierror
import json
from config.constants import (
    WINDOW_CONFIG, 
    FONT_SIZES, 
    BARCODE_PREFIXES,
    FILE_PATHS, 
    API_CONFIG,
    ERROR_MESSAGES,
    TIMING,
    LAYOUT,
    STYLES,
    BARCODE,
    SYSTEM_MESSAGES,
    COLORS,
    KEY_BINDINGS,
    BUTTON_TEXTS,
    LABEL_TEXTS,
    SHIFT_VALUES,
    TRAY_VALUES,
    UC_VALUES,
    DATE_FORMATS
)
from config.settings import settings
# 프로그램 시작

# Global URL
url = f"{settings.API_HOST}/includes/insert_barcode_injection.php"

# New function to save data locally
def save_data_locally(data):
    with open('local_data.txt', 'a') as file:
        file.write(str(data) + '\n')


# Updated send_data_to_server function
def send_data_to_server(name, shift, barcode1, barcode2, barcode3, barcode4):
    
    data = {
        'name': name,
        'shift': shift,
        'date_time': datetime.datetime.now().strftime(DATE_FORMATS["DATETIME"]),
        'barcode1': barcode1,
        'barcode2': barcode2,
        'barcode3': barcode3,
        'barcode4': barcode4
    }
    try:
        response = requests.post(url, data=data, timeout=API_CONFIG["TIMEOUT"])
        print(response.text)
    except (ConnectionError, Timeout, RequestException, socket.gaierror):
        print(SYSTEM_MESSAGES["INTERNET_ERROR"])
        save_data_locally(data)


# New function to check internet availability
def is_internet_available():
    try:
        requests.get('https://www.google.com/', timeout=TIMING["INTERNET_TIMEOUT"]/1000)
        return True
    except (ConnectionError, Timeout, RequestException):
        return False


# New function to sync data
def sync_data():
    if not is_internet_available():
        print(SYSTEM_MESSAGES["INTERNET_ERROR"])
        return

    with open(FILE_PATHS["LOCAL_DATA"], 'r+') as file:
        lines = file.readlines()
        file.seek(0)
        file.truncate()

        data_entries = []
        for line in lines:
            try:
                data_entry = eval(line.strip())
                data_entry['date_time'] = datetime.datetime.strptime(
                    data_entry['date_time'], 
                    DATE_FORMATS["DATETIME"]
                )
                data_entries.append(data_entry)
            except Exception as e:
                print(SYSTEM_MESSAGES["SYNC_ERROR"].format(e))

        data_entries.sort(key=lambda x: x['date_time'])

        for data in data_entries:
            try:
                data['date_time'] = data['date_time'].strftime(DATE_FORMATS["DATETIME"])
                response = requests.post(url, data=data, timeout=API_CONFIG["TIMEOUT"])
                print(response.text)
            except (ConnectionError, Timeout, RequestException, socket.gaierror) as e:
                print(SYSTEM_MESSAGES["SYNC_ERROR"].format(e))
                file.write(json.dumps(data) + '\n')


def open_other_file():
    current_directory = os.path.dirname(os.path.abspath(__file__))
    target_script = os.path.join(current_directory, "parts_counter.py")
    subprocess.Popen(["python", target_script])

barcode_scanned_successfully = False

def clear_last_scanned_barcode():
    global barcode_scanned_successfully
    if not barcode_scanned_successfully:
        last_barcode_value.config(text=ERROR_MESSAGES["NO_BARCODE"])
        return

    # Determine the filename based on tray and UC selection
    tray_value = tray_var.get()
    uc_value = uc_var.get()
    filename = determine_filename(tray_value, uc_value)

    with open(filename, "r") as f:
        lines = f.readlines()

    if len(lines) == 0:
        return  # File is empty, nothing to clear

    # Remove the last line
    lines = lines[:-1]

    # Write the remaining lines back to the file
    with open(filename, "w") as f:
        f.writelines(lines)

    last_barcode_value.config(text=ERROR_MESSAGES["BARCODE_CLEARED"])

    # Reset the flag
    barcode_scanned_successfully = False


def load_files():
    files_content = {}
    files_to_check = [
        FILE_PATHS["SCAN_LOG"],
        FILE_PATHS["UNKNOWN"],
        FILE_PATHS["TRAY1_UC1"],
        FILE_PATHS["TRAY1_UC2"],
        FILE_PATHS["TRAY2_UC1"],
        FILE_PATHS["TRAY2_UC2"],
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
        font=FONT_SIZES["EXTRA_LARGE"],
        fg=COLORS["BLACK"],
        bg=COLORS["SUCCESS_BG"],
    )
    root.after(TIMING["PASS_DISPLAY"], hide_pass_label)


# Function to hide the "pass" label
def hide_pass_label():
    result_label.config(
        text="", 
        bg=COLORS["DEFAULT_BG"]
    )


def clear_red_background():
    barcode1_entry.configure(bg=COLORS["WHITE"])
    barcode2_entry.configure(bg=COLORS["WHITE"])
    barcode3_entry.configure(bg=COLORS["WHITE"])
    barcode4_entry.configure(bg=COLORS["WHITE"])


def disable_barcodes():  # Function to disable all barcodes
    barcode1_entry.configure(state="disabled")
    barcode2_entry.configure(state="disabled")
    barcode3_entry.configure(state="disabled")
    barcode4_entry.configure(state="disabled")
    root.after(TIMING["BACKGROUND_CLEAR"], lambda: enable_barcodes())


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


def clear_result():
    result_label.config(text="", bg=COLORS["DEFAULT_BG"])


def show_tray_popup():
    messagebox.showinfo(
        SYSTEM_MESSAGES["REMINDER_TITLE"],
        SYSTEM_MESSAGES["REMINDER_MESSAGE"],
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
        barcode_entry.configure(bg=COLORS["ERROR_FG"])
        barcode1_entry.focus_set()


def process_tray1_uc1(barcode1, barcode2, barcode3, barcode4):
    error_messages = []
    invalid_barcodes = check_barcodes_against_first(
        barcode1, barcode2, barcode3, barcode4
    )
    if not all(
        barcode.startswith(BARCODE_PREFIXES["TRAY1_UC1"])
        for barcode in [barcode1, barcode2, barcode3, barcode4]
    ):
        error_messages.append(ERROR_MESSAGES["TRAY1_UC1_WRONG"])
    elif invalid_barcodes:
        error_messages.append(ERROR_MESSAGES["MISMATCH_BARCODES"])
        highlight_invalid_barcodes(invalid_barcodes)
    elif any(
        barcode.startswith(BARCODE_PREFIXES["TRAY2_UC2"])
        for barcode in [barcode1, barcode2, barcode3, barcode4]
    ):
        error_messages.append(ERROR_MESSAGES["TRAY2_LABEL"])
    else:
        for barcode in [barcode1, barcode2, barcode3, barcode4]:
            if barcode.startswith(BARCODE_PREFIXES["TRAY1_UC1"]):
                barcode_number = int(barcode[4:])
                if barcode_number < BARCODE["MIN_SERIES_NUMBER"]:
                    error_messages.append(ERROR_MESSAGES["OLD_SERIES"])
    return error_messages

def process_tray1_uc2(barcode1, barcode2, barcode3, barcode4):
    error_messages = []
    invalid_barcodes = check_barcodes_against_first(
        barcode1, barcode2, barcode3, barcode4
    )
    if not all(
        barcode.startswith(BARCODE_PREFIXES["TRAY1_UC2"])
        for barcode in [barcode1, barcode2, barcode3, barcode4]
    ):
        error_messages.append(ERROR_MESSAGES["TRAY1_UC2_WRONG"])
    elif invalid_barcodes:
        error_messages.append(ERROR_MESSAGES["MISMATCH_BARCODES"])
        highlight_invalid_barcodes(invalid_barcodes)
    return error_messages

def process_tray2_uc1(barcode1, barcode2, barcode3, barcode4):
    error_messages = []
    invalid_barcodes = check_barcodes_against_first(
        barcode1, barcode2, barcode3, barcode4
    )
    if not all(
        barcode.startswith(BARCODE_PREFIXES["TRAY2_UC1"])
        for barcode in [barcode1, barcode2, barcode3, barcode4]
    ):
        error_messages.append(ERROR_MESSAGES["TRAY2_UC1_WRONG"])
    elif invalid_barcodes:
        error_messages.append(ERROR_MESSAGES["MISMATCH_BARCODES"])
        highlight_invalid_barcodes(invalid_barcodes)
    else:
        for barcode in [barcode1, barcode2, barcode3, barcode4]:
            if barcode.startswith(BARCODE_PREFIXES["TRAY2_UC1"]):
                barcode_number = int(barcode[4:])
                if barcode_number < BARCODE["MIN_SERIES_NUMBER"]:
                    error_messages.append(ERROR_MESSAGES["OLD_SERIES"])
                    highlight_invalid_barcodes(
                        ["barcode1", "barcode2", "barcode3", "barcode4"]
                    )
    return error_messages

def process_tray2_uc2(barcode1, barcode2, barcode3, barcode4):
    error_messages = []
    invalid_barcodes = check_barcodes_against_first(
        barcode1, barcode2, barcode3, barcode4
    )
    if not all(
        barcode.startswith(BARCODE_PREFIXES["TRAY2_UC2"])
        for barcode in [barcode1, barcode2, barcode3, barcode4]
    ):
        error_messages.append(ERROR_MESSAGES["TRAY2_UC2_WRONG"])
    elif invalid_barcodes:
        error_messages.append(ERROR_MESSAGES["MISMATCH_BARCODES"])
        highlight_invalid_barcodes(invalid_barcodes)
    return error_messages


def tray_selected(*args):
    tray_value = tray_var.get()

    if tray_value == TRAY_VALUES["TRAY1"]:
        uc1_button.configure(state="normal")
        uc2_button.configure(state="normal")
    elif tray_value == TRAY_VALUES["TRAY2"]:
        uc1_button.configure(state="normal")
        uc2_button.configure(state="normal")
    else:
        uc1_button.configure(state="disabled")
        uc2_button.configure(state="disabled")

    # Clear the UC selection when changing trays
    uc_var.set("")


scanning_in_progress = False
last_barcode_set = ""


def scan_barcodes(*args):
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
            text=ERROR_MESSAGES["NO_LOGIN"],
            font=FONT_SIZES["MEDIUM"],
            fg=COLORS["ERROR_FG"],
            bg=COLORS["ERROR_BG"]
        )
        return
    else:
        result_label.config(text="", bg=COLORS["DEFAULT_BG"])  # Clear the alert

    if len(barcode4) == BARCODE["LENGTH"]:
        process_barcodes()

    tray_value = tray_var.get()
    uc_value = uc_var.get()

    if tray_value in [TRAY_VALUES["TRAY1"], TRAY_VALUES["TRAY2"]] and not uc_value:
        result_label.config(
            text=ERROR_MESSAGES["SELECT_UC"],
            font=FONT_SIZES["MEDIUM"],
            fg=COLORS["ERROR_FG"],
            bg=COLORS["ERROR_BG"]
        )
        return

    if tray_value in [TRAY_VALUES["TRAY1"], TRAY_VALUES["TRAY2"]] and uc_value not in [UC_VALUES["UC1"], UC_VALUES["UC2"]]:
        result_label.config(
            text=ERROR_MESSAGES["SELECT_UC"],
            font=FONT_SIZES["MEDIUM"],
            fg=COLORS["ERROR_FG"],
            bg=COLORS["ERROR_BG"]
        )
        return


def determine_filename(tray_value, uc_value):
    if tray_value == TRAY_VALUES["TRAY1"] and uc_value == UC_VALUES["UC1"]:
        return FILE_PATHS["TRAY1_UC1"]
    elif tray_value == TRAY_VALUES["TRAY1"] and uc_value == UC_VALUES["UC2"]:
        return FILE_PATHS["TRAY1_UC2"]
    elif tray_value == TRAY_VALUES["TRAY2"] and uc_value == UC_VALUES["UC1"]:
        return FILE_PATHS["TRAY2_UC1"]
    elif tray_value == TRAY_VALUES["TRAY2"] and uc_value == UC_VALUES["UC2"]:
        return FILE_PATHS["TRAY2_UC2"]
    else:
        return FILE_PATHS["UNKNOWN"]


def process_barcodes(*args):
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
        error_messages.append(SYSTEM_MESSAGES["SELECT_TRAY"])
        barcode1_entry.focus_set()

    if not name or not shift:
        error_messages.append(ERROR_MESSAGES["NO_LOGIN"])
        barcode1_entry.focus_set()

    # Call the appropriate function based on tray and UC selection

    if tray_var.get() == TRAY_VALUES["TRAY1"]:
        if uc_var.get() == UC_VALUES["UC1"]:
            error_messages += process_tray1_uc1(barcode1, barcode2, barcode3, barcode4)
        elif uc_var.get() == UC_VALUES["UC2"]:
            error_messages += process_tray1_uc2(barcode1, barcode2, barcode3, barcode4)
    elif tray_var.get() == TRAY_VALUES["TRAY2"]:
        if uc_var.get() == UC_VALUES["UC1"]:
            error_messages += process_tray2_uc1(barcode1, barcode2, barcode3, barcode4)
        elif uc_var.get() == UC_VALUES["UC2"]:
            error_messages += process_tray2_uc2(barcode1, barcode2, barcode3, barcode4)

    # Restoring the background color of the barcode entries if there are no error messages
    if not error_messages:
        for barcode in ["barcode1", "barcode2", "barcode3", "barcode4"]:
            barcode_entry = globals()[f"{barcode}_entry"]
            barcode_entry.configure(bg=COLORS["WHITE"])

    # If there are error messages, show them and return
    if error_messages:
        error_message = "\n".join(error_messages)
        result_label.config(
            text=error_message,
            font=FONT_SIZES["MEDIUM"],
            fg=COLORS["BLACK"],
            bg=COLORS["ERROR_BG"],
            wraplength=STYLES["LABEL_WRAPLENGTH"],
        )
        clear_barcode_entries()
        barcode1_entry.focus_set()
        # Clear the red background after 10 seconds
        root.after(TIMING["BACKGROUND_CLEAR"], clear_red_background)
        root.after(TIMING["ERROR_DISPLAY"], clear_result)  # Clear the error message after 10 seconds
        scanning_in_progress = False
        disable_barcodesindef()
        return  # Return early if there are error messages

    now = datetime.datetime.now()
    log_time = now.strftime(DATE_FORMATS["LOG_TIME"])
    barcode_set = f"{barcode1}, {barcode2}, {barcode3}, {barcode4}"

    # Determine the filename based on tray and UC selection
    tray_value = tray_var.get()
    uc_value = uc_var.get()
    filename = determine_filename(tray_value, uc_value)

    # Check for duplicate barcodes in the corresponding file
    duplicate_barcodes = False
    with open(filename, "r") as f:
        log_lines = f.readlines()
        for line in log_lines:
            if barcode_set in line:
                duplicate_barcodes = True
                break

    if duplicate_barcodes:
        duplicate_message = ERROR_MESSAGES["DUPLICATE_ENTRY"].format(barcode_set)
        # Highlight the barcode entries to indicate duplicate entry
        highlight_invalid_barcodes(["barcode1", "barcode2", "barcode3", "barcode4"])
        # Show the duplicate message in the result label
        result_label.config(
            text=duplicate_message,
            font=FONT_SIZES["MEDIUM"],
            fg=COLORS["BLACK"],
            bg=COLORS["ERROR_BG"],
            wraplength=STYLES["LABEL_WRAPLENGTH"],
        )
        root.after(TIMING["DUPLICATE_DISPLAY"], clear_result)  # Clear the duplicate message after 15 seconds
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
root.title(WINDOW_CONFIG["TITLE"])
# Adjust the window dimensions to fit the GUI
window_width = WINDOW_CONFIG["WIDTH"]
window_height = WINDOW_CONFIG["HEIGHT"]
root.attributes("-fullscreen", False)
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x_coordinate = int((screen_width / 2) - (window_width / 2))
y_coordinate = int((screen_height / 2) - (window_height / 2))
root.geometry(f"{window_width}x{window_height}+{x_coordinate}+{y_coordinate}")


def handle_keys(event):
    # Key sequence to exit full-screen mode (e.g., pressing "Ctrl+e")
    if (event.state == KEY_BINDINGS["FULLSCREEN_EXIT"]["state"] and 
        event.keysym == KEY_BINDINGS["FULLSCREEN_EXIT"]["key"]):
        root.attributes("-fullscreen", False)
    # Key sequence to close the application (e.g., pressing "Ctrl+q")
    elif (event.state == KEY_BINDINGS["QUIT"]["state"] and 
          event.keysym == KEY_BINDINGS["QUIT"]["key"]):
        root.quit()


def auto_tab(event, next_widget):
    entry_widget = event.widget
    if len(entry_widget.get()) == BARCODE["LENGTH"]:
        next_widget.focus_set()


# Bind the handle_keys function to all key events
root.bind_all("<Key>", handle_keys)

root.lift()

clear_last_scanned_button = tk.Button(
    root, 
    text=BUTTON_TEXTS["CLEAR_LAST"], 
    font=FONT_SIZES["MEDIUM"], 
    command=clear_last_scanned_barcode
)
clear_last_scanned_button.place(**LAYOUT["BUTTONS"]["CLEAR_LAST_SCANNED"])


tray_var = tk.StringVar()
tray_var.trace("w", tray_selected)
uc_var = tk.StringVar()

tray1_button = tk.Radiobutton(
    root,
    text=TRAY_VALUES["TRAY1"],
    variable=tray_var,
    value=TRAY_VALUES["TRAY1"],
    font=FONT_SIZES["MEDIUM"],
    command=tray_selected,
)
tray2_button = tk.Radiobutton(
    root,
    text=TRAY_VALUES["TRAY2"],
    variable=tray_var,
    value=TRAY_VALUES["TRAY2"],
    font=FONT_SIZES["MEDIUM"],
    command=tray_selected,
)

tray1_button.place(**LAYOUT["BUTTONS"]["TRAY1"])
tray2_button.place(**LAYOUT["BUTTONS"]["TRAY2"])

uc1_button = tk.Radiobutton(
    root,
    text=UC_VALUES["UC1"],
    variable=uc_var,
    value=UC_VALUES["UC1"],
    font=FONT_SIZES["MEDIUM"],
    state="disabled",
)
uc2_button = tk.Radiobutton(
    root,
    text=UC_VALUES["UC2"],
    variable=uc_var,
    value=UC_VALUES["UC2"],
    font=FONT_SIZES["MEDIUM"],
    state="disabled",
)

uc1_button.place(**LAYOUT["BUTTONS"]["UC1"])
uc2_button.place(**LAYOUT["BUTTONS"]["UC2"])

# Deselect the radio buttons
tray1_button.deselect()
tray2_button.deselect()
uc1_button.deselect()
uc2_button.deselect()


close_button = tk.Button(root, text=BUTTON_TEXTS["CLOSE"], font=FONT_SIZES["MEDIUM"], command=root.quit)
close_button.place(**LAYOUT["BUTTONS"]["CLOSE"])

Log_button = tk.Button(root, text=BUTTON_TEXTS["LOG_OFF"], font=FONT_SIZES["MEDIUM"], command=clear_user_shift)
Log_button.place(**LAYOUT["BUTTONS"]["LOG_OFF"])

clear_button = tk.Button(root, text=BUTTON_TEXTS["CLEAR_BARCODES"], font=FONT_SIZES["MEDIUM"], command=clear_barcode_entries)
clear_button.place(**LAYOUT["BUTTONS"]["CLEAR_BARCODES"])

disable_button = tk.Button(root, text=BUTTON_TEXTS["DISABLE_ALL"], font=FONT_SIZES["MEDIUM"], command=disable_barcodesindef)
disable_button.place(**LAYOUT["BUTTONS"]["DISABLE_ALL"])

enable_button = tk.Button(root, text=BUTTON_TEXTS["ENABLE_SCANNER"], font=FONT_SIZES["MEDIUM"], command=enable_barcodes)
enable_button.place(**LAYOUT["BUTTONS"]["ENABLE_SCANNER"])

enableshift_button = tk.Button(root, text=BUTTON_TEXTS["ENABLE_NAME_SHIFT"], font=FONT_SIZES["MEDIUM"], command=enable_nameshift)
enableshift_button.place(**LAYOUT["BUTTONS"]["ENABLE_SHIFT"])

shift_var = tk.StringVar()
shift_var.set("")


def update_shift3():
    shift_var.set(SHIFT_VALUES["THIRD"])
    enable_barcodes()
    barcode1_entry.focus_set()


Thirdshift_button = tk.Button(root, text=BUTTON_TEXTS["THIRD_SHIFT"], font=FONT_SIZES["MEDIUM"], command=update_shift3)
Thirdshift_button.place(**LAYOUT["BUTTONS"]["THIRD_SHIFT"])


def update_shift2():
    shift_var.set(SHIFT_VALUES["SECOND"])
    enable_barcodes()
    barcode1_entry.focus_set()


secondshift_button = tk.Button(root, text=BUTTON_TEXTS["SECOND_SHIFT"], font=FONT_SIZES["MEDIUM"], command=update_shift2)
secondshift_button.place(**LAYOUT["BUTTONS"]["SECOND_SHIFT"])


def update_shift1():
    shift_var.set(SHIFT_VALUES["FIRST"])
    enable_barcodes()
    barcode1_entry.focus_set()


count_button = tk.Button(root, text=BUTTON_TEXTS["OPEN_COUNTER"], font=FONT_SIZES["MEDIUM"], command=open_other_file)
count_button.place(**LAYOUT["BUTTONS"]["COUNT"])




secondshift_button = tk.Button(root, text=BUTTON_TEXTS["FIRST_SHIFT"], font=FONT_SIZES["MEDIUM"], command=update_shift1)
secondshift_button.place(**LAYOUT["BUTTONS"]["FIRST_SHIFT"])

last_barcode_label = tk.Label(root, text=LABEL_TEXTS["LAST_BARCODE"], font=FONT_SIZES["SMALL"])
last_barcode_label.place(**LAYOUT["LABELS"]["LAST_BARCODE"])
last_barcode_value = tk.Label(root, text="", font=FONT_SIZES["SMALL"], wraplength=STYLES["LABEL_WRAPLENGTH"])
last_barcode_value.place(**LAYOUT["LABELS"]["LAST_BARCODE_VALUE"])

root.attributes("-topmost", True)
root.after_idle(root.attributes, "-topmost", True)

name_var = tk.StringVar()
name_label = tk.Label(root, text=LABEL_TEXTS["NAME"], font=FONT_SIZES["LARGE"])
name_label.place(**LAYOUT["LABELS"]["NAME"])
name_entry = tk.Entry(root, justify=STYLES["ENTRY_JUSTIFY"], textvariable=name_var, font=FONT_SIZES["LARGE"])
name_entry.place(**LAYOUT["ENTRIES"]["NAME"])
name_entry.focus_set()
name_var.trace("w", scan_barcodes)

shift_var = tk.StringVar()
shift_label = tk.Label(root, text=LABEL_TEXTS["SHIFT"], font=FONT_SIZES["LARGE"])
shift_label.place(**LAYOUT["LABELS"]["SHIFT"])
shift_entry = tk.Entry(root, justify=STYLES["ENTRY_JUSTIFY"], textvariable=shift_var, font=FONT_SIZES["LARGE"])
shift_entry.place(**LAYOUT["ENTRIES"]["SHIFT"])
shift_var.trace("w", scan_barcodes)

barcode1_var = tk.StringVar()
barcode1_label = tk.Label(root, text=LABEL_TEXTS["BARCODE1"], font=FONT_SIZES["LARGE"])
barcode1_label.place(**LAYOUT["LABELS"]["BARCODE1"])
barcode1_entry = tk.Entry(root, textvariable=barcode1_var, font=FONT_SIZES["LARGE"])
barcode1_entry.place(**LAYOUT["ENTRIES"]["BARCODE1"])
barcode1_var.trace("w", scan_barcodes)

barcode2_var = tk.StringVar()
barcode2_label = tk.Label(root, text=LABEL_TEXTS["BARCODE2"], font=FONT_SIZES["LARGE"])
barcode2_label.place(**LAYOUT["LABELS"]["BARCODE2"])
barcode2_entry = tk.Entry(root, textvariable=barcode2_var, font=FONT_SIZES["LARGE"])
barcode2_entry.place(**LAYOUT["ENTRIES"]["BARCODE2"])
barcode2_var.trace("w", scan_barcodes)

barcode3_var = tk.StringVar()
barcode3_label = tk.Label(root, text=LABEL_TEXTS["BARCODE3"], font=FONT_SIZES["LARGE"])
barcode3_label.place(**LAYOUT["LABELS"]["BARCODE3"])
barcode3_entry = tk.Entry(root, textvariable=barcode3_var, font=FONT_SIZES["LARGE"])
barcode3_entry.place(**LAYOUT["ENTRIES"]["BARCODE3"])
barcode3_var.trace("w", scan_barcodes)

barcode4_var = tk.StringVar()
barcode4_label = tk.Label(root, text=LABEL_TEXTS["BARCODE4"], font=FONT_SIZES["LARGE"])
barcode4_label.place(**LAYOUT["LABELS"]["BARCODE4"])
barcode4_entry = tk.Entry(root, textvariable=barcode4_var, font=FONT_SIZES["LARGE"])
barcode4_entry.place(**LAYOUT["ENTRIES"]["BARCODE4"])
barcode4_var.trace("w", scan_barcodes)

result_label = tk.Label(root, text="", font=FONT_SIZES["EXTRA_LARGE"], width=20, height=5)
result_label.place(**LAYOUT["RESULT_LABEL"])
barcodes_disabled_start()


def on_switch_key_press(event):
    enable_barcodes()


# Add the bindings here
barcode1_entry.bind("<KeyRelease>", lambda event: auto_tab(event, barcode2_entry))
barcode2_entry.bind("<KeyRelease>", lambda event: auto_tab(event, barcode3_entry))
barcode3_entry.bind(
    "<KeyRelease>", lambda event: auto_tab(event, barcode4_entry)
)  # Bind the F12 key to the on_switch_key_press function
root.bind(KEY_BINDINGS["ENABLE_SCANNER"], on_switch_key_press)


root.mainloop()
