import tkinter as tk
from tkinter import filedialog, messagebox
from datetime import datetime, time, timedelta
import re
from tkcalendar import Calendar  # Import the Calendar widget

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.create_widgets()
        self.overtime_file = "overtime.txt"  # File to store overtime info

    def create_widgets(self):
        self.select_file_btn = tk.Button(self)
        self.select_file_btn["text"] = "Select Text file"
        self.select_file_btn["command"] = self.load_file
        self.select_file_btn.pack(side="top")

        self.shift_label = tk.Label(self, text="Select your shift:")
        self.shift_label.pack()

        self.shift_var = tk.IntVar()
        self.shift1_rb = tk.Radiobutton(self, text="Shift 1 (7am - 3pm)", variable=self.shift_var, value=1)
        self.shift1_rb.pack()
        self.shift2_rb = tk.Radiobutton(self, text="Shift 2 (3pm - 11pm)", variable=self.shift_var, value=2)
        self.shift2_rb.pack()
        self.shift3_rb = tk.Radiobutton(self, text="Shift 3 (11pm - 7am)", variable=self.shift_var, value=3)
        self.shift3_rb.pack()

        self.ot_label = tk.Label(self, text="Enter overtime if any:")
        self.ot_label.pack()
        self.ot_entry = tk.Entry(self)
        self.ot_entry.pack()

        self.date_label = tk.Label(self, text="Select date:")
        self.date_label.pack()
        self.date_calendar = Calendar(self)  # Create the Calendar widget
        self.date_calendar.pack()

        # New widgets for time range
        self.time_start_label = tk.Label(self, text="Start Time (HH:MM):")
        self.time_start_label.pack()
        self.time_start_entry = tk.Entry(self)
        self.time_start_entry.pack()

        self.time_end_label = tk.Label(self, text="End Time (HH:MM):")
        self.time_end_label.pack()
        self.time_end_entry = tk.Entry(self)
        self.time_end_entry.pack()

        self.calculate_btn = tk.Button(self)
        self.calculate_btn["text"] = "Calculate"
        self.calculate_btn["command"] = self.calculate_parts
        self.calculate_btn.pack(side="bottom")

    def load_file(self):
        self.filename = filedialog.askopenfilename(filetypes=(("Text files", "*.txt"), ("All files", "*.*")))

    def calculate_parts(self):
        try:
            shift_start_times = [time(7, 0), time(15, 0), time(23, 0)]
            shift_end_times = [time(15, 0), time(23, 0), time(7, 0)]
            
            shift_start = shift_start_times[self.shift_var.get() - 1]
            shift_end = shift_end_times[self.shift_var.get() - 1]
            selected_date = self.date_calendar.get_date()  # Get the selected date from the Calendar widget
            
            # Adjust end time for overtime of current shift
            current_shift_overtime = int(self.ot_entry.get())
            if current_shift_overtime:
                shift_end = (datetime.combine(datetime.today(), shift_end) + timedelta(hours=current_shift_overtime)).time()

            # Get user-specified time range
            time_start_str = self.time_start_entry.get()
            time_end_str = self.time_end_entry.get()
            
            time_start = datetime.strptime(time_start_str, '%H:%M').time()
            time_end = datetime.strptime(time_end_str, '%H:%M').time()

            num_lines = 0
            selected_date_obj = datetime.strptime(selected_date, '%m/%d/%y')
            selected_date_str = selected_date_obj.strftime('%d %B')

            with open(self.filename, 'r') as f:
                for line in f:
                    match = re.search(r'\d{1,2} \w+ \d{2}:\d{2}', line)
                    if match:
                        date_str = match.group()
                        line_date, line_time = date_str.rsplit(' ', 1)
                        if selected_date_str in line_date:  # Compare with selected date
                            line_time_obj = datetime.strptime(line_time, '%H:%M').time()
                            if ((time_start < time_end and time_start <= line_time_obj < time_end) or
                                (time_start > time_end and (line_time_obj >= time_start or line_time_obj < time_end))):
                                num_lines += 1

            total_parts = num_lines
            messagebox.showinfo("Total Parts Produced", f"Total parts produced in the selected time range: {total_parts}")

            # Store overtime for this shift
            self.store_overtime(current_shift_overtime)
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def store_overtime(self, overtime):
        try:
            with open(self.overtime_file, 'a') as f:
                f.write(f"{self.shift_var.get()},{overtime}\n")  # Store shift number and overtime
        except Exception as e:
            messagebox.showerror("Error", str(e))

root = tk.Tk()
root.geometry("500x500")
root.attributes("-topmost", True)
app = Application(master=root)
app.mainloop()
